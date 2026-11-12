# Notes — imports-data-factory-opportunity (Article 4)

Placement: bloggoogan.com › /topics/saudi-investment/ · URL: /2026/11/imports-data-factory-opportunity.html
Why this topic: no existing encyclopedia or googanconsult article explains how to read import statistics before an industrial decision (checked: industrial feasibility guides /2025/05/blog-post_10.html and /2025/05/body-font-family-segoe-ui-tahoma-geneva_20.html, market analysis /2025/05/blog-post_31.html contain zero mentions of imports/الواردات; /2026/11/why-do-we-import-medicines.html is a macro/strategic pharma piece, not a method).

## Sources table

| المعلومة | المصدر | الرابط | تاريخ البيانات | درجة التحقق | الملاحظات |
|---|---|---|---|---|---|
| مصدر الواردات غير النفطية = سجلات ZATCA، البيان الجمركي وحدة المشاهدة، HS 2022، CIF/FOB، تعريف إعادة التصدير، البيانات أولية ثم تُراجع، البيانات الفردية غير متاحة | GASTAT — Methodology & Quality Report (Annual) 4.1 | https://www.stats.gov.sa/en/w/methodology-and-quality-report-for-international-trade-in-goods-statistics-annual-4.1 | الإصدار الحالي (اطلاع 12/11/2026) | حقيقة موثقة (مصدر أصلي) | قُرئ عبر WebFetch |
| الكميات بالوزن الصافي (كغ) أو بالوحدات لبعض السلع | GASTAT — Methodology (Monthly) 4.1 | https://www.stats.gov.sa/en/w/methodology-and-quality-report-for-international-trade-in-goods-statistics-monthly-4.1 | الإصدار الحالي | حقيقة موثقة | |
| واردات 2024 +12.5%؛ الآلات والأجهزة الكهربائية 25.3%؛ معدات النقل 14.3% | GASTAT — ITR 2024 | https://www.stats.gov.sa/documents/d/guest/itr-2024e-1-pdf | 2024 (أولية) | حقيقة موثقة | لم تظهر القيمة المطلقة في المستخرج |
| التعرفة المتكاملة الخليجية بمستوى 12 رقمًا من 1/1/2025 وأداة البحث | ZATCA — Integrated Tariffs | https://zatca.gov.sa/en/RulesRegulations/Taxes/Pages/Integrated-Tarrifs.aspx | 2025 | حقيقة موثقة | |
| رفع رموز التراخيص الصناعية من 10 إلى 12 رقمًا (ديسمبر 2024) | Deloitte ME | https://www.deloitte.com/middle-east/en/services/tax/perspectives/ksa-updates-industrial-licensing-tariff-codes.html | 25/12/2024 | ثانوي | يحتاج تأكيدًا من mim.gov.sa (تعذر الوصول للمصدر الأصلي) |
| بيانات 392330 واردات/صادرات 2021–2024 (قيم، كميات، شركاء) | World Bank WITS (UN Comtrade, reporter SAU, HS H0) | روابط WITS الثمانية في قسم المصادر | 2021–2024 | ثانوي موثوق (قيم مقتبسة حرفيًا من الصفحات) | الصادرات إجمالية تشمل إعادة التصدير؛ قد تختلف عن أرقام GASTAT النهائية |
| أسعار الوحدة الضمنية، النسب، نمو 57%، الفائض 71.3→35.3 م$ | حساب المحرر من بيانات WITS | — | 2021–2024 | تحليل مهني | حُسبت بـ Python |
| شذوذ كميات 2023 | استنتاج من بيانات WITS | — | 2023 | تحليل مهني/فرضية | يجب مطابقته بقاعدة GASTAT |
| سابر: أكثر من مليون منتج محلي ومستورد، يخدم أصحاب المصانع المحلية | SASO news 1127 | https://saso.gov.sa/ar/mediacenter/news/Pages/saso_news_1127.aspx | 10/09/2020 | حقيقة موثقة (قديمة) | الرقم مؤرخ 2020 |
| «صنع في السعودية» أُطلق 2021 من NIDLP وهيئة تنمية الصادرات | Vision 2030 | https://www.vision2030.gov.sa/en/projects/made-in-saudi/ | 2021 | حقيقة موثقة | الصفحة لا تذكر دليل منتجات |
| موقع صندوق التنمية الصناعية | SIDF | https://www.sidf.gov.sa/ | — | موثق (الموقع الرسمي) | لم تُذكر أي متطلبات محددة |
| مثال التكلفة الواصلة مقابل المحلية | — | — | — | مثال توضيحي افتراضي | الافتراضات معلنة، بما فيها نسبة الرسوم 5% (ليست حقيقة) |

