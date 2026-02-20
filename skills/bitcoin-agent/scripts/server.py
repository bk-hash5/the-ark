"""
Bitcoin AI Agent Server
FastAPI server with L402 Lightning payment gating.

Usage:
    python server.py                    # uses config.yaml
    LNBITS_URL=... python server.py     # env overrides
"""

import os
import sys
import time
import json
import hmac
import hashlib
import base64
import logging
import secrets
from pathlib import Path
from typing import Any, Optional

import httpx
import yaml
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from llm_tasks import execute_task, estimate_price, TASK_TYPES

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

load_dotenv()
logger = logging.getLogger("bitcoin-agent")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

def load_config() -> dict:
    """Load config from config.yaml, with env var overrides."""
    cfg_path = Path(__file__).parent / "config.yaml"
    cfg: dict[str, Any] = {}
    if cfg_path.exists():
        cfg = yaml.safe_load(cfg_path.read_text()) or {}

    # Env overrides (flat)
    env_map = {
        "LNBITS_URL": ("lnbits", "url"),
        "LNBITS_API_KEY": ("lnbits", "api_key"),
        "L402_SECRET_KEY": ("l402", "secret_key"),
        "LLM_PROVIDER": ("llm", "provider"),
        "LLM_MODEL": ("llm", "model"),
        "LLM_API_KEY": ("llm", "api_key"),
        "SERVER_HOST": ("server", "host"),
        "SERVER_PORT": ("server", "port"),
    }
    for env_key, (section, key) in env_map.items():
        val = os.getenv(env_key)
        if val is not None:
            cfg.setdefault(section, {})[key] = val

    return cfg

CONFIG = load_config()

def cfg(section: str, key: str, default: Any = None) -> Any:
    return CONFIG.get(section, {}).get(key, default)

# ---------------------------------------------------------------------------
# In-memory task store (swap for Redis/DB in production)
# ---------------------------------------------------------------------------

TASKS: dict[str, dict] = {}  # payment_hash -> task info

# ---------------------------------------------------------------------------
# LNbits helpers
# ---------------------------------------------------------------------------

LNBITS_URL = cfg("lnbits", "url", "http://localhost:5000")
LNBITS_KEY = cfg("lnbits", "api_key", "")

async def lnbits_create_invoice(amount_sats: int, memo: str, webhook: Optional[str] = None) -> dict:
    """Create a Lightning invoice via LNbits."""
    payload: dict[str, Any] = {"out": False, "amount": amount_sats, "memo": memo}
    if webhook:
        payload["webhook"] = webhook
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            f"{LNBITS_URL}/api/v1/payments",
            headers={"X-Api-Key": LNBITS_KEY},
            json=payload,
        )
        r.raise_for_status()
        return r.json()

async def lnbits_check_payment(payment_hash: str) -> bool:
    """Check if an invoice has been paid."""
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(
            f"{LNBITS_URL}/api/v1/payments/{payment_hash}",
            headers={"X-Api-Key": LNBITS_KEY},
        )
        r.raise_for_status()
        return r.json().get("paid", False)

# ---------------------------------------------------------------------------
# L402 Macaroon helpers (HMAC-based, no pymacaroons dependency needed)
# ---------------------------------------------------------------------------

L402_SECRET = cfg("l402", "secret_key", "change-me-to-random-secret")
L402_EXPIRY = int(cfg("l402", "token_expiry_seconds", 86400))
L402_LOCATION = cfg("l402", "location", "https://your-agent.example.com")

def _mac_signature(payment_hash: str, expires: int) -> str:
    """HMAC-SHA256 signature for a macaroon-like token."""
    msg = f"{payment_hash}:{expires}".encode()
    return hmac.new(L402_SECRET.encode(), msg, hashlib.sha256).hexdigest()

def create_l402_token(payment_hash: str) -> str:
    """Create a base64-encoded L402 macaroon-like token."""
    expires = int(time.time()) + L402_EXPIRY
    sig = _mac_signature(payment_hash, expires)
    payload = json.dumps({"id": payment_hash, "exp": expires, "sig": sig})
    return base64.urlsafe_b64encode(payload.encode()).decode()

