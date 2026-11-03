#!/usr/bin/env python3
"""GOOGAN Encyclopedia v2 — 'Najdi research dossier' design.
Reuses parsing/cleaning/classification from build.py; replaces all rendering.
Usage: python3 site.py <feed.atom> <dist>
"""
import html, json, re, shutil, sys, math
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import build as B

SRC = Path(__file__).parent
SITE, NAME, SHORT = B.SITE, B.NAME, B.SHORT
PILLAR = {"A": ("موسوعة الجدوى والاستثمار", "pa"), "B": ("موسوعة الترجمة والخدمات اللغوية", "pb"), "X": ("أرشيف عام", "px")}

# ---------------------------------------------------------------- content
JUNK_LINE = re.compile(r"^(الكلمات (المفتاحية|الدالة)( الرئيسية)?\s*:?|تاريخ\s*النشر|وقت\s*القراءة|بقلم\s*:|المؤلف\s*:)")


def paragraphize(h):
    """Turn <div>/<br>-built legacy posts into real paragraphs."""
    if h.count("<p") > 3 and h.count("<br") < 6:
        return h
    h = re.sub(r"</?div[^>]*>", "<br><br>", h)
    h = re.sub(r"(\s*<br\s*/?>\s*){2,}", "\n\n", h)
    parts = [x.strip() for x in h.split("\n\n")]
    out = []
    block_start = re.compile(r"^<(h[1-6]|ul|ol|table|figure|blockquote|p|iframe)\b", re.I)
    for x in parts:
        if not x or not BeautifulSoup(x, "lxml").get_text(strip=True) and "<img" not in x and "<iframe" not in x:
            continue
        out.append(x if block_start.match(x) else f"<p>{x}</p>")
    return "\n".join(out)


def improve(body_html, title):
    body_html = paragraphize(body_html)
    s = BeautifulSoup(body_html, "lxml")
    root = s.body or s
    # 1) drop pasted metadata / keyword-stuffing paragraphs
    for el in root.find_all(["p", "div", "li", "strong", "b"]):
        t = el.get_text(" ", strip=True)
        if t and JUNK_LINE.match(t) and len(t) < 400:
            el.decompose()
    # 2) drop leading heading/paragraph that just repeats the title
    norm = lambda x: re.sub(r"[^\w]", "", x)
    for el in root.find_all(["h2", "h3", "p"], limit=3):
        t = el.get_text(" ", strip=True)
        if t and (norm(t) == norm(title) or (len(t) > 15 and norm(t) in norm(title))):
            el.decompose()
            break
    # 3) articles without H2: promote standalone bold lines / short heading-like paragraphs
    if not root.find("h2") and root.find("h3"):
        for h in root.find_all(["h3", "h4"]):
            h.name = "h2" if h.name == "h3" else "h3"
    if not root.find("h2"):
        for p in root.find_all("p"):
            t = p.get_text(" ", strip=True)
            if not t or len(t) > 90:
                continue
            bold = p.find(["b", "strong"])
            only_bold = bold and bold.get_text(" ", strip=True) == t
            headingish = only_bold or (len(t) < 70 and not re.search(r"[.!؟?،,]$", t) and t.endswith(":") is False and len(t.split()) <= 10 and p.find_next_sibling("p") is not None and len(p.find_next_sibling("p").get_text()) > 140)
            if headingish:
                p.name = "h2"
                p.string = t.rstrip(":：")
    # 4) wrap images as figures, give them alt text from context
    for img in root.find_all("img"):
        if not img.get("alt"):
            img["alt"] = title
        a = img.parent if img.parent and img.parent.name == "a" else img
        if a.parent and a.parent.name != "figure":
            a.wrap(s.new_tag("figure"))
    # 5) remove empty containers
    for el in root.find_all(["p", "div", "span"]):
        if not el.get_text(strip=True) and not el.find(["img", "iframe", "table"]):
            el.decompose()
    return "".join(str(c) for c in root.contents)


