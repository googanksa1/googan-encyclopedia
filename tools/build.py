#!/usr/bin/env python3
"""GOOGAN Encyclopedia static site builder.

Reads a Blogger export (Atom; Google Takeout or classic Blogger export) and
writes a static site to dist/ that keeps every original Blogger URL path
(/YYYY/MM/slug.html and /p/slug.html), for deployment on Cloudflare Pages.

Usage: python3 build.py <feed.atom> <dist_dir>
"""
import html, json, re, sys, shutil
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup, Comment

SITE = "https://www.bloggoogan.com"
NAME = "موسوعة جوجان للأعمال والاستثمار والترجمة"
SHORT = "موسوعة جوجان"
CONSULT = "https://googanconsult.com/"
TRANSL = "https://googantranslation.com/"
ORG_NAME = "Googan Business Services Company"

# Service pages verified live on 2 Nov 2026 (copied from the sites' own menus).
SVC = {
    "c_studies": CONSULT + "service-details/" + quote("دراسات-الجدوى-لمشاريع-الاستثمار"),
    "c_office": CONSULT + "service-details/" + quote("مكتب-دراسات-جدوى-معتمد"),
    "c_sidf": CONSULT + "service-details/" + quote("دراسة-جدوى-لصندوق-التنمية-الصناعي"),
    "c_restructure": CONSULT + "service-details/" + quote("إعادة-هيكلة-الأعمال-وتحسين-الأداء"),
    "c_digital": CONSULT + "service-details/" + quote("دراسات-الجدوى-للتحول-الرقمي-وتكامل-الذكاء-الاصطناعي"),
    "t_certified": TRANSL + "service-details/" + quote("الترجمة-المعتمدة"),
    "t_legal": TRANSL + "service-details/" + quote("الترجمة-القانونية"),
    "t_medical": TRANSL + "service-details/" + quote("الترجمة-الطبية"),
    "t_visa": TRANSL + "service-details/" + quote("ترجمة-التأشيرات"),
    "t_interp": TRANSL + "service-details/" + quote("الترجمة-الفورية-المتكاملة-للمؤتمرات-والندوات-والمعارض"),
    "t_financial": TRANSL + "service-details/" + quote("الترجمة-المالية"),
    "t_academic": TRANSL + "service-details/" + quote("الترجمة-الأكاديمية"),
}

# ---- taxonomy: (slug, code, title, pillar, keywords, cta-service) ----
TOPICS = [
    ("feasibility", "A1", "دراسات الجدوى", "A", ["جدوى", "feasibility"], "c_studies"),
    ("industry", "A2", "الصناعة والتصنيع", "A", ["مصنع", "صناع", "تصنيع", "factory", "إنتاج"], "c_sidf"),
    ("market-research", "A3", "بحوث السوق", "A", ["سوق", "تسويق", "عينة", "إحصا", "احصا", "market"], "c_studies"),
    ("financial-analysis", "A4", "التحليل المالي", "A", ["مالي", "تكلفة", "التكلف", "موازن", "عائد", "قيمة العملة", "npv", "irr"], "c_studies"),
    ("financing", "A5", "تمويل المشاريع", "A", ["تمويل", "صندوق", "قرض"], "c_sidf"),
    ("saudi-investment", "A6", "بيئة الاستثمار السعودية", "A", ["استثمار", "رؤية 2030", "الرياض", "السعودية", "invest"], "c_office"),
    ("management", "A7", "الإدارة وإعادة الهيكلة", "A", ["إدار", "ادار", "إشراف", "اشراف", "هيكل", "تخطيط", "ثقافة التنظيمية", "الموارد البشرية", "التغيير", "قيادة", "human resources", "management"], "c_restructure"),
    ("sectors", "A8", "موسوعة القطاعات", "A", ["منصة", "تطبيق", "منتجع", "مركز", "سياح", "زراع", "تقني", "طاقة"], "c_studies"),
    ("certified-translation", "B1", "الترجمة المعتمدة", "B", ["ترجمة معتمد", "ترجمه معتمد", "مكتب ترجمة", "مكاتب الترجمة", "certified"], "t_certified"),
    ("legal-translation", "B2", "الترجمة القانونية", "B", ["قانوني", "المحاكم", "وزارة العدل", "عقود", "legal", "علامة تجارية", "العلامة التجارية"], "t_legal"),
    ("medical-translation", "B3", "الترجمة الطبية", "B", ["طبي", "تقرير طبي", "medical"], "t_medical"),
    ("academic-translation", "B4", "الترجمة الأكاديمية", "B", ["أكاديمي", "شهادات دراسية", "academic"], "t_academic"),
    ("business-translation", "B5", "ترجمة الأعمال والمالية", "B", ["ترجمة مالية", "ترجمة تجارية"], "t_financial"),
    ("travel-documents", "B6", "وثائق السفر والتأشيرات", "B", ["سفار", "تأشير", "visa", "embass"], "t_visa"),
    ("interpretation", "B7", "الترجمة الفورية", "B", ["فوري", "interpret"], "t_interp"),
    ("translation-standards", "B8", "معايير الترجمة وتقنياتها", "B", ["الترجمة الآلية", "جودة الترجمة"], "t_certified"),
    ("languages", "B9", "أدلة اللغات", "B", ["فرنسي", "أردي", "اردو", "صيني", "عبري", "اندونيس", "إندونيس", "traduction", "اردو", "中"], "t_certified"),
]
TOPIC = {t[0]: t for t in TOPICS}
ARCHIVE = ("archive", "—", "أرشيف عام", "X", [], None)

