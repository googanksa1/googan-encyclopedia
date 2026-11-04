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
        others = [q for q in studies if q is not p][:6]
        body = f"""<section class="banner pb bk-banner"><div class="wrap">{crumbs(cr)}<h1>{esc(p['title'])}</h1>
<p class="sub">{icon('cal')}نُشر <time datetime="{iso_pub}">{d_pub}</time> · {p['mins']} دقيقة قراءة</p></div></section>
<div class="wrap art-grid bk-grid"><article class="art-main">{lead}{toc}<div class="prose">{p['body']}</div>
{credit_line}
<p class="disclaimer">{icon('book')}المحتوى للاطلاع العلمي العام، والمرجع النهائي هو نص الدراسة الأصلية المذكورة في أعلى الصفحة.</p></article>
<aside class="art-side"><nav class="side-box bk-side" aria-label="دراسات أخرى"><h2>دراسات أخرى</h2><ol>{''.join(f'<li><a href="{q["path"]}">{esc(q["title"])}</a></li>' for q in others)}</ol><p><a href="/studies/">كل الدراسات</a></p></nav></aside></div>"""
        url = SITE + p["path"]
        ld = [{"@context": "https://schema.org", "@graph": [org,
               {"@type": "Article", "@id": url + "#article", "headline": p["title"][:110], "description": p["desc"], "datePublished": p["published"],
                "dateModified": p["updated"], "inLanguage": "ar", "mainEntityOfPage": url, "wordCount": p["words"],
                "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}},
               {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (u or p["path"])} for i, (n, u) in enumerate(cr)]}]}]
        d = out / "studies" / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(f"{p.get('seo_title') or p['title']} | {NAME}", p["desc"], p["path"], body, ld=ld, og_type="article", cls="is-article"), encoding="utf-8")

    def study_list(lst):
        return "<ul class=\"bk-cards\">" + "".join(
            f'<li class="bk-card"><a href="{p["path"]}"><strong>{esc(p["title"])}</strong><span>{esc(p["desc"][:150].rsplit(" ", 1)[0])}…</span><span>{p["mins"]} دقيقة قراءة</span></a></li>' for p in lst) + "</ul>"

    st_intro = M.HUB_INTRO.get("translated-studies", "")
    body = banner("الدراسات المترجمة", f"{len(studies)} دراسة منشورة حتى الآن." if studies else "تُنشر الدراسات تباعاً.", crumbs([home_c, ("الدراسات المترجمة", None)]), pc="pb") + \
        f'<div class="wrap narrow"><div class="prose"><p>{st_intro}</p></div>{study_list(studies)}</div>'
    (out / "studies").mkdir(exist_ok=True)
    (out / "studies" / "index.html").write_text(page(f"الدراسات المترجمة | {NAME}", st_intro[:155], "/studies/", body), encoding="utf-8")

    # ---------------- books
    import books
    (out / "assets").mkdir(exist_ok=True)   # reader scripts; the worker falls back to the root /assets/
    book_urls, host_redirects = books.build_books(out, page=page, banner=banner, crumbs=crumbs, esc=esc, icon=icon, transl=M.TRANSL, short=NAME, ver=M.V)
    for u in book_urls:
        redirects[u] = SITE + u
    for k, v in host_redirects.items():   # retired text chapters -> straight to the library reader
        redirects[k] = SITE + v

    # ---------------- home
    home = banner(NAME, "كتب كاملة ودراسات علمية محكّمة ترجمها قسم الترجمة في شركة جوجان لخدمات الأعمال، تُقرأ مجاناً على الموقع مع ذكر المصدر الأصلي.", "", pc="pb") + f"""
<div class="wrap narrow" style="padding-top:1.5rem">
<section><div class="sec-head"><h2>الكتب</h2><a class="link" href="/books/">كل الكتب ({len(books.BOOKS)}) {icon('chev')}</a></div>{books.category_sections(esc, heading="h3", limit=6)}</section>
<section><div class="sec-head"><h2>أحدث الدراسات المترجمة</h2><a class="link" href="/studies/">كل الدراسات {icon('chev')}</a></div>{study_list(studies[:8])}</section>
</div>"""
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
    urls = ["/", "/studies/", "/about/"] + [p["path"] for p in studies] + book_urls
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    upd = {p["path"]: p["updated"][:10] for p in studies}
    sm += [f"<url><loc>{SITE}{u}</loc><lastmod>{upd.get(u, today)}</lastmod></url>" for u in urls]
    (out / "sitemap.xml").write_text("\n".join(sm + ["</urlset>"]), encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    fi = "".join(f'<entry><title>{esc(p["title"])}</title><link href="{SITE}{p["path"]}"/><id>{SITE}{p["path"]}</id><published>{p["published"]}</published><updated>{p["updated"]}</updated><summary>{esc(p["desc"])}</summary></entry>' for p in studies[:30])
    (out / "feed.xml").write_text(f'<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>{NAME}</title><link href="{SITE}/"/><id>{SITE}/</id><updated>{studies[0]["updated"] if studies else today}</updated>{fi}</feed>', encoding="utf-8")
    return {"redirects": redirects, "host_redirects": host_redirects, "summary": {"studies": len(studies), "books": len(books.BOOKS), "pages": len(urls)}}
