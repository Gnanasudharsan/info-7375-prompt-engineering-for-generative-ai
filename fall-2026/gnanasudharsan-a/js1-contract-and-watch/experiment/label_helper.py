"""Reading aid for hand labeling: prints only the parts of each posting that the
labeling rule asks about. It makes NO relevance decision. Drafted in a Claude chat
on 2026-10-28; labels are written by hand."""
import json, re, sys

SHIPPED = ["Python", "PyTorch", "SQL", "Hugging Face Transformers", "sentence-transformers",
           "FastAPI", "MLflow", "PostgreSQL", "AWS"]
REQ_START = r"(You may be a good fit if you(?: have)?:?|Minimum qualifications|Qualifications:)"
REQ_END = r"(Strong candidates may (?:also )?(?:have|need)|Preferred (?:qualifications|Experience)|Strong candidates need not|The annual compensation)"
RESP_START = r"(Responsibilities:?|Key responsibilities|Representative projects:?)"
RESP_END = r"(You may be a good fit|Minimum qualifications|Qualifications:|The annual compensation)"

def section(text, start, end):
    m = re.search(start + r"(.*?)" + end, text, re.S | re.I)
    return (m.group(1) + " " + m.group(2)).strip() if m else "(section not found under these headings — read the full content)"

def mark(text):
    for s in SHIPPED:
        text = re.sub(rf"(?<![\w-])({re.escape(s)})(?![\w-])", r">>\1<<", text, flags=re.I)
    return text

split = sys.argv[1] if len(sys.argv) > 1 else "dev"
for p in json.load(open(f"experiment/postings_{split}.json")):
    c = p["content"]
    print("=" * 100)
    print(f"ID {p['id']} | {p['title'].strip()} | {p['location.name']}")
    print("-- years mentioned:", re.findall(r"\d+\s*(?:-\s*\d+)?\+?\s*years?[^.]{0,40}", c, re.I) or "none")
    print("-- degree mentions:", re.findall(r"[^.]{0,40}\b(?:PhD|MS or PhD|advanced degree)\b[^.]{0,40}", c, re.I) or "none")
    print("-- negative sponsorship phrase present:", "not currently able to sponsor" in c.lower())
    print("-- RESPONSIBILITIES:\n", mark(section(c, RESP_START, RESP_END))[:1500])
    print("-- REQUIRED (good-fit / minimum section; shipped skills marked >>like this<<):\n", mark(section(c, REQ_START, REQ_END))[:1500])
print("=" * 100)
