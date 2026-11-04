#!/usr/bin/env python3
"""GOOGAN Encyclopedia v4 — rebuilt from scratch on the original URLs.
Layout follows the owner's reference (ranked guide list + banner + must-reads + FAQ),
brand colour #1c1b42. Usage: python3 build4.py <feed.atom> <dist>"""
import collections, html, json, os, re, shutil, sys, warnings
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning, NavigableString
from urllib.parse import unquote

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
import build as B
import gsite as G

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
HERE = Path(__file__).parent
SITE = B.SITE
NAME = "موسوعة جوجان للأعمال والاستثمار والترجمة"
SHORT = "موسوعة جوجان"
CONSULT, TRANSL = B.CONSULT, B.TRANSL
LOGO = "https://googanconsult.com/storage/settings/site/Ulnh7JiOy6P65aUaaHTSjHZG2DXZMOXhuzG6UwvK.png"
MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
NOW = datetime.now()
REVIEWED = f"{MONTHS[NOW.month - 1]} {NOW.year}"
V = __import__("hashlib").md5((HERE / "site.css").read_bytes() + (HERE / "site.js").read_bytes()).hexdigest()[:8]

# verified on the live commercial sites (Nov 2026)
SVC = dict(B.SVC)
SVC["c_ops"] = CONSULT + "service-details/" + B.quote("استشارات-تحسين-الأداء-والتشغيل")
SVC["c_quote"] = CONSULT + "quote"
SVC["t_quote"] = TRANSL + "quote"
# WhatsApp numbers as published on each commercial site (verified Nov 2026)
WA = {"A": "966507975011", "B": "966543784171"}
TEL = {"A": "+966507975011", "B": "+966543784171"}


def wa_link(pillar, title=None):
    from urllib.parse import quote as q
    dept = "قسم الدراسات والاستشارات" if pillar == "A" else "قسم الترجمة المعتمدة"
    msg = f"السلام عليكم، أتواصل مع {dept} في جوجان" + (f" بخصوص ما قرأته في موسوعة جوجان: {title}" if title else " عن طريق موسوعة جوجان")
    return f"https://wa.me/{WA[pillar]}?text={q(msg)}"

# topic: (slug, title, pillar, service, service label, short blurb)
TOPICS = {
    "feasibility": ("دراسات الجدوى", "A", "c_studies", "دراسات الجدوى لمشاريع الاستثمار", "منهجيات إعداد دراسة الجدوى وقراءتها وتقييم الفرص."),
    "industry": ("الصناعة والتصنيع", "A", "c_sidf", "دراسة جدوى لصندوق التنمية الصناعي", "دراسات المصانع وخطوط الإنتاج والتكاليف الصناعية."),
    "market-research": ("بحوث السوق", "A", "c_studies", "دراسات الجدوى لمشاريع الاستثمار", "حجم السوق والمنافسة والعينات والتحليل الإحصائي."),
    "financial-analysis": ("التحليل المالي", "A", "c_studies", "دراسات الجدوى لمشاريع الاستثمار", "التكلفة والعائد والموازنات التقديرية وقيمة العملة."),
    "saudi-investment": ("بيئة الاستثمار السعودية", "A", "c_office", "مكتب دراسات جدوى معتمد", "القطاعات الواعدة والفرص الاستثمارية في المملكة."),
    "management": ("الإدارة وإعادة الهيكلة", "A", "c_restructure", "إعادة هيكلة الأعمال وتحسين الأداء", "القيادة والإشراف وإدارة التغيير وتشخيص الأداء."),
    "sectors": ("موسوعة القطاعات", "A", "c_studies", "دراسات الجدوى لمشاريع الاستثمار", "دراسات قطاعية: تدوير، طاقة، تقنية، زراعة، سياحة."),
    "certified-translation": ("الترجمة المعتمدة", "B", "t_certified", "الترجمة المعتمدة", "ما الترجمة المعتمدة ومتى تحتاجها وكيف تختار مكتباً."),
    "legal-translation": ("الترجمة القانونية", "B", "t_legal", "الترجمة القانونية", "العقود والوكالات والعلامات التجارية ووثائق المحاكم."),
    "medical-translation": ("الترجمة الطبية", "B", "t_medical", "الترجمة الطبية", "التقارير الطبية والوثائق الصحية ودقة المصطلح."),
    "travel-documents": ("وثائق السفر والسفارات", "B", "t_visa", "ترجمة التأشيرات", "ترجمة وثائق التأشيرات والسفارات والدراسة بالخارج."),
    "languages": ("أدلة اللغات", "B", "t_certified", "الترجمة المعتمدة", "الترجمة من لغات محددة وإلى العربية."),
    "translated-studies": ("مكتبة الدراسات المترجمة", "B", "t_academic", "الترجمة الأكاديمية", "دراسات علمية منشورة ترجمها قسم الترجمة في جوجان، مع مصدرها الأصلي."),
}
PILLARS = {"A": ("الجدوى والاستثمار", "pa", "c_studies"), "B": ("الترجمة المعتمدة", "pb", "t_certified")}
OVERRIDE = {
    "/2025/05/blog-post_71.html": "medical-translation", "/2025/06/blog-post_16.html": "legal-translation",
    "/2025/09/blog-post.html": "legal-translation", "/2025/05/blog-post_14.html": "languages",
    "/2025/06/httpscertified-translation-office.coarticlefrench-language-translation-office.html": "languages",
    "/2025/05/blog-post_119.html": "legal-translation", "/2025/05/blog-post_63.html": "travel-documents",
    "/p/blog-page_25.html": "feasibility", "/2025/05/blog-post_20.html": "feasibility",
}

BILINGUAL_OK = {"/2026/09/feasibility-study-off-plan-sales.html"}

# ---------------------------------------------------------------- icons (inline SVG only)
def icon(name, cls="ic"):
    P = {
        "check": '<path d="M4 10.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
        "clock": '<circle cx="10" cy="10" r="7.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M10 6v4.4l3 1.8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
        "cal": '<rect x="3" y="4.5" width="14" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3 8.5h14M7 2.8v3.4M13 2.8v3.4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
        "search": '<circle cx="8.5" cy="8.5" r="5.8" fill="none" stroke="currentColor" stroke-width="2"/><path d="M13 13l4.5 4.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        "menu": '<path d="M3 5.5h14M3 10h14M3 14.5h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        "close": '<path d="M5 5l10 10M15 5L5 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        "chev": '<path d="M12.5 4.5L7 10l5.5 5.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        "down": '<path d="M5 7.5l5 5 5-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        "chart": '<path d="M3 17h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><rect x="4.5" y="10" width="2.6" height="5" rx=".6" fill="currentColor"/><rect x="8.7" y="6.5" width="2.6" height="8.5" rx=".6" fill="currentColor"/><rect x="12.9" y="3.5" width="2.6" height="11.5" rx=".6" fill="currentColor"/>',
        "doc": '<path d="M5.5 2.8h6l3.5 3.5v10.9H5.5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M11.3 2.8v3.7H15M8 10.5h4.5M8 13.5h4.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
        "globe": '<circle cx="10" cy="10" r="7.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M2.5 10h15M10 2.5c2.3 2.2 3.3 4.7 3.3 7.5s-1 5.3-3.3 7.5c-2.3-2.2-3.3-4.7-3.3-7.5s1-5.3 3.3-7.5z" fill="none" stroke="currentColor" stroke-width="1.5"/>',
        "book": '<path d="M3 4.5c2.5-1 5-1 7 .7v11.3c-2-1.7-4.5-1.7-7-.7zM17 4.5c-2.5-1-5-1-7 .7v11.3c2-1.7 4.5-1.7 7-.7z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
        "mail": '<rect x="2.8" y="4.5" width="14.4" height="11" rx="1.8" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3.5 5.5l6.5 5 6.5-5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
        "chat": '<path d="M10 2.6a7.4 7.4 0 0 0-6.4 11.1L2.7 17.4l3.8-1a7.4 7.4 0 1 0 3.5-13.8z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M7.3 7.4c.2-.5.5-.5.8-.5h.5c.2 0 .4.1.5.4l.6 1.4c.1.2 0 .4-.1.6l-.4.5c-.1.1-.1.3 0 .5.5.9 1.2 1.6 2.1 2.1.2.1.4.1.5 0l.5-.5c.2-.2.4-.2.6-.1l1.4.6c.3.1.4.3.4.5v.5c0 .3-.1.6-.5.8-.6.3-1.4.4-2.4 0-1.8-.7-3.3-2.2-4-4-.4-1-.3-1.8 0-2.4z" fill="currentColor"/>',
        "star": '<path d="M10 2.5l2.2 4.6 5 .7-3.6 3.5.9 5-4.5-2.4-4.5 2.4.9-5L2.8 7.8l5-.7z" fill="currentColor"/>',
    }
    return f'<svg class="{cls}" viewBox="0 0 20 20" aria-hidden="true" focusable="false">{P[name]}</svg>'


def esc(x):
    return html.escape(x or "", quote=True)