OFF_TOPIC_HINTS = ["الركبة", "ضغط الدم", "الغدة", "السعادة", "اليهودية", "السجائر", "زوجتي", "عبادة",
                   "القران", "القرآن", "التخلف العقلي", "البيت الواسع", "اوراق الزيتون", "أوراق الزيتون"]

OLD_HOSTS = ("googan.co", "www.googan.co", "services.googan.co", "googangroup.com", "www.googangroup.com",
             "certified-translation-office.co", "www.certified-translation-office.co")


def text_of(el, tag, ns):
    x = el.find(tag, ns)
    return (x.text or "").strip() if x is not None and x.text else ""


def parse_feed(path):
    tree = ET.parse(path)
    root = tree.getroot()
    A = "{http://www.w3.org/2005/Atom}"
    out = []
    for e in root.iter(A + "entry"):
        typ = status = filename = ""
        for ch in e:
            local = ch.tag.split("}")[-1]
            if local == "type" and "blogger" in ch.tag:
                typ = (ch.text or "").strip().upper()
            elif local == "status" and "blogger" in ch.tag:
                status = (ch.text or "").strip().upper()
            elif local == "filename":
                filename = (ch.text or "").strip()
        cats = [c.get("term", "") for c in e.findall(A + "category")]
        kinds = [t for t in cats if t.startswith("http://schemas.google.com/blogger/2008/kind#")]
        if not typ and kinds:  # classic export
            typ = kinds[0].split("#")[-1].upper()
        if typ not in ("POST", "PAGE"):
            continue
        draft = e.find(".//{http://purl.org/atom/app#}draft")
        if status in ("DRAFT", "DELETED") or (draft is not None and (draft.text or "").strip() == "yes"):
            continue
        if not filename:
            for l in e.findall(A + "link"):
                if l.get("rel") == "alternate":
                    filename = re.sub(r"^https?://[^/]+", "", l.get("href", ""))
        if not filename:
            continue
        labels = [t for t in cats if t and not t.startswith("http://schemas.google.com/")]
        out.append({
            "type": typ, "path": filename,
            "title": text_of(e, A + "title", {}) or "بدون عنوان",
            "published": text_of(e, A + "published", {}),
            "updated": text_of(e, A + "updated", {}),
            "labels": labels,
            "html": text_of(e, A + "content", {}),
        })
    return out


