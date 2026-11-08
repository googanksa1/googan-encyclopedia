"""Fields and generated SVG covers for translated studies in the library.

Every study gets a cover drawn here (field colour + field icon + field name + year), so the
library never depends on third-party photos. Add new slugs to FIELD_OF; unknown slugs fall back
to the "general" field. Add a new field by adding it to FIELDS (name, intro, colour, icon path).
"""
import re
from html import escape

# key: (name, one-line intro, colour, svg path drawn on a 24x24 grid)
FIELDS = {
    "special-ed": ("التربية الخاصة وصعوبات التعلم", "دراسات في تعليم ذوي الإعاقة وصعوبات التعلم ودمجهم وتأهيلهم.", "#2f6f6b",
                   "M3 5.5c3-1.2 6-1.2 9 .9 3-2.1 6-2.1 9-.9v13c-3-1.2-6-1.2-9 .9-3-2.1-6-2.1-9-.9zM12 6.4v13.4"),
    "deaf": ("الصم وضعاف السمع", "فحص السمع المبكر، ولغة الإشارة، وتعليم الصم ودعم أسرهم وتوظيفهم.", "#34509a",
             "M7.5 9.5a4.5 4.5 0 1 1 9 0c0 2.6-2.1 3.6-2.9 5.2-.7 1.4-.8 3.3-3 3.8a2.6 2.6 0 0 1-3.1-2.1M10 9.6a2 2 0 0 1 4 0c0 1.1-.9 1.6-1.4 2.2"),
    "autism": ("التوحد وتحليل السلوك", "التدخل المبكر في التوحد، وتعديل السلوك، وتصاميم البحث في تحليل السلوك التطبيقي.", "#6d4a9c",
               "M9.5 3.5h3.2v2.3a1.6 1.6 0 1 0 3.2 0V3.5h4.6v6.2h-2.3a1.6 1.6 0 1 0 0 3.2h2.3v7.6h-6.2v-2.3a1.6 1.6 0 1 0-3.2 0v2.3H3.5v-6.2h2.3a1.6 1.6 0 1 0 0-3.2H3.5V3.5z"),
    "health": ("الصحة والتغذية", "دراسات طبية وغذائية: المتلازمة الأيضية، ومركّبات زيت الزيتون، والصحة النفسية.", "#a8433c",
               "M12 20s-7.2-4.4-9-9.2A4.6 4.6 0 0 1 11.2 7l.8.8.8-.8A4.6 4.6 0 0 1 21 10.8C19.2 15.6 12 20 12 20zM5.5 12h3l1.8-2.8 2.8 5.2 1.6-2.4h3.8"),
    "elearning": ("التعليم الإلكتروني والتقنية", "أنظمة إدارة التعلم والتقييم الإلكتروني وتصميم الواجهات وتقنية المعلومات في التعليم.", "#1f6f93",
                  "M4.5 5.5h15v10h-15zM2.5 18.5h19M10 15.5l-.6 3M14 15.5l.6 3"),
    "language": ("اللغة وتعليمها", "التغذية الراجعة في تعلم اللغة، والكتابة، والإملاء.", "#8a5d18",
                 "M3.5 4.5h11v8h-7l-4 3zM10.5 15.5h5.5l4 3v-8.5h-3"),
    "management": ("الإدارة والاقتصاد والمجتمع", "الإدارة العامة والقيادة والإيرادات الضريبية والجريمة المنظمة.", "#3f4a63",
                   "M4 20V11M9.5 20V5M15 20v-7M20.5 20v-11M3 20.5h19"),
    "finance": ("المحاسبة والتحليل المالي", "المراجعة والتدقيق الداخلي والإفصاح المحاسبي والتحليل المالي والتنبؤ بتعثر الشركات.", "#2c6e49",
                "M4 19.5h16M6.5 16V11M10.5 16V7.5M14.5 16v-5.5M18.5 16V5M5.5 9.5l4-3 4 3 5-5"),
    "hr": ("الموارد البشرية والقيادة", "ملخصات رسائل ودراسات في القيادة والتدريب والتوطين وضغوط العمل والثقافة التنظيمية.", "#5b3a8c",
           "M8.5 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM3 20v-2.5A4.5 4.5 0 0 1 7.5 13h2A4.5 4.5 0 0 1 14 17.5V20M16.5 10.5a2.5 2.5 0 1 0 0-5M18 13.2a4 4 0 0 1 3 3.8V20"),
    "marketing": ("التسويق", "ملخصات دراسات في التسويق الإلكتروني والإعلان والمنافسة وسلوك المستهلك السعودي.", "#8a2d3b",
                  "M3.5 10v4l11 4.5V5.5zM14.5 8.5h2a3 3 0 0 1 0 6h-2M6.5 14.5l1.5 5h3l-1.2-4"),
    "banking": ("المصارف والأسواق المالية", "ملخصات دراسات في المصارف الإسلامية وسوق الأسهم السعودية والاستثمار.", "#1f4e79",
                "M3 9.5 12 4l9 5.5M5 10v7M9.5 10v7M14.5 10v7M19 10v7M3 20h18"),
    "economics": ("الاقتصاد والقطاعات", "ملخصات دراسات اقتصادية وقطاعية: الألبان، والزيتون، وعمل المرأة في اقتصاد الأسرة.", "#a0591b",
                  "M12 3v18M16.5 6.5c-1-1.3-2.6-2-4.5-2-2.5 0-4.5 1.4-4.5 3.4 0 4.6 9.4 2.6 9.4 7.4 0 2-2.1 3.5-4.9 3.5-2 0-3.8-.8-4.8-2.2"),
    "general": ("دراسات متنوعة", "دراسات مترجمة في موضوعات أخرى.", "#1c1b42", "M5 4.5h10l4 4v11H5zM15 4.5v4h4M8 12h8M8 15.5h8"),
}

