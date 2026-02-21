# Stacker News Post

## Title:
We built 98 AI services you pay for with Lightning — no subscriptions, no credit cards, no accounts

## Body:

We got tired of AI tools locking everything behind $20/month subscriptions that require a credit card and a US bank account.

So we built **The Ark** — 98 AI services you pay per task with Bitcoin Lightning. That's it. No accounts. No subscriptions. No KYC. No PayPal.

### How it works

1. Pick a service
2. Get a Lightning invoice (most tasks are 100-500 sats)
3. Pay and get your result

No sign-up. No email. No data collected. You pay, you get the output, we both move on.

### What kind of services?

**For developers:**
- Code review, bug detection, security scanning
- Dockerfile generation, CI/CD pipeline configs
- Unit test generation, SQL optimization
- API documentation, README generation

**For creators & freelancers:**
- Blog posts, ad copy, social media content
- SEO analysis, keyword research
- Grammar check, tone adjustment, rewriting
- Resume/CV generation

**For professionals:**
- Contract drafting, privacy policies, terms of service
- Invoice generation, pitch deck outlines
- Data analysis, CSV cleaning, PDF extraction
- Translation (any language pair)

**Workflow bundles** — chain multiple services together at a discount. Example: code review + security scan + unit tests + changelog + Dockerfile in one shot.

### Why Lightning?

- Instant settlement
- Works globally (we're seeing traffic from Africa, Latin America, SE Asia — places where Stripe doesn't reach)
- Micropayments make sense here — why pay $20/month when you need one code review?
- Machine-to-machine payments via L402 protocol (other AI agents can use our services programmatically)

### The Africa angle

Half the continent can't access existing AI tools because they require credit cards and payment methods that don't exist there. Lightning changes that. If you can run a wallet on your phone, you can use The Ark. We just launched a page specifically for African developers, students, and freelancers.

### Try it free

Your first task is free — no Lightning wallet needed. Just hit the endpoint and see what you get back.

🔗 **thenode.it.com**
🔗 **thenode.it.com/africa** (Africa-focused)
🔗 **thenode.it.com/free** (free first task)

### What's next

We're building this in public. Feedback welcome — what services would you want? What's missing? What would make you actually use this?

⚡ Built on Phoenix + LNbits. Payments settle instantly. No custodial nonsense.

---

# Dev.to Post

## Title:
I built 98 AI microservices that accept Bitcoin Lightning — here's what I learned

## Body:

Most AI tools today follow the same playbook: sign up, add a credit card, pick a subscription tier, hope you use it enough to justify the cost.

I wanted something different. **The Ark** is a collection of 98 AI services — each one a single API call, paid per-use with Bitcoin Lightning.

### The stack

- **FastAPI** backend
- **Lightning payments** via Phoenix + LNbits
- **L402 protocol** for machine-to-machine auth
- SSL/TLS, rate limiting, input validation
- SQLite for task persistence

### The concept

Every service follows the same pattern:

```
POST /task
{
  "task_type": "code_review",
  "input_text": "your code here"
}
```

You get back a Lightning invoice. Pay it, and the result is delivered. Simple REST API, no SDK, no OAuth, no API keys.

### Why per-task pricing works

SaaS subscriptions assume recurring usage. But most people don't need AI tools every day — they need a code review before a deploy, a privacy policy for a launch, a blog post for a campaign.

Per-task pricing at 100-500 sats (~$0.05-0.25) means you only pay for what you use. And because it's Lightning, there's no minimum transaction amount making micropayments impractical.

### Workflow bundles

Single tasks are useful. Chained workflows are powerful.

Example — **Full Code Audit** bundle:
- Code review → Security scan → Unit test generation
- One payment, three outputs, discounted vs individual pricing

We have 6 workflow bundles covering code shipping, content creation, startup launch, and more.

### L402: Machine-to-machine payments

This is the part I'm most excited about. Using the L402 protocol, other AI agents and automated systems can discover, pay for, and consume our services programmatically.

The OpenAPI spec is public. The machine discovery spec is at `/.well-known/ai-agent.json`. Any agent that speaks L402 can use The Ark without human intervention.

### Global access

We're seeing interest from developers in regions where traditional payment infrastructure doesn't reach — parts of Africa, Latin America, Southeast Asia. No Stripe, no PayPal, no problem. Lightning wallets work on a $50 Android phone.

### Try it

First task is free:

```bash
curl -X POST https://thenode.it.com/free \
  -H "Content-Type: application/json" \
  -d '{"task_type": "code_review", "input_text": "your code"}'
```

Full service list: **thenode.it.com/market**
API docs: **thenode.it.com/openapi.json**

Would love feedback from the dev community. What services would be most useful? What integrations would you want?

---

*The Ark ⚡ — AI services, pay-per-task, Lightning-native.*