HUB_INTRO = {
    "translated-studies": "دراسات علمية منشورة في مجلات محكّمة، ترجمها قسم الترجمة الأكاديمية في جوجان إلى العربية ليستفيد منها الباحثون والطلاب. ننشر الترجمة الكاملة فقط حين تسمح رخصة الدراسة الأصلية بذلك، وننشر لغيرها قراءة عربية في أهم ما جاء فيها. في آخر كل صفحة العنوان الأصلي والمؤلفون والمجلة والسنة ورابط الدراسة.",
    "feasibility": "دراسة الجدوى هي الأداة التي تحدد إن كان المشروع يستحق رأس المال قبل إنفاقه. تجمع هذه الأدلة منهجيات الإعداد خطوة بخطوة، والفرق بين الدراسة التسويقية والفنية والمالية، وكيف تُقرأ مؤشرات مثل صافي القيمة الحالية ومعدل العائد الداخلي وفترة الاسترداد، إضافة إلى دراسات مبدئية لمشاريع في قطاعات مختلفة في السعودية. ابدأ بالأدلة الأشمل في أعلى القائمة إن كنت تتعرف على الموضوع لأول مرة.",
    "industry": "المشاريع الصناعية في السعودية تحتاج دراسة جدوى أدق من غيرها: خطوط إنتاج ومواد خام وتراخيص صناعية ومتطلبات تمويل من جهات مثل صندوق التنمية الصناعية السعودي. تجمع هذه الأدلة قراءات أولية لفرص صناعية محددة، وتشرح ما الذي تسأله قبل تثبيت السعة الإنتاجية والاستثمار في المعدات.",
    "market-research": "بحوث السوق هي الأساس الذي تُبنى عليه بقية دراسة الجدوى: من يشتري، وبكم، ومن ينافسك. تشرح هذه الأدلة طرق تقدير حجم السوق، وتحليل المنافسين، واختيار العينات، والتحليل الإحصائي، وكيف تتحول النتائج إلى افتراضات مالية قابلة للدفاع عنها.",
    "financial-analysis": "التحليل المالي يحوّل خطة المشروع إلى أرقام يمكن الحكم عليها. تجمع هذه المداخل مفاهيم تحليل التكلفة والعائد والموازنات التقديرية وغيرها من أدوات التخطيط والرقابة المالية التي يحتاجها صاحب المشروع والمستثمر عند تقييم أي فرصة.",
    "saudi-investment": "تتغير فرص الاستثمار في السعودية بسرعة مع برامج رؤية 2030 والقطاعات الجديدة. تجمع هذه الأدلة قراءات للقطاعات الواعدة والفرص في الرياض وبقية المناطق، مع التنبيه دائماً إلى أن الأرقام الرسمية هي المرجع، وأن كل فرصة تحتاج اختباراً خاصاً بها قبل الاستثمار.",
    "management": "كثير من المشاريع لا تتعثر بسبب الفكرة بل بسبب الإدارة. تجمع هذه المداخل مفاهيم الإشراف الإداري والقيادة والثقافة التنظيمية وإدارة التغيير والتخطيط الاستراتيجي، إلى جانب أدلة حديثة في تشخيص الخلل الإداري وإعادة الهيكلة واستخدام الذكاء الاصطناعي في القرار.",
    "sectors": "دراسات مبدئية لمشاريع في قطاعات محددة: إعادة التدوير، والطاقة المتجددة، والتقنية، والزراعة، والسياحة البيئية، والخدمات الرقمية. كل دراسة هنا قراءة أولية تساعدك على فهم الفرصة وأسئلتها الرئيسية، ولا تغني عن دراسة جدوى مخصصة بأرقام محدثة لمشروعك.",
    "certified-translation": "الترجمة المعتمدة مطلوبة عندما تقدم وثيقة أجنبية إلى جهة رسمية: سفارة، أو جامعة، أو محكمة، أو وزارة. تشرح هذه الأدلة معنى الترجمة المعتمدة ومتى تحتاجها، وكيف تختار مكتب ترجمة في الرياض، وما الذي يؤثر في السعر ومدة التسليم، وكيف تطلب الخدمة أونلاين.",
    "legal-translation": "الترجمة القانونية لا تحتمل الخطأ: كلمة واحدة قد تغير معنى بند في عقد أو وكالة. تشرح هذه الأدلة متطلبات ترجمة الوثائق المقدمة إلى وزارة العدل والمحاكم، وترجمة مستندات العلامات التجارية، وأهم ما تراجعه قبل تقديم الترجمة.",
    "medical-translation": "الترجمة الطبية تحتاج دقة في المصطلح والجرعات والتشخيص، لأن أي خطأ قد يؤثر في العلاج أو في قبول الملف لدى المستشفى أو شركة التأمين أو السفارة. يشرح هذا القسم الوثائق الطبية الشائعة ومتطلبات ترجمتها ترجمة معتمدة.",
    "travel-documents": "لكل سفارة متطلباتها في لغة الوثائق وصيغة الترجمة. يجمع هذا القسم متطلبات ترجمة وثائق التأشيرات والسفارات في الرياض حسب ما تنشره المصادر الرسمية، مع تذكير دائم بمراجعة صفحة السفارة قبل التقديم لأن المتطلبات تتغير.",
    "languages": "أدلة للترجمة المعتمدة بين العربية ولغات محددة، مثل الفرنسية والإندونيسية والأمهرية: الوثائق الشائعة لكل لغة، وما يحتاج انتباهاً خاصاً في الأسماء والتواريخ والمصطلحات.",
}

# ---------------------------------------------------------------- photos
PHOTOS = json.load(open(HERE / "photos.json"))
RELATED = {"feasibility": ["market-research", "financial-analysis", "home"], "industry": ["sectors", "feasibility"],
           "market-research": ["feasibility"], "financial-analysis": ["financing", "feasibility"],
           "saudi-investment": ["home", "feasibility"], "management": ["feasibility"], "sectors": ["industry"],
           "certified-translation": ["translation-standards", "business-translation"], "legal-translation": ["business-translation"],
           "medical-translation": ["certified-translation"], "travel-documents": ["certified-translation"],
           "languages": ["translation-standards", "academic-translation"],
           "translated-studies": ["academic-translation", "translation-standards"]}
USED = set()


def take_photo(topic):
    for k in [topic] + RELATED.get(topic, []) + list(PHOTOS):
        for pid in PHOTOS.get(k, []):
            if pid not in USED:
                USED.add(pid)
                return pid
    return PHOTOS[topic][0]


def purl(pid, w, h):
    return f"https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&w={w}&h={h}&q=70"


def pimg(pid, alt, w, h, eager=False, sizes=None):
    srcset = f'{purl(pid, w // 2, h // 2)} {w // 2}w, {purl(pid, w, h)} {w}w'
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    sz = f' sizes="{sizes}"' if sizes else ""
    return f'<img src="{purl(pid, w, h)}" srcset="{srcset}"{sz} alt="{esc(alt)}" width="{w}" height="{h}" {load}>'


# ---------------------------------------------------------------- content cleaning
PHONE = re.compile(r"(\+?966|05\d{8}|0\s?5\d[\s\d]{7,}|٠٥)")
TEXT_SUBS = [
    (re.compile(r"مجموعة\s+جوجان"), "جوجان"),
    (re.compile(r"جوجان\s+(جروب|قروب)"), "جوجان"),
    (re.compile(r"Googan\s*Group", re.I), "جوجان"),
    (re.compile(r"(https?://)?(www\.)?googangroup(\.blogspot)?\.com/?\S*", re.I), ""),
    (re.compile(r"(https?://)?(www\.)?certified-translation-office\.co\S*", re.I), ""),
    (re.compile(r"(https?://)?(www\.)?googan\.co\b(?!m)/?", re.I), "جوجان"),
    (re.compile(r"info@googan\.net\.com"), "info@googan.net"),
    (re.compile(r"أكثر من 15 عاماً"), "أكثر من 30 عاماً"),
    (re.compile(r"منذ 2009،\s*"), ""),
    (re.compile(r"خبرة تمتد منذ 2009"), "خبرة في الأردن والسعودية"),
    (re.compile(r"^\s*[ØüÜ§·•]\s+"), ""),
]
PROMO = re.compile(r"(جميع الحقوق محفوظة|زيارة موقعنا|زوروا موقعنا|واتساب|اتصل بنا|تواصل معنا|للتواصل\s*:|احجز استشارتك|اطلب عرض سعر|تعرف على خدماتنا)")
DROP_SECTION = re.compile(r"(^دراسات حالة|دعوة للعمل|\(CTA\)|الجانب العاطفي والتسويقي|دراسة حالة واقعية|مثال واقعي|معلومات الاتصال|عن المؤلف|^\d+\.\s*دراسة حالة$|قصة نجاح|قصة واقعية|قصص نجاح|تجربة حقيقية|تجارب حقيقية|شهادات العملاء|آراء العملاء|ماذا يقول عملاؤنا|قالوا عنا|الكلمات (الدلالية|المفتاحية)|^الفهرس$|^جدول المحتويات$|^محتويات المقال$|^الوسوم$|^الفهرس\s*:)")
STORY = re.compile(r"(Manus|manus\.ai|عن المؤلف\s*:|تعاونت\s+.{0,40}مع جوجان|^الكلمات (الدلالية|المفتاحية)\s*:|(يقول|تقول|يروي|تروي|يحكي|تحكي)\s+\S+(\s+\S+)?\s*\(\d+\s*عام)")
CODE_JUNK = {"html", "```", "```html", "</html>", "<html>", "css", "html>", "]]>", "-->"}
OLD = ("googan.co", "googangroup.com", "certified-translation-office.co", "googangroup.blogspot.com")


