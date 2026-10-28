#!/usr/bin/env python3
"""brief_pdf.py: render a simple markdown file to PDF (US Letter, 11 pt, 1-inch margins) with headless Chrome,
then print the page count. Handles the subset PROJECT-BRIEF.md uses: '#' headings, paragraphs, '- ' bullet
lists, **bold**, `code` and bare https:// links. Pandoc is not installed on this machine; this is the equivalent.

Usage: python3 brief_pdf.py <in.md> <out.pdf>
"""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CSS = """@page { size: Letter; margin: 1in; }
body { font-family: 'Times New Roman', Times, serif; font-size: 11pt; line-height: 1.2; margin: 0; color: #000; }
h1 { font-size: 11.5pt; margin: 0 0 5pt 0; } p { margin: 0 0 5pt 0; } ul { margin: 0 0 5pt 0; padding-left: 16pt; }
li { margin: 0; } code { font-family: Menlo, monospace; font-size: 9.5pt; } a { color: #000; }"""


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(https://[^\s)<]+)", r'<a href="\1">\1</a>', s)
    return s


def to_html(md):
    out, items = [], []
    for line in md.splitlines() + [""]:
        if line.startswith("- "):
            items.append(f"<li>{inline(line[2:])}</li>")
            continue
        if items:
            out.append("<ul>" + "".join(items) + "</ul>"); items = []
        if not line.strip():
            continue
        m = re.match(r"(#+)\s+(.*)", line)
        out.append(f"<h{len(m.group(1))}>{inline(m.group(2))}</h{len(m.group(1))}>" if m else f"<p>{inline(line)}</p>")
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(out)}</body></html>"


def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2]).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "brief.html"
        page.write_text(to_html(src.read_text()))
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--user-data-dir={tmp}/profile", f"--print-to-pdf={dst}", page.as_uri()],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    data = dst.read_bytes()
    pages = len(re.findall(rb"/Type\s*/Page(?![s\w])", data))
    print(f"{dst.name}: {pages} page(s), {len(src.read_text().split())} words")


if __name__ == "__main__":
    main()
