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
    print("=" * 60)
    print(f"DOCUMENT: {p.name}")
    for idx, b in enumerate(blocks):
        print(f"--- Block {idx+1} ---")
        print(b)