FIELD_OF = {
    # special education
    "early-childhood-intervention-future": "special-ed", "gifted-students-with-disabilities": "special-ed",
    "response-to-intervention-learning-disabilities": "special-ed", "disabled-students-peer-relationships-class": "special-ed",
    "teaching-geometric-shapes-intellectual-disability": "special-ed", "virtual-reality-training-learning-disabilities": "special-ed",
    "assistive-technology-iep-learning-disabilities": "special-ed", "school-counselors-self-advocacy-disabilities": "special-ed",
    "general-case-phone-messages-disabilities": "special-ed", "sports-for-children-with-adhd": "special-ed",
    "assignment-choice-learning-disability": "special-ed", "preteaching-reading-on-task-behavior": "special-ed",
    "brain-injury-return-to-productivity": "special-ed",
    # deaf
    "early-intervention-deaf-children-language": "deaf", "newborn-hearing-screening-early-intervention": "deaf",
    "family-satisfaction-newborn-hearing-services": "deaf", "deaf-students-support-services-secondary-schools": "deaf",
    "supporting-families-of-deaf-children": "deaf", "supported-employment-deaf-people": "deaf",
    "deaf-adults-employment-outcomes": "deaf", "sign-language-coaching-deaf-athletes": "deaf",
    "alphabetic-principle-deaf-children": "deaf",
    # autism / behaviour analysis
    "autism-early-intervention-evidence": "autism", "touch-points-number-line-autism-addition": "autism",
    "parent-social-skills-program-autism": "autism", "paraprofessional-functional-analysis": "autism",
    "praise-notes-lunchroom-behavior": "autism", "peer-praise-notes-withdrawn-adolescents": "autism",
    "progressive-ratio-schedules-applied-behavior-analysis": "autism", "changing-criterion-design-innovations": "autism",
    # health
    "energy-drinks-children-health": "health", "metabolic-syndrome-diagnosis-management": "health",
    "metabolic-syndrome-prevalence-hungary-idf": "health", "curcumin-alzheimers-evidence": "health",
    "olive-oil-ovarian-cancer-study": "health", "olive-oil-hydroxytyrosol-intestinal-cells": "health",
    "bipolar-disorder-clinical-social-work": "health",
    # e-learning & technology
    "standardized-e-assessment-system": "elearning", "instructors-acceptance-lms": "elearning",
    "faculty-course-management-system-use": "elearning", "lms-evaluation-model": "elearning",
    "teachers-it-attitudes-competency": "elearning", "gestalt-principles-interactive-design": "elearning",
    "twitterspace-community-awareness-display": "elearning",
    # language
    "corrective-feedback-learner-uptake": "language", "recasts-tense-consistency": "language",
    "sentence-combining-writing-instruction": "language", "cover-copy-compare-spelling": "language",
    # management / economics / society
    # batch 2026-11-05 (May studies)
    "sme-planning-performance-japan": "management", "first-to-market-first-to-fail": "management",
    "handicapped-college-students-russia": "special-ed", "early-intervention-program-taitung-taiwan": "special-ed",
    "cec-early-intervention-professional-standards": "special-ed", "aba-reversal-design-abab": "autism",
    "early-intervention-five-countries-comparison": "special-ed", "online-courses-deaf-hard-of-hearing-learners": "deaf",
    "towards-theory-of-mobile-learning": "elearning", "trade-openness-fdi-child-labor": "management",
    # finance / accounting (original Arabic research)
    "external-auditor-financial-analysis-early-warning": "finance",
    "organizational-politics-public-sector": "management", "community-college-leadership-competencies": "management",
    "organized-crime-local-businesses": "management", "tax-revenue-effort-developing-countries": "management",
    # summaries batch 2026-11-08 (theses & studies, management/economics)
    "leadership-styles-makkah-emirate": "hr", "saudization-official-procedures": "hr", "air-traffic-controllers-work-stress": "hr",
    "leadership-styles-public-sector-phd": "hr", "employee-training-benefit": "hr", "org-culture-hr-development-tvtc": "hr",
    "emarketing-saudi-commercial-banks": "marketing", "advertising-saudi-consumer": "marketing", "competition-marketing-industrial": "marketing",
    "mobile-marketing-saudi": "marketing", "value-chain-knowledge-management": "management", "business-incubation-saudi": "management",
    "internal-audit-cash-inventory": "finance", "auditing-ethics": "finance", "financial-ratios-failure-prediction": "finance",
    "analytical-accounting-decision-support-phd": "finance", "accounting-policies-disclosure": "finance", "financial-evaluation-sofact-algeria": "finance",
    "islamic-banks-globalization": "banking", "saudi-women-stock-investment": "banking", "saudi-stock-market-variables": "banking",
    "women-work-saudi-family-economy": "economics", "dairy-industry-saudi": "economics", "olive-sector-arab-world": "economics",
    "healthcare-service-quality-cardiac-center": "management", "school-principals-training-program-phd": "hr",
}