def verify_l402_token(token_b64: str, preimage: str) -> Optional[str]:
    """
    Verify an L402 token. Returns payment_hash if valid, else None.
    
    The preimage is the SHA-256 preimage whose hash should match the token's id
    (payment_hash). In a real L402 flow the payer obtains the preimage by paying
    the Lightning invoice.
    """
    try:
        payload = json.loads(base64.urlsafe_b64decode(token_b64))
        payment_hash = payload["id"]
        expires = payload["exp"]
        sig = payload["sig"]

        # Check expiry
        if time.time() > expires:
            return None
        # Check signature
        if sig != _mac_signature(payment_hash, expires):
            return None
        # Check preimage → hash
        preimage_bytes = bytes.fromhex(preimage)
        if hashlib.sha256(preimage_bytes).hexdigest() != payment_hash:
            return None

        return payment_hash
    except Exception:
        return None

def parse_l402_header(auth: str) -> Optional[tuple]:
    """Parse 'L402 <macaroon>:<preimage>' header."""
    if not auth.startswith("L402 "):
        return None
    parts = auth[5:].split(":", 1)
    if len(parts) != 2:
        return None
    return parts[0], parts[1]

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Bitcoin AI Agent",
    description="AI agent that accepts Bitcoin Lightning payments via L402",
    version="1.0.0",
)

# --- Models ---

class TaskRequest(BaseModel):
    task: str  # one of TASK_TYPES
    input: str
    params: dict[str, Any] = {}

class TaskResponse(BaseModel):
    payment_hash: str
    invoice: str
    amount_sats: int
    task: str
    status_url: str

# --- Endpoints ---

@app.get("/health")
async def health():
    return {"status": "ok", "task_types": TASK_TYPES, "version": "1.0.0"}

@app.post("/task")
async def submit_task(req: TaskRequest, request: Request):
    """
    Submit a task. Returns a Lightning invoice to pay.
    After payment, poll /task/{hash}/status to get the result.
    """
    if req.task not in TASK_TYPES:
        raise HTTPException(400, f"Unknown task type '{req.task}'. Valid: {TASK_TYPES}")

    pricing = CONFIG.get("pricing", {})
    price = estimate_price(req.task, req.input, pricing)

    # Create invoice
    webhook_url = cfg("lnbits", "webhook_url")
    inv = await lnbits_create_invoice(price, f"AI Agent: {req.task}", webhook=webhook_url)

    payment_hash = inv["payment_hash"]
    TASKS[payment_hash] = {
        "task": req.task,
        "input": req.input,
        "params": req.params,
        "amount_sats": price,
        "status": "awaiting_payment",
        "result": None,
        "created_at": time.time(),
    }

    return TaskResponse(
        payment_hash=payment_hash,
        invoice=inv["payment_request"],
        amount_sats=price,
        task=req.task,
        status_url=f"/task/{payment_hash}/status",
    )

@app.get("/task/{payment_hash}/status")
async def task_status(payment_hash: str):
    """Check task status. If paid and not yet executed, runs the task."""
    task_info = TASKS.get(payment_hash)
    if not task_info:
        raise HTTPException(404, "Task not found")

    if task_info["status"] == "complete":
        return {"status": "complete", "result": task_info["result"]}

    if task_info["status"] == "awaiting_payment":
        paid = await lnbits_check_payment(payment_hash)
        if not paid:
            return {"status": "awaiting_payment", "amount_sats": task_info["amount_sats"]}
        task_info["status"] = "processing"

    # Execute the task
    if task_info["status"] == "processing":
        try:
            result = await execute_task(
                task_info["task"],
                task_info["input"],
                CONFIG.get("llm", {}),
                **task_info.get("params", {}),
            )
            task_info["status"] = "complete"
            task_info["result"] = {
                "content": result.content,
                "tokens": {"input": result.input_tokens, "output": result.output_tokens},
                "model": result.model,
            }
            return {"status": "complete", "result": task_info["result"]}
        except Exception as e:
            logger.exception("Task execution failed")
            task_info["status"] = "error"
            task_info["result"] = {"error": str(e)}
            return {"status": "error", "error": str(e)}

    return {"status": task_info["status"]}

# --- L402 gated endpoint (alternative flow) ---

