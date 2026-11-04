"""Step 2. Turn the finished book PDF into the page images the flip-book reader shows.

    python3 tools/book_tools/book_pages.py BOOK.pdf SLUG

Writes tools/content/books/SLUG-pages/001.webp, 002.webp, ... (840 px wide, WebP quality 68,
about 50-80 KB a page). The PDF itself is never published.

Cover: if PDF page 1 is a full cover spread (much wider than page 2, front + spine + back), it is
split: the LEFT half becomes 001.webp (front cover, for an Arabic book) and the RIGHT half becomes
the last image (back cover). Check 001.webp after running; if front and back are swapped, run
again with --swap-cover. If page 1 is a normal single page, pages are copied 1:1.

Numbering rule used by the reader and by the contents file: image NNN = PDF page NNN
(with a split spread, the back cover is one extra image at the end).
"""
import argparse, shutil
from pathlib import Path
import pymupdf as fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / "content" / "books"
ap = argparse.ArgumentParser()
ap.add_argument("pdf"); ap.add_argument("slug")
ap.add_argument("--width", type=int, default=840)
ap.add_argument("--quality", type=int, default=68)
ap.add_argument("--swap-cover", action="store_true")
a = ap.parse_args()

out = ROOT / f"{a.slug}-pages"
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)
d = fitz.open(a.pdf)


def save(img, n):
    img = img.convert("RGB")
    img = img.resize((a.width, round(img.height * a.width / img.width)), Image.LANCZOS)
    img.save(out / f"{n:03d}.webp", "WEBP", quality=a.quality, method=6)


def render(i, dpi):
    pm = d[i].get_pixmap(dpi=dpi)
    return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)


w1, w2 = d[0].rect.width, d[1].rect.width
dpi = round(a.width / (w2 / 72) * 1.05)
spread = w1 > 1.6 * w2
if spread:
    im = render(0, dpi * 2)
    sc = im.width / w1
    left = im.crop((0, 0, round(w2 * sc), im.height))
    right = im.crop((im.width - round(w2 * sc), 0, im.width, im.height))
    front, back = (right, left) if a.swap_cover else (left, right)
    save(front, 1)
    save(back, len(d) + 1)
else:
    save(render(0, dpi), 1)
for i in range(1, len(d)):
    save(render(i, dpi), i + 1)
total = len(list(out.glob("*.webp")))
size = sum(f.stat().st_size for f in out.glob("*.webp")) / 1e6
print(f"{total} images ({'cover spread split' if spread else 'no cover spread'}), {size:.1f} MB -> {out}")
