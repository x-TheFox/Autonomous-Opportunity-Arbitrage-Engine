import re
import subprocess
import tempfile
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
    for idx, b in enumerate(blocks):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f_in:
            f_in.write(b.strip())
            in_path = f_in.name
        out_path = in_path.replace('.mmd', '.svg')
        cmd = ['/opt/homebrew/bin/mmdc', '-i', in_path, '-o', out_path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"SUCCESS: {p.name} Diagram {idx+1} rendered cleanly.")
        else:
            print(f"FAILURE: {p.name} Diagram {idx+1} failed:\n{res.stderr}")
