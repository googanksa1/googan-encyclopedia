"""Read-only online books (no download). Generated into dist/books/ by build4.build()."""
import json, re
from pathlib import Path

HERE = Path(__file__).parent
BOOKS = [{
    "slug": "staying-sober",
    "file": "staying-sober.json",
    "title": "البقاء متزناً: دليل الوقاية من الانتكاسة",
    "orig": "Staying Sober: A Guide for Relapse Prevention",
    "authors": "Terence T. Gorski & Merlene Miller",
    "authors_ar": "تيرنس غورسكي وميرلين ميلر",
    "desc": "النسخة العربية من كتاب «Staying Sober» لتيرنس غورسكي وميرلين ميلر: دليل عملي لفهم الانتكاسة في مرض الإدمان وعلاماتها التحذيرية وكيفية التخطيط للوقاية منها، مع دور الأسرة ومجموعات المساعدة الذاتية.",
    "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال",
}]

FIX = [(re.compile(r'([.،:؛])(?=[ء-ي])'), r'\1 '), (re.compile(r'([ً-ْ])\1+'), r'\1')]


def clean(t):
    for rx, rep in FIX:
        t = rx.sub(rep, t)
    return t


def render(blocks, esc):
    out = []
    for kind, txt in blocks:
        if kind == "mixed":
            a, _, b = txt.partition("||")
            out.append(f"<p><strong>{esc(clean(a))}</strong> {esc(clean(b))}</p>")
            continue
        t = esc(clean(txt))
        if kind == "h2": out.append(f"<h2>{t}</h2>")
        elif kind == "h3": out.append(f"<h3>{t}</h3>")
        elif kind == "quote": out.append(f'<blockquote class="bk-key"><p>{t}</p></blockquote>')
        elif kind == "bold": out.append(f"<p><strong>{t}</strong></p>")
        else: out.append(f"<p>{t}</p>")
    return "\n".join(out)


def label(s):
    return s["title"] + (f": {s['sub']}" if s.get("sub") else "")


def build_books(dist, *, page, banner, crumbs, esc, icon, transl, short):
    root = Path(dist) / "books"
    cards = []
    for bk in BOOKS:
        secs = json.load(open(HERE / "content" / "books" / bk["file"], encoding="utf-8"))
        base = f"/books/{bk['slug']}/"
        credit = f'<p class="bk-credit">{icon("book")}{esc(bk["credit"])}. <a href="{transl}">googantranslation.com</a></p>'
        words = sum(len(t.split()) for s in secs for _, t in s["blocks"])
        toc = "".join(f'<li><a href="{base}{i+1:02d}/">{esc(label(s))}</a></li>' for i, s in enumerate(secs))
        info = f"""<dl class="bk-info"><div><dt>العنوان الأصلي</dt><dd dir="ltr">{esc(bk['orig'])}</dd></div><div><dt>المؤلفان</dt><dd>{esc(bk['authors_ar'])} <span dir="ltr">({esc(bk['authors'])})</span></dd></div><div><dt>الترجمة والتدقيق</dt><dd>شركة جوجان لخدمات الأعمال، لجمعية المشعل الخيرية وقويم</dd></div><div><dt>الحجم</dt><dd>{len(secs)} قسماً، نحو {words // 1000} ألف كلمة</dd></div><div><dt>الإتاحة</dt><dd>قراءة مجانية على الموقع</dd></div></dl>"""
        body = banner(esc(bk["title"]), esc(bk["desc"]), crumbs([(short, "/"), ("مكتبة الكتب", "/books/"), (bk["title"], None)])) + f"""
<div class="wrap narrow bk-index">{info}{credit}
<p><a class="btn" href="{base}01/">ابدأ القراءة</a></p>
<h2>فهرس الكتاب</h2><ol class="bk-toc">{toc}</ol></div>"""
        (root / bk["slug"]).mkdir(parents=True, exist_ok=True)
        (root / bk["slug"] / "index.html").write_text(page(f"{bk['title']} | {short}", bk["desc"], base, body, noindex=True), encoding="utf-8")
        for i, s in enumerate(secs):
            n = i + 1
            prev_a = f'<a class="bk-prev" href="{base}{n-1:02d}/"><small>السابق</small>{esc(label(secs[i-1]))}</a>' if i else f'<a class="bk-prev" href="{base}"><small>السابق</small>غلاف الكتاب وفهرسه</a>'
            next_a = f'<a class="bk-next" href="{base}{n+1:02d}/"><small>التالي</small>{esc(label(secs[i+1]))}</a>' if n < len(secs) else ""
            side = "".join(f'<li{" aria-current=page" if j == i else ""}><a href="{base}{j+1:02d}/">{esc(label(x))}</a></li>' for j, x in enumerate(secs))
            h1 = esc(s["title"]) + (f'<span class="bk-sub">{esc(s["sub"])}</span>' if s.get("sub") else "")
            body = f"""<section class="banner pb bk-banner"><div class="wrap">{crumbs([(short, "/"), ("مكتبة الكتب", "/books/"), (bk["title"], base), (s["title"], None)])}<p class="bk-book"><a href="{base}">{esc(bk["title"])}</a></p><h1>{h1}</h1><p class="sub">القسم {n} من {len(secs)}</p></div></section>
<div class="wrap art-grid bk-grid"><article class="art-main"><div class="prose bk-text">{render(s["blocks"], esc)}</div>
{credit}<nav class="bk-pager" aria-label="التنقل بين الفصول">{prev_a}{next_a}</nav></article>
<aside class="art-side"><nav class="side-box bk-side" aria-label="فهرس الكتاب"><h2>فهرس الكتاب</h2><ol>{side}</ol></nav></aside></div>"""
            d = root / bk["slug"] / f"{n:02d}"
            d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(page(f"{label(s)} | {bk['title']}", f"{label(s)}، من كتاب {bk['title']}. قراءة مجانية على موسوعة جوجان.", f"{base}{n:02d}/", body, noindex=True), encoding="utf-8")
        cards.append(f'<li class="bk-card"><a href="{base}"><strong>{esc(bk["title"])}</strong><span>{esc(bk["authors_ar"])}</span><span>{len(secs)} قسماً</span></a></li>')
    body = banner("مكتبة الكتب", "كتب كاملة ترجمها قسم الترجمة في جوجان وتُقرأ مجاناً على الموقع.", crumbs([(short, "/"), ("مكتبة الكتب", None)])) + f'<div class="wrap narrow"><ul class="bk-cards">{"".join(cards)}</ul></div>'
    (root / "index.html").write_text(page(f"مكتبة الكتب | {short}", "كتب مترجمة تُقرأ مجاناً على موسوعة جوجان.", "/books/", body, noindex=True), encoding="utf-8")