def scrub(body, topic_svc):
    s = BeautifulSoup(body, "lxml")
    root = s.body or s
    for t in root.find_all(["fb:like", "fb:comments", "form", "input", "button", "select", "textarea", "svg"]):
        t.decompose()
    for f in root.find_all("iframe"):
        src = f.get("src", "")
        if "youtube.com/embed" in src:
            f["src"] = src.replace("http://", "https://")
            f["loading"] = "lazy"
            f["title"] = "فيديو"
            for a in ("width", "height", "frameborder"):
                f.attrs.pop(a, None)
            f.wrap(s.new_tag("div", attrs={"class": "video"}))
        else:
            f.decompose()
    for a in root.find_all("a"):
        h = a.get("href", "")
        hu = re.sub(r"[\u200b-\u200f\u202a-\u202e\u2066-\u2069]", "", unquote(h)) if "%" in h or re.search(r"[\u200b-\u202e]", h) else h
        host = re.sub(r"^https?://", "", hu).split("/")[0].lower().replace("www.", "")
        if host in OLD or host.endswith("googan.co"):
            a["href"] = SVC[topic_svc]
        if host in ("googanmarketing.com", "blogger.com", "keydevelopmenttraining.com", "draft.blogger.com") or "googleusercontent.com" in host or "bp.blogspot.com" in host:
            a.unwrap()
            continue
        if "googanconsult.com/service-details/" in hu and "تقييم-المشروع" in hu:
            a["href"] = SVC["c_studies"]
        if h.startswith("mailto:info@googan.net.com"):
            a["href"] = "mailto:info@googan.net"
        if a.get("href", "").startswith("tel:") or "wa.me" in a.get("href", "") or "whatsapp" in a.get("href", ""):
            a.unwrap()
    for node in list(root.find_all(string=True)):
        if not isinstance(node, NavigableString) or getattr(node, "parent", None) is None or node.parent.name in ("script", "style"):
            continue
        txt = str(node)
        new = txt
        for rx, rep in TEXT_SUBS:
            new = rx.sub(rep, new)
        if new != txt:
            node.replace_with(new)
    # fabricated-looking stories / keyword dumps: drop whole sections by heading
    heads = root.find_all(["h2", "h3", "h4"])
    for h in heads:
        if getattr(h, "decomposed", False) or h.parent is None:
            continue
        t = h.get_text(" ", strip=True)
        if DROP_SECTION.search(t):
            lvl = int(h.name[1])
            sib = h.find_next_sibling()
            while sib is not None and not (sib.name in ("h2", "h3", "h4") and int(sib.name[1]) <= lvl):
                nxt = sib.find_next_sibling()
                sib.decompose()
                sib = nxt
            h.decompose()
    for el in root.find_all(["p", "blockquote", "li", "h2", "h3", "div"]):
        if getattr(el, "decomposed", False):
            continue
        t = el.get_text(" ", strip=True)
        if STORY.search(t) and (el.name != "div" or len(t) < 600):
            el.decompose()
    # phone numbers: drop the smallest block holding them
    for node in list(root.find_all(string=PHONE)):
        if getattr(node, "parent", None) is None:
            continue
        blk = node.find_parent(["p", "li", "div", "h2", "h3", "h4", "td", "span"])
        if blk is not None and len(blk.get_text(" ", strip=True)) < 400:
            blk.decompose()
        else:
            node.replace_with(PHONE.sub("", str(node)))
    # promotional / contact blocks
    for el in root.find_all(["p", "div", "li", "h2", "h3", "h4", "span", "b", "strong"]):
        if getattr(el, "decomposed", False):
            continue
        t = el.get_text(" ", strip=True)
        if not t:
            continue
        if len(t) < 260 and (PHONE.search(t) or PROMO.search(t)):
            el.decompose()
    for node in list(root.find_all(string=True)):
        if getattr(node, "parent", None) is None:
            continue
        if str(node).strip().lower() in CODE_JUNK or re.fullmatch(r"[`\s]*(html|css)?[`\s]*(html)?\s*", str(node).strip().lower() or "x"):
            node.extract()
    for h in root.find_all(["h2", "h3"]):
        t = h.get_text(" ", strip=True)
        if len(t) < 3 or (len(t) < 25 and re.search(r"[:：]\s*-?$", t)):
            h.name = "p"
            h.string = t.rstrip(":：- ")
    for a in root.find_all("a"):
        if not a.get_text(strip=True) and not a.find("img"):
            a.decompose()
    for el in root.find_all(["p", "div", "li", "span", "strong", "b"]):
        if not el.get_text(strip=True) and not el.find(["img", "iframe", "table"]):
            el.decompose()
    for img in root.find_all("img"):
        src = img.get("src", "")
        bad = (not src or src.startswith("file:") or "source.unsplash.com" in src or "certified-translation-office.co" in src
               or "googan.co/" in src or "googangroup" in src or "manuscdn.com" in src
               or (src.startswith("data:") and not valid_data_uri(src)))
        if bad:
            par = img.find_parent("figure")
            (par if par is not None and len(par.find_all("img")) == 1 else img).decompose()
            continue
        if src.startswith("http://"):
            img["src"] = src = "https://" + src[7:]
        if "googleusercontent.com" in src or "bp.blogspot.com" in src:
            img["src"] = re.sub(r"/(s\d+(-[a-z0-9-]+)?|w\d+-h\d+(-[a-z0-9-]+)?)/", "/w1000/", src)
        img["loading"] = "lazy"
        img["decoding"] = "async"
        img.attrs.pop("srcset", None)
        for a in ("width", "height", "border"):
            img.attrs.pop(a, None)
    for h in root.find_all(["h4", "h5", "h6"]):
        h.name = "h3"
    for h in root.find_all(["h2", "h3"]):
        if len(h.get_text(" ", strip=True)) > 200 or h.find(["p", "div", "ul", "ol", "table", "h2", "h3"]):
            h.name = "div"
    return "".join(str(c) for c in root.contents)


def valid_data_uri(src):
    import base64
    try:
        head, data = src.split(",", 1)
        raw = base64.b64decode(data, validate=True) if ";base64" in head else data.encode()
        return len(raw) > 100 and (raw.lstrip()[:5] in (b"<svg ", b"<?xml") or raw[:4] in (b"\x89PNG", b"GIF8") or raw[:2] == b"\xff\xd8")
    except Exception:
        return False


def clean_title(t, body):
    t = html.unescape(t or "").strip().strip('"“”«»')
    if not t or t == "بدون عنوان":
        h = BeautifulSoup(body, "lxml").find(["h2", "h3", "strong", "b"])
        t = h.get_text(" ", strip=True) if h else "مقال من موسوعة جوجان"
    t = re.sub(r"\s*\|.*$", "", t)
    t = re.sub(r"\s*[-–]\s*(شركة\s+)?جوجان.*$", "", t)
    t = PHONE.sub("", t)
    for rx, rep in TEXT_SUBS:
        t = rx.sub(rep, t)
    t = re.sub(r"^(الدراسات والاستشارات والتدريب|دراسات وبحوث)\s*:\s*", "", t)
    t = re.sub(r"^(اكتشف|تعرف على)\s+", "", t)
    if len(t) > 95 and "." in t[:95]:
        t = t[: t.index(".")]
    t = re.sub(r"\s+", " ", t).strip(" -–:،.")
    if len(t) > 95:
        t = t[:92].rsplit(" ", 1)[0] + "…"
    return t[0:1].upper() + t[1:] if t else "مقال من موسوعة جوجان"


def seo_title(t, override=None):
    t = override or t
    base = t if len(t) <= 60 else t[:58].rsplit(" ", 1)[0] + "…"
    return f"{base} | {SHORT}"


def desc_of(lead, body):
    t = lead or BeautifulSoup(body, "lxml").get_text(" ", strip=True)
    t = re.sub(r"\s+", " ", t)
    return t if len(t) <= 158 else t[:155].rsplit(" ", 1)[0] + "…"


def insert_mid_cta(body, cta_html):
    s = BeautifulSoup(body, "lxml")
    root = s.body or s
    hs = root.find_all("h2")
    if len(hs) >= 3:
        hs[2].insert_before(BeautifulSoup(cta_html, "lxml").find("aside"))
        return "".join(str(c) for c in root.contents)
    return body


