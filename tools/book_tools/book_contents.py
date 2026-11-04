"""Step 3. Build the book's contents file: chapter list (for the index and the reader's
"jump to chapter") plus the text of the first sections (shown as readable text on the book page).

    python3 tools/book_tools/book_contents.py BOOK.pdf SLUG TOC.txt

TOC.txt is written by hand from the book's own contents page, one section per line:

    PDF_PAGE | TITLE | SUBTITLE (optional) | PRINTED_PAGE (optional)
    10 | إهداء
    32 | الفصل الأول | الانتكاسة بالنسبة لمرض الإدمان | 31

PDF_PAGE is the page number in the PDF file (the number your PDF viewer shows), i.e. the image
number made by book_pages.py. PRINTED_PAGE is the number printed on the page; if omitted it is
PDF_PAGE - 1 (true for the Almashal books, where PDF page 1 is the cover).

Writes tools/content/books/SLUG.json. Every section gets its text blocks; only the sections listed
in the book's "preview" setting (books.py) are shown on the site. Read the preview text once on the
built page: if a line is garbled, see legacy_text.py (unknown glyph names) and rerun.
"""
import collections, json, re, statistics, sys
from pathlib import Path
import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).parent))
import legacy_text as L

ROOT = Path(__file__).resolve().parents[1] / "content" / "books"
pdf, slug, tocf = sys.argv[1:4]
toc = []
for ln in open(tocf, encoding="utf-8"):
    ln = ln.strip()
    if not ln or ln.startswith("#"):
        continue
    parts = [x.strip() for x in ln.split("|")]
    sec = {"page": int(parts[0]), "title": parts[1], "sub": parts[2] if len(parts) > 2 else ""}
    if len(parts) > 3 and parts[3]:
        sec["printed"] = int(parts[3])
    toc.append(sec)
toc.sort(key=lambda s: s["page"])

d = fitz.open(pdf)
legacy = L.is_legacy(d)
print("text layer:", "old Arabic design fonts (decoded by glyph name)" if legacy else "normal Unicode")


def blocks_for(first, last):
    lines = []
    for pn in range(first, last + 1):
        h = d[pn - 1].rect.height
        for l in L.page_lines(d, pn - 1, legacy):
            if l["text"] and h * .07 < l["y"] < h * .9 and not re.search(r"\.{5,}|…{3,}", l["text"]):   # drop running header, page number, footer, contents-page leader lines
                lines.append(dict(l, pn=pn))
    if not lines:
        return []
    body = collections.Counter(round(l["size"]) for l in lines).most_common(1)[0][0]
    lines = [l for l in lines if l["size"] >= body * .8]   # small running headers and notes
    left = statistics.median(l["x0"] for l in lines)
    gaps = [b["y"] - a["y"] for a, b in zip(lines, lines[1:]) if a["pn"] == b["pn"] and 0 < b["y"] - a["y"] < body * 3]
    lead = statistics.median(gaps) if gaps else body * 1.6

    def kind(l):
        if l["size"] >= body * 1.25:
            return "h2"
        if l["size"] >= body * 1.08:
            return "h3"
        if re.search(r"Bold|Black|Heavy", l["font"]):
            return "bold"
        return "p"

    out, prev = [], None
    for l in lines:
        k, t = kind(l), l["text"]
        if prev and k == prev["k"] and l["pn"] == prev["pn"]:
            gap = l["y"] - prev["y"]
            short = k in ("p", "bold") and prev["x0"] > left + 25
            new = gap > lead * 1.35 or short or re.match(r"^([٠-٩0-9]+[.\-)]|•|-|□)\s*", t)
            if not new:
                out[-1][1] += " " + t; prev = dict(l, k=k); continue
        if out and k == "p" and out[-1][0] == "p" and l["pn"] != prev["pn"] and not re.search(r"[.:؟!»)]\s*$", out[-1][1]):
            out[-1][1] += " " + t; prev = dict(l, k=k); continue   # paragraph continues on the next page
        out.append([k, t]); prev = dict(l, k=k)
    # the section title itself is the first heading(s); the site prints it separately
    while out and out[0][0] in ("h2", "h3") and len(out[0][1]) < 80:
        out.pop(0)
    return out


secs = []
for i, s in enumerate(toc):
    last = (toc[i + 1]["page"] - 1) if i + 1 < len(toc) else len(d)
    secs.append(dict(s, blocks=blocks_for(s["page"], last)))
    print(f'{s["page"]:>4}  {s["title"]}  ({len(secs[-1]["blocks"])} blocks)')
(ROOT / f"{slug}.json").write_text(json.dumps(secs, ensure_ascii=False), encoding="utf-8")
if L.UNKNOWN:
    print("UNKNOWN GLYPHS (add to namemap.json):", L.UNKNOWN.most_common(20))
print("->", ROOT / f"{slug}.json")
