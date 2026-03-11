#!/usr/bin/env python3
"""Fix garbled streaming output caused by broken think-tag filter."""

with open("/opt/bitcoin-agent/scripts/server.py", "r") as f:
    srv = f.read()

old_block = '''                                if text:
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

new_block = '''                                if text:
                                    full_content += text
                                    # Simple think-tag filter: skip everything between <think> and </think>
                                    if '<think>' in full_content and '</think>' not in full_content:
                                        continue  # Still inside thinking, don't yield
                                    if '</think>' in text:
                                        continue  # This chunk closes thinking, skip it
                                    if '<think>' in text:
                                        continue  # This chunk opens thinking, skip it
                                    yield f'data: {{"type":"content","text":{json.dumps(text)}}}\\n\\n\''''

if old_block in srv:
    srv = srv.replace(old_block, new_block)
    print("OK: Replaced broken think filter with simple version")
else:
    print("ERROR: Could not find the broken filter block")
    # Debug - show what's around the area
    idx = srv.find("Strip Qwen3 thinking")
    if idx > 0:
        print(f"Found 'Strip Qwen3 thinking' at pos {idx}")
        print("Context:", repr(srv[idx-50:idx+200]))

with open("/opt/bitcoin-agent/scripts/server.py", "w") as f:
    f.write(srv)
