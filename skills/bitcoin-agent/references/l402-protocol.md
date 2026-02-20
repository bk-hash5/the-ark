# L402 Protocol Reference

## Overview

L402 (Lightning HTTP 402) uses the reserved HTTP 402 "Payment Required" status code to gate API access behind Lightning micropayments. It combines **macaroons** (bearer tokens with caveats) and **Lightning invoices** into a seamless pay-to-access flow.

## Flow

```
Client                          Server
  |-- GET /resource ------------>|
  |<-- 402 Payment Required -----|
  |    WWW-Authenticate: L402    |
  |    macaroon="...", invoice="lnbc..." |
  |                              |
  |-- [pays Lightning invoice] --|
  |   (receives preimage)        |
  |                              |
  |-- GET /resource ------------>|
  |   Authorization: L402 <macaroon>:<preimage> |
  |<-- 200 OK + response --------|
```

## Key Components

| Component | Description |
|-----------|-------------|
| **HTTP 402** | Status code signaling payment is needed |
| **Macaroon** | Bearer token with `identifier = payment_hash`, signed by server's secret key |
| **Invoice** | BOLT11 Lightning invoice; paying it yields the preimage |
| **Preimage** | 32-byte hex; `SHA256(preimage) == payment_hash` proves payment |
| **L402 Token** | `macaroon:preimage` pair sent in `Authorization` header |

## Macaroon Structure

```
location:   https://your-api.com
identifier: <payment_hash>       ← ties token to specific invoice
signature:  HMAC(secret, payload)
caveats:    (optional restrictions)
  - expires_at = <unix_timestamp>
  - task_type = summarize
  - max_uses = 10
```

**Attenuation**: Anyone can add caveats (restrictions) to a macaroon without server involvement. Caveats can only restrict, never expand permissions.

## Implementation Notes

1. **Token = macaroon + preimage**: The macaroon alone is not useful; the preimage (obtained only by paying) completes it.
2. **Verification**: Server checks HMAC signature, validates caveats, and confirms `SHA256(preimage) == identifier`.
3. **Stateless possible**: Server only needs its secret key to verify — no database lookup required if using HMAC.
4. **Token reuse**: Tokens can be reused until caveats expire. Good for sessions or rate-limited access.
5. **Pricing flexibility**: Different endpoints can require different payment amounts.

## Header Format

**Server → Client (402 response):**
```
WWW-Authenticate: L402 macaroon="<base64>", invoice="<bolt11>"
```

**Client → Server (authenticated request):**
```
Authorization: L402 <base64_macaroon>:<hex_preimage>
```

## Libraries

- **Python**: `pymacaroons` for macaroon ops, or simple HMAC-based tokens
- **Go**: `gopkg.in/macaroon.v2`, or use Aperture (full L402 proxy)
- **JavaScript**: `macaroons.js`
