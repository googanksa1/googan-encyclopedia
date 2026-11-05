"""Training courses section of the encyclopedia (/courses/): Googan's earlier management and skills courses,
read as flip-books (same reader as the library books) with an indexable course page: overview, audience,
outcomes, units and an «ما الذي تغيّر» box listing verified updates since the course was written.

Data: tools/content/courses/<slug>.json + tools/content/courses/<slug>-pages/NNN.webp (page N = PDF page N).
Add a course by producing those two with tools/course_tools/ (see README there) and listing its slug in ORDER.
"""
import json, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "content" / "courses"

CATS = {   # key: (name, intro, colour)
    "management": ("الإدارة والتخطيط", "دورات في دراسات الجدوى وإدارة المشاريع والجودة والأداء والوقت والاجتماعات وفرق العمل.", "#1f4e79"),
    "marketing": ("التسويق وخدمة العملاء", "دورات في خدمة العملاء والإعلان والتسويق الإلكتروني والمعارض التجارية.", "#8a2d3b"),
    "skills": ("المهارات الشخصية والاتصال", "دورات في الإقناع والتفكير والاتصال وإدارة ضغوط العمل.", "#a0591b"),
    "tourism": ("السياحة", "دورات في التسويق السياحي وتخطيط البرامج السياحية والإرشاد السياحي.", "#1f6f6b"),
    "media": ("الإعلام والصحافة", "دورات في التحرير الصحفي وإدارة اللقاءات الصحفية.", "#5b3a8c"),
    "education": ("التعليم والأسرة", "دورات في إدارة الصف والتحصيل الدراسي والتعامل مع المراهقين.", "#2c6e49"),
}


def load():
    out = []
    for f in sorted(DATA.glob("*.json")):
        c = json.load(open(f, encoding="utf-8"))
        if c.get("hidden"):
            continue
        out.append(c)
    order = list(CATS)
    out.sort(key=lambda c: (order.index(c["category"]), c.get("order", 99), c["title"]))
    return out


def card(c, esc, ver=""):
    return (f'<li><a class="cr-card" href="/courses/{c["slug"]}/"><img src="/courses/{c["slug"]}/pages/001.webp?v={ver}" alt="" loading="lazy" width="210" height="297">'
            f'<span class="cr-meta"><strong>{esc(c["title"])}</strong><small>{c["pages"]} صفحة · نحو {c["minutes"]} دقيقة قراءة</small></span></a></li>')


