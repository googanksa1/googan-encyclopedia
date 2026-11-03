#!/usr/bin/env python3
"""One-off editorial pass on content/legacy.json: claims, titles, merges. Idempotent."""
import json, re
from pathlib import Path
HERE = Path(__file__).parent
F = HERE / "content" / "legacy.json"
d = json.load(open(F))
REPL = [
    ("+90% دقة في التقدير", ""),
    ("+20 عاماً من الخبرة", "+30 عاماً من الخبرة"),
    ("#1 جائزة بصمة بلدي", "المركز الأول في جائزة بصمة بلدي"),
    ("AMER33478", "241026019612"),
    ("AMERICO (UAF/IAF)", "ARS Assessment (UAF)"),
    ("معتمدة لدى صندوق التنمية الصناعي، تفتح لك أبواب التمويل وتضمن انطلاقة مشروعك", "مُعدّة وفق متطلبات صندوق التنمية الصناعي، تساعدك في ملف التمويل وتدعم انطلاقة مشروعك"),
    ("من خلال زيارة موقع شركة جوجان على جوجان", "من خلال زيارة موقع جوجان للدراسات والاستشارات"),
    ("كما ترى جوجان مكتب دراسة جدوى معتمدة بالرياض", "وفق هذا التحليل"),
    ("وفق شركة جوجان مكتب دراسات جدوى", "وفق هذا التحليل"),
    ("وفق تحليل شركة جوجان دراسات جدوى اقتصادية معتمدة في الرياض", "وفق هذا التحليل"),
    ("وفق استطلاع شركة جوجان مكتب دراسات جدوى", "وفق هذا التحليل، مع"),
    ("شركة Googan", "جوجان"),
    ("بخبرتها الممتدة لأكثر من 30 عاماً في مجال دراسات الجدوى والاستشارات", "بخبرة تمتد لأكثر من 30 عاماً بين الأردن والسعودية"),
    ("بخبرتها الممتدة لأكثر من 30 عاماً في السوق السعودي", "بخبرة تمتد لأكثر من 30 عاماً بين الأردن والسعودية"),
    ("هي شريكك الأمثل لضمان بناء مشروعك على أسس قوية", "تساعدك على بناء مشروعك على أسس واضحة"),
    ("حيث تجمع بين الخبرة الطويلة التي تمتد لأكثر من ثلاثة عقود، والاعتمادات الرسمية من أهم الجهات الحكومية،", "حيث تجمع بين خبرة تمتد لأكثر من ثلاثة عقود"),
    ("تبرز شركة جوجان للترجمة المعتمدة كرائدة في مجال الترجمة الفرنسية في المملكة العربية السعودية", "تقدم شركة جوجان للترجمة المعتمدة خدمات الترجمة الفرنسية في المملكة العربية السعودية"),
    ("تُعتبر شركة جوجان من أعرق وأفضل مكاتب الترجمة في السعودية", "تقدم شركة جوجان خدمات الترجمة المعتمدة في السعودية"),
    ("شركة جوجان للترجمة المعتمدة - الرائدة في المملكة", "شركة جوجان للترجمة المعتمدة"),
    ("تُعتبر شركة جوجان للترجمة المعتمدة من أفضل مكاتب الترجمة في السعودية بخبرة 30 عام", "تقدم شركة جوجان للترجمة المعتمدة خدماتها بخبرة تتجاوز 30 عاماً"),
    ("في أفضل المكاتب مثل شركة جوجان", "لدى مكاتب مثل جوجان"),
    ("تقف شركة جوجان للترجمة المعتمدة اليوم كرائدة لا منازع لها في مجال الترجمة الفرنسية في المملكة العربية السعودية.", ""),
    ("فإن شركة جوجان هي خيارك الأمثل للحصول على أفضل مكتب ترجمة معتمدة فرنسي في المملكة.", "يمكنك طلب الخدمة من قسم الترجمة المعتمدة في جوجان."),
    ("ما يميز شركة جوجان عن غيرها من مكاتب الترجمة هو حصولها على اعتمادات رسمية من أهم الجهات الحكومية في المملكة.", "وتحمل جوجان شهادة ISO 17100:2015 الخاصة بمقدمي خدمات الترجمة، وشهادة ISO 9001:2015 لنظام إدارة الجودة."),
    ("تأسست شركة جوجان للترجمة المعتمدة في مدينة الرياض منذ أكثر من 30 عاماً، لتصبح بذلك من أعرق وأقدم الشركات المتخصصة في مجال الترجمة في المملكة العربية السعودية.", "تمتد خبرة جوجان في الترجمة والاستشارات لأكثر من 30 عاماً بين الأردن والسعودية."),
    ("خبرتنا التي تمتد لأكثر من 20 سنة، واعتمادنا الرسمي من جميع الجهات المختصة، وفريقنا المتخصص من أمهر المترجمين، كلها عوامل تجعل من مكتب جوجان الخيار الأمثل لجميع احتياجاتك في مجال الترجمة المعتمدة.", "تمتد خبرة جوجان لأكثر من 30 عاماً، وتحمل شهادة ISO 17100:2015 الخاصة بمقدمي خدمات الترجمة."),
    ("مكتب جوجان هو خيارك الذكي إن كنت تبحث عن ترجمة معتمدة مضمونة في الرياض لعام 2025.", ""),
    ("من اعتمادها لدى جهات التمويل، إلى حصولها على جائزة وزارة الإسكان، إلى إنجازاتها الصناعية والطبية والتعليمية في دول عدة، تبقى جوجان علامة ثقة وجودة عالية.", ""),
    ('مثل "جوجان" يضمن الحصول', 'مثل "جوجان" يساعد على الحصول'),
    ("شركة جوجان، على سبيل المثال، توفر 88 لغة", "شركة جوجان، على سبيل المثال، تقدم الترجمة بأكثر من 88 لغة"),
]
REMOVE_BLOCK = [re.compile(p) for p in [r"1,?855 عميل", r"قيّموا خدمات جوجان"]]
hits = {}
for p in d["keep"]:
    for k in ("lead", "body", "desc"):
        s = p[k]
        for a, b in REPL:
            if a in s:
                hits[a] = hits.get(a, 0) + s.count(a)
                s = s.replace(a, b)
        for rx in REMOVE_BLOCK:
            s2 = re.sub(r"<(p|li|div|h[2-4])[^>]*>(?:(?!</\1>).)*?" + rx.pattern + r".*?</\1>", "", s, flags=re.S)
            if s2 != s:
                hits[rx.pattern] = hits.get(rx.pattern, 0) + 1
            s = s2
        p[k] = s