def first_image(body_html):
    m = re.search(r'<img[^>]+src="([^"]+)"', body_html)
    if not m:
        return None
    u = html.unescape(m.group(1))
    if "googleusercontent.com" in u or "bp.blogspot.com" in u:
        u = re.sub(r"/(s\d+(-[a-z0-9-]+)?|w\d+-h\d+[^/]*)/", "/w1200/", u)
    return u if u.startswith("http") else None


def lead_and_rest(body_html):
    s = BeautifulSoup(body_html, "lxml")
    root = s.body or s
    for p in root.find_all("p"):
        t = p.get_text(" ", strip=True)
        if len(t) > 80:
            lead = t if len(t) < 420 else t[:400].rsplit(" ", 1)[0] + "…"
            if len(t) < 420:
                p.decompose()
            return lead, "".join(str(c) for c in root.contents)
    return "", body_html


def reading_minutes(body_html):
    n = len(BeautifulSoup(body_html, "lxml").get_text(" ").split())
    return max(1, math.ceil(n / 200)), n


# ---------------------------------------------------------------- covers
TRI = "M0 40 L20 0 L40 40 Z"


def cover_svg(title, pillar, topic_title):
    bg = {"A": "#10304d", "B": "#0f5a4d", "X": "#3b4552"}[pillar]
    t = html.escape(title)
    words, lines, cur = title.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > 26 and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    lines = lines[:4]
    if len(" ".join(lines)) < len(title):
        lines[-1] = lines[-1].rstrip("،,") + "…"
    tspans = "".join(f'<tspan x="1120" dy="{0 if i == 0 else 78}">{html.escape(l)}</tspan>' for i, l in enumerate(lines))
    y0 = 300 - (len(lines) - 1) * 39
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img" aria-label="{t}">
<defs><pattern id="n" width="40" height="44" patternUnits="userSpaceOnUse"><path d="{TRI}" fill="none" stroke="#c9a94e" stroke-opacity=".22" stroke-width="2"/></pattern></defs>
<rect width="1200" height="630" fill="{bg}"/>
<rect x="0" y="0" width="300" height="630" fill="url(#n)"/>
<rect x="0" y="560" width="1200" height="70" fill="url(#n)"/>
<rect x="300" y="0" width="6" height="560" fill="#c9a94e"/>
<text x="1120" y="110" fill="#c9a94e" font-family="Cairo, sans-serif" font-size="30" font-weight="700" text-anchor="start" direction="rtl">{html.escape(topic_title)}</text>
<text x="1120" y="{y0}" fill="#ffffff" font-family="Cairo, sans-serif" font-size="58" font-weight="800" text-anchor="start" direction="rtl">{tspans}</text>
<text x="1120" y="530" fill="#dfe6ee" font-family="Cairo, sans-serif" font-size="26" text-anchor="start" direction="rtl">موسوعة جوجان للأعمال والاستثمار والترجمة</text>
</svg>'''


# ---------------------------------------------------------------- shell
def page(title, desc, canonical, body, *, noindex=False, jsonld=None, og_type="website", og_image=None, body_class=""):
    ld = "".join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + "</script>\n" for o in (jsonld or []))
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large"
    ogi = f'<meta property="og:image" content="{og_image}">\n<meta name="twitter:card" content="summary_large_image">\n' if og_image else ""
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="ar_SA">
<meta property="og:site_name" content="{NAME}">
{ogi}<meta name="theme-color" content="#10304d">
<link rel="icon" href="/assets/mark.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@500;600;700;800;900&family=Noto+Naskh+Arabic:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="alternate" type="application/atom+xml" title="{NAME}" href="/feeds/posts/default">
<link rel="stylesheet" href="/assets/site.css?v=2">
{ld}</head>
<body class="{body_class}">
<a class="skip" href="#main">تخطَّ إلى المحتوى</a>
<header class="masthead">
 <div class="mh-top wrap">
  <a class="logo" href="/" aria-label="{NAME} — الصفحة الرئيسية">
   <img src="https://googanconsult.com/storage/settings/site/Ulnh7JiOy6P65aUaaHTSjHZG2DXZMOXhuzG6UwvK.png" alt="شعار جوجان" width="52" height="52">
   <span><b>موسوعة جوجان</b><i>للأعمال والاستثمار والترجمة</i></span>
  </a>
  <form class="search" action="https://www.google.com/search" method="get" role="search">
   <input type="hidden" name="as_sitesearch" value="bloggoogan.com">
   <label class="sr" for="q">ابحث في الموسوعة</label>
   <input id="q" name="q" type="search" placeholder="ابحث في الموسوعة: دراسة جدوى مصنع، ترجمة تقرير طبي…">
   <button type="submit">بحث</button>
  </form>
 </div>
 <nav class="mh-nav" aria-label="التنقل الرئيسي"><div class="wrap">
  <a href="/topics/feasibility/">دراسات الجدوى</a>
  <a href="/topics/industry/">الصناعة</a>
  <a href="/topics/financial-analysis/">التحليل المالي</a>
  <a href="/topics/management/">الإدارة</a>
  <a href="/topics/certified-translation/" class="b">الترجمة المعتمدة</a>
  <a href="/topics/legal-translation/" class="b">الترجمة القانونية</a>
  <a href="/topics/languages/" class="b">أدلة اللغات</a>
  <a href="/topics/" class="all">كل المحاور</a>
 </div></nav>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
 <div class="najdi" aria-hidden="true"></div>
 <div class="wrap foot-grid">
  <div class="foot-about"><b>{NAME}</b><p>مرجع عربي تعليمي في دراسات الجدوى والاستثمار في السعودية والترجمة المعتمدة، تحرره شركة جوجان لخدمات الأعمال في الرياض.</p></div>
  <div><h2>اطلب خدمة</h2><a href="{B.CONSULT}">دراسات الجدوى والاستشارات</a><a href="{B.TRANSL}">الترجمة المعتمدة</a></div>
  <div><h2>الموسوعة</h2><a href="/topics/">فهرس المحاور</a><a href="/about/">منهجية التحرير</a><a href="/sitemap.xml">خريطة الموقع</a></div>
 </div>
 <p class="wrap copy">© {datetime.now().year} شركة جوجان لخدمات الأعمال — الرياض</p>
</footer>
</body>
</html>"""


def img_tag(p, cls, w, h, eager=False):
    src = p["image"] or p["cover"]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<img class="{cls}" src="{html.escape(src)}" alt="{html.escape(p["title"])}" width="{w}" height="{h}" {load}>'


def card(p, size="m"):
    t = B.TOPIC.get(p["topic"], B.ARCHIVE)
    pc = PILLAR[t[3]][1]
    d, iso = B.fmt_date(p["published"])
    ex = f'<p>{html.escape(p["desc"])}</p>' if size != "s" else ""
    return (f'<article class="card card-{size} {pc}"><a class="card-link" href="{p["path"]}">'
            f'<div class="card-img">{img_tag(p, "", 600, 315)}</div>'
            f'<div class="card-body"><span class="topic">{t[2]}</span><h3>{html.escape(p["title"])}</h3>{ex}'
            f'<span class="card-meta"><time datetime="{iso}">{d}</time><span>{p["mins"]} دقائق قراءة</span></span></div></a></article>')


def cta(key, compact=False):
    if not key:
        return ""
    url = B.SVC[key]
    if key.startswith("c_"):
        h, p, b, c = "تحتاج دراسة جدوى لمشروعك؟", "قسم الدراسات في جوجان يعدّ دراسات الجدوى وبحوث السوق للمشاريع في السعودية.", "تواصل مع قسم الدراسات", "pa"
    else:
        h, p, b, c = "تحتاج ترجمة معتمدة لمستنداتك؟", "قسم الترجمة في جوجان يترجم الوثائق والعقود والتقارير الطبية ترجمة معتمدة.", "تواصل مع قسم الترجمة", "pb"
    return f'<aside class="cta {c}{" compact" if compact else ""}"><h2>{h}</h2><p>{p}</p><a href="{url}">{b}</a></aside>'


# ---------------------------------------------------------------- build
def build(feed, dist):
    dist = Path(dist)
    if dist.exists():
        shutil.rmtree(dist)
    (dist / "assets").mkdir(parents=True)
    (dist / "covers").mkdir()
    shutil.copy(SRC / "site.css", dist / "assets" / "site.css")
    shutil.copy(SRC / "mark.svg", dist / "assets" / "mark.svg")
    shutil.copy(SRC / "_worker.js", dist / "_worker.js")
    (dist / "covers" / "_home.svg").write_text(cover_svg("المرجع العربي لدراسات الجدوى والاستثمار والترجمة المعتمدة", "A", "موسوعة جوجان"), encoding="utf-8")
    items = B.parse_feed(feed)
    posts = [x for x in items if x["type"] == "POST"]
    pages = [x for x in items if x["type"] == "PAGE"]
    stats = {"h2_added": 0, "covers_generated": 0, "real_images": 0}
    for p in posts + pages:
        body = B.clean_body(p["html"])
        p["topic"] = B.classify(p) if p["type"] == "POST" else "archive"
        about = p["topic"] == "about"
        if about:
            p["topic"] = "archive"
        t = B.TOPIC.get(p["topic"], B.ARCHIVE)
        body, _ = B.retarget_links(body, t[5])
        if p["title"] in ("بدون عنوان", ""):
            h = BeautifulSoup(body, "lxml").find(["h2", "h3", "strong", "b"])
            p["title"] = h.get_text(" ", strip=True)[:90] if h else "مقال من أرشيف جوجان"
        had_h2 = "<h2" in body
        body = improve(body, p["title"])
        if not had_h2 and "<h2" in body:
            stats["h2_added"] += 1
        p["image"] = first_image(body)
        key = re.sub(r"[^A-Za-z0-9_-]", "_", p["path"].strip("/")[:-5])
        (dist / "covers" / f"{key}.svg").write_text(cover_svg(p["title"], t[3], t[2]), encoding="utf-8")
        p["cover"] = f"/og/{key}.jpg"
        p["svg"] = f"/covers/{key}.svg"
        p["key"] = key
        stats["real_images" if p["image"] else "covers_generated"] += 1
        p["lead"], body = lead_and_rest(body)
        p["body"], p["toc"] = B.toc_and_ids(body)
        p["toc_items"] = re.findall(r'<li><a href="#(s\d+)">(.*?)</a></li>', p["toc"])
        p["desc"] = (p["lead"] or B.plain(p["body"]))[:155]
        p["mins"], p["words"] = reading_minutes(p["lead"] + p["body"])
        p["noindex"] = p["type"] == "POST" and p["topic"] == "archive" and not about
    posts.sort(key=lambda x: x["published"], reverse=True)
    indexed = [p for p in posts if not p["noindex"]]

    org = {"@type": "Organization", "@id": B.CONSULT + "#org", "name": B.ORG_NAME, "url": B.CONSULT, "sameAs": [B.TRANSL]}
    rewrites_keys = []
    for p in posts + pages:
        t = B.TOPIC.get(p["topic"], B.ARCHIVE)
        pl, pc = PILLAR[t[3]]
        d_pub, iso_pub = B.fmt_date(p["published"])
        d_upd, iso_upd = B.fmt_date(p["updated"])
        url = SITE + p["path"]
        hub = f"/topics/{t[0]}/"
        crumbs = [("الموسوعة", "/"), (t[2], hub)] if p["type"] == "POST" else [("الموسوعة", "/")]
        related = [q for q in indexed if q is not p and q["topic"] == p["topic"]][:3]
        toc_side = ""
        if len(p["toc_items"]) >= 2:
            toc_side = '<nav class="toc" aria-label="محتويات المقال"><h2>في هذا المقال</h2><ol>' + "".join(
                f'<li><a href="#{i}">{tx}</a></li>' for i, tx in p["toc_items"]) + "</ol></nav>"
        hero_img = (f'<figure class="art-cover">{img_tag(p, "", 1200, 630, eager=True)}</figure>')
        lead = f'<div class="lead-box"><h2>الخلاصة</h2><p>{html.escape(p["lead"])}</p></div>' if p["lead"] else ""
        rel = ("<section class=\"more wrap\"><h2>مداخل ذات صلة في " + t[2] + "</h2><div class=\"row3\">" + "".join(card(q) for q in related) + "</div></section>") if related else ""
        art = f"""<article class="art {pc}">
<header class="art-head"><div class="wrap">
<nav class="crumbs" aria-label="مسار التنقل">{''.join(f'<a href="{u}">{html.escape(n)}</a>' for n, u in crumbs)}</nav>
<h1>{html.escape(p["title"])}</h1>
<p class="art-meta"><span>{pl}</span><span>نُشر <time datetime="{iso_pub}">{d_pub}</time></span>{f'<span>حُدّث <time datetime="{iso_upd}">{d_upd}</time></span>' if iso_upd != iso_pub else ''}<span>{p["mins"]} دقائق قراءة</span></p>
</div><div class="najdi" aria-hidden="true"></div></header>
<div class="wrap art-grid">
<div class="art-main">
{hero_img}
{lead}
<div class="prose">{p["body"]}</div>
<p class="byline">تحرير: فريق جوجان للدراسات والترجمة · المحتوى تعليمي ولا يغني عن استشارة مهنية لحالتك.</p>
</div>
<aside class="art-side">{toc_side}{cta(t[5], compact=True)}</aside>
</div>
</article>
{rel}"""
        ld = [{"@context": "https://schema.org", "@graph": [org,
               {"@type": "BlogPosting" if p["type"] == "POST" else "WebPage", "headline": p["title"][:110],
                "image": [p["image"] or (SITE + p["cover"])], "datePublished": p["published"], "dateModified": p["updated"],
                "inLanguage": "ar", "mainEntityOfPage": url, "publisher": {"@id": B.CONSULT + "#org"}, "author": {"@id": B.CONSULT + "#org"}},
               {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)]}]}]
        out = dist / "_posts" / (p["key"] + ".html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(p["title"] + " | " + SHORT, p["desc"], url, art, noindex=p["noindex"], jsonld=ld, og_type="article",
                            og_image=p["image"] or (SITE + p["cover"]), body_class="is-article"), encoding="utf-8")

    # hubs
    hubs = []
    for t in B.TOPICS + [B.ARCHIVE]:
        lst = [p for p in posts if p["topic"] == t[0] and (t[0] == "archive" or not p["noindex"])]
        if not lst:
            continue
        hubs.append((t, lst))
        pl, pc = PILLAR[t[3]]
        intro = ("مقالات قديمة خارج تخصص الموسوعة، محفوظة للأرشيف." if t[0] == "archive" else f"كل ما نشرته الموسوعة في {t[2]}، من الأحدث إلى الأقدم.")
        lead_card = card(lst[0], "l")
        body = f"""<header class="hub-head {pc}"><div class="wrap">
<nav class="crumbs"><a href="/">الموسوعة</a><a href="/topics/">المحاور</a></nav>
<p class="pillar-name">{pl}</p><h1>{t[2]}</h1><p class="hub-intro">{intro}</p><p class="count">{len(lst)} مدخلاً</p>
</div><div class="najdi" aria-hidden="true"></div></header>
<section class="wrap hub-body"><div class="hub-lead">{lead_card}{cta(t[5])}</div>
<div class="row3">{''.join(card(p) for p in lst[1:])}</div></section>"""
        d = dist / "topics" / t[0]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(f"{t[2]} | {SHORT}", intro, f"{SITE}/topics/{t[0]}/", body, noindex=(t[0] == "archive")), encoding="utf-8")

    def pillar_index(pl):
        return "".join(f'<li><a href="/topics/{t[0]}/"><span>{t[2]}</span><em>{len(l)}</em></a></li>' for t, l in hubs if t[3] == pl)

    (dist / "topics").mkdir(exist_ok=True)
    idx = f"""<header class="hub-head pa"><div class="wrap"><h1>فهرس محاور الموسوعة</h1><p class="hub-intro">محوران رئيسيان: الجدوى والاستثمار، والترجمة والخدمات اللغوية.</p></div><div class="najdi" aria-hidden="true"></div></header>
<section class="wrap pillars"><div class="pillar pa"><h2>موسوعة الجدوى والاستثمار</h2><ul>{pillar_index("A")}</ul></div><div class="pillar pb"><h2>موسوعة الترجمة والخدمات اللغوية</h2><ul>{pillar_index("B")}</ul></div></section>"""
    (dist / "topics" / "index.html").write_text(page(f"فهرس المحاور | {SHORT}", "فهرس محاور موسوعة جوجان.", f"{SITE}/topics/", idx), encoding="utf-8")

    # home
    A = [p for p in indexed if B.TOPIC.get(p["topic"], B.ARCHIVE)[3] == "A"]
    Bp = [p for p in indexed if B.TOPIC.get(p["topic"], B.ARCHIVE)[3] == "B"]
    feat_path = "/2026/09/feasibility-study-off-plan-sales.html"
    featured = next((p for p in indexed if p["path"] == feat_path), indexed[0])
    side = [p for p in indexed if p is not featured][:4]
    home = f"""<section class="home-hero"><div class="wrap hero-grid">
<div class="hero-copy">
<h1>المرجع العربي لدراسات الجدوى والاستثمار والترجمة المعتمدة</h1>
<p>{len(indexed)} مدخلاً تشرح المنهجيات والأرقام والإجراءات، من صافي القيمة الحالية إلى ترجمة التقرير الطبي، بلغة واضحة ومصادر رسمية.</p>
<div class="hero-doors"><a class="door pa" href="/topics/feasibility/"><b>الجدوى والاستثمار</b><span>{len(A)} مدخلاً</span></a><a class="door pb" href="/topics/certified-translation/"><b>الترجمة والخدمات اللغوية</b><span>{len(Bp)} مدخلاً</span></a></div>
</div>
<div class="hero-feature">{card(featured, "l")}</div>
</div><div class="najdi" aria-hidden="true"></div></section>
<section class="wrap band"><h2 class="band-title">أحدث المداخل</h2><div class="row4">{''.join(card(p, "s") for p in side)}</div></section>
<section class="pillar-band pa"><div class="wrap"><div class="band-head"><h2>موسوعة الجدوى والاستثمار</h2><a href="/topics/">كل المحاور</a></div>
<div class="split">{card(A[0], "l") if A else ""}<div class="stack">{''.join(card(p, "s") for p in A[1:5])}</div></div>
<ul class="chips">{pillar_index("A")}</ul></div></section>
<section class="pillar-band pb"><div class="wrap"><div class="band-head"><h2>موسوعة الترجمة والخدمات اللغوية</h2><a href="/topics/">كل المحاور</a></div>
<div class="split">{card(Bp[0], "l") if Bp else ""}<div class="stack">{''.join(card(p, "s") for p in Bp[1:5])}</div></div>
<ul class="chips">{pillar_index("B")}</ul></div></section>
<section class="wrap two-cta">{cta("c_studies")}{cta("t_certified")}</section>"""
    site_ld = [{"@context": "https://schema.org", "@graph": [org, {"@type": "WebSite", "name": NAME, "url": SITE + "/", "inLanguage": "ar", "publisher": {"@id": B.CONSULT + "#org"}}]}]
    (dist / "index.html").write_text(page(NAME, "المرجع العربي لدراسات الجدوى والاستثمار في السعودية والترجمة المعتمدة، من جوجان.", SITE + "/", home, jsonld=site_ld, og_image=SITE + "/og/home.jpg", body_class="is-home"), encoding="utf-8")

    about = f"""<header class="hub-head pa"><div class="wrap"><h1>عن الموسوعة ومنهجية التحرير</h1></div><div class="najdi" aria-hidden="true"></div></header>
<section class="wrap narrow prose"><p>«{NAME}» مرجع تعليمي تحرره شركة جوجان لخدمات الأعمال في الرياض، ويخدم قسمين: الدراسات والاستشارات (<a href="{B.CONSULT}">googanconsult.com</a>) والترجمة المعتمدة (<a href="{B.TRANSL}">googantranslation.com</a>).</p>
<h2>منهجية التحرير</h2><ul><li>كل رقم أو اشتراط نظامي يُنسب إلى مصدره الرسمي، ويُذكر تاريخ آخر مراجعة.</li><li>المحتوى تعليمي ولا يغني عن استشارة مهنية لحالتك.</li><li>نصحح الأخطاء عند اكتشافها ونحدّث تاريخ المراجعة.</li></ul>
<h2>التصحيح والتواصل</h2><p>لملاحظة على أي مقال: info@googan.net</p></section>"""
    (dist / "about").mkdir(exist_ok=True)
    (dist / "about" / "index.html").write_text(page(f"عن الموسوعة | {SHORT}", "منهجية التحرير في موسوعة جوجان.", f"{SITE}/about/", about), encoding="utf-8")
    (dist / "404.html").write_text(page(f"الصفحة غير موجودة | {SHORT}", "الصفحة غير موجودة.", SITE + "/404", '<header class="hub-head pa"><div class="wrap"><h1>الصفحة غير موجودة</h1><p class="hub-intro">قد تكون الصفحة نُقلت. ابدأ من <a href="/topics/">فهرس المحاور</a>.</p></div></header>', noindex=True), encoding="utf-8")

    # sitemap, robots, feed, redirects, headers
    urls = [SITE + "/", SITE + "/topics/", SITE + "/about/"] + [f"{SITE}/topics/{t[0]}/" for t, l in hubs if t[0] != "archive"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'] + [f"<url><loc>{u}</loc></url>" for u in urls]
    sm += [f"<url><loc>{SITE}{p['path']}</loc><lastmod>{p['updated'][:10]}</lastmod></url>" for p in posts + pages if not p["noindex"]]
    (dist / "sitemap.xml").write_text("\n".join(sm + ["</urlset>"]), encoding="utf-8")
    (dist / "robots.txt").write_text(f"User-agent: *\nDisallow: /_posts/\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    fi = "".join(f'<entry><title>{html.escape(p["title"])}</title><link href="{SITE}{p["path"]}"/><id>{SITE}{p["path"]}</id><published>{p["published"]}</published><updated>{p["updated"]}</updated><summary>{html.escape(p["desc"])}</summary></entry>' for p in indexed[:30])
    (dist / "feeds" / "posts").mkdir(parents=True, exist_ok=True)
    (dist / "feeds" / "posts" / "default").write_text(f'<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>{NAME}</title><link href="{SITE}/"/><id>{SITE}/</id><updated>{posts[0]["updated"]}</updated>{fi}</feed>', encoding="utf-8")
    (dist / "_headers").write_text("/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n/covers/*\n  Cache-Control: public, max-age=604800\n", encoding="utf-8")
    json.dump([{"key": p["key"], "cover": p["svg"]} for p in posts + pages if not p["image"]], open(dist.parent / "og-todo.json", "w"))
    return {"pages": len(posts) + len(pages), "indexed": len(indexed), **stats}


if __name__ == "__main__":
    print(json.dumps(build(sys.argv[1], sys.argv[2]), ensure_ascii=False))
