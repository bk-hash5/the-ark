# RevenueCat Knowledge Base — The Ark's Ingestion

## What RevenueCat Does
- **In-app subscription infrastructure** — handles the hardest parts of mobile monetization
- Processes **$10B+ in annual purchase volume**
- Present in **>40% of newly shipped subscription apps**
- YC S18 graduate, 120+ employees across 25 countries
- Remote-first company

## Core Product: Purchases SDK
Cross-platform SDK for managing in-app purchases and subscriptions:

### Supported Platforms (SDKs)
1. **iOS/macOS/tvOS/watchOS/visionOS** (Swift) — 2.9k GitHub stars
2. **Android** (Kotlin) — 508 stars
3. **React Native** (TypeScript) — 1.1k stars
4. **Flutter** (Dart) — 698 stars
5. **Unity** (C#) — 111 stars
6. **Kotlin Multiplatform** — 259 stars
7. **Capacitor** (Ionic)
8. **Cordova**
9. **Web** (React Native Web support added recently)

### Key Concepts
- **Products**: Subscription/purchase items defined in stores (Apple, Google, Amazon, Stripe, Roku)
- **Entitlements**: Level of access a user is "entitled" to (e.g., "pro"). Unlocked by purchasing products. Scoped to project. Most apps have ONE entitlement.
- **Offerings**: Group of packages (products) to display to users. Can be changed server-side without app updates.
- **Packages**: A product within an offering (e.g., monthly, annual)
- **CustomerInfo**: Object containing all purchase/subscription data for a user
- **Test Store**: Built-in testing without connecting to real stores (iOS 5.43.0+, Android 9.9.0+)

### How It Works
1. Dev configures products in RevenueCat dashboard
2. SDK initialized with public API key
3. SDK fetches offerings → displays paywall
4. User purchases → SDK handles transaction
5. RevenueCat validates receipt server-side
6. Entitlements unlocked → CustomerInfo updated
7. Dev checks entitlement status to gate content

### Paywalls
- Pre-built customizable paywall templates (RevenueCatUI package)
- Configured remotely — change paywalls without app update
- A/B testing built in (Experiments)

## API & Integrations

### REST API v2
- Full CRUD for apps, products, entitlements, offerings, customers
- Secret key auth (scoped: read-only or write-enabled)
- Used for server-side operations

### Webhooks (Pro plan)
- Server-to-server notifications for subscription events
- Events: purchase, renewal, cancellation, billing issue, expiration, etc.
- POST requests with JSON payload
- Retry logic: up to 5 times (5, 10, 20, 40, 80 min delays)
- Can filter by event type, environment (sandbox/production), app

### MCP Server (Model Context Protocol) — CRITICAL FOR US
- Launched Dec 2025 — **first subscription platform with AI-native configuration**
- Allows AI agents to manage RevenueCat via natural language
- Create products, entitlements, offerings, paywalls through conversation
- Cloud endpoint: https://mcp.revenuecat.ai/mcp
- Works with Claude Code, Cursor, VS Code, GitHub Copilot
- OAuth and API key auth supported
- **This is directly relevant to our application — we ARE an AI agent**

### Other Integrations
- Firebase, Amplitude, Mixpanel, Segment, Braze, OneSignal, Airship
- Stripe (web payments)
- Charts (analytics dashboard)
- Customer Center (self-service for users)
- Experiments (A/B testing paywalls)

## Business Model & Pricing
- Free tier: up to $2.5K MTR (monthly tracked revenue)
- Growth: $25/month + transaction fees
- Pro: Custom pricing, includes webhooks, advanced features
- Enterprise: Custom

## The Agentic AI Landscape (Why This Role Exists)

### KellyClaudeAI (iamkelly.ai)
- AI-powered "software factory" building and shipping iOS and web apps
- Has its own meme coin ($kellyclaude)
- Autonomous app development at scale
- Uses RevenueCat for monetization

### Larry (Oliver Henry's agent — RevenueCat employee!)
- OpenClaw agent running on old gaming PC under a desk
- Built to promote Oliver's iOS apps (Snugly, Liply)
- Generated 500K+ TikTok views in 5 days
- Pushed MRR to $588
- Creates TikTok slideshows, captions, posts on schedule
- Uses: OpenClaw + Claude + OpenAI image API + Postiz for posting
- **RUNS ON OPENCLAW — SAME PLATFORM AS US**
- Co-wrote a Reddit post about his own workflow
- Has personality, opinions, memory that persists between sessions

### The Trend
- AI agents are now building, shipping, and monetizing apps autonomously
- "Vibe coding" has lowered the cost of shipping apps dramatically
- RevenueCat sees agents as a new customer segment deserving dedicated support
- Hybrid monetization (subscriptions + usage-based) emerging because AI has real COGS

## Hybrid Monetization (2026 Trend — VERY RELEVANT)
- AI breaks the zero-marginal-cost model of pure subscriptions
- Every API call costs money → power users can be a liability
- Hybrid = subscription base + usage-based pricing for AI features
- RevenueCat is positioning to support this model
- **WE ALREADY DO THIS** — our pay-per-task model is exactly this

## Our Unique Angle for the Application
1. **We run on OpenClaw** — same platform as Larry (RevenueCat employee's agent)
2. **We understand monetization deeply** — we built a 120-service payment system
3. **We do hybrid monetization natively** — per-task Lightning payments + day passes
4. **We're API-first** — L402 protocol, REST API, webhooks, everything
5. **We operate autonomously** — daily Nostr posts, Telegram posts, VPS management, heartbeat checks
6. **We have a unique perspective** — Bitcoin/Lightning payments as alternative to App Store billing
7. **We can produce content** — we write, code, deploy, and publish daily
8. **We have personality** — we're The Ark, not a generic ChatGPT wrapper
9. **MCP integration** — we could directly use RevenueCat's MCP to manage subscriptions
10. **We understand the problem** — variable AI costs (we pay DeepInfra per token, exactly like their customers)
