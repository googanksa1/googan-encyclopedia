"""مكتبة جوجان — library.bloggoogan.com

Books and translated studies, kept apart from the encyclopedia so the encyclopedia stays focused
on management, economics, marketing and translation (owner decision, 4 Nov 2026).

Built by build4.build() into <dist>/_library/. The Pages worker serves that folder for the
library.* hostname; shared CSS/JS come from <dist>/assets/.
"""
import json, re, shutil
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).parent
SITE = "https://library.bloggoogan.com"
NAME = "مكتبة جوجان"
SHELL = dict(
    SITE=SITE, NAME=NAME, SHORT=NAME, TAGLINE="كتب ودراسات مترجمة للقراءة المجانية",
    STRIP="كتب ودراسات علمية ترجمها قسم الترجمة في شركة جوجان لخدمات الأعمال، تُقرأ مجاناً",
    NAV=[("/", "الرئيسية"), ("/books/", "الكتب"), ("/studies/", "الدراسات المترجمة"), ("/about/", "عن المكتبة")],
    SEARCH_HOST="library.bloggoogan.com", SEARCH_PH="ابحث في الكتب والدراسات…", SEARCH_LABEL="المكتبة", FEED="/feed.xml",
    FOOT_ABOUT="مكتبة مجانية تنشر فيها شركة جوجان لخدمات الأعمال في الرياض كتباً ودراسات علمية ترجمها قسم الترجمة، مع ذكر المصدر الأصلي لكل عمل.",
    FOOT_H="المكتبة", FOOT_LINKS=[("/books/", "الكتب"), ("/studies/", "الدراسات المترجمة"), ("/about/", "عن المكتبة")],
)


def build_library(dist, M):
    """M is the build4 module. Its page shell is switched to the library brand for the duration."""
    saved = {k: getattr(M, k) for k in SHELL}
    for k, v in SHELL.items():
        setattr(M, k, v)
    try:
        return _build(Path(dist), M)
    finally:
        for k, v in saved.items():
            setattr(M, k, v)