def clean_body(raw):
    """Strip pasted full documents, Word junk, inline styles/scripts; demote h1."""
    raw = re.sub(r"<!--\[if[\s\S]*?<!\[endif\]-->", "", raw)
    soup = BeautifulSoup(raw, "lxml")
    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for t in soup.find_all(["style", "script", "meta", "link", "title", "noscript", "xml", "o:p"]):
        t.decompose()
    body = soup.body or soup
    for h in body.find_all("h1"):
        h.name = "h2"
    for t in body.find_all(True):
        for a in ("style", "class", "lang", "dir", "align", "face", "size", "color", "id"):
            if a in t.attrs and not (t.name == "a" and a == "id"):
                del t.attrs[a]
        if t.name in ("font", "span") and not t.attrs:
            t.unwrap()
    for img in body.find_all("img"):
        img["loading"] = "lazy"
        img["decoding"] = "async"
        if not img.get("alt"):
            img["alt"] = ""
    for tb in body.find_all("table"):
        tb.wrap(soup.new_tag("div", attrs={"class": "table-wrap"}))
    inner = "".join(str(c) for c in body.contents)
    inner = re.sub(r"(<p>\s*(&nbsp;| )?\s*</p>\s*)+", "", inner)
    inner = re.sub(r"<(/?)(html|body|head)[^>]*>", "", inner)
    return inner


def retarget_links(body_html, topic_cta):
    soup = BeautifulSoup(body_html, "lxml")
    changed = 0
    for a in soup.find_all("a", href=True):
        h = a["href"]
        m = re.match(r"^https?://([^/]+)(/.*)?$", h)
        if not m:
            continue
        host = m.group(1).lower()
        if host in ("bloggoogan.com", "www.bloggoogan.com", "googangroup.blogspot.com"):
            a["href"] = re.sub(r"^https?://[^/]+", "", h).replace("?m=1", "") or "/"
            continue
        if host in OLD_HOSTS:
            p = (m.group(2) or "").lower()
            if "translation" in p or "certified-translation-office" in host or "ترجم" in p:
                key = "t_legal" if ("legal" in p or "court" in p) else ("t_medical" if "medical" in p else "t_certified")
            elif "industrial" in p or "factory" in p or "صناع" in p:
                key = "c_sidf"
            else:
                key = topic_cta if (topic_cta or "").startswith("c_") else "c_studies"
            a["href"] = SVC[key]
            changed += 1
        if not host.endswith("bloggoogan.com"):
            a["rel"] = "noopener"
    b = soup.body or soup
    return "".join(str(c) for c in b.contents), changed


def plain(s, n=158):
    t = BeautifulSoup(s, "lxml").get_text(" ", strip=True)
    t = re.sub(r"\s+", " ", t)
    return (t[:n].rsplit(" ", 1)[0] + "…") if len(t) > n else t


OVERRIDES = {
    "/2025/09/blog-post_18.html": "management", "/2025/09/blog-post_25.html": "feasibility",
    "/2025/06/top-10-feasibility-study-questions.html": "feasibility", "/2012/02/blog-post.html": "feasibility",
    "/2012/03/blog-post_25.html": "market-research", "/2025/01/what-is-devaluation.html": "financial-analysis",
    "/2025/05/blog-post_26.html": "sectors", "/2012/08/blog-post_862.html": "sectors",
    "/2012/02/persian-translation.html": "languages", "/2012/02/ukrainian-translation.html": "languages",
    "/2012/04/blog-post_7476.html": "languages", "/2012/02/blog-post_8927.html": "languages",
    "/2026/08/about-googan.html": "about",
}


def classify(p):
    if p["path"] in OVERRIDES:
        return OVERRIDES[p["path"]]
    hay = (p["title"] + " " + " ".join(p["labels"])).lower()
    if any(k in hay for k in OFF_TOPIC_HINTS):
        return "archive"
    best, score = "archive", 0
    for slug, code, title, pillar, kws, cta in TOPICS:
        s = sum(hay.count(k.lower()) for k in kws)
        if slug in ("certified-translation",) and s:
            s += 0.5
        if s > score:
            best, score = slug, s
    return best


def fmt_date(iso):
    try:
        d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except Exception:
        return iso[:10], iso[:10]
    months = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
    return f"{d.day} {months[d.month-1]} {d.year}", d.strftime("%Y-%m-%d")


CSS = Path(__file__).with_name("style.css").read_text(encoding="utf-8")