# editorial overrides: titles, SEO titles, descriptions
ov = json.load(open(HERE / "content" / "seo_overrides.json"))
for p in d["keep"]:
    o = ov.get(p["path"], {})
    if "t" in o: p["title"] = o["t"]
    if "s" in o: p["seo_title"] = o["s"]
    if "d" in o: p["desc"] = o["d"]
# merges of thin / cannibalising pages
MERGE = {
    "/2025/06/blog-post_61.html": "/2025/06/blog-post_19.html",
    "/2026/08/invest-in-saudi-arabia.html": "/topics/saudi-investment/",
    "/2026/08/economic-feasibility-study.html": "/2025/05/blog-post_98.html",
    "/p/blog-page_25.html": "/2026/08/feasibility-study-office-riyadh.html",
    "/2025/06/blog-post_30.html": "/2026/08/feasibility-study-office-riyadh.html",
    "/2025/01/blog-post_22.html": "/2026/08/feasibility-study-office-riyadh.html",
    "/2011/05/blog-post.html": "/2026/08/certified-translation-riyadh.html",
}
for src, dst in MERGE.items():
    if any(p["path"] == src for p in d["keep"]):
        d["keep"] = [p for p in d["keep"] if p["path"] != src]
        d["redirects"][src] = dst
        d["extra"][src] = "merged"
        for p in d["keep"]:
            p["body"] = p["body"].replace(f'href="{src}"', f'href="{dst}"')

# ---- pass 2: tag-tolerant phrase fixes and block removals
from bs4 import BeautifulSoup
def tol(phrase):
    words = phrase.split()
    return re.compile(r"(?:\s|<[^>]+>)+".join(re.escape(w) for w in words))
REPL2 = [
    ("كما ترى جوجان مكتب دراسة جدوى معتمدة بالرياض", "وفق هذا التحليل"),
    ("وفق شركة جوجان مكتب دراسات جدوى", "وفق هذا التحليل"),
    ("وفق تحليل شركة جوجان دراسات جدوى اقتصادية معتمدة في الرياض جداً", "جداً وفق هذا التحليل"),
    ("وفق استطلاع شركة جوجان مكتب دراسات جدوى نمو هائلة", "نمو كبيرة وفق هذا التحليل"),
    ("تُعتبر شركة جوجان من أعرق وأفضل مكاتب الترجمة في السعودية", "تقدم شركة جوجان خدمات الترجمة المعتمدة في السعودية"),
    ("تُعتبر شركة جوجان للترجمة المعتمدة من أفضل مكاتب الترجمة في السعودية بخبرة 30 عام", "تقدم شركة جوجان للترجمة المعتمدة خدماتها بخبرة تتجاوز 30 عاماً"),
    ("ما يجعل مكتب جوجان للترجمة المعتمدة الخيار الأمثل في الرياض لعام 2025،", "ما يميز خدمات مكتب جوجان للترجمة المعتمدة في الرياض،"),
    ("مما يجعلنا الخيار الأمثل للشركات الدولية والمستثمرين الأجانب في الرياض", "وهو ما يخدم الشركات الدولية والمستثمرين الأجانب في الرياض"),
    ("التي تجعلنا الخيار الأمثل لخدمات الترجمة الطبية المعتمدة", "التي تميز خدماتنا في الترجمة الطبية المعتمدة"),
    ("مما يجعله الخيار الأمثل لكل من يسعى", "لخدمة كل من يسعى"),
    ("يمثل مكتبنا في الرياض الخيار الأمثل لكل من يسعى", "يخدم مكتبنا في الرياض كل من يسعى"),
    ("فإن شركة جوجان هي خيارك الأمثل للحصول على أفضل مكتب ترجمة معتمدة فرنسي في المملكة.", "يمكنك طلب الخدمة من قسم الترجمة المعتمدة في جوجان."),
    ("نحو النجاح المضمون", "نحو النجاح"),
    ("لكن العوائد مضمونة مع وجود عملاء كبار مثل أرامكو وسابك مستعدين للاستثمار بقوة", "والعوائد مرتبطة بقدرة المشروع على التعاقد مع عملاء صناعيين كبار"),
    ("، مما جعلنا نتعامل مع أكثر من 15,000 عميل راضٍ عن خدماتنا", ""),
    ("تشمل تجربتنا العمل على مشاريع ترجمة لجهات من بينها:", ""),
    ("⭐ التقييم", ""),
]
DROP_BLOCK = [r"1,855 مراجعة", r"تقييم من العملاء", r"التقييم\s*4\.9", r"ضمان استرداد كامل", r"تحول أعمال الترجمة الفرنسية المعقدة إلينا",
              r"ذكر هذه الجهات لا يعني بالضرورة"]