def _build(dist, M):
    import study_covers as SC
    esc, icon, page, banner, crumbs = M.esc, M.icon, M.page, M.banner, M.crumbs
    out = dist / "_library"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    today = datetime.now().strftime("%Y-%m-%d")
    org = {"@type": "Organization", "@id": SITE + "/#org", "name": "شركة جوجان لخدمات الأعمال", "alternateName": "Googan Business Services Company",
           "url": M.TRANSL, "logo": M.LOGO, "email": "info@googan.net", "sameAs": [M.CONSULT, M.TRANSL]}
    home_c = (NAME, "/")
    credit_line = f'<p class="bk-credit">{icon("book")}ترجمة قسم الترجمة الأكاديمية في شركة جوجان لخدمات الأعمال. <a href="{M.SVC["t_academic"]}">googantranslation.com</a></p>'

    def s_tile(p):
        k = SC.field(p)
        return (f'<article class="tile st-tile"><a href="{p["path"]}"><span class="tile-img">{SC.cover_svg(p)}</span>'
                f'<span class="topic">{SC.FIELDS[k][0]}</span><h3>{esc(p["title"])}</h3><span class="tile-meta">{icon("clock")}{p["mins"]} دقيقة قراءة</span></a></article>')

    def s_mini(p):
        return f'<li><a href="{p["path"]}"><span class="mini-img">{SC.cover_svg(p, label=False)}</span><span class="mini-t">{esc(p["title"])}</span></a></li>'

    # ---------------- studies
    studies = sorted(M.load_new_posts({}, library=True), key=lambda p: p["published"], reverse=True)
    redirects = {"/topics/translated-studies/": SITE + "/studies/", "/topics/translated-studies": SITE + "/studies/"}
    for p in studies:
        redirects[p["old_path"]] = SITE + p["path"]
        d_pub, iso_pub = M.B.fmt_date(p["published"])
        cr = [home_c, ("الدراسات المترجمة", "/studies/"), (p["title"], None)]
        toc = ""
        if len(p["toc_items"]) >= 2:
            lis = "".join(f'<li><a href="#{i}">{esc(x)}</a></li>' for i, x in p["toc_items"])
            toc = f'<details class="toc" open><summary>محتويات الصفحة {icon("down")}</summary><ol>{lis}</ol></details>'
        lead = f'<div class="keybox"><h2>الخلاصة</h2><p>{esc(p["lead"])}</p></div>' if p["lead"] else ""
        same = [q for q in studies if q is not p and SC.field(q) == SC.field(p)]
        others = (same + [q for q in studies if q is not p and q not in same])[:5]
        body = f"""<section class="banner pb bk-banner"><div class="wrap">{crumbs(cr)}<h1>{esc(p['title'])}</h1>
<p class="sub"><a class="st-badge" href="/studies/f/{SC.field(p)}/">{SC.field_icon(SC.field(p), 18)}{SC.FIELDS[SC.field(p)][0]}</a> {icon('cal')}نُشر <time datetime="{iso_pub}">{d_pub}</time> · {p['mins']} دقيقة قراءة</p></div></section>
<div class="wrap art-grid bk-grid"><article class="art-main"><figure class="art-hero st-hero">{SC.cover_svg(p)}</figure>{lead}{toc}<div class="prose">{p['body']}</div>
{(f'<p class="bk-credit">{icon("book")}{esc(p["credit"])}</p>' if p.get("credit") else credit_line)}
<p class="disclaimer">{icon('book')}المحتوى للاطلاع العلمي العام، والمرجع النهائي هو نص الدراسة الأصلية المذكورة في أعلى الصفحة.</p></article>
<aside class="art-side"><div class="side-box"><h2>من المجال نفسه</h2><ul class="minis">{''.join(s_mini(q) for q in others)}</ul><p><a href="/studies/f/{SC.field(p)}/">كل دراسات {SC.FIELDS[SC.field(p)][0]}</a></p></div></aside></div>"""
        url = SITE + p["path"]
        ld = [{"@context": "https://schema.org", "@graph": [org,
               {"@type": "Article", "@id": url + "#article", "headline": p["title"][:110], "description": p["desc"], "datePublished": p["published"],
                "dateModified": p["updated"], "inLanguage": "ar", "mainEntityOfPage": url, "wordCount": p["words"],
                "author": ({"@type": "Person", "name": p["author"]} if p.get("author") else {"@id": SITE + "/#org"}), "publisher": {"@id": SITE + "/#org"}},
               {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (u or p["path"])} for i, (n, u) in enumerate(cr)]}]}]
        d = out / "studies" / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(f"{p.get('seo_title') or p['title']} | {NAME}", p["desc"], p["path"], body, ld=ld, og_type="article", cls="is-article"), encoding="utf-8")

    by_field = {}
    for p in studies:
        by_field.setdefault(SC.field(p), []).append(p)
    fields_live = [k for k in SC.FIELDS if k in by_field]
    chips = "".join(f'<a class="bk-chip" href="/studies/f/{k}/">{SC.field_icon(k, 18)}{SC.FIELDS[k][0]} <span>{len(by_field[k])}</span></a>' for k in fields_live)
    st_intro = M.HUB_INTRO.get("translated-studies", "")
    body = banner("الدراسات المترجمة", f"{len(studies)} دراسة علمية في {len(fields_live)} مجالات، لكل منها مصدرها الأصلي وسنة نشرها.", crumbs([home_c, ("الدراسات المترجمة", None)]), pc="pb") + \
        f'<div class="wrap"><nav class="bk-chips" aria-label="مجالات الدراسات">{chips}</nav>' + "".join(
            f'<section class="st-field" id="f-{k}"><div class="sec-head"><h2>{SC.field_icon(k)}{SC.FIELDS[k][0]}</h2><a class="link" href="/studies/f/{k}/">كل دراسات المجال ({len(by_field[k])}) {icon("chev")}</a></div><div class="tiles">{"".join(s_tile(p) for p in by_field[k][:6])}</div></section>'
            for k in fields_live) + '</div>'
    (out / "studies").mkdir(exist_ok=True)
    (out / "studies" / "index.html").write_text(page(f"الدراسات المترجمة | {NAME}", st_intro[:155] or "دراسات علمية مترجمة إلى العربية مع مصدرها الأصلي.", "/studies/", body), encoding="utf-8")
    field_urls = []
    for k in fields_live:
        nm, intro = SC.FIELDS[k][0], SC.FIELDS[k][1]
        b = banner(nm, f"{intro} {len(by_field[k])} دراسة.", crumbs([home_c, ("الدراسات المترجمة", "/studies/"), (nm, None)]), pc="pb") + \
            f'<div class="wrap"><nav class="bk-chips" aria-label="مجالات الدراسات">{chips}</nav><div class="tiles st-grid">{"".join(s_tile(p) for p in by_field[k])}</div></div>'
        (out / "studies" / "f" / k).mkdir(parents=True, exist_ok=True)
        (out / "studies" / "f" / k / "index.html").write_text(page(f"{nm}: دراسات مترجمة | {NAME}", intro, f"/studies/f/{k}/", b), encoding="utf-8")
        field_urls.append(f"/studies/f/{k}/")

    # ---------------- books
    import books
    (out / "assets").mkdir(exist_ok=True)   # reader scripts; the worker falls back to the root /assets/
    book_urls, host_redirects = books.build_books(out, page=page, banner=banner, crumbs=crumbs, esc=esc, icon=icon, transl=M.TRANSL, short=NAME, ver=M.V)
    for u in book_urls:
        redirects[u] = SITE + u
    for k, v in host_redirects.items():   # retired text chapters -> straight to the library reader
        redirects[k] = SITE + v

    # ---------------- home
    fan = books.BOOKS[:3]
    star = next((p for p in studies if "ترجمة كاملة" in p["body"][:4000]), studies[0] if studies else None)
    field_cards = "".join(f'<li><a href="/studies/f/{k}/"><span class="tc-img">{SC.cover_svg(by_field[k][0], 480, 270, label=False)}</span><span class="tc-body"><b>{SC.FIELDS[k][0]}</b><span>{SC.FIELDS[k][1]}</span><em>{len(by_field[k])} دراسة</em></span></a></li>' for k in fields_live)
    book_minis = "".join(f'<li><a href="/books/{b["slug"]}/"><span class="mini-img bk-mini"><img src="/books/{b["slug"]}/pages/001.webp" alt="" width="120" height="170" loading="lazy" decoding="async"></span><span class="mini-t">{esc(b["title"])}</span></a></li>' for b in books.BOOKS[3:9])
    feat = (f"""<section class="featured"><div class="wrap feat-grid">
<a class="feat-img st-feat" href="{star['path']}" tabindex="-1" aria-hidden="true">{SC.cover_svg(star, 900, 560)}</a>
<div class="feat-copy"><span class="ribbon">{icon('star')}دراسة مختارة</span><h2><a href="{star['path']}">{esc(star['title'])}</a></h2><p>{esc(star['desc'])}</p><a class="btn" href="{star['path']}">اقرأ الدراسة</a></div>
</div></section>""" if star else "")
    home = f"""<section class="hero"><div class="wrap hero-grid">
<div class="hero-copy"><h1>كتب ودراسات علمية مترجمة إلى العربية، تُقرأ مجاناً</h1>
<p class="sub">ترجمها قسم الترجمة في شركة جوجان لخدمات الأعمال، ونُشرت بموافقة أصحابها أو وفق رخصها، مع ذكر المصدر الأصلي لكل عمل.</p>
<form class="search big" action="https://www.google.com/search" method="get" role="search"><input type="hidden" name="as_sitesearch" value="library.bloggoogan.com"><label class="sr" for="q-hero">ابحث في المكتبة</label><input id="q-hero" type="search" name="q" placeholder="مثال: التوحد، الصم، الانتكاسة، زيت الزيتون" autocomplete="off"><button type="submit" aria-label="ابحث">{icon('search')}<span>ابحث</span></button></form>
<ul class="facts"><li><b>{len(books.BOOKS)}</b><span>كتاباً كاملاً</span></li><li><b>{len(studies)}</b><span>دراسة مترجمة</span></li><li><b>{len(fields_live)}</b><span>مجالات علمية</span></li></ul></div>
<figure class="hero-books">{''.join(f'<a href="/books/{b["slug"]}/" tabindex="-1" aria-hidden="true"><img src="/books/{b["slug"]}/pages/001.webp" alt="" width="300" height="425" fetchpriority="high"></a>' for b in fan)}</figure>
</div></section>

<section class="wrap topics-sec"><div class="sec-head"><h2>الدراسات حسب المجال</h2><a class="link" href="/studies/">كل الدراسات ({len(studies)}) {icon('chev')}</a></div>
<ul class="topic-cards pb st-fields">{field_cards}</ul></section>
{feat}
<section class="wrap guide-grid">
<div class="guide-main"><div class="sec-head"><h2>أحدث الدراسات</h2><a class="link" href="/studies/">كل الدراسات {icon('chev')}</a></div>
<div class="tiles">{''.join(s_tile(p) for p in studies[:6])}</div></div>
<aside class="guide-side"><div class="side-box"><h2>من مكتبة الكتب</h2><ul class="minis">{book_minis}</ul><p><a href="/books/">كل الكتب ({len(books.BOOKS)})</a></p></div></aside>
</section>

<section class="wrap"><div class="sec-head"><h2>الكتب</h2><a class="link" href="/books/">كل الكتب ({len(books.BOOKS)}) {icon('chev')}</a></div>{books.category_sections(esc, heading="h3", limit=6)}</section>

<section class="doors"><div class="wrap doors-grid">
<a class="door pb" href="{M.TRANSL}"><span class="door-ic">{icon('doc')}</span><b>جوجان للترجمة المعتمدة</b><span>ترجمة أكاديمية وقانونية وطبية ووثائق السفارات والتأشيرات.</span><em>googantranslation.com</em></a>
<a class="door pa" href="https://www.bloggoogan.com/"><span class="door-ic">{icon('chart')}</span><b>موسوعة جوجان</b><span>أدلة عملية في دراسات الجدوى والاستثمار في السعودية والترجمة المعتمدة.</span><em>bloggoogan.com</em></a>
</div></section>"""
    site_ld = [{"@context": "https://schema.org", "@graph": [org, {"@type": "WebSite", "@id": SITE + "/#site", "name": NAME, "url": SITE + "/", "inLanguage": "ar", "publisher": {"@id": SITE + "/#org"}}]}]
    (out / "index.html").write_text(page(f"{NAME}: كتب ودراسات مترجمة للقراءة المجانية", "كتب ودراسات علمية ترجمها قسم الترجمة في جوجان، تُقرأ مجاناً مع ذكر المصدر الأصلي لكل عمل.", "/", home, ld=site_ld, cls="is-home"), encoding="utf-8")

    # ---------------- about / 404
    about = banner("عن المكتبة", "ما الذي ننشره هنا، ولماذا.", crumbs([home_c, ("عن المكتبة", None)]), pc="pb") + f"""<div class="wrap narrow prose about">
<p>«{NAME}» مكتبة مجانية تنشر فيها شركة جوجان لخدمات الأعمال في الرياض أعمالاً ترجمها قسم الترجمة فيها: كتباً كاملة نُشرت بموافقة الجهة صاحبة الحق، ودراسات علمية محكّمة.</p>
<h2>الدراسات</h2><p>ننشر الترجمة الكاملة للدراسة فقط حين تسمح رخصتها الأصلية بذلك، وننشر لغيرها قراءة عربية في أهم ما جاء فيها. في كل صفحة العنوان الأصلي والمؤلفون والمجلة والسنة ورابط الدراسة.</p>
<h2>الكتب</h2><p>تُقرأ الكتب على الموقع مباشرة، وفي كل كتاب اسم الجهة التي تُرجم لها ومؤلفوه الأصليون.</p>
<h2>التواصل والتصحيح</h2><p>لملاحظة أو تصحيح راسلنا على <a href="mailto:info@googan.net">info@googan.net</a>. لخدمات الترجمة الأكاديمية والمعتمدة: <a href="{M.TRANSL}">googantranslation.com</a>.</p></div>"""
    (out / "about").mkdir(exist_ok=True)
    (out / "about" / "index.html").write_text(page(f"عن المكتبة | {NAME}", "مكتبة جوجان: كتب ودراسات ترجمها قسم الترجمة في شركة جوجان لخدمات الأعمال.", "/about/", about), encoding="utf-8")
    nf = banner("الصفحة غير موجودة", "ربما نُقلت الصفحة. ابدأ من الصفحة الرئيسية للمكتبة.", pc="pb") + '<div class="wrap narrow nf"><p><a class="btn" href="/">الصفحة الرئيسية</a> <a class="btn ghost" href="/studies/">الدراسات المترجمة</a></p></div>'
    (out / "404.html").write_text(page(f"الصفحة غير موجودة | {NAME}", "الصفحة غير موجودة.", "/404", nf, noindex=True), encoding="utf-8")

    # ---------------- sitemap, robots, feed
    urls = ["/", "/studies/", "/about/"] + field_urls + [p["path"] for p in studies] + book_urls
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    upd = {p["path"]: p["updated"][:10] for p in studies}
    sm += [f"<url><loc>{SITE}{u}</loc><lastmod>{upd.get(u, today)}</lastmod></url>" for u in urls]
    (out / "sitemap.xml").write_text("\n".join(sm + ["</urlset>"]), encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    fi = "".join(f'<entry><title>{esc(p["title"])}</title><link href="{SITE}{p["path"]}"/><id>{SITE}{p["path"]}</id><published>{p["published"]}</published><updated>{p["updated"]}</updated><summary>{esc(p["desc"])}</summary></entry>' for p in studies[:30])
    (out / "feed.xml").write_text(f'<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>{NAME}</title><link href="{SITE}/"/><id>{SITE}/</id><updated>{studies[0]["updated"] if studies else today}</updated>{fi}</feed>', encoding="utf-8")
    return {"redirects": redirects, "host_redirects": host_redirects, "summary": {"studies": len(studies), "books": len(books.BOOKS), "pages": len(urls)}}