def page(title, desc, canonical, body, *, noindex=False, jsonld=None, og_type="website"):
    ld = ""
    for obj in (jsonld or []):
        ld += '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>\n"
    robots = '<meta name="robots" content="noindex,follow">\n' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">\n'
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
{robots}<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="ar_SA">
<meta property="og:site_name" content="{NAME}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="alternate" type="application/atom+xml" title="{NAME}" href="/feeds/posts/default">
<link rel="stylesheet" href="/assets/site.css">
{ld}</head>
<body>
<a class="skip" href="#main">تخطَّ إلى المحتوى</a>
<header class="site-header">
 <div class="wrap hdr">
  <a class="brand" href="/"><span class="mark">ج</span><span><strong>{SHORT}</strong><small>للأعمال والاستثمار والترجمة</small></span></a>
  <nav class="nav" aria-label="التنقل الرئيسي">
   <a href="/topics/feasibility/">الجدوى والاستثمار</a>
   <a href="/topics/certified-translation/">الترجمة</a>
   <a href="/topics/">كل المحاور</a>
   <a href="/about/">عن الموسوعة</a>
  </nav>
  <div class="cta-pair">
   <a class="btn btn-a" href="{CONSULT}">جوجان للدراسات</a>
   <a class="btn btn-b" href="{TRANSL}">جوجان للترجمة</a>
  </div>
 </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
 <div class="wrap foot">
  <div><strong>{NAME}</strong><p>مرجع عربي تعليمي في دراسات الجدوى والاستثمار والترجمة المعتمدة، تحرره شركة جوجان لخدمات الأعمال في الرياض.</p></div>
  <div><h2>الأقسام التجارية</h2><a href="{CONSULT}">الدراسات والاستشارات — googanconsult.com</a><a href="{TRANSL}">الترجمة المعتمدة — googantranslation.com</a></div>
  <div><h2>الموسوعة</h2><a href="/about/">عن الموسوعة ومنهجية التحرير</a><a href="/topics/">فهرس المحاور</a><a href="/sitemap.xml">خريطة الموقع</a></div>
 </div>
 <p class="copy wrap">© {datetime.now().year} شركة جوجان لخدمات الأعمال</p>