# ---------------------------------------------------------------- layout
def page(title, desc, path, body, *, ld=None, og_image=None, og_type="website", cls="", noindex=False, keywords=None, wa=None):
    url = SITE + path
    lds = "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>\n' for o in (ld or []))
    ogi = f'<meta property="og:image" content="{esc(og_image)}">\n<meta name="twitter:card" content="summary_large_image">\n' if og_image else ""
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{f'<meta name="keywords" content="{esc(keywords)}">' if keywords else ''}
<link rel="canonical" href="{url}">
<meta name="robots" content="{'noindex,follow' if noindex else 'index,follow,max-image-preview:large,max-snippet:-1'}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="ar_SA">
<meta property="og:site_name" content="{NAME}">
{ogi}<meta name="theme-color" content="#1c1b42">
<link rel="icon" href="/assets/mark.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com">
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;800&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={V}">
<link rel="alternate" type="application/atom+xml" title="{NAME}" href="/feeds/posts/default">
{lds}</head>
<body class="{cls}">
<a class="skip" href="#main">تخطَّ إلى المحتوى</a>
<div class="strip"><div class="wrap strip-row"><span>مرجع عربي مجاني في الجدوى والاستثمار والترجمة المعتمدة</span><nav aria-label="أقسام جوجان"><a href="{CONSULT}">قسم الدراسات والاستشارات</a><a href="{TRANSL}">قسم الترجمة المعتمدة</a></nav></div></div>
<header class="top">
 <div class="wrap top-row">
  <a class="logo" href="/" aria-label="{SHORT} — الصفحة الرئيسية"><img src="{LOGO}" alt="" width="44" height="44" onerror="this.onerror=null;this.src='/assets/mark.svg'"><span><b>{SHORT}</b><i>للأعمال والاستثمار والترجمة</i></span></a>
  <nav class="nav" aria-label="التنقل الرئيسي">
   <a href="/topics/feasibility/">دراسات الجدوى</a>
   <a href="/topics/saudi-investment/">الاستثمار في السعودية</a>
   <a href="/topics/management/">الإدارة</a>
   <a href="/topics/certified-translation/">الترجمة المعتمدة</a>
   <a href="/topics/">كل المحاور</a>
   <a href="/about/">عن الموسوعة</a>
  </nav>
  <details class="menu"><summary aria-label="القائمة">{icon('menu','ic open')}{icon('close','ic shut')}</summary>
  <nav class="mnav" aria-label="قائمة الجوال">
   <a href="/topics/feasibility/">دراسات الجدوى</a>
   <a href="/topics/saudi-investment/">الاستثمار في السعودية</a>
   <a href="/topics/management/">الإدارة</a>
   <a href="/topics/certified-translation/">الترجمة المعتمدة</a>
   <a href="/topics/">كل المحاور</a>
   <a href="/about/">عن الموسوعة</a>
  </nav></details>
  <form class="search" action="https://www.google.com/search" method="get" role="search" data-search>
   <input type="hidden" name="as_sitesearch" value="bloggoogan.com">
   <label class="sr" for="q-top">ابحث في الموسوعة</label>
   <input id="q-top" type="search" name="q" placeholder="ابحث عن دليل…" autocomplete="off" data-q>
   <button type="submit" aria-label="بحث">{icon('search')}</button>
   <div class="results" role="listbox" hidden></div>
  </form>
 </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
 <div class="wrap foot-grid">
  <div class="foot-about"><b>{NAME}</b><p>مرجع تعليمي عربي تحرره شركة جوجان لخدمات الأعمال في الرياض، في محورين: دراسات الجدوى والاستثمار، والترجمة المعتمدة.</p></div>
  <div><h2>اطلب خدمة</h2><a href="{SVC['c_studies']}">دراسات الجدوى</a><a href="{SVC['c_sidf']}">دراسة جدوى للصندوق الصناعي</a><a href="{SVC['t_certified']}">الترجمة المعتمدة</a><a href="{SVC['t_legal']}">الترجمة القانونية</a></div>
  <div><h2>الموسوعة</h2><a href="/topics/">فهرس المحاور</a><a href="/about/">عن الموسوعة ومنهجية التحرير</a></div>
  <div><h2>تواصل</h2><a href="mailto:info@googan.net">{icon('mail')} info@googan.net</a><a href="{CONSULT}">googanconsult.com</a><a href="{TRANSL}">googantranslation.com</a></div>
 </div>
 <div class="wrap copy"><span>© {NOW.year} شركة جوجان لخدمات الأعمال، الرياض</span><span>الصور التوضيحية من Unsplash</span></div>
</footer>
{f'<a class="wa-float" href="{wa[0]}" target="_blank" rel="noopener" aria-label="{wa[1]}">{icon("chat")}<span>{wa[1]}</span></a>' if wa else ''}
<script src="/assets/site.js?v={V}" defer></script>
</body></html>"""


def count_label(n):
    if n == 1: return "دليل واحد"
    if n == 2: return "دليلان"
    if n <= 10: return f"{n} أدلة"
    return f"{n} دليلاً"


def checks(p, n=4):
    pts = [re.sub(r"<[^>]+>", "", html.unescape(t)) for _, t in p["toc_items"]][:n]
    pts = [x if len(x) < 70 else x[:67].rsplit(" ", 1)[0] + "…" for x in pts]
    if not pts and p["lead"]:
        pts = [p["lead"][:120].rsplit(" ", 1)[0] + "…"]
    return "".join(f"<li>{icon('check')}<span>{esc(x)}</span></li>" for x in pts)


def card(p, rank=None, ribbon=None):
    t = TOPICS[p["topic"]]
    pc = PILLARS[t[1]][1]
    rk = f'<span class="rank" aria-label="الترتيب {rank}">{rank}</span>' if rank else ""
    rb = f'<span class="ribbon">{icon("star")}{ribbon}</span>' if ribbon else ""
    return f"""<article class="card {pc}{' first' if ribbon else ''}">{rk}{rb}