def build_courses(dist, *, page, banner, crumbs, esc, icon, consult, short, ver):
    courses = load()
    if not courses:
        return []
    root = Path(dist) / "courses"
    (Path(dist) / "assets").mkdir(exist_ok=True)
    shutil.copy(HERE / "page-flip.js", Path(dist) / "assets" / "page-flip.js")
    shutil.copy(HERE / "reader.js", Path(dist) / "assets" / "reader.js")
    site = page.__globals__["SITE"]
    urls = ["/courses/"]
    home = (short, "/")
    for c in courses:
        cname, cintro, col = CATS[c["category"]]
        base = f"/courses/{c['slug']}/"
        read = base + "read/"
        d = root / c["slug"]
        shutil.copytree(DATA / f"{c['slug']}-pages", d / "pages", dirs_exist_ok=True)
        from PIL import Image
        with Image.open(DATA / f"{c['slug']}-pages" / "002.webp") as im:
            ratio = round(im.height / im.width, 4)
        units = "".join(f'<li><a href="{read}#p={s["page"]}"><span class="bk-ch">{esc(s["title"])}</span><small>صفحة {s["page"]}</small></a></li>' for s in c["sections"])
        intro = "".join(f"<p>{esc(p)}</p>" for p in c["intro"])
        aud = "".join(f"<li>{esc(x)}</li>" for x in c.get("audience", []))
        outc = "".join(f"<li>{esc(x)}</li>" for x in c.get("outcomes", []))
        ups = c.get("updates", [])
        upd = ("" if not ups else
               '<section class="cr-upd"><h2>ما الذي تغيّر منذ إعداد الدورة؟</h2><p class="bk-hint">أُعدّت هذه الدورة قبل سنوات، وبقي أغلب محتواها صالحاً. راجعنا ما تغيّر منذ ذلك الوقت، وهذه أهم النقاط:</p><ul>'
               + "".join(f'<li>{esc(u["text"])}{f" <a href=\"{esc(u["source"])}\" rel=\"noopener\" target=\"_blank\">المصدر</a>" if u.get("source") else ""}</li>' for u in ups)
               + "</ul></section>")
        info = (f'<dl class="bk-info"><div><dt>الإعداد</dt><dd>شركة جوجان لخدمات الأعمال، ضمن دوراتها التدريبية في المجال الإداري</dd></div>'
                f'<div><dt>المجال</dt><dd><a href="/courses/#c-{c["category"]}">{cname}</a></dd></div>'
                f'<div><dt>عدد الصفحات</dt><dd>{c["pages"]} صفحة</dd></div><div><dt>مدة القراءة</dt><dd>نحو {c["minutes"]} دقيقة</dd></div>'
                f'<div><dt>الإتاحة</dt><dd>قراءة مجانية على الموقع بتقليب الصفحات</dd></div></dl>')
        body = banner(esc(c["title"]), esc(c["subtitle"]), crumbs([home, ("الدورات التدريبية", "/courses/"), (c["title"], None)])) + f"""
<div class="wrap bk-top"><a class="bk-cover" href="{read}#p=1"><img src="{base}pages/001.webp?v={ver}" alt="غلاف {esc(c['title'])}" width="420" height="594" fetchpriority="high"></a>
<div class="bk-top-copy">{info}<p class="bk-go"><a class="btn" href="{read}">{icon('book')}ابدأ قراءة الدورة</a></p>
<p class="bk-credit">{icon('book')}<span>دورة من إعداد شركة جوجان لخدمات الأعمال. للتدريب والاستشارات الإدارية: <a href="{consult}">googanconsult.com</a></span></p></div></div>
<div class="wrap narrow prose cr-body"><h2>عن الدورة</h2>{intro}
{f'<div class="cr-two"><div><h3>لمن هذه الدورة؟</h3><ul>{aud}</ul></div><div><h3>ماذا ستتعلم؟</h3><ul>{outc}</ul></div></div>' if aud or outc else ''}
{upd}</div>
<div class="wrap bk-contents"><h2>محاور الدورة</h2><p class="bk-hint">اختر محوراً لتُفتح الدورة على صفحته مباشرة.</p><ol class="bk-chs">{units}</ol></div>"""
        ld = [{"@context": "https://schema.org", "@type": "Course", "name": c["title"], "description": c["desc"], "inLanguage": "ar",
               "provider": {"@type": "Organization", "name": "شركة جوجان لخدمات الأعمال", "sameAs": consult},
               "isAccessibleForFree": True, "url": site + base, "image": site + base + "pages/001.webp"}]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(f"{c['title']} | {short}", c["desc"], base, body, ld=ld, og_image=site + base + "pages/001.webp"), encoding="utf-8")
        urls.append(base)
        opts = "".join(f'<option value="{s["page"]}">{esc(s["title"])}</option>' for s in c["sections"])
        rbody = f"""<div class="rd" data-reader data-pages="{c['pages']}" data-ratio="{ratio}" data-spread="0" style="--rd-ratio:{ratio}" data-dir="{base}pages/" data-slug="c-{c['slug']}">
<div class="rd-bar"><a class="rd-back" href="{base}">{esc(c['title'])}</a>
<label class="rd-toc"><span class="sr">انتقل إلى محور</span><select data-toc><option value="">المحاور</option>{opts}</select></label>
<span class="rd-count" data-count aria-live="polite"></span>
<span class="rd-tools"><button type="button" data-zoom title="تكبير الصفحة">تكبير</button><button type="button" data-sound aria-pressed="true">الصوت</button><button type="button" data-fs title="ملء الشاشة">ملء الشاشة</button></span></div>
<div class="rd-stage"><button class="rd-nav rd-prev" type="button" data-prev aria-label="الصفحة السابقة">›</button><div class="rd-wrap"><div class="rd-book"></div></div><button class="rd-nav rd-next" type="button" data-next aria-label="الصفحة التالية">‹</button></div>
<p class="rd-credit">دورة من إعداد شركة جوجان لخدمات الأعمال. <a href="{consult}">googanconsult.com</a></p>
<div class="rd-zoom" hidden tabindex="-1" role="dialog" aria-label="الصفحة مكبرة"><button type="button" data-close>إغلاق</button><div class="rd-zoom-in"></div></div>
</div>
<script src="/assets/page-flip.js?v={ver}" defer></script><script src="/assets/reader.js?v={ver}" defer></script>"""
        (d / "read").mkdir(parents=True, exist_ok=True)
        (d / "read" / "index.html").write_text(page(f"اقرأ: {c['title']} | {short}", c["desc"], read, rbody, noindex=True, cls="is-reader"), encoding="utf-8")
    # index
    chips = "".join(f'<a class="bk-chip" href="#c-{k}">{v[0]} <span>{sum(1 for c in courses if c["category"] == k)}</span></a>' for k, v in CATS.items() if any(c["category"] == k for c in courses))
    secs = "".join(
        f'<section class="bk-cat cr-cat" id="c-{k}" style="--cr:{v[2]}"><div class="sec-head"><h2>{v[0]} <span class="bk-count">{sum(1 for c in courses if c["category"] == k)} دورة</span></h2></div><p class="bk-hint">{v[1]}</p>'
        f'<ul class="cr-grid">{"".join(card(c, esc, ver) for c in courses if c["category"] == k)}</ul></section>'
        for k, v in CATS.items() if any(c["category"] == k for c in courses))
    total_pages = sum(c["pages"] for c in courses)
    body = banner("الدورات التدريبية", f"{len(courses)} دورة تدريبية قدّمتها شركة جوجان في مسيرتها في الاستشارات الإدارية، تُقرأ كاملة ومجاناً بتقليب الصفحات.",
                  crumbs([home, ("الدورات التدريبية", None)]),
                  extra=f'<p class="cr-facts"><b>{len(courses)}</b> دورة <b>{total_pages:,}</b> صفحة <b>{len([1 for k in CATS if any(c["category"] == k for c in courses)])}</b> مجالات</p>') + \
        f'<div class="wrap"><nav class="bk-chips" aria-label="مجالات الدورات">{chips}</nav>{secs}</div>'
    ld = [{"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": site + f"/courses/{c['slug']}/"} for i, c in enumerate(courses)]}]
    root.mkdir(parents=True, exist_ok=True)
    (root / "index.html").write_text(page(f"الدورات التدريبية المجانية | {short}", "دورات تدريبية مجانية من شركة جوجان في الإدارة والتسويق والمهارات والسياحة والإعلام والتعليم، تُقرأ بتقليب الصفحات.", "/courses/", body, ld=ld), encoding="utf-8")
    return urls