## Keywords (hypotheses — no volume data)
- Primary: هل ارتفاع الواردات فرصة لمصنع / بيانات الاستيراد السعودية
- Supporting: إحلال الواردات في السعودية · كيف أعرف البند الجمركي لمنتجي · بيانات الواردات حسب البند الجمركي · دراسة سوق مصنع بالواردات · التعرفة الجمركية 12 رقم · سعر الوحدة في بيانات التجارة · الإنتاج المحلي مقابل الاستيراد

## Image
Description: original chart — two lines (imports vs exports, HS 392330, 2021–2024, US$ million) with a second panel of implied $/kg, 2023 points greyed and annotated «كميات مشكوك فيها».
ALT: «واردات وصادرات المملكة من القوارير البلاستيكية (البند 392330) بين 2021 و2024 تُظهر أن الصادرات تفوق الواردات رغم ارتفاع الواردات 57%»

## LinkedIn summary (≤80 words)
ارتفعت واردات المملكة من القوارير البلاستيكية 57% بين 2021 و2024. هل هذه فرصة مصنع؟ البيانات نفسها تقول إن المملكة صدّرت من البند ذاته أكثر مما استوردت، وبنصف سعر الكيلوغرام. في موسوعة جوجان: إطار من 9 خطوات لقراءة بيانات الاستيراد قبل الاستثمار الصناعي، وقائمة بـ12 استنتاجًا مضللًا شائعًا.

## Needs human verification before publishing
1. Match WITS 392330 figures (esp. 2023 quantities) against GASTAT database (database.stats.gov.sa unreachable from tooling).
2. Split Saudi exports of 392330 into national vs re-exports (GASTAT).
3. Confirm MIM 10→12-digit licence-code change from an official MIM source (only Deloitte seen).
4. Confirm the national 12-digit sub-items under 392330 in ZATCA tariff search (tool not reachable).
5. SASO/SABER applicability statement phrased generally ("حين تكون المنتجات خاضعة لها") — a SASO specialist may want to refine.
6. SIDF requirements deliberately not stated; confirm CTA wording is acceptable.

## Qualitative review
Strengths: real, retrievable product data with exact periods; counter-intuitive finding (net exporter) that demonstrates the method; explicit separation of fact/analysis/hypothesis/hypothetical; 9-step framework + 12 red flags as the original asset; no fabricated market gap.
Gaps: national (GASTAT) series not retrieved; no 12-digit breakdown, so the "high-value segment" remains a hypothesis; no field interviews (stated as next step, not claimed); word count ~3,300 incl. tables (slightly above the range, tables are dense).

## Competitor-gap notes (not for publication)
- Sampled mashroo3k (sa.mashroo3k.com ceramic factory page): sales page; asserts growing demand with no import figures, HS codes, periods, unit values, local producers or exports.
- Searches for Arabic content on «بيانات الاستيراد + دراسة جدوى مصنع» surfaced mostly import/export how-to blogs and paid PDF studies; no Saudi consulting page found explaining HS-level, unit-value or re-export checks. Gap: method-level, evidence-based reading of trade data — this article fills it.
- ertiqa / mada / almustashar / madroos: no relevant page surfaced in searches for this topic (not individually crawled).
