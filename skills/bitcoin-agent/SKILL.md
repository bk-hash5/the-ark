---
name: bitcoin-agent
description: AI agent that accepts Bitcoin Lightning payments via L402 protocol. FastAPI server with LNbits integration, multiple task types (summarize, translate, code gen, research, etc.), macaroon-based auth, Lightning Address support. Use when building pay-per-task AI services over Lightning.
---

# Bitcoin AI Agent

An AI agent that gets paid in Bitcoin over Lightning Network using the L402 protocol. Submit a task, pay a Lightning invoice, get your result.

## Quick Start

```bash
cd scripts/
bash setup.sh          # Install deps, create config files
# Edit config.yaml with your LNbits API key and LLM API key
python server.py       # Start on :8402
python test_client.py  # Test the flow
```

**Prerequisites**: LNbits instance (for invoicing) backed by Phoenixd or any Lightning node.

## Architecture

```
Client → FastAPI Server (:8402) → LNbits API → Phoenixd → Lightning Network
                ↓
          LLM API (OpenAI/Anthropic)
```

**Two payment flows:**

1. **Basic**: `POST /task` → get invoice → pay → poll `/task/{hash}/status` → get result
2. **L402**: `POST /l402/task` → get 402 + macaroon + invoice → pay → retry with `Authorization: L402 <mac>:<preimage>` → get result

## Task Types

| Task | Price (default) | Description |
|------|----------------|-------------|
| `summarize` | 50 sats | Summarize text |
| `translate` | 50 sats | Translate text (pass `target_language` in params) |
| `code_gen` | 500 sats | Generate code from description |
| `research` | 2,000 sats | In-depth research analysis |
| `content_write` | 1,000 sats | Blog posts, emails, content |
| `data_analyze` | 500 sats | Analyze data, find patterns |
| `image_describe` | 200 sats | Describe images for accessibility |

## Configuration

Edit `scripts/config.yaml`:

```yaml
lnbits:
  url: "http://localhost:5000"
  api_key: "your-invoice-read-key"  # from LNbits wallet

l402:
  secret_key: "random-secret"       # for token signing

llm:
  provider: "openai"                # or "anthropic"
  api_key: "sk-..."
  model: "gpt-4o-mini"

pricing:
  summarize: 50                     # sats per task
  code_gen: 500
```

Environment variables override config.yaml — see `.env` file.

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check + supported task types |
| `/task` | POST | Submit task, get Lightning invoice |
| `/task/{hash}/status` | GET | Check payment + get result |
| `/l402/task` | POST | L402-gated task (402 → pay → retry) |
| `/webhook/payment` | POST | LNbits payment webhook |
| `/.well-known/lnurlp/{user}` | GET | Lightning Address endpoint |

## Files

| File | Purpose |
|------|---------|
| `scripts/server.py` | Main FastAPI server |
| `scripts/llm_tasks.py` | LLM task execution module |
| `scripts/setup.sh` | One-command setup |
| `scripts/test_client.py` | Test client with L402 flow demo |
| `scripts/config.yaml.template` | Default configuration |
| `references/l402-protocol.md` | L402 protocol reference |
| `references/deployment.md` | Production deployment guide |
| `references/pricing-guide.md` | Pricing strategy & calculations |

## Adding New Task Types

1. Add system prompt in `llm_tasks.py` → `SYSTEM_PROMPTS` dict
2. Add pricing in `config.yaml` → `pricing` section
3. That's it — the server auto-discovers task types from `TASK_TYPES`

## See Also

- [Deployment Guide](references/deployment.md) — Phoenixd, LNbits, nginx, TLS setup
- [Pricing Guide](references/pricing-guide.md) — Cost analysis and pricing strategy
- [L402 Protocol](references/l402-protocol.md) — How L402 works