<a class="card-img" href="{p['path']}" tabindex="-1" aria-hidden="true">{pimg(p['photo'], '', 440, 300, sizes='(max-width:700px) 100vw, 220px')}</a>
<div class="card-main"><a class="topic" href="/topics/{p['topic']}/">{t[0]}</a><h3><a href="{p['path']}">{esc(p['title'])}</a></h3><ul class="ticks">{checks(p)}</ul></div>
<div class="card-side"><div class="dial"><b>{p['mins']}</b><span>دقيقة قراءة</span></div><a class="btn" href="{p['path']}">اقرأ الدليل</a><a class="svc" href="{SVC[t[2]]}">اطلب الخدمة</a></div>
</article>"""


def mini(p):
    return f"""<li><a href="{p['path']}"><span class="mini-img">{pimg(p['photo'], '', 240, 160)}</span><span class="mini-t">{esc(p['title'])}</span></a></li>"""


def tile(p):
    t = TOPICS[p["topic"]]
    return f"""<article class="tile"><a href="{p['path']}"><span class="tile-img">{pimg(p['photo'], '', 600, 380, sizes='(max-width:700px) 100vw, 33vw')}</span><span class="topic">{t[0]}</span><h3>{esc(p['title'])}</h3><span class="tile-meta">{icon('clock')}{p['mins']} دقيقة قراءة</span></a></article>"""


def cta(svc, variant="box", title=None):
    url = SVC[svc]
    if svc.startswith("c_"):
        h, tx, b = "تحتاج دراسة جدوى لمشروعك؟", "قسم الدراسات في جوجان يعدّ دراسات الجدوى وبحوث السوق والملفات التمويلية للمشاريع في السعودية.", "تواصل مع قسم الدراسات"
        cls = "pa"
    else:
        h, tx, b = "تحتاج ترجمة معتمدة لمستنداتك؟", "قسم الترجمة في جوجان يترجم العقود والوثائق الرسمية والتقارير الطبية ترجمة معتمدة.", "تواصل مع قسم الترجمة"
        cls = "pb"
    pill = "A" if svc.startswith("c_") else "B"
    return (f'<aside class="cta {cls} {variant}"><p class="cta-title">{h}</p><p>{tx}</p><div class="cta-btns">'
            f'<a class="btn" href="{url}">{b}</a><a class="btn wa" href="{wa_link(pill, title)}" target="_blank" rel="noopener">{icon("chat")}واتساب</a></div></aside>')


def online_box(city, title=None):
    """Remote-service box for city guides: Googan is an online option, not a local branch."""
    return (f'<aside class="online-box" aria-label="خدمة الترجمة أونلاين من جوجان">'
            f'<p class="ob-kicker">لسكان {city}: خدمة عن بُعد من الرياض</p>'
            f'<p class="ob-title">ترجمة معتمدة أونلاين، واستلم ترجمتك بصيغة PDF</p>'
            f'<ul><li>{icon("chat")}ترسل صورة واضحة أو ملف PDF للمستند عبر واتساب</li>'
            f'<li>{icon("doc")}نراجع المستند ونرسل لك السعر والمدة قبل البدء</li>'
            f'<li>{icon("check")}تستلم الترجمة المعتمدة ملف PDF، ونتفق معك على النسخة الورقية إن احتجتها</li></ul>'
            f'<div class="cta-btns"><a class="btn wa" href="{wa_link("B", title)}" target="_blank" rel="noopener">{icon("chat")}تواصل معنا الآن عبر واتساب</a>'
            f'<a class="btn ghost" href="{SVC["t_certified"]}">صفحة الترجمة المعتمدة</a></div>'
            f'<p class="ob-note">جوجان لا تملك فرعاً في {city}؛ الخدمة تُقدَّم عن بُعد من مكتبنا في الرياض.</p></aside>')


def banner(h1, sub, crumbs="", extra="", pc="pa"):
    return f"""<section class="banner {pc}"><div class="wrap">{crumbs}<h1>{h1}</h1>{f'<p class="sub">{sub}</p>' if sub else ''}{extra}<p class="reviewed">{icon('check','ic tick')}آخر مراجعة للمحتوى: {REVIEWED}</p></div></section>"""


def crumbs(lst):
    return '<nav class="crumbs" aria-label="مسار التنقل"><ol>' + "".join(
        f'<li><a href="{u}">{esc(n)}</a></li>' if u else f'<li aria-current="page">{esc(n)}</li>' for n, u in lst) + "</ol></nav>"


FAQ_HOME = [
    ("ما موسوعة جوجان؟", "مرجع تعليمي عربي مجاني تحرره شركة جوجان لخدمات الأعمال في الرياض. يجمع أدلة عملية في محورين: دراسات الجدوى والاستثمار في السعودية، والترجمة المعتمدة والخدمات اللغوية."),
    ("هل المحتوى بديل عن الاستشارة المهنية؟", "لا. المحتوى تعليمي يشرح المفاهيم والخطوات العامة. القرار الاستثماري أو المتطلبات النظامية لحالتك تحتاج مراجعة مختص وجهة الاختصاص الرسمية."),
    ("كيف أطلب دراسة جدوى أو ترجمة معتمدة؟", f'الموسوعة للتعليم فقط. لطلب دراسة جدوى تواصل مع <a href="{CONSULT}">قسم الدراسات والاستشارات</a>، ولطلب ترجمة معتمدة تواصل مع <a href="{TRANSL}">قسم الترجمة المعتمدة</a>.'),
    ("كيف ترتَّب الأدلة في القوائم؟", "ترتَّب الأدلة حسب شمولها، أي حجم المحتوى وعدد أقسامه، ويظهر لكل دليل وقت القراءة التقريبي وعدد أقسامه. لا نستخدم تقييمات أو مراجعات مستخدمين."),
    ("وجدت خطأ في مقال، كيف أبلغ عنه؟", 'راسلنا على <a href="mailto:info@googan.net">info@googan.net</a> مع رابط المقال، ونصحح الخطأ ونحدّث تاريخ المراجعة.'),
]


def faq(items):
    return '<div class="faq">' + "".join(f'<details><summary><span>{q}</span>{icon("down")}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in items) + "</div>"


# ---------------------------------------------------------------- build
def prepare_legacy(feed):
    decisions = json.load(open(HERE / "decisions.json"))
    items = B.parse_feed(feed)
    keep = [p for p in items if decisions[p["path"]]["action"] == "keep"]
    redirects = {k: v["target"] for k, v in decisions.items() if v["action"] == "redirect"}
    # pass 1: content
    for p in keep:
        topic = OVERRIDE.get(p["path"]) or decisions[p["path"]]["topic"]
        if topic not in TOPICS:
            topic = "feasibility"
        p["topic"] = topic
        svc = TOPICS[topic][2]
        raw = re.sub(r"</(span|a|b|strong|em|i)>(?=<(span|a|b|strong|em|i)\b)", r"</\1> ", p["html"])
        raw = re.sub(r"(?<![<\w\"'=])/(h[1-6]|p|div|li|strong|b|span)(&gt;|>)", r"</\1>", raw)
        body = B.clean_body(raw)
        body, _ = B.retarget_links(body, svc)
        body = scrub(body, svc)
        p["title"] = clean_title(p["title"], body)
        body = G.improve(body, p["title"])
        body = scrub(body, svc)
        p["lead"], body = G.lead_and_rest(body)
        p["body0"] = body
        p["mins"], p["words"] = G.reading_minutes(p["lead"] + body)
    # language: pages that are mostly non-Arabic are retired to their hub
    extra = {}
    for p in list(keep):
        tx = BeautifulSoup(p["lead"] + p["body0"], "lxml").get_text(" ")
        ar, la = len(re.findall(r"[\u0600-\u06FF]", tx)), len(re.findall(r"[A-Za-z]", tx))
        if la > ar and p["path"] not in BILINGUAL_OK:
            keep.remove(p); redirects[p["path"]] = f"/topics/{p['topic']}/"; extra[p["path"]] = "non-Arabic page"
    # duplicate blocks across posts: keep each block only in the most comprehensive post
    seen, owner, seen_cases = {}, {}, {}
    for p in sorted(keep, key=lambda x: -x["words"]):
        sp = BeautifulSoup(p["body0"], "lxml")
        dup_from = collections.Counter()
        for h in sp.find_all(["h2", "h3"]):
            ht = re.sub(r"\W+", "", h.get_text(" ", strip=True))
            if not h.get_text(strip=True).startswith("دراسة حالة"):
                continue
            core = ht[:30]
            if core in seen_cases and seen_cases[core] != p["path"]:
                dup_from[seen_cases[core]] += 1
                lvl = int(h.name[1]); sib = h.find_next_sibling()
                while sib is not None and not (sib.name in ("h2", "h3") and int(sib.name[1]) <= lvl):
                    nx = sib.find_next_sibling(); sib.decompose(); sib = nx
                h.decompose()
            else:
                seen_cases[core] = p["path"]
        for el in sp.find_all(["p", "li", "table", "blockquote"]):
            if getattr(el, "decomposed", False):
                continue
            key = re.sub(r"\W+", "", el.get_text(" ", strip=True))
            if len(key) < 80:
                continue
            if key in seen and seen[key] != p["path"]:
                dup_from[seen[key]] += 1
                el.decompose()
            else:
                seen[key] = p["path"]
        for h in sp.find_all(["h2", "h3"]):
            nxt = h.find_next_sibling()
            if (nxt is None or nxt.name in ("h2", "h3")) and len(h.get_text(strip=True)) < 200 and not h.find(["p", "div", "ul", "table"]):
                h.decompose()
        p["body0"] = "".join(str(c) for c in (sp.body or sp).contents)
        p["mins"], p["words"] = G.reading_minutes(p["lead"] + p["body0"])
        if p["words"] < 250 and not dup_from:
            keep.remove(p); redirects[p["path"]] = f"/topics/{p['topic']}/"; extra[p["path"]] = f"thin ({p['words']} words)"
        elif dup_from and p["words"] < 350:
            target = dup_from.most_common(1)[0][0]
            keep.remove(p); redirects[p["path"]] = target; extra[p["path"]] = "duplicate"
    redirects = {k: (redirects.get(v, v)) for k, v in redirects.items()}
    keep.sort(key=lambda x: x["published"], reverse=True)
    known = {p["path"] for p in keep}
    # photos: most comprehensive first get first pick
    for p in sorted(keep, key=lambda x: -x["words"]):
        p["photo"] = take_photo(p["topic"])

    # pass 2: links
    stats = {"internal_redirected": 0, "dead_unwrapped": 0}
    for p in keep:
        s = BeautifulSoup(p["body0"], "lxml")
        for a in s.find_all("a", href=True):
            h = a["href"]
            h2 = re.sub(r"^https?://(www\.)?bloggoogan\.com", "", h)
            if h2 != h:
                a["href"] = h = h2 or "/"
            if not h.startswith("/"):
                if h.startswith("http"):
                    a["rel"] = "noopener"
                elif not h.startswith(("#", "mailto:")):
                    a.unwrap()
                    stats["dead_unwrapped"] += 1
                continue
            path = h.split("#")[0].split("?")[0]
            if path in known or path in ("/", "/topics/", "/about/") or path.startswith("/topics/"):
                continue
            if path in redirects:
                a["href"] = redirects[path]
                stats["internal_redirected"] += 1
            else:
                a.unwrap()
                stats["dead_unwrapped"] += 1
        body = "".join(str(c) for c in (s.body or s).contents)
        body, _ = B.toc_and_ids(body)
        s = BeautifulSoup(body, "lxml")
        ids = {t["id"] for t in s.find_all(id=True)} | {t["name"] for t in s.find_all("a", attrs={"name": True})}
        for a in s.find_all("a", href=True):
            if a["href"].startswith("#") and a["href"][1:] not in ids:
                if a.get_text(strip=True):
                    a.unwrap()
                else:
                    a.decompose()
                stats["dead_unwrapped"] += 1
        body = "".join(str(c) for c in (s.body or s).contents)
        s = BeautifulSoup(body, "lxml")
        p["toc_items"] = [(h["id"], h.get_text(" ", strip=True)) for h in s.find_all("h2") if h.get("id")]
        p["body"] = insert_mid_cta(body, cta(TOPICS[p["topic"]][2], "inline"))
        p["desc"] = desc_of(p["lead"], body)
    print("links:", stats)
    return keep, redirects, extra


SNAP_KEYS = ("path", "type", "title", "topic", "published", "updated", "lead", "body", "toc_items", "desc", "mins", "words", "photo")
CONTENT = HERE / "content"
RIYADH = __import__("datetime").timezone(__import__("datetime").timedelta(hours=3))
LIBRARY_TOPICS = {"translated-studies"}
LIBRARY_CUTOFF = datetime(2026, 11, 4, 0, 0, tzinfo=RIYADH)


def load_new_posts(redirects):
    """New articles: content/posts/*.md with a front-matter block between --- lines.
    Fields: title, slug, topic, date (YYYY-MM-DD HH:MM, Riyadh time), description (optional), photo (optional).
    A post is published only when its date has passed."""
    import markdown
    out = []
    now = datetime.now(RIYADH)
    for f in sorted((CONTENT / "posts").glob("*.md")) if (CONTENT / "posts").exists() else []:
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
        if not m:
            print("skip (no front matter):", f.name); continue
        meta = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1); meta[k.strip()] = v.strip().strip('"')
        when = datetime.strptime(meta["date"], "%Y-%m-%d %H:%M").replace(tzinfo=RIYADH)
        if when > now and not os.environ.get("PREVIEW_ALL"):
            continue
        # Owner decision 4 Nov 2026: books and translated studies move to library.bloggoogan.com.
        # Studies not already live on the encyclopedia are held here and will publish on the library.
        if meta.get("topic") in LIBRARY_TOPICS and when > LIBRARY_CUTOFF:
            continue
        topic = meta.get("topic", "feasibility")
        if topic not in TOPICS:
            topic = "feasibility"
        slug = re.sub(r"[^a-z0-9-]", "", meta["slug"].lower())
        path = f"/{when:%Y}/{when:%m}/{slug}.html"
        html_body = markdown.markdown(m.group(2), extensions=["tables", "sane_lists"])
        html_body = scrub(html_body, TOPICS[topic][2])
        if meta.get("city"):
            html_body = re.sub(r"<p>\s*\[\[online-box\]\]\s*</p>", lambda _m: online_box(meta["city"], meta["title"]), html_body)
        lead, html_body = G.lead_and_rest(html_body)
        html_body, _ = B.toc_and_ids(html_body)
        sp = BeautifulSoup(html_body, "lxml")
        toc_items = [(h["id"], h.get_text(" ", strip=True)) for h in sp.find_all("h2") if h.get("id")]
        iso = when.isoformat()
        p = {"path": path, "type": "POST", "title": meta["title"], "topic": topic, "published": iso,
             "updated": meta.get("updated", iso), "lead": lead, "toc_items": toc_items,
             "body": html_body if meta.get("city") else insert_mid_cta(html_body, cta(TOPICS[topic][2], "inline")),
             "desc": meta.get("description") or desc_of(lead, html_body)}
        p["mins"], p["words"] = G.reading_minutes(lead + html_body)
        p["photo"] = meta.get("photo") or take_photo(topic)
        if meta.get("seo"):
            p["seo_title"] = meta["seo"]
        redirects.pop(path, None)
        out.append(p)
    return out


def build(feed, dist):
    dist = Path(dist)
    if dist.exists():
        shutil.rmtree(dist)
    (dist / "assets").mkdir(parents=True)
    for f in ("site.css", "site.js", "mark.svg"):
        shutil.copy(HERE / f, dist / "assets" / f)
    snap_file = CONTENT / "legacy.json"
    if feed == "--snapshot":
        snap = json.load(open(snap_file))
        keep, redirects, extra = snap["keep"], snap["redirects"], snap["extra"]
        for p in keep:
            p["toc_items"] = [tuple(x) for x in p["toc_items"]]
            USED.add(p["photo"])
    else:
        keep, redirects, extra = prepare_legacy(feed)
        CONTENT.mkdir(exist_ok=True)
        json.dump({"keep": [{k: p[k] for k in SNAP_KEYS} for p in keep], "redirects": redirects, "extra": extra},
                  open(snap_file, "w"), ensure_ascii=False)
    for _ in range(5):
        redirects = {k: redirects.get(v, v) for k, v in redirects.items()}
    new_posts = load_new_posts(redirects)
    keep = sorted(keep + new_posts, key=lambda x: x["published"], reverse=True)
    print("new posts published:", len(new_posts))


    org = {"@type": "Organization", "@id": SITE + "/#org", "name": "شركة جوجان لخدمات الأعمال", "alternateName": "Googan Business Services Company",
           "url": CONSULT, "logo": LOGO, "email": "info@googan.net", "sameAs": [CONSULT, TRANSL],
           "address": {"@type": "PostalAddress", "addressLocality": "الرياض", "addressCountry": "SA"},
           "contactPoint": [{"@type": "ContactPoint", "contactType": "customer service", "telephone": TEL["A"], "areaServed": "SA", "availableLanguage": ["ar", "en"], "name": "قسم الدراسات والاستشارات"},
                            {"@type": "ContactPoint", "contactType": "customer service", "telephone": TEL["B"], "areaServed": "SA", "availableLanguage": ["ar", "en"], "name": "قسم الترجمة المعتمدة"}]}
    by_topic = {k: sorted([p for p in keep if p["topic"] == k], key=lambda x: -x["words"]) for k in TOPICS}
    live_topics = [k for k in TOPICS if by_topic[k]]
    topic_photo = {k: by_topic[k][0]["photo"] for k in live_topics}

    # ---------------- articles
    for p in keep:
        t = TOPICS[p["topic"]]
        pl, pc, _ = PILLARS[t[1]]
        d_pub, iso_pub = B.fmt_date(p["published"])
        d_upd, iso_upd = B.fmt_date(p["updated"])
        cr = [("الموسوعة", "/"), (t[0], f"/topics/{p['topic']}/"), (p["title"], None)]
        same = [q for q in by_topic[p["topic"]] if q is not p]
        reads = (same + [q for q in keep if q is not p and TOPICS[q["topic"]][1] == t[1] and q not in same])[:5]
        related = (same[5:8] if len(same) > 7 else [q for q in keep if q is not p and q not in reads and TOPICS[q["topic"]][1] == t[1]][:3])
        upd = f'<span>{icon("cal")}حُدّث <time datetime="{iso_upd}">{d_upd}</time></span>' if iso_upd != iso_pub else ""
        toc = ""
        if len(p["toc_items"]) >= 2:
            lis = "".join(f'<li><a href="#{i}">{esc(x)}</a></li>' for i, x in p["toc_items"])
            toc = f'<details class="toc" open><summary>في هذا الدليل {icon("down")}</summary><ol>{lis}</ol></details>'
        lead = f'<div class="keybox"><h2>الخلاصة</h2><p>{esc(p["lead"])}</p></div>' if p["lead"] else ""
        svc_line = (f'<p class="svc-line">{icon("doc")}<span>تحتاج تطبيق ما في هذا الدليل على حالتك؟ اطلع على خدمة <a href="{SVC[t[2]]}">{t[3]}</a> '
                    f'لدى {"قسم الدراسات والاستشارات" if t[1] == "A" else "قسم الترجمة المعتمدة"} في جوجان، أو <a href="{wa_link(t[1], p["title"])}" target="_blank" rel="noopener">راسلنا عبر واتساب</a>.</span></p>')
        art_body = re.sub(r'<aside class="cta [^"]*inline">.*?</aside>', lambda m: cta(t[2], "inline", p["title"]), p["body"], count=1, flags=re.S)
        body = f"""<div class="art-head {pc}"><div class="wrap art-head-grid">
<div class="art-head-copy">{crumbs(cr)}<a class="pill" href="/topics/{p['topic']}/">{t[0]}</a><h1>{esc(p['title'])}</h1>
<p class="meta"><span>{icon('cal')}نُشر <time datetime="{iso_pub}">{d_pub}</time></span>{upd}<span>{icon('clock')}{p['mins']} دقيقة قراءة</span></p>
<p class="byline"><span>تحرير: فريق موسوعة جوجان</span><span>آخر مراجعة: {REVIEWED}</span></p></div>
<figure class="art-hero">{pimg(p['photo'], p['title'], 960, 600, eager=True, sizes='(max-width:900px) 100vw, 46vw')}</figure>
</div></div>
<div class="wrap art-grid">
<article class="art-main">
{lead}{svc_line}{toc}
<div class="prose">{art_body}</div>
<p class="disclaimer">{icon('book')}المحتوى تعليمي عام ولا يغني عن استشارة مهنية لحالتك أو عن الرجوع إلى الجهة الرسمية المختصة.</p>
{cta(t[2], "box", p["title"])}
</article>
<aside class="art-side"><div class="side-box"><h2>قراءات مهمة</h2><ul class="minis">{''.join(mini(q) for q in reads)}</ul></div>
<div class="side-box svc-box {pc}"><h2>خدمة مرتبطة</h2><p>{t[3]}</p><a class="btn" href="{SVC[t[2]]}">اعرف التفاصيل</a><a class="btn wa" href="{wa_link(t[1], p["title"])}" target="_blank" rel="noopener">{icon("chat")}واتساب</a></div></aside>
</div>
{f'<section class="wrap related"><h2>مواضيع ذات صلة</h2><div class="tiles">{"".join(tile(q) for q in related)}</div></section>' if related else ''}"""
        url = SITE + p["path"]
        ld = [{"@context": "https://schema.org", "@graph": [org,
               {"@type": "Article", "@id": url + "#article", "headline": p["title"][:110], "description": p["desc"], "image": [purl(p["photo"], 1200, 675)],
                "datePublished": p["published"], "dateModified": p["updated"], "inLanguage": "ar", "mainEntityOfPage": url,
                "articleSection": t[0], "wordCount": p["words"],
                "author": {"@type": "Organization", "name": "فريق موسوعة جوجان", "url": SITE + "/about/"}, "publisher": {"@id": SITE + "/#org"}},
               {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (u or p["path"])} for i, (n, u) in enumerate(cr)]}]}]
        out = dist / "_posts" / (re.sub(r"[^A-Za-z0-9_-]", "_", p["path"].strip("/")[:-5]) + ".html")
        out.parent.mkdir(parents=True, exist_ok=True)
        kw = "، ".join(dict.fromkeys([p.get("seo_title") or p["title"], t[0], "السعودية", "جوجان"]))
        wa_label = "استفسر عبر واتساب"
        out.write_text(page(seo_title(p["title"], p.get("seo_title")), p["desc"], p["path"], body, ld=ld, og_image=purl(p["photo"], 1200, 630), og_type="article", cls="is-article",
                            keywords=kw, wa=(wa_link(t[1], p["title"]), wa_label)), encoding="utf-8")

    # ---------------- hubs
    for k in live_topics:
        t = TOPICS[k]
        pl, pc, _ = PILLARS[t[1]]
        lst = by_topic[k]
        other = [x for x in live_topics if x != k and TOPICS[x][1] == t[1]]
        intro = f"{t[4]} {count_label(len(lst))} {'مرتبة' if len(lst) > 2 else ''} حسب الشمول.".replace("  ", " ")
        hub_text = HUB_INTRO.get(k, "")
        tags = "".join(f'<a href="/topics/{x}/">{TOPICS[x][0]}</a>' for x in other)
        ex = f'<div class="banner-tags"><a href="/topics/">كل المحاور</a>{tags}</div>'
        body = banner(t[0], intro, crumbs([("الموسوعة", "/"), ("المحاور", "/topics/"), (t[0], None)]), ex, pc) + f"""
{f'<div class="wrap hub-intro prose"><p>{hub_text}</p></div>' if hub_text else ''}
<div class="wrap list-grid"><section class="cards" aria-labelledby="list-h"><h2 class="sr" id="list-h">أدلة {t[0]} مرتبة حسب الشمول</h2>{''.join(card(p, i + 1, 'الدليل الأشمل' if i == 0 else None) for i, p in enumerate(lst))}</section>
<aside class="list-side">{cta(t[2], 'box', t[0])}<div class="side-box"><h2>محاور قريبة</h2><ul class="links">{''.join(f'<li><a href="/topics/{x}/">{TOPICS[x][0]}<em>{len(by_topic[x])}</em></a></li>' for x in other)}</ul></div></aside></div>"""
        ld = [{"@context": "https://schema.org", "@graph": [org, {"@type": "CollectionPage", "name": t[0], "url": f"{SITE}/topics/{k}/", "inLanguage": "ar",
               "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + p["path"], "name": p["title"]} for i, p in enumerate(lst)]}}]}]
        d = dist / "topics" / k
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(f"{t[0]}: أدلة ومراجع | {SHORT}", desc_of(hub_text or intro, ""), f"/topics/{k}/", body, ld=ld, og_image=purl(topic_photo[k], 1200, 630),
                                           keywords=f"{t[0]}، {t[3]}، السعودية، جوجان", wa=(wa_link(t[1], t[0]), "استفسر عبر واتساب")), encoding="utf-8")

    def topic_cards(pl):
        return "".join(f'<li><a href="/topics/{k}/"><span class="tc-img">{pimg(topic_photo[k], '', 480, 300)}</span><span class="tc-body"><b>{TOPICS[k][0]}</b><span>{TOPICS[k][4]}</span><em>{count_label(len(by_topic[k]))}</em></span></a></li>' for k in live_topics if TOPICS[k][1] == pl)

    idx = banner("فهرس محاور الموسوعة", "محوران رئيسيان: دراسات الجدوى والاستثمار في السعودية، والترجمة المعتمدة والخدمات اللغوية.", crumbs([("الموسوعة", "/"), ("المحاور", None)])) + f"""
<div class="wrap">
<section class="pillar-sec pa"><h2>{icon('chart')}محور الجدوى والاستثمار</h2><ul class="topic-cards pa">{topic_cards('A')}</ul></section>
<section class="pillar-sec pb"><h2>{icon('globe')}محور الترجمة المعتمدة</h2><ul class="topic-cards pb">{topic_cards('B')}</ul></section>
</div>"""
    (dist / "topics" / "index.html").write_text(page(f"فهرس المحاور | {SHORT}", "فهرس محاور موسوعة جوجان: دراسات الجدوى والاستثمار في السعودية، والترجمة المعتمدة والخدمات اللغوية.", "/topics/", idx), encoding="utf-8")

    # ---------------- home
    A = sorted([p for p in keep if TOPICS[p["topic"]][1] == "A"], key=lambda x: -x["words"])
    Bp = sorted([p for p in keep if TOPICS[p["topic"]][1] == "B"], key=lambda x: -x["words"])
    top_a, top_b = A[:7], Bp[:7]
    star = next((p for p in keep if p["path"] == "/2026/09/feasibility-study-off-plan-sales.html"), A[0])
    latest = [p for p in keep if p not in top_a + top_b and p is not star][:6]
    reads = [p for p in keep if p not in top_a + top_b + latest and p is not star][:5]
    n_all = len(keep)
    hero_photo = PHOTOS["home"][0]
    home = f"""<section class="hero"><div class="wrap hero-grid">
<div class="hero-copy"><h1>أدلة عملية لدراسات الجدوى والاستثمار في السعودية والترجمة المعتمدة</h1>
<p class="sub">{n_all} دليلاً عربياً مراجعاً، مرتبة حسب الشمول: من قراءة دراسة الجدوى وتقييم التمويل إلى ترجمة العقود والتقارير الطبية.</p>
<form class="search big" action="https://www.google.com/search" method="get" role="search" data-search><input type="hidden" name="as_sitesearch" value="bloggoogan.com"><label class="sr" for="q-hero">ابحث في الموسوعة</label><input id="q-hero" type="search" name="q" placeholder="مثال: دراسة جدوى مصنع، ترجمة معتمدة للسفارات" autocomplete="off" data-q><button type="submit" aria-label="ابحث">{icon('search')}<span>ابحث</span></button><div class="results" role="listbox" hidden></div></form>
<ul class="facts"><li><b>{len(A)}</b><span>دليلاً في الجدوى والاستثمار</span></li><li><b>{len(Bp)}</b><span>دليلاً في الترجمة المعتمدة</span></li><li><b>{len(live_topics)}</b><span>محوراً فرعياً</span></li></ul>
<p class="reviewed">{icon('check','ic tick')}آخر مراجعة للمحتوى: {REVIEWED}</p></div>
<figure class="hero-img">{pimg(hero_photo, 'تحليل بيانات الأعمال', 900, 640, eager=True, sizes='(max-width:900px) 100vw, 42vw')}</figure>
</div></section>

<section class="wrap ranked" id="guides">
<div class="sec-head"><h2>الأدلة الأشمل في الموسوعة</h2><p>ترتيب حسب حجم المحتوى وعدد الأقسام، لا حسب تقييمات.</p></div>
<div class="tabs">
<input type="radio" name="pill" id="tab-a" checked><label for="tab-a">{icon('chart')}الجدوى والاستثمار</label>
<input type="radio" name="pill" id="tab-b"><label for="tab-b">{icon('globe')}الترجمة المعتمدة</label>
<div class="tab-panel panel-a">{''.join(card(p, i + 1, 'الدليل الأشمل' if i == 0 else None) for i, p in enumerate(top_a))}<a class="more" href="/topics/feasibility/">كل أدلة الجدوى والاستثمار {icon('chev')}</a></div>
<div class="tab-panel panel-b">{''.join(card(p, i + 1, 'الدليل الأشمل' if i == 0 else None) for i, p in enumerate(top_b))}<a class="more" href="/topics/certified-translation/">كل أدلة الترجمة المعتمدة {icon('chev')}</a></div>
</div></section>

<section class="featured"><div class="wrap feat-grid">
<a class="feat-img" href="{star['path']}" tabindex="-1" aria-hidden="true">{pimg(star['photo'], '', 900, 560, sizes='(max-width:900px) 100vw, 50vw')}</a>
<div class="feat-copy"><span class="ribbon">{icon('star')}دليل مختار</span><h2><a href="{star['path']}">{esc(star['title'])}</a></h2><p>{esc(star['desc'])}</p><ul class="ticks">{checks(star, 4)}</ul><a class="btn" href="{star['path']}">اقرأ الدليل</a></div>
</div></section>

<section class="wrap topics-sec"><div class="sec-head"><h2>تصفح حسب المحور</h2><a class="link" href="/topics/">فهرس المحاور {icon('chev')}</a></div>
<h3 class="pillar-h pa">{icon('chart')}الجدوى والاستثمار</h3><ul class="topic-cards pa">{topic_cards('A')}</ul>
<h3 class="pillar-h pb">{icon('globe')}الترجمة المعتمدة</h3><ul class="topic-cards pb">{topic_cards('B')}</ul>
</section>

<section class="wrap guide-grid">
<div class="guide-main">
<div class="sec-head"><h2>أحدث المداخل</h2></div>
<div class="tiles">{''.join(tile(p) for p in latest)}</div>
<div class="sec-head"><h2>أسئلة شائعة عن الموسوعة</h2></div>
{faq(FAQ_HOME)}
</div>
<aside class="guide-side"><div class="side-box"><h2>قراءات مهمة</h2><ul class="minis">{''.join(mini(p) for p in reads)}</ul></div></aside>
</section>

<section class="doors"><div class="wrap doors-grid">
<a class="door pa" href="{CONSULT}"><span class="door-ic">{icon('chart')}</span><b>جوجان للدراسات والاستشارات</b><span>دراسات الجدوى، بحوث السوق، ملفات التمويل الصناعي، إعادة الهيكلة.</span><em>googanconsult.com</em></a>
<a class="door pb" href="{TRANSL}"><span class="door-ic">{icon('doc')}</span><b>جوجان للترجمة المعتمدة</b><span>ترجمة قانونية وطبية وأكاديمية ووثائق السفارات والتأشيرات.</span><em>googantranslation.com</em></a>
<a class="door-wa" href="{wa_link('A')}" target="_blank" rel="noopener">{icon('chat')}واتساب قسم الدراسات</a>
<a class="door-wa" href="{wa_link('B')}" target="_blank" rel="noopener">{icon('chat')}واتساب قسم الترجمة</a>
</div></section>"""
    site_ld = [{"@context": "https://schema.org", "@graph": [org, {"@type": "WebSite", "@id": SITE + "/#site", "name": NAME, "alternateName": SHORT, "url": SITE + "/", "inLanguage": "ar", "publisher": {"@id": SITE + "/#org"}}]}]
    (dist / "index.html").write_text(page(f"{SHORT}: أدلة دراسات الجدوى والاستثمار والترجمة المعتمدة", f"{n_all} دليلاً عربياً في دراسات الجدوى والاستثمار في السعودية والترجمة المعتمدة، مرتبة حسب الشمول ومراجعة {REVIEWED}.", "/", home, ld=site_ld, og_image=purl(hero_photo, 1200, 630), cls="is-home"), encoding="utf-8")

    # ---------------- about / 404
    about = banner("عن الموسوعة ومنهجية التحرير", "من يحرر الموسوعة، وكيف نختار المحتوى ونراجعه ونصححه.", crumbs([("الموسوعة", "/"), ("عن الموسوعة", None)])) + f"""<div class="wrap narrow prose about">
<h2 id="who">من نحن</h2><p>«{NAME}» مرجع تعليمي عربي تحرره شركة جوجان لخدمات الأعمال في الرياض. تخدم الموسوعة قسمين في الشركة: قسم الدراسات والاستشارات (<a href="{CONSULT}">googanconsult.com</a>) وقسم الترجمة المعتمدة (<a href="{TRANSL}">googantranslation.com</a>).</p>
<h2 id="credentials">الشركة واعتماداتها</h2><ul>
<li>الاسم النظامي: شركة جوجان لخدمات الأعمال (Googan Business Services Company)، الرياض، المملكة العربية السعودية.</li>
<li>خبرة تمتد لأكثر من 30 عاماً في الأردن والسعودية.</li>
<li>شهادة ISO 17100:2015 الخاصة بمقدمي خدمات الترجمة، رقم RSBV-2601-9791، صادرة عن Royal Stancert B.V.</li>
<li>شهادة ISO 9001:2015 لنظام إدارة الجودة، رقم 241026019612، صادرة عن ARS Assessment.</li>
<li>المركز الأول في برنامج «بصمة بلدي» التابع لوزارة البلديات والإسكان عام 2024.</li>
</ul>
<h2 id="contact">التواصل</h2><ul>
<li>قسم الدراسات والاستشارات: <a href="{CONSULT}">googanconsult.com</a>، واتساب <a href="{wa_link('A')}" target="_blank" rel="noopener"><bdi dir="ltr">+966 50 797 5011</bdi></a></li>
<li>قسم الترجمة المعتمدة: <a href="{TRANSL}">googantranslation.com</a>، واتساب <a href="{wa_link('B')}" target="_blank" rel="noopener"><bdi dir="ltr">+966 54 378 4171</bdi></a></li>
<li>البريد الإلكتروني: <a href="mailto:info@googan.net">info@googan.net</a></li>
</ul>
<h2 id="method">منهجية التحرير</h2><ul><li>تنشر الموسوعة أدلة تعليمية تشرح المفاهيم والخطوات العامة، ولا تنشر وعوداً بنتائج أو تقييمات.</li><li>عند ذكر اشتراط نظامي أو رقم رسمي نحيل إلى مصدره، ونذكر تاريخ آخر مراجعة على كل صفحة.</li><li>رُتّبت الأدلة في القوائم حسب شمول المحتوى (حجمه وعدد أقسامه)، وليس حسب تقييمات.</li><li>دُمجت المقالات المكررة، وأُحيلت المقالات القصيرة أو الخارجة عن تخصص الموسوعة إلى أقرب صفحة مناسبة، مع الحفاظ على روابطها القديمة.</li></ul>
<h2 id="images">الصور</h2><p>الصور الرئيسية في المقالات صور توضيحية من منصة Unsplash، ولا تمثل مشاريع أو عملاء لجوجان.</p>
<h2 id="fix">التصحيح والتواصل</h2><p>لملاحظة أو تصحيح على أي مقال راسلنا على <a href="mailto:info@googan.net">info@googan.net</a> مع رابط المقال.</p>
<h2 id="disclaimer">إخلاء المسؤولية</h2><p>المحتوى تعليمي عام ولا يغني عن استشارة مهنية لحالتك أو عن الرجوع إلى الجهة الرسمية المختصة.</p></div>"""
    (dist / "about").mkdir(exist_ok=True)
    (dist / "about" / "index.html").write_text(page(f"عن الموسوعة ومنهجية التحرير | {SHORT}", "من يحرر موسوعة جوجان، وكيف نختار المحتوى ونراجعه ونصححه، ومصدر الصور.", "/about/", about, ld=[{"@context": "https://schema.org", "@graph": [org, {"@type": "AboutPage", "name": "عن الموسوعة", "url": SITE + "/about/"}]}]), encoding="utf-8")
    nf = banner("الصفحة غير موجودة", "ربما نُقلت الصفحة أو حُذفت. ابحث عن الدليل الذي تريده أو ابدأ من فهرس المحاور.") + f"""<div class="wrap narrow nf"><form class="search big" action="https://www.google.com/search" method="get" role="search" data-search><input type="hidden" name="as_sitesearch" value="bloggoogan.com"><label class="sr" for="q-nf">ابحث في الموسوعة</label><input id="q-nf" type="search" name="q" placeholder="ابحث عن دليل…" autocomplete="off" data-q><button type="submit" aria-label="ابحث">{icon('search')}<span>ابحث</span></button><div class="results" role="listbox" hidden></div></form><p><a class="btn" href="/topics/">فهرس المحاور</a> <a class="btn ghost" href="/">الصفحة الرئيسية</a></p></div>"""
    (dist / "404.html").write_text(page(f"الصفحة غير موجودة | {SHORT}", "الصفحة غير موجودة.", "/404", nf, noindex=True), encoding="utf-8")

    import books
    book_urls = books.build_books(dist, page=page, banner=banner, crumbs=crumbs, esc=esc, icon=icon, transl=TRANSL, short=SHORT)

    # ---------------- search index, sitemap, robots, feed, headers, redirects
    norm_topic = {k: TOPICS[k][0] for k in TOPICS}
    json.dump([{"t": p["title"], "u": p["path"], "c": norm_topic[p["topic"]]} for p in keep], open(dist / "assets" / "search.json", "w"), ensure_ascii=False)
    urls = [("/", None), ("/topics/", None), ("/about/", None)] + [(f"/topics/{k}/", None) for k in live_topics]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"<url><loc>{SITE}{u}</loc><lastmod>{NOW.strftime('%Y-%m-%d')}</lastmod></url>" for u, _ in urls]
    sm += [f"<url><loc>{SITE}{p['path']}</loc><lastmod>{p['updated'][:10]}</lastmod></url>" for p in keep]
    sm += [f"<url><loc>{SITE}{u}</loc><lastmod>{NOW.strftime('%Y-%m-%d')}</lastmod></url>" for u in book_urls]
    (dist / "sitemap.xml").write_text("\n".join(sm + ["</urlset>"]), encoding="utf-8")
    (dist / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /_posts/\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    fi = "".join(f'<entry><title>{esc(p["title"])}</title><link href="{SITE}{p["path"]}"/><id>{SITE}{p["path"]}</id><published>{p["published"]}</published><updated>{p["updated"]}</updated><summary>{esc(p["desc"])}</summary></entry>' for p in keep[:30])
    (dist / "feeds" / "posts").mkdir(parents=True, exist_ok=True)
    (dist / "feeds" / "posts" / "default").write_text(f'<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>{NAME}</title><link href="{SITE}/"/><id>{SITE}/</id><updated>{keep[0]["updated"]}</updated>{fi}</feed>', encoding="utf-8")
    (dist / "_headers").write_text("/assets/*\n  Cache-Control: public, max-age=86400\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n", encoding="utf-8")
    worker = (HERE / "_worker.js").read_text(encoding="utf-8").replace("/*REDIRECTS*/{}", json.dumps(redirects, ensure_ascii=False))
    (dist / "_worker.js").write_text(worker, encoding="utf-8")
    json.dump({"kept": [p["path"] for p in keep], "redirects": redirects, "extra_reasons": extra}, open(HERE / "manifest.json", "w"), ensure_ascii=False, indent=0)
    return {"kept": len(keep), "redirects": len(redirects), "topics": live_topics, "photos_used": len(USED)}


if __name__ == "__main__":
    print(json.dumps(build(sys.argv[1], sys.argv[2]), ensure_ascii=False))