</footer>
</body>
</html>"""


def card(p):
    d, _ = fmt_date(p["published"])
    t = TOPIC.get(p["topic"], ARCHIVE)
    return (f'<article class="card"><span class="tag tag-{t[3]}">{t[2]}</span>'
            f'<h3><a href="{p["path"]}">{html.escape(p["title"])}</a></h3>'
            f'<p>{html.escape(p["desc"])}</p><time datetime="{p["published"][:10]}">{d}</time></article>')


def cta_box(key):
    if not key:
        return ""
    url = SVC[key]
    if key.startswith("c_"):
        return (f'<aside class="cta cta-a"><strong>تحتاج دراسة جدوى لمشروعك؟</strong>'
                f'<p>هذا المقال تعليمي. لإعداد دراسة فعلية لمشروعك تواصل مع قسم الدراسات في جوجان.</p>'
                f'<a class="btn btn-a" href="{url}">جوجان للدراسات والاستشارات ←</a></aside>')
    return (f'<aside class="cta cta-b"><strong>تحتاج ترجمة معتمدة لمستنداتك؟</strong>'
            f'<p>هذا المقال تعليمي. لطلب ترجمة معتمدة تواصل مع قسم الترجمة في جوجان.</p>'
            f'<a class="btn btn-b" href="{url}">جوجان للترجمة المعتمدة ←</a></aside>')


def toc_and_ids(body):
    soup = BeautifulSoup(body, "lxml")
    heads = soup.find_all("h2")
    items = []
    for i, h in enumerate(heads, 1):
        h["id"] = f"s{i}"
        items.append(f'<li><a href="#s{i}">{html.escape(h.get_text(" ", strip=True))}</a></li>')
    b = soup.body or soup
    out = "".join(str(c) for c in b.contents)
    toc = f'<nav class="toc" aria-label="محتويات المقال"><strong>محتويات المقال</strong><ol>{"".join(items)}</ol></nav>' if len(items) >= 3 else ""
    return out, toc


REWRITES = []


def build(feed, dist):
    REWRITES.clear()
    dist = Path(dist)
    if dist.exists():
        shutil.rmtree(dist)
    (dist / "assets").mkdir(parents=True)
    (dist / "assets" / "site.css").write_text(CSS, encoding="utf-8")
    items = parse_feed(feed)
    posts = [x for x in items if x["type"] == "POST"]
    pages = [x for x in items if x["type"] == "PAGE"]
    log = {"posts": len(posts), "pages": len(pages), "links_retargeted": 0, "by_topic": {}}

    for p in posts + pages:
        body = clean_body(p["html"])
        p["topic"] = classify(p) if p["type"] == "POST" else "archive"
        cta = TOPIC.get(p["topic"], ARCHIVE)[5]
        body, n = retarget_links(body, cta)
        log["links_retargeted"] += n
        p["body"], p["toc"] = toc_and_ids(body)
        if p["title"] in ("بدون عنوان", ""):
            h = BeautifulSoup(p["body"], "lxml").find(["h2", "h3", "strong"])
            p["title"] = h.get_text(" ", strip=True)[:90] if h else "مقال من أرشيف جوجان"
        p["desc"] = plain(p["body"])
        p["noindex"] = p["type"] == "POST" and p["topic"] == "archive"
        if p["topic"] == "about":
            p["topic"] = "archive"; p["noindex"] = False
        log["by_topic"][p["topic"]] = log["by_topic"].get(p["topic"], 0) + 1
    posts.sort(key=lambda x: x["published"], reverse=True)

    org = {"@type": "Organization", "@id": CONSULT + "#org", "name": ORG_NAME,
           "url": CONSULT, "sameAs": [TRANSL]}
    for p in posts + pages:
        t = TOPIC.get(p["topic"], ARCHIVE)
        d_pub, iso_pub = fmt_date(p["published"])
        d_upd, iso_upd = fmt_date(p["updated"])
        crumbs = [("الموسوعة", "/")]
        if p["type"] == "POST" and t[0] != "archive":
            crumbs.append((t[2], f"/topics/{t[0]}/"))
        elif p["type"] == "POST":
            crumbs.append(("أرشيف عام", "/topics/archive/"))
        bc = '<nav class="crumbs" aria-label="مسار التنقل">' + " / ".join(
            f'<a href="{u}">{html.escape(n)}</a>' for n, u in crumbs) + "</nav>"
        related = [q for q in posts if q is not p and q["topic"] == p["topic"]][:4]
        rel = ""
        if related and p["topic"] != "archive":
            rel = '<section class="related"><h2>مداخل ذات صلة</h2><div class="grid">' + "".join(card(q) for q in related) + "</div></section>"
        url = SITE + p["path"]
        ld = [{"@context": "https://schema.org", "@graph": [org,
               {"@type": "BlogPosting" if p["type"] == "POST" else "WebPage", "headline": p["title"][:110],
                "datePublished": p["published"], "dateModified": p["updated"], "inLanguage": "ar",
                "mainEntityOfPage": url, "publisher": {"@id": CONSULT + "#org"},
                "author": {"@id": CONSULT + "#org"}},
               {"@type": "BreadcrumbList", "itemListElement": [
                   {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)]}]}]
        art = f"""<div class="wrap article-layout">
