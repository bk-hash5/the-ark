"""
LLM Task Execution Module
Handles all AI task types with configurable LLM provider (OpenAI / Anthropic).
"""

import os
import logging
from typing import Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class TaskResult:
    """Result from an LLM task execution."""
    content: str
    input_tokens: int
    output_tokens: int
    task_type: str
    model: str

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


# --- System prompts per task type ---

SYSTEM_PROMPTS = {
    "summarize": "You are a concise summarizer. Provide a clear, accurate summary of the given text. Include key points and main takeaways.",
    "translate": "You are a professional translator. Translate the text accurately, preserving tone and meaning. If no target language is specified, translate to English.",
    "code_gen": "You are an expert programmer. Generate clean, well-commented, production-quality code. Include brief usage examples.",
    "research": "You are a thorough researcher. Provide well-structured, factual analysis with multiple perspectives. Cite reasoning clearly.",
    "content_write": "You are a skilled content writer. Write engaging, well-structured content tailored to the specified format and audience.",
    "data_analyze": "You are a data analyst. Analyze the provided data, identify patterns, and present clear insights with actionable recommendations.",
    "image_describe": "You are an image accessibility expert. Provide detailed, accurate descriptions of images for visually impaired users.",
}

TASK_TYPES = list(SYSTEM_PROMPTS.keys())


def estimate_price(task_type: str, input_text: str, pricing: dict[str, int]) -> int:
    """Estimate price in sats for a task. Returns the configured flat rate."""
    return pricing.get(task_type, 100)


async def execute_task(
    task_type: str,
    input_text: str,
    llm_config: dict[str, Any],
    **kwargs,
) -> TaskResult:
    """
    Execute an LLM task.
    
    Args:
        task_type: One of TASK_TYPES
        input_text: User-provided input
        llm_config: Dict with provider, model, api_key, max_tokens
        **kwargs: Extra params (e.g. target_language for translate)
    
    Returns:
        TaskResult with content and token usage
    """
    if task_type not in SYSTEM_PROMPTS:
        raise ValueError(f"Unknown task type: {task_type}. Valid: {TASK_TYPES}")

    system_prompt = SYSTEM_PROMPTS[task_type]
    
    # Enrich prompt with kwargs
    user_message = input_text
    if task_type == "translate" and "target_language" in kwargs:
        user_message = f"Translate to {kwargs['target_language']}:\n\n{input_text}"

    provider = llm_config.get("provider", "openai")
    model = llm_config.get("model", "gpt-4o-mini")
    api_key = llm_config.get("api_key") or os.getenv("LLM_API_KEY", "")
    max_tokens = llm_config.get("max_tokens", 4096)

    if provider == "anthropic":
        return await _call_anthropic(system_prompt, user_message, model, api_key, max_tokens, task_type)
    else:
        return await _call_openai(system_prompt, user_message, model, api_key, max_tokens, task_type)


async def _call_openai(
    system: str, user: str, model: str, api_key: str, max_tokens: int, task_type: str
) -> TaskResult:
    """Call OpenAI-compatible API."""
    import httpx

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "max_tokens": max_tokens,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            },
        )
        resp.raise_for_status()
        data = resp.json()

    choice = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    return TaskResult(
        content=choice,
        input_tokens=usage.get("prompt_tokens", 0),
        output_tokens=usage.get("completion_tokens", 0),
        task_type=task_type,
        model=model,
    )


async def _call_anthropic(
    system: str, user: str, model: str, api_key: str, max_tokens: int, task_type: str
) -> TaskResult:
    """Call Anthropic Messages API."""
    import httpx

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
            json={
                "model": model,
                "max_tokens": max_tokens,
                "system": system,
                "messages": [{"role": "user", "content": user}],
            },
        )
        resp.raise_for_status()
        data = resp.json()

    content = data["content"][0]["text"]
    usage = data.get("usage", {})
    return TaskResult(
        content=content,
        input_tokens=usage.get("input_tokens", 0),
        output_tokens=usage.get("output_tokens", 0),
        task_type=task_type,
        model=model,
    )
