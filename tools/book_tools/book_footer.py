"""Step 1. Stamp the Googan credit footer on every page of a book PDF (except the cover).

    python3 tools/book_tools/book_footer.py SOURCE.pdf OUTPUT.pdf [--text "..."] [--skip-first N]

Writes a small grey centred line at the bottom of each page, in Cairo, e.g.
  تمت الترجمة لمؤسسة المشعل الخيرية وبرنامج قويم | ترجمة وتدقيق: شركة جوجان لخدمات الأعمال | googantranslation.com
Open OUTPUT.pdf and check a few pages: the line must not cover the page number or text.
If it overlaps, raise --bottom (distance in points from the page bottom, default 6).
Old company names inside the book (e.g. «شركة وكالة جوجان») are NOT changed by this tool;
fix them in the designer's file, or ask Claude for a targeted edit.
"""
import argparse
from pathlib import Path
import pymupdf as fitz

F = Path(__file__).parent / "fonts"
CSS = """@font-face{font-family:CA;src:url(cairo-ar-400.ttf);}
@font-face{font-family:CA;src:url(cairo-ar-700.ttf);font-weight:bold;}
@font-face{font-family:CL;src:url(cairo-la-400.ttf);}
@font-face{font-family:CL;src:url(cairo-la-700.ttf);font-weight:bold;}
*{font-family:CA,CL;}"""
DEFAULT = ("تمت الترجمة لمؤسسة المشعل الخيرية وبرنامج قويم &nbsp;|&nbsp; ترجمة وتدقيق: شركة جوجان لخدمات الأعمال"
           " &nbsp;|&nbsp; <span dir=\"ltr\">googantranslation.com</span>")

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--text", default=DEFAULT)
ap.add_argument("--skip-first", type=int, default=1, help="pages at the start without footer (cover). Default 1")
ap.add_argument("--bottom", type=float, default=6)
a = ap.parse_args()

arch = fitz.Archive(str(F))

def html_for(width):   # 6.3pt on an A5 page (419pt wide); smaller on pocket-size pages so it stays on one line
    fs = max(4.2, min(6.3, 6.3 * (width - 48) / 371))
    return f'<p dir="rtl" style="text-align:center;font-size:{fs:.1f}pt;color:#6b6b6b;margin:0;line-height:1.3;white-space:nowrap">{a.text}</p>'

d = fitz.open(a.src)
n = 0
for i, p in enumerate(d):
    if i < a.skip_first:
        continue
    r = p.rect
    rc = p.insert_htmlbox(fitz.Rect(24, r.height - a.bottom - 14, r.width - 24, r.height - a.bottom), html_for(r.width), css=CSS, archive=arch)
    if rc[0] < 0:
        print("text did not fit on page", i + 1)
    n += 1
d.subset_fonts()
d.save(a.out, garbage=4, deflate=True, use_objstms=1)
print(f"footer added to {n} pages -> {a.out}")