<article class="article">
{bc}
<h1>{html.escape(p["title"])}</h1>
<p class="meta">نُشر في <time datetime="{iso_pub}">{d_pub}</time>{f' · آخر تحديث <time datetime="{iso_upd}">{d_upd}</time>' if iso_upd != iso_pub else ''} · تحرير: فريق جوجان</p>
{p["toc"]}
<div class="prose">{p["body"]}</div>
{cta_box(t[5])}
</article>
</div>
{f'<div class="wrap">{rel}</div>' if rel else ''}"""
        # Cloudflare Pages strips ".html" with a redirect. To keep the exact Blogger
        # URLs, store the file under /_posts/ and serve it at the original path with
        # a 200 rewrite in _redirects (rewrites take precedence over assets).
        key = re.sub(r"[^A-Za-z0-9_-]", "_", p["path"].strip("/")[:-5] if p["path"].endswith(".html") else p["path"].strip("/"))
        REWRITES.append(f'{p["path"]}  /_posts/{key}  200')
        out = dist / "_posts" / (key + ".html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(p["title"] + " | " + SHORT, p["desc"], url, art, noindex=p["noindex"], jsonld=ld, og_type="article"), encoding="utf-8")

    # topic hubs
    hub_list = []
    for t in TOPICS + [ARCHIVE]:
        lst = [p for p in posts if p["topic"] == t[0]]
        if not lst and t[0] != "archive":
            continue
        hub_list.append((t, len(lst)))
        intro = ("مقالات خارج نطاق الموسوعة محفوظة للأرشيف ولا تظهر في الفهرس." if t[0] == "archive"
                 else f"مداخل الموسوعة في محور «{t[2]}»، مرتبة من الأحدث.")
        body = (f'<section class="hub wrap"><nav class="crumbs"><a href="/">الموسوعة</a> / <a href="/topics/">المحاور</a></nav>'
                f'<p class="kicker">{"محور الجدوى والاستثمار" if t[3]=="A" else ("محور الترجمة والخدمات اللغوية" if t[3]=="B" else "أرشيف")} · {t[1]}</p>'
                f'<h1>{t[2]}</h1><p class="lead">{intro}</p>{cta_box(t[5])}'
                f'<div class="grid">{"".join(card(p) for p in lst)}</div></section>')
        d = dist / "topics" / t[0]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(f"{t[2]} | {SHORT}", intro, f"{SITE}/topics/{t[0]}/", body, noindex=(t[0] == "archive")), encoding="utf-8")

    def pillar_block(pl, label, kicker_cls):
        rows = "".join(f'<li><a href="/topics/{t[0]}/"><span class="code">{t[1]}</span>{t[2]}<em>{n}</em></a></li>'
                       for t, n in hub_list if t[3] == pl)
        return f'<section class="pillar pillar-{kicker_cls}"><h2>{label}</h2><ul class="topic-list">{rows}</ul></section>'

    topics_idx = (f'<section class="wrap hub"><h1>فهرس محاور الموسوعة</h1>'
                  f'<div class="pillars">{pillar_block("A", "موسوعة الجدوى والاستثمار", "a")}{pillar_block("B", "موسوعة الترجمة والخدمات اللغوية", "b")}</div></section>')
    (dist / "topics").mkdir(exist_ok=True)
    (dist / "topics" / "index.html").write_text(page(f"فهرس المحاور | {SHORT}", "فهرس محاور موسوعة جوجان في الجدوى والاستثمار والترجمة المعتمدة.", f"{SITE}/topics/", topics_idx), encoding="utf-8")

    indexed = [p for p in posts if not p["noindex"]]
    a_latest = [p for p in indexed if TOPIC.get(p["topic"], ARCHIVE)[3] == "A"][:6]
    b_latest = [p for p in indexed if TOPIC.get(p["topic"], ARCHIVE)[3] == "B"][:6]
    home = f"""<section class="hero"><div class="wrap">
<p class="kicker">مرجع عربي في الأعمال والاستثمار والترجمة</p>
<h1>{NAME}</h1>
<p class="lead">شروح ومنهجيات ومصطلحات في دراسات الجدوى والتحليل المالي وبيئة الاستثمار في السعودية، وأدلة عملية في الترجمة المعتمدة والقانونية والطبية.</p>
<div class="pillars">{pillar_block("A", "موسوعة الجدوى والاستثمار", "a")}{pillar_block("B", "موسوعة الترجمة والخدمات اللغوية", "b")}</div>
</div></section>
<section class="wrap"><h2 class="sec">أحدث مداخل الجدوى والاستثمار</h2><div class="grid">{"".join(card(p) for p in a_latest)}</div></section>
<section class="wrap"><h2 class="sec">أحدث مداخل الترجمة</h2><div class="grid">{"".join(card(p) for p in b_latest)}</div></section>
<section class="wrap split-cta">{cta_box("c_studies")}{cta_box("t_certified")}</section>"""
    site_ld = [{"@context": "https://schema.org", "@graph": [org, {"@type": "WebSite", "name": NAME, "url": SITE + "/", "inLanguage": "ar", "publisher": {"@id": CONSULT + "#org"}}]}]
    (dist / "index.html").write_text(page(NAME, "موسوعة عربية من جوجان في دراسات الجدوى والاستثمار في السعودية والترجمة المعتمدة.", SITE + "/", home, jsonld=site_ld), encoding="utf-8")

    about = f"""<section class="wrap hub prose"><h1>عن الموسوعة ومنهجية التحرير</h1>
