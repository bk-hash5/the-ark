# Pricing Guide

## Cost Basis

At ~$100k BTC: **1 sat ≈ $0.001** (1/10th of a cent)

### LLM Costs (approximate)

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Typical task cost |
|-------|----------------------|------------------------|-------------------|
| GPT-4o-mini | $0.15 | $0.60 | ~$0.001-0.005 |
| GPT-4o | $2.50 | $10.00 | ~$0.01-0.05 |
| Claude Sonnet | $3.00 | $15.00 | ~$0.01-0.08 |

### Your Cost per Task (using GPT-4o-mini)

| Task | Est. tokens | USD cost | Sats cost |
|------|------------|----------|-----------|
| Summarize | ~1,000 | $0.001 | ~1 sat |
| Translate | ~500 | $0.0005 | ~0.5 sat |
| Code gen | ~2,000 | $0.002 | ~2 sats |
| Research | ~4,000 | $0.004 | ~4 sats |
| Content write | ~3,000 | $0.003 | ~3 sats |

## Recommended Pricing (with margin)

Apply a **10-50x markup** for convenience, API hosting, and Lightning infrastructure costs:

| Task | Cost to you | Sell price | Margin |
|------|-------------|------------|--------|
| **Summarize** | ~1 sat | 50 sats | 50x |
| **Translate** | ~1 sat | 50 sats | 50x |
| **Code gen** | ~2 sats | 500 sats | 250x |
| **Research** | ~4 sats | 2,000 sats | 500x |
| **Content write** | ~3 sats | 1,000 sats | 333x |
| **Data analyze** | ~3 sats | 500 sats | 167x |
| **Image describe** | ~2 sats | 200 sats | 100x |

These margins cover: server costs (~$5-20/mo), Lightning routing fees (~1%), LLM API overhead, and profit.

## Pricing Strategies

1. **Start high, adjust down** — easier to lower prices than raise them
2. **Free first request** — let users test before paying; hook them
3. **Volume discounts** — prepaid balance: 10,000 sats = 20% bonus credits
4. **Dynamic pricing** — adjust based on actual token usage per request (use hold invoices)

## Dollar-Cost Averaging Your Pricing

BTC price fluctuates. Options:
- **Fixed sats** (simple): prices stay constant in sats regardless of BTC/USD
- **USD-pegged** (stable for users): recalculate sat prices daily based on exchange rate
- **Hybrid**: set a floor in sats, adjust upward when BTC drops

For simplicity, start with fixed sat pricing and revisit quarterly.
