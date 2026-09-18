import re
import sys
from pathlib import Path

def check_file(path_str):
    p = Path(path_str)
    if not p.exists():
        print(f"File not found: {path_str}")
        return False
    text = p.read_text(encoding="utf-8")
    placeholders = re.findall(r'\b(TODO|TBD|FIXME|LOREM IPSUM)\b', text, re.IGNORECASE)
    print(f"File: {p.name}")
    print(f"  Size: {len(text)} bytes, {len(text.splitlines())} lines")
    print(f"  Placeholders: {placeholders}")
    mermaid_blocks = re.findall(r'```mermaid', text)
    print(f"  Mermaid blocks: {len(mermaid_blocks)}")
    math_blocks = re.findall(r'\$\$', text)
    print(f"  Block math tags ($$): {len(math_blocks)} (pairs: {len(math_blocks)//2})")
    tables = re.findall(r'\| :---', text)
    print(f"  Tables: {len(tables)}")
    return len(placeholders) == 0

if __name__ == '__main__':
    for f in sys.argv[1:]:
        check_file(f)
