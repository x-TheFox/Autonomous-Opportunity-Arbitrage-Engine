import re
from pathlib import Path

docs = [
    '/Users/mb/Documents/antigravity/clever-chandrasekhar/docs/01_executive_verdict.md',
    '/Users/mb/Documents/antigravity/clever-chandrasekhar/docs/02_pdf_thesis_teardown.md',
    '/Users/mb/Documents/antigravity/clever-chandrasekhar/docs/03_bounty_economics_and_probabilistic_model.md'
]

for doc_path in docs:
    p = Path(doc_path)
    text = p.read_text(encoding="utf-8")
    blocks = re.findall(r'```mermaid\s*\n(.*?)```', text, re.DOTALL)
    print(f"Doc: {p.name} -> {len(blocks)} Mermaid block(s)")
    for idx, b in enumerate(blocks):
        lines = [line for line in b.strip().splitlines() if line.strip()]
        header = lines[0] if lines else "EMPTY"
        print(f"  Diagram {idx+1} ({len(lines)} lines): {header}")
