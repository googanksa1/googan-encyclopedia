"""Step 1. Stamp the Googan credit footer on every page of a book PDF (except the cover).

    python3 tools/book_tools/book_footer.py SOURCE.pdf OUTPUT.pdf [--text "..."] [--skip-first N]

Writes a small dark centred line (website in bold brand colour) at the bottom of each page, in Cairo, e.g.
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
           " &nbsp;|&nbsp; <b dir=\"ltr\" style=\"color:#1c1b42\">googantranslation.com</b>")

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--text", default=DEFAULT)
ap.add_argument("--skip-first", type=int, default=1, help="pages at the start without footer (cover). Default 1")
ap.add_argument("--bottom", type=float, default=6)
a = ap.parse_args()

arch = fitz.Archive(str(F))

def html_for(width):   # 6.3pt on an A5 page (419pt wide); smaller on pocket-size pages so it stays on one line
    fs = max(4.6, min(7.6, 7.0 * (width - 48) / 371))
    return f'<p dir="rtl" style="text-align:center;font-size:{fs:.1f}pt;color:#333333;margin:0;line-height:1.45;white-space:nowrap">{a.text}</p>'

d = fitz.open(a.src)
import re
plain = re.sub(r"<[^>]+>", "", a.text).replace("&nbsp;", " ")
FONT_AR = fitz.Font(fontfile=str(F / "cairo-ar-700.ttf"))
n = 0
for i, p in enumerate(d):
    if i < a.skip_first:
        continue
    r = p.rect
    fs = max(4.6, min(7.6, 7.0 * (r.width - 48) / 371))
    w = min(r.width - 24, FONT_AR.text_length(plain, fs) * 0.92 + 14)   # white strip behind the line, so it reads on coloured footers too
    y1 = r.height - a.bottom + 1
    p.draw_rect(fitz.Rect((r.width - w) / 2, y1 - fs * 1.75, (r.width + w) / 2, y1), color=None, fill=(1, 1, 1), radius=0.3, overlay=True)
    rc = p.insert_htmlbox(fitz.Rect(16, r.height - a.bottom - 15, r.width - 16, r.height - a.bottom), html_for(r.width), css=CSS, archive=arch)
    if rc[0] < 0:
        print("text did not fit on page", i + 1)
    n += 1
d.subset_fonts()
d.save(a.out, garbage=4, deflate=True, use_objstms=1)
print(f"footer added to {n} pages -> {a.out}")
