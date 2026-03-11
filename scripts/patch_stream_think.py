#!/usr/bin/env python3
"""
Fix 3 issues:
1. Strip <think> tags from streaming responses
2. Improve image generation prompts for photorealistic quality
3. Remove Developer and Professionals menu items from site
"""

# ===== FIX 1: Strip <think> tags from streaming =====
with open("/opt/bitcoin-agent/scripts/server.py", "r") as f:
    srv = f.read()

# Replace the streaming chunk handler to filter out <think> content
old_stream = '''                            try:
                                chunk = json.loads(data_str)
                                delta = chunk.get("choices", [{}])[0].get("delta", {})
                                text = delta.get("content", "")
                                if text:
                                    full_content += text
                                    yield f'data: {{"type":"content","text":{json.dumps(text)}}}\\n\\n\''''

new_stream = '''                            try:
                                chunk = json.loads(data_str)
                                delta = chunk.get("choices", [{}])[0].get("delta", {})
                                text = delta.get("content", "")
                                if text:
                                    full_content += text
                                    # Strip Qwen3 thinking tags from streaming output
                                    if not hasattr(stream_gen, '_in_think'):
                                        stream_gen._in_think = False
                                    if '<think>' in full_content and not stream_gen._in_think:
                                        stream_gen._in_think = True
                                    if stream_gen._in_think:
                                        if '</think>' in full_content:
                                            stream_gen._in_think = False
                                            # Extract content after </think>
                                            import re as _re_s
                                            cleaned = _re_s.sub(r'<think>.*?</think>\\s*', '', full_content, flags=_re_s.DOTALL)
                                            if cleaned and len(cleaned) > len(full_content) - len(text) - 20:
                                                after_think = cleaned[max(0, len(cleaned) - len(text) - 5):]
                                                if after_think.strip():
                                                    yield f'data: {{"type":"content","text":{json.dumps(after_think.strip())}}}\\n\\n'
                                        continue  # Don't yield thinking content
                                    yield f'data: {{"type":"content","text":{json.dumps(text)}}}\\n\\n\''''

if old_stream in srv:
    srv = srv.replace(old_stream, new_stream)
    print("OK: Streaming think-tag filter added")
else:
    print("WARN: Exact streaming pattern not found, trying simpler approach...")
    # Simpler: just filter individual chunks containing <think> or </think>
    simple_old = '''                                if text:
                                    full_content += text
                                    yield f'data: {{"type":"content","text":{json.dumps(text)}}}\\n\\n\''''
    simple_new = '''                                if text:
                                    full_content += text
                                    # Filter out Qwen3 <think> tags from streaming
                                    if '<think>' in text or '</think>' in text or (hasattr(stream_gen, '_skip_think') and stream_gen._skip_think):
                                        if '<think>' in text:
                                            stream_gen._skip_think = True
                                        if '</think>' in text:
                                            stream_gen._skip_think = False
                                            # Send any text after </think>
                                            after = text.split('</think>')[-1].strip()
                                            if after:
                                                yield f'data: {{"type":"content","text":{json.dumps(after)}}}\\n\\n'
                                        continue
                                    yield f'data: {{"type":"content","text":{json.dumps(text)}}}\\n\\n\''''
    if simple_old in srv:
        srv = srv.replace(simple_old, simple_new)
        print("OK: Simple streaming think-tag filter added")
    else:
        print("ERROR: Could not find streaming content pattern at all")

with open("/opt/bitcoin-agent/scripts/server.py", "w") as f:
    f.write(srv)
print("server.py saved")
