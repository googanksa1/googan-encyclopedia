"""Read-only online books (no download). Generated into dist/books/ by build4.build()."""
import json, re, shutil
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


PREVIEW = (0, 1, 3)   # sections shown as readable text on the book page


def build_books(dist, *, page, banner, crumbs, esc, icon, transl, short, ver):
    """Book page (indexable: info, prominent contents, first pages as text) + flip-book reader
    (noindex, page images only, no download link). Returns (sitemap urls, redirects)."""
    import hashlib
    ver = hashlib.md5((HERE / "reader.js").read_bytes()).hexdigest()[:8]
    root = Path(dist) / "books"
    cards, urls, redirects = [], ["/books/"], {}
    shutil.copy(HERE / "page-flip.js", Path(dist) / "assets" / "page-flip.js")
    shutil.copy(HERE / "reader.js", Path(dist) / "assets" / "reader.js")
    for bk in BOOKS:
        secs = json.load(open(HERE / "content" / "books" / bk["file"], encoding="utf-8"))
        imgs = HERE / "content" / "books" / f"{bk['slug']}-pages"
        npages = len(list(imgs.glob("*.webp")))
        base = f"/books/{bk['slug']}/"
        read = base + "read/"
        shutil.copytree(imgs, root / bk["slug"] / "pages")
        credit = f'<p class="bk-credit">{icon("book")}<span>{esc(bk["credit"])}. <a href="{transl}">googantranslation.com</a></span></p>'
        toc_cards = "".join(
            f'<li><a href="{read}#p={s["page"]}"><span class="bk-ch">{esc(s["title"])}</span>{"<b>" + esc(s["sub"]) + "</b>" if s.get("sub") else ""}<small>صفحة {s["page"] - 1}</small></a></li>'
            for s in secs)
        preview = "".join(f'<section class="bk-pre"><h2>{esc(label(secs[i]))}</h2><div class="prose bk-text">{render(secs[i]["blocks"], esc)}</div></section>' for i in PREVIEW)
        info = f"""<dl class="bk-info"><div><dt>العنوان الأصلي</dt><dd dir="ltr">{esc(bk['orig'])}</dd></div><div><dt>المؤلفان</dt><dd>{esc(bk['authors_ar'])} <span dir="ltr">({esc(bk['authors'])})</span></dd></div><div><dt>الترجمة والتدقيق</dt><dd>شركة جوجان لخدمات الأعمال، لجمعية المشعل الخيرية وقويم</dd></div><div><dt>عدد الصفحات</dt><dd>{npages - 2} صفحة</dd></div><div><dt>الإتاحة</dt><dd>قراءة مجانية على الموقع بتقليب الصفحات</dd></div></dl>"""
        body = banner(esc(bk["title"]), esc(bk["desc"]), crumbs([(short, "/"), ("مكتبة الكتب", "/books/"), (bk["title"], None)])) + f"""
<div class="wrap bk-top"><a class="bk-cover" href="{read}#p=1"><img src="{base}pages/001.webp" alt="غلاف كتاب {esc(bk['title'])}" width="420" height="625"></a>
<div class="bk-top-copy">{info}<p class="bk-go"><a class="btn" href="{read}">{icon('book')}اقرأ الكتاب</a></p>{credit}</div></div>
<div class="wrap bk-contents"><h2>فهرس الكتاب</h2><p class="bk-hint">اختر فصلاً ليُفتح الكتاب على صفحته مباشرة.</p><ol class="bk-chs">{toc_cards}</ol></div>
<div class="wrap narrow bk-preview"><h2 class="bk-pre-h">من الصفحات الأولى</h2>{preview}
<p class="bk-go"><a class="btn" href="{read}#p={secs[PREVIEW[-1] + 1]['page']}">أكمل القراءة في الكتاب</a></p>{credit}</div>"""
        (root / bk["slug"]).mkdir(parents=True, exist_ok=True)
        ld = [{"@context": "https://schema.org", "@type": "Book", "name": bk["title"], "inLanguage": "ar", "numberOfPages": npages - 2,
               "author": [{"@type": "Person", "name": n.strip()} for n in bk["authors"].split("&")],
               "translator": {"@type": "Organization", "name": "شركة جوجان لخدمات الأعمال"}, "workTranslation": None,
               "translationOfWork": {"@type": "Book", "name": bk["orig"], "inLanguage": "en"}, "url": page.__globals__["SITE"] + base,
               "image": page.__globals__["SITE"] + base + "pages/001.webp"}]
        ld[0].pop("workTranslation")
        (root / bk["slug"] / "index.html").write_text(page(f"{bk['title']} | {short}", bk["desc"], base, body, ld=ld, og_image=page.__globals__["SITE"] + base + "pages/001.webp"), encoding="utf-8")
        urls.append(base)
        opts = "".join(f'<option value="{s["page"]}">{esc(label(s))}</option>' for s in secs)
        rbody = f"""<div class="rd" data-reader data-pages="{npages}" data-dir="{base}pages/" data-slug="{bk['slug']}">
<div class="rd-bar"><a class="rd-back" href="{base}">{esc(bk['title'])}</a>
<label class="rd-toc"><span class="sr">انتقل إلى فصل</span><select data-toc><option value="">الفهرس</option>{opts}</select></label>
<span class="rd-count" data-count aria-live="polite"></span>
<span class="rd-tools"><button type="button" data-zoom title="تكبير الصفحة">تكبير</button><button type="button" data-sound aria-pressed="true">الصوت</button><button type="button" data-fs title="ملء الشاشة">ملء الشاشة</button></span></div>
<div class="rd-stage"><button class="rd-nav rd-prev" type="button" data-prev aria-label="الصفحة السابقة">›</button><div class="rd-wrap"><div class="rd-book"></div></div><button class="rd-nav rd-next" type="button" data-next aria-label="الصفحة التالية">‹</button></div>
<p class="rd-credit">{esc(bk['credit'])}. <a href="{transl}">googantranslation.com</a></p>
<div class="rd-zoom" hidden tabindex="-1" role="dialog" aria-label="الصفحة مكبرة"><button type="button" data-close>إغلاق</button><div class="rd-zoom-in"></div></div>
</div>
<script src="/assets/page-flip.js?v={ver}" defer></script><script src="/assets/reader.js?v={ver}" defer></script>"""
        (root / bk["slug"] / "read").mkdir(parents=True, exist_ok=True)
        (root / bk["slug"] / "read" / "index.html").write_text(page(f"اقرأ: {bk['title']} | {short}", bk["desc"], read, rbody, noindex=True, cls="is-reader"), encoding="utf-8")
        for i, s in enumerate(secs):   # retired text-chapter URLs -> same place in the reader
            redirects[f"{base}{i+1:02d}/"] = f"{read}#p={s['page']}"
            redirects[f"{base}{i+1:02d}"] = f"{read}#p={s['page']}"
        cards.append(f'<li class="bk-card"><a href="{base}"><img src="{base}pages/001.webp" alt="" width="120" height="179" loading="lazy"><span><strong>{esc(bk["title"])}</strong><span>{esc(bk["authors_ar"])}</span><span>{npages - 2} صفحة</span></span></a></li>')
    body = banner("مكتبة الكتب", "كتب كاملة ترجمها قسم الترجمة في جوجان، تُقرأ مجاناً على الموقع بتقليب الصفحات.", crumbs([(short, "/"), ("مكتبة الكتب", None)])) + f'<div class="wrap narrow"><ul class="bk-cards">{"".join(cards)}</ul></div>'
    (root / "index.html").write_text(page(f"مكتبة الكتب | {short}", "كتب مترجمة تُقرأ مجاناً على موسوعة جوجان بتقليب الصفحات.", "/books/", body), encoding="utf-8")
    return urls, redirects