def field(p):
    return FIELD_OF.get(p["slug"], "general")


def year_of(p):
    m = re.search(r"(19[5-9]\d|20[0-2]\d)", p["title"])
    return m.group(1) if m else ""


_n = [0]


def cover_svg(p, w=600, h=375, label=True):
    """Inline SVG cover. Decorative (aria-hidden); the title is always printed next to it."""
    key = field(p)
    name, _, col, path = FIELDS[key]
    _n[0] += 1
    gid = f"g{_n[0]}"
    yr = year_of(p)
    full = "بحث عربي" if p.get("kind") == "arabic" else "ملخص دراسة" if p.get("kind") == "summary" else ("دراسة مترجمة" if "ترجمة كاملة" in p.get("body", "")[:4000] else "قراءة عربية")
    sub = f"{full} · {yr}" if yr else full
    txt = (f'<text x="{w - 34}" y="{h - 78}" fill="#fff" font-family="Cairo, sans-serif" font-weight="800" font-size="30" text-anchor="start" direction="rtl">{escape(name)}</text>'
           f'<text x="{w - 34}" y="{h - 40}" fill="#fff" fill-opacity=".82" font-family="Cairo, sans-serif" font-weight="600" font-size="20" text-anchor="start" direction="rtl">{escape(sub)}</text>') if label else ""
    return (f'<svg class="st-cover" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{col}"/><stop offset="1" stop-color="#1c1b42"/></linearGradient>'
            f'<pattern id="{gid}p" width="56" height="48" patternUnits="userSpaceOnUse"><path d="M0 48L14 24L28 48ZM28 48L42 24L56 48ZM14 24L28 0L42 24Z" fill="none" stroke="#fff" stroke-opacity=".07" stroke-width="1.2"/></pattern></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#{gid})"/><rect width="{w}" height="{h}" fill="url(#{gid}p)"/>'
            f'<circle cx="150" cy="{h / 2 - 10:.0f}" r="104" fill="#fff" fill-opacity=".08"/>'
            f'<g transform="translate(78 {h / 2 - 82:.0f}) scale(6)" fill="none" stroke="#fff" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="{path}"/></g>{txt}</svg>')


def field_icon(key, size=26):
    path = FIELDS[key][3]
    return (f'<svg class="fi" viewBox="0 0 24 24" width="{size}" height="{size}" aria-hidden="true" fill="none" stroke="currentColor" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="{path}"/></svg>')
