"""
Test Client for Bitcoin AI Agent
Demonstrates the full L402 payment flow.

Usage:
    python test_client.py                          # basic task flow
    python test_client.py --l402                   # L402 flow
    python test_client.py --server http://host:port
"""

import asyncio
import argparse
import json
import re
import sys
import httpx

DEFAULT_SERVER = "http://localhost:8402"


async def demo_basic_flow(server: str):
    """Demonstrate the basic task submission flow."""
    print("=" * 60)
    print("Bitcoin AI Agent — Basic Task Flow")
    print("=" * 60)

    async with httpx.AsyncClient(timeout=60) as client:
        # Step 1: Submit task
        print("\n[1] Submitting task...")
        r = await client.post(f"{server}/task", json={
            "task": "summarize",
            "input": "Bitcoin is a decentralized digital currency. It was invented in 2008 by an unknown person or group using the name Satoshi Nakamoto. Transactions are verified by network nodes through cryptography and recorded in a public distributed ledger called a blockchain.",
        })
        data = r.json()
        print(f"    Status: {r.status_code}")
        print(f"    Payment hash: {data['payment_hash']}")
        print(f"    Amount: {data['amount_sats']} sats")
        print(f"    Invoice: {data['invoice'][:60]}...")

        payment_hash = data["payment_hash"]

        # Step 2: Check status (unpaid)
        print("\n[2] Checking status (before payment)...")
        r = await client.get(f"{server}/task/{payment_hash}/status")
        print(f"    Status: {r.json()['status']}")

        print("\n[3] >>> Pay the invoice above with a Lightning wallet <<<")
        print(f"    Full invoice: {data['invoice']}")
        print("\n    Waiting... (press Enter after paying, or Ctrl+C to quit)")
        await asyncio.get_event_loop().run_in_executor(None, input)

        # Step 3: Check status (after payment)
        print("\n[4] Checking status (after payment)...")
        r = await client.get(f"{server}/task/{payment_hash}/status")
        result = r.json()
        print(f"    Status: {result['status']}")
        if result["status"] == "complete":
            print(f"    Result: {result['result']['content'][:200]}...")
            print(f"    Tokens: {result['result']['tokens']}")
        else:
            print(f"    Response: {json.dumps(result, indent=2)}")


async def demo_l402_flow(server: str):
    """Demonstrate the L402 payment flow."""
    print("=" * 60)
    print("Bitcoin AI Agent — L402 Flow")
    print("=" * 60)

    async with httpx.AsyncClient(timeout=60) as client:
        task_body = {
            "task": "translate",
            "input": "Hello, how are you today?",
            "params": {"target_language": "Spanish"},
        }

        # Step 1: Request without token → get 402
        print("\n[1] Requesting without L402 token...")
        r = await client.post(f"{server}/l402/task", json=task_body)
        print(f"    Status: {r.status_code}")

        if r.status_code == 402:
            www_auth = r.headers.get("WWW-Authenticate", "")
            print(f"    WWW-Authenticate: {www_auth[:80]}...")

            # Parse macaroon and invoice
            mac_match = re.search(r'macaroon="([^"]+)"', www_auth)
            inv_match = re.search(r'invoice="([^"]+)"', www_auth)
            if mac_match and inv_match:
                macaroon = mac_match.group(1)
                invoice = inv_match.group(1)
                print(f"\n    Macaroon: {macaroon[:50]}...")
                print(f"    Invoice:  {invoice[:60]}...")
                print(f"\n[2] >>> Pay this invoice: {invoice}")
                print("    After paying, you'll get a preimage (hex string).")
                print("    Enter the preimage below:")
                preimage = (await asyncio.get_event_loop().run_in_executor(None, input)).strip()

                if preimage:
                    # Step 2: Retry with L402 token
                    print(f"\n[3] Retrying with L402 token...")
                    r2 = await client.post(
                        f"{server}/l402/task",
                        json=task_body,
                        headers={"Authorization": f"L402 {macaroon}:{preimage}"},
                    )
                    print(f"    Status: {r2.status_code}")
                    print(f"    Response: {json.dumps(r2.json(), indent=2)}")
        else:
            print(f"    Unexpected: {r.json()}")


async def main():
    parser = argparse.ArgumentParser(description="Bitcoin AI Agent Test Client")
    parser.add_argument("--server", default=DEFAULT_SERVER)
    parser.add_argument("--l402", action="store_true", help="Use L402 flow instead of basic")
    args = parser.parse_args()

    # Health check
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.get(f"{args.server}/health")
            print(f"Server health: {r.json()}")
        except httpx.ConnectError:
            print(f"ERROR: Cannot connect to {args.server}")
            sys.exit(1)

    if args.l402:
        await demo_l402_flow(args.server)
    else:
        await demo_basic_flow(args.server)


if __name__ == "__main__":
    asyncio.run(main())
