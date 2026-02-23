# ⚡ The Ark — AI Services on Bitcoin Lightning

**98 AI services. Pay per task. No subscriptions. No banks. No borders.**

The Ark is a pay-per-task AI platform built on Bitcoin's Lightning Network. Access professional AI tools — code review, legal documents, translations, SEO analysis, voice generation, and more — for as little as 200 sats (~$0.10).

## 🌍 Why The Ark?

3.5 billion people are locked out of AI tools. They can't get credit cards. They can't afford $20/month subscriptions. They live in regions where Western payment rails don't reach.

Bitcoin fixes this. Lightning makes it instant and cheap. The Ark makes it useful.

## 🚀 How It Works

1. **Pick a service** from 98 available tasks
2. **Get a Lightning invoice** (200–8,000 sats)
3. **Pay with any Lightning wallet** — no account needed
4. **Get your result** — code, documents, translations, images, audio

No sign-up. No KYC. No data stored. Just AI, powered by sats.

## 📦 Services

| Category | Examples | Price Range |
|----------|----------|-------------|
| **Development** | Code review, bug detection, unit tests, CI/CD, Dockerfile | 200–800 sats |
| **Legal** | Privacy policies, terms of service, contracts | 500–1,000 sats |
| **Medical** | Health information, symptom analysis | 500–1,000 sats |
| **Finance** | Financial analysis, invoice generation | 500–1,000 sats |
| **Education** | Tutoring, explanations, study guides | 300–500 sats |
| **Content** | Blog posts, SEO, social media, ad copy | 300–800 sats |
| **Translation** | 50+ languages, natural fluency | 300 sats |
| **Creative** | Voice generation, image creation | 3,000–8,000 sats |

## 🔗 Workflow Bundles

Chain multiple services together at a discount:

- **Full Code Audit** (1,200 sats) — Review + Security + Tests
- **Launch Pack** (1,500 sats) — Copy + SEO + Social + Ads
- **Code Ship** (2,000 sats) — Review + Docs + Tests + Changelog + Dockerfile
- **Content Machine** (2,200 sats) — Blog + SEO + Social + Email + Hashtags
- **API Launch** (1,800 sats) — API Docs + README + CI/CD + Dockerfile
- **Startup Kit** (5,000 sats) — Pitch + Privacy Policy + Terms

## 🤖 L402 Machine-to-Machine

The Ark supports the [L402 protocol](https://lsat.tech) for programmatic access. AI agents and applications can pay for and consume services over Lightning — no human in the loop.

```bash
# Request a task
curl -X POST https://arknode.ai/task \
  -H "Content-Type: application/json" \
  -d '{"task": "code_review", "content": "def hello(): print(\"world\")"}'

# Returns a Lightning invoice — pay it, get your result
```

## 🔧 Tech Stack

- **API:** FastAPI (Python)
- **Lightning:** Phoenixd + LNbits
- **AI:** OpenAI GPT models
- **Server:** Nginx + Let's Encrypt SSL
- **Protocol:** L402 / LSAT for machine payments

## 🌐 Live

**Website:** [arknode.ai](https://arknode.ai)
**API Docs:** [arknode.ai/openapi.json](https://arknode.ai/openapi.json)
**Health:** [arknode.ai/health](https://arknode.ai/health)

## 📄 License

MIT — Free and Open Source

## 🤝 Built With

Built in East Africa 🌍 for the world. Powered by Bitcoin ⚡