DROP_SECTION = [r"الشركات الفرنسية الكبرى التي تثق", r"^ثقة المتخصصين$"]
for p in d["keep"]:
    for k in ("lead", "body"):
        h = p[k]
        for a, b in REPL2:
            h2 = tol(a).sub(b, h)
            if h2 != h:
                hits[a] = hits.get(a, 0) + 1
            h = h2
        s = BeautifulSoup(h, "lxml"); root = s.body or s
        for t in root.find_all(True):
            for at in [x for x in t.attrs if x.startswith("data-")]:
                del t.attrs[at]
        for rx in DROP_BLOCK:
            for node in list(root.find_all(string=re.compile(rx))):
                blk = node.find_parent(["p", "li", "div", "h2", "h3", "h4", "span", "td"])
                while blk is not None and blk.name in ("span",) and blk.parent is not None:
                    blk = blk.parent
                if blk is not None:
                    blk.decompose(); hits[rx] = hits.get(rx, 0) + 1
        for h3 in root.find_all(["h2", "h3"]):
            if getattr(h3, "decomposed", False): continue
            if any(re.search(rx, h3.get_text(" ", strip=True)) for rx in DROP_SECTION):
                lvl = int(h3.name[1]); sib = h3.find_next_sibling()
                while sib is not None and not (sib.name in ("h2", "h3") and int(sib.name[1]) <= lvl):
                    nx = sib.find_next_sibling(); sib.decompose(); sib = nx
                h3.decompose(); hits["section"] = hits.get("section", 0) + 1
        for div in root.find_all("div"):
            if getattr(div, "decomposed", False): continue
            kids = div.find_all("div", recursive=False)
            if kids and "Boeing International" in div.get_text() and len(div.get_text()) < 600:
                div.decompose(); hits["client-list"] = hits.get("client-list", 0) + 1
        p[k] = "".join(str(c) for c in root.contents)
json.dump(d, open(F, "w"), ensure_ascii=False)
print("hits:", json.dumps(hits, ensure_ascii=False, indent=0))
print("kept:", len(d["keep"]), "redirects:", len(d["redirects"]))
missing = [p["path"] for p in d["keep"] if p["path"] not in ov]
print("no override:", missing)

# ---- pass 3: heading structure fixes, then re-index H2s for the table of contents
import sys
sys.path.insert(0, str(HERE))
import build as Bld
for p in d["keep"]:
    s = BeautifulSoup(p["body"], "lxml"); root = s.body or s
    changed = False
    if not root.find("h2"):
        for h in root.find_all("h3"):
            h.name = "h2"; changed = True
    if p["path"] == "/2026/01/blog-post.html":
        for b in root.find_all("b"):
            t = re.sub(r"\s+", " ", b.get_text(" ", strip=True))
            if re.match(r"^و?السؤال ", t) and b.parent is not None and b.parent.name in ("p", "div", "span"):
                h = s.new_tag("h2"); h.string = re.sub(r"^و", "", t)
                blk = b.find_parent(["p", "div"]) or b.parent
                b.decompose(); blk.insert_before(h); changed = True
    if changed:
        body, _ = Bld.toc_and_ids("".join(str(c) for c in root.contents))
        sp = BeautifulSoup(body, "lxml")
        p["toc_items"] = [(h["id"], h.get_text(" ", strip=True)) for h in sp.find_all("h2") if h.get("id")]
        p["body"] = body
        print("headings fixed:", p["path"], len(p["toc_items"]))
json.dump(d, open(F, "w"), ensure_ascii=False)
