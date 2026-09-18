#!/usr/bin/env python3
import re
import subprocess
import tempfile
from pathlib import Path

repo_root = Path('/Users/mb/Documents/antigravity/clever-chandrasekhar')
files = [repo_root / 'README.md'] + sorted(list((repo_root / 'docs').glob('*.md')))

mermaid_block_re = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)
total_diagrams = 0
passed_diagrams = 0
failed = []

for f in files:
    content = f.read_text(encoding='utf-8')
    blocks = mermaid_block_re.findall(content)
    for idx, block in enumerate(blocks):
        lines = [l.strip() for l in block.strip().splitlines() if l.strip() and not l.strip().startswith("%%")]
        if not lines:
            continue
        total_diagrams += 1
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f_in:
            f_in.write(block.strip())
            in_path = f_in.name
        out_path = in_path.replace('.mmd', '.svg')
        cmd = ['/opt/homebrew/bin/mmdc', '-i', in_path, '-o', out_path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            passed_diagrams += 1
            print(f"PASS [{passed_diagrams}/{total_diagrams}]: {f.name} block #{idx+1}")
        else:
            failed.append((f.name, idx+1, res.stderr))
            print(f"FAIL: {f.name} block #{idx+1}: {res.stderr[:200]}")

print("\n--- SUMMARY ---")
print(f"Total diagrams: {total_diagrams}")
print(f"Passed: {passed_diagrams}")
print(f"Failed: {len(failed)}")

if failed:
    for name, idx, err in failed:
        print(f"ERROR in {name} block #{idx}:\n{err}\n")
    exit(1)
else:
    print("ALL MERMAID DIAGRAMS COMPILED CLEANLY WITH MMDC!")
    exit(0)