<p>«{NAME}» مرجع تعليمي تحرره شركة جوجان لخدمات الأعمال في الرياض. تخدم الموسوعة قسمين: الدراسات والاستشارات (<a href="{CONSULT}">googanconsult.com</a>) والترجمة المعتمدة (<a href="{TRANSL}">googantranslation.com</a>).</p>
<h2>منهجية التحرير</h2><ul><li>كل رقم أو اشتراط نظامي يُنسب إلى مصدره الرسمي، ويُذكر تاريخ آخر مراجعة.</li><li>المحتوى تعليمي ولا يغني عن استشارة مهنية لحالتك.</li><li>نصحح الأخطاء عند اكتشافها، ونحدّث تاريخ المراجعة.</li></ul>
<h2>التصحيح والتواصل</h2><p>لملاحظة على أي مقال: info@googan.net</p></section>"""
    (dist / "about").mkdir(exist_ok=True)
    (dist / "about" / "index.html").write_text(page(f"عن الموسوعة | {SHORT}", "عن موسوعة جوجان ومنهجية التحرير والتصحيح.", f"{SITE}/about/", about), encoding="utf-8")

    (dist / "404.html").write_text(page(f"الصفحة غير موجودة | {SHORT}", "الصفحة غير موجودة.", SITE + "/404", '<section class="wrap hub"><h1>الصفحة غير موجودة</h1><p class="lead">ربما نُقلت الصفحة. ابدأ من <a href="/topics/">فهرس المحاور</a>.</p></section>', noindex=True), encoding="utf-8")

    # sitemap (indexable only), robots, feed, redirects, headers
    urls = [SITE + "/", SITE + "/topics/", SITE + "/about/"] + [f"{SITE}/topics/{t[0]}/" for t, n in hub_list if t[0] != "archive"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"<url><loc>{u}</loc></url>")
    for p in [x for x in posts + pages if not x["noindex"]]:
        sm.append(f"<url><loc>{SITE}{p['path']}</loc><lastmod>{p['updated'][:10]}</lastmod></url>")
    sm.append("</urlset>")
    (dist / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")
    (dist / "robots.txt").write_text(f"User-agent: *\nDisallow: /_posts/\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")

    feed_items = "".join(
        f'<entry><title>{html.escape(p["title"])}</title><link href="{SITE}{p["path"]}"/><id>{SITE}{p["path"]}</id>'
        f'<published>{p["published"]}</published><updated>{p["updated"]}</updated><summary>{html.escape(p["desc"])}</summary></entry>'
        for p in indexed[:30])
    (dist / "feeds" / "posts").mkdir(parents=True, exist_ok=True)
    (dist / "feeds" / "posts" / "default").write_text(
        f'<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>{NAME}</title>'
        f'<link href="{SITE}/"/><id>{SITE}/</id><updated>{posts[0]["updated"] if posts else ""}</updated>{feed_items}</feed>', encoding="utf-8")

    # Cloudflare Pages _redirects: old Blogger label/search/archive URLs -> hubs (301)
    redir = ["# Blogger legacy URLs -> encyclopedia hubs (301)",
             "/search/label/*  /topics/  301",
             "/search  /topics/  301",
             "/feeds/posts/summary  /feeds/posts/default  301"]
    months = sorted({p["path"][:9] for p in posts if re.match(r"^/\d{4}/\d{2}/", p["path"])})
    redir += [f"{m}  /topics/  301" for m in months]
    shutil.copy(Path(__file__).with_name("_worker.js"), dist / "_worker.js")
    (dist / "_redirects").write_text("\n".join(redir) + "\n", encoding="utf-8")
    (dist / "_headers").write_text("/feeds/*\n  Content-Type: application/atom+xml; charset=utf-8\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n", encoding="utf-8")
    (dist / "build-log.json").write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    return log


if __name__ == "__main__":
    print(json.dumps(build(sys.argv[1], sys.argv[2]), ensure_ascii=False, indent=1))
