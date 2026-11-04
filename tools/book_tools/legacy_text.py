"""Text extraction for Arabic PDFs.

Two cases:
* Normal Unicode PDFs: PyMuPDF reads the text directly.
* Old Arabic design fonts (Muna, Ahmad, Hassan: "Arabic XT" visual encoding, used in the
  Almashal books): the text layer is garbage. We read each glyph's *name* from the embedded CFF
  font (via its glyph id) and map it to Arabic with namemap.json, then put the line back into
  logical (right-to-left) order. If the decoder meets a glyph name it does not know, it prints it
  under "UNKNOWN GLYPHS" and writes '�' in the text: add that name to namemap.json and rerun.
"""
import collections, io, json, re
from pathlib import Path
from fontTools.cffLib import CFFFontSet

NAME = json.load(open(Path(__file__).parent / "namemap.json", encoding="utf-8"))
LEGACY_FONTS = ("Muna", "Ahmad", "Hassan")
DIAC = set("ًٌٍَُِّْ")
UNKNOWN = collections.Counter()
_cache = {}


def is_legacy(doc, pages=range(5, 15)):
    for i in pages:
        if i < len(doc):
            for f in doc[i].get_fonts():
                if f[3].split("+")[-1].startswith(LEGACY_FONTS):
                    return True
    return False


def _names(doc, xref):
    if xref in _cache:
        return _cache[xref]
    try:
        _, _, _, buf = doc.extract_font(xref)
        cf = CFFFontSet(); cf.decompile(io.BytesIO(buf), None)
        r = list(cf[cf.fontNames[0]].CharStrings.keys())
    except Exception:
        r = None
    _cache[xref] = r
    return r


def _fix(seq):
    seq = seq[::-1]; res = []
    for t in seq:
        if t and all(c in DIAC for c in t) and res:
            res[-1] += t; continue
        res.append(t)
    s = "".join(res)
    s = re.sub(r"[٠-٩]+(?:[./:][٠-٩]+)*", lambda m: m.group(0)[::-1] if len(m.group(0)) > 1 else m.group(0), s)
    s = re.sub(r"[A-Za-z0-9][A-Za-z0-9 .,'&\-]*[A-Za-z0-9]", lambda m: m.group(0)[::-1], s)
    return s


def legacy_lines(doc, p):
    """Lines of one page as dicts: y, x0, x1, size, font, text (logical Arabic order)."""
    fonts = {f[3].split("+")[-1]: f[0] for f in p.get_fonts()}
    rows = collections.defaultdict(list)
    for sp in p.get_texttrace():
        fn, size = sp["font"], sp["size"]
        ar = fn.startswith(LEGACY_FONTS)
        nm = _names(doc, fonts.get(fn)) if ar else None
        for u, gid, org, bb in sp["chars"]:
            if ar and nm and gid < len(nm):
                tok = NAME.get(nm[gid])
                if tok is None:
                    UNKNOWN[nm[gid]] += 1; tok = "�"
            else:
                tok = chr(u) if u > 0 else ""
            rows[round(org[1])].append((org[0], tok, ar, size, fn, bb))
    isd = lambda t: t and all(c in DIAC for c in t)
    ys = sorted(rows)
    main = [y for y in ys if not all(isd(i[1]) or i[1] == " " for i in rows[y])]
    for y in ys:   # diacritics sit on their own baseline: attach them to the nearest text row
        if y in main:
            continue
        near = min(main, key=lambda m: abs(m - y)) if main else None
        if near is not None and abs(near - y) <= 6:
            for it in rows[y]:
                if not isd(it[1]):
                    continue
                cx = (it[5][0] + it[5][2]) / 2
                bases = [b for b in rows[near] if not isd(b[1]) and b[5][0] - .3 <= cx <= b[5][2] + .3 and b[1].strip()]
                xk = (min(bases, key=lambda b: abs((b[5][0] + b[5][2]) / 2 - cx))[0] - .001) if bases else it[0]
                rows[near].append((xk,) + it[1:])
            del rows[y]
    out = []
    for y in sorted(rows):
        items = sorted(rows[y], key=lambda t: t[0])
        ar = sum(1 for i in items if i[2]) > len(items) / 2
        toks = [i[1] for i in items]
        txt = _fix(toks) if ar else "".join(toks)
        out.append(dict(y=y, x0=min(i[5][0] for i in items), x1=max(i[5][2] for i in items),
                        size=max(i[3] for i in items), font=collections.Counter(i[4] for i in items).most_common(1)[0][0],
                        text=re.sub(r" {2,}", " ", txt).strip()))
    return out


def unicode_lines(p):
    out = []
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            sp = [s for s in l["spans"] if s["text"].strip()]
            if not sp:
                continue
            out.append(dict(y=round(l["bbox"][3]), x0=l["bbox"][0], x1=l["bbox"][2], size=max(s["size"] for s in sp),
                            font=sp[0]["font"].split("+")[-1], text=" ".join(s["text"].strip() for s in sp)))
    return sorted(out, key=lambda l: l["y"])


def page_lines(doc, i, legacy):
    return legacy_lines(doc, doc[i]) if legacy else unicode_lines(doc[i])