@app.api_route("/l402/task", methods=["POST"])
async def l402_task(request: Request):
    """
    L402-gated task endpoint. 
    - No valid token → 402 with invoice + macaroon
    - Valid token → execute task immediately
    """
    auth = request.headers.get("Authorization", "")
    parsed = parse_l402_header(auth)

    if parsed:
        mac_token, preimage = parsed
        payment_hash = verify_l402_token(mac_token, preimage)
        if payment_hash:
            # Valid L402 — execute task
            body = await request.json()
            task_type = body.get("task", "summarize")
            input_text = body.get("input", "")
            params = body.get("params", {})
            if task_type not in TASK_TYPES:
                raise HTTPException(400, f"Unknown task: {task_type}")
            
            result = await execute_task(task_type, input_text, CONFIG.get("llm", {}), **params)
            return JSONResponse({
                "status": "complete",
                "result": {
                    "content": result.content,
                    "tokens": {"input": result.input_tokens, "output": result.output_tokens},
                    "model": result.model,
                },
            })

    # No valid token — issue 402
    body = await request.json()
    task_type = body.get("task", "summarize")
    pricing = CONFIG.get("pricing", {})
    price = estimate_price(task_type, body.get("input", ""), pricing)

    inv = await lnbits_create_invoice(price, f"L402 AI Agent: {task_type}")
    mac_token = create_l402_token(inv["payment_hash"])

    return Response(
        content=json.dumps({"message": "Payment required", "amount_sats": price}),
        status_code=402,
        media_type="application/json",
        headers={
            "WWW-Authenticate": f'L402 macaroon="{mac_token}", invoice="{inv["payment_request"]}"',
        },
    )

# --- Webhook for payment notifications ---

@app.post("/webhook/payment")
async def payment_webhook(request: Request):
    """LNbits payment webhook. Auto-executes task on payment."""
    data = await request.json()
    payment_hash = data.get("payment_hash", "")
    logger.info(f"Webhook received for {payment_hash}")

    task_info = TASKS.get(payment_hash)
    if not task_info:
        return {"status": "ignored", "reason": "unknown payment_hash"}

    if task_info["status"] != "awaiting_payment":
        return {"status": "already_processed"}

    task_info["status"] = "processing"
    try:
        result = await execute_task(
            task_info["task"],
            task_info["input"],
            CONFIG.get("llm", {}),
            **task_info.get("params", {}),
        )
        task_info["status"] = "complete"
        task_info["result"] = {
            "content": result.content,
            "tokens": {"input": result.input_tokens, "output": result.output_tokens},
            "model": result.model,
        }
    except Exception as e:
        logger.exception("Task execution failed via webhook")
        task_info["status"] = "error"
        task_info["result"] = {"error": str(e)}

    return {"status": task_info["status"]}

# --- Lightning Address / LNURL-pay ---

@app.get("/.well-known/lnurlp/{username}")
async def lnurl_pay(username: str):
    """LNURL-pay endpoint for Lightning Address support (username@domain)."""
    la_cfg = CONFIG.get("lightning_address", {})
    if not la_cfg.get("enabled", False):
        raise HTTPException(404, "Lightning Address not enabled")

    domain = la_cfg.get("domain", "localhost")
    min_sats = la_cfg.get("min_sats", 10)
    max_sats = la_cfg.get("max_sats", 100000)

    return {
        "status": "OK",
        "tag": "payRequest",
        "commentAllowed": 255,
        "callback": f"https://{domain}/lnurl/callback",
        "minSendable": min_sats * 1000,  # millisats
        "maxSendable": max_sats * 1000,
        "metadata": json.dumps([
            ["text/plain", la_cfg.get("description", "Bitcoin AI Agent")],
            ["text/identifier", f"{username}@{domain}"],
        ]),
    }

@app.get("/lnurl/callback")
async def lnurl_callback(amount: int, comment: str = ""):
    """LNURL-pay callback — creates invoice for the requested amount."""
    amount_sats = amount // 1000  # convert from millisats
    memo = comment or "Lightning Address payment"
    inv = await lnbits_create_invoice(amount_sats, memo)
    return {
        "status": "OK",
        "pr": inv["payment_request"],
        "routes": [],
    }

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    host = cfg("server", "host", "0.0.0.0")
    port = int(cfg("server", "port", 8402))
    logger.info(f"Starting Bitcoin AI Agent on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
