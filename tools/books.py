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
},
    {"slug": "relapse-prevention-workbook", "file": "relapse-prevention-workbook.json", "title": "كتيب تمارين للوقاية من الانتكاس", "orig": "Relapse Prevention Counseling Workbook: Practical Exercises for Managing High-Risk Situations", "authors": "Terence T. Gorski with Arthur B. Trundy", "authors_ar": "تيرنس ت. جورسكي", "desc": "كتيب تمارين عملية للمتعافين من تعاطي الكحول والمخدرات، يتضمن سبعة تمارين للالتزام بالتوقف وخطة التدخل عند الانتكاس وتحديد المواقف عالية الخطورة وإدارتها ووضع خطة التعافي، مع ملاحق ونماذج وعقود.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [0, 1], "page_labels": False, "cover_spread": False},
    {"slug": "therapy-manual-cbt-cocaine", "file": "therapy-manual-cbt-cocaine.json", "title": "الأدلة العلاجية لإدمان المخدرات - الدليل الأول: النموذج المعرفي السلوكي، علاج إدمان الكوكايين (المخدرات)", "orig": "", "authors": "Kathleen M. Carroll, Ph.D", "authors_ar": "الدكتورة كاثلين كارول", "desc": "دليل للمعالجين في العلاج المعرفي السلوكي لتعاطي الكوكايين: مبادئه وبناء جلساته، وجلسة تمهيدية وثمانية موضوعات لمهارات التكيف كالتغلب على الشوق ومهارات الرفض وحل المشاكل، مع ملحقين عن تدريب المعالجين والبحث الإكلينيكي.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [0, 1], "page_labels": False, "cover_spread": False},
    {"slug": "cbt-coping-skills", "file": "cbt-coping-skills.json", "title": "دليل المعالجة المعرفية السلوكية بمهارات المقاومة", "orig": "Cognitive-Behavioral Coping Skills Therapy Manual: A Clinical Research Guide for Therapists Treating Individuals With Alcohol Abuse and Dependence", "authors": "National Institute on Alcohol Abuse and Alcoholism", "authors_ar": "المعهد الوطني لتعاطي الكحول والإدمان على الكحول", "desc": "دليل بحثي للمعالجين القائمين على علاج من يتعاطون الكحول ويدمنونه، أُعد لمشروع MATCH، يعرض برنامج العلاج المعرفي السلوكي بمهارات المقاومة وبنية جلساته الأساسية والاختيارية وتمريناتها وأوراقها التذكيرية.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [0, 3], "page_labels": False, "cover_spread": False},
    {"slug": "matrix-counselor-manual", "file": "matrix-counselor-manual.json", "title": "دليل المرشد العلاجي", "orig": "Counselor's Treatment Manual: Matrix Intensive Outpatient Treatment for People With Stimulant Use Disorders", "authors": "SAMHSA", "authors_ar": "مركز علاج تعاطي المواد المخدرة", "desc": "دليل لتطبيق نموذج مصفوفة العلاج المكثف ماتريكس في العيادات الخارجية لمن يعانون اضطرابات تعاطي المنشطات، يشرح الجلسات الفردية والمشتركة ومجموعات مهارات التعافي المبكر والوقاية من الانتكاس والدعم الاجتماعي مع نشراتها.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [0, 1], "page_labels": False, "cover_spread": False},
    {"slug": "matrix-client-handbook", "file": "matrix-client-handbook.json", "title": "دليل العميل: نموذج مصفوفة للعلاج المكثف ماتريكس في العيادات الخارجية للأشخاص الذين يعانون من اضطرابات تعاطي المنشطات", "orig": "", "authors": "", "authors_ar": "جين إل أوبيرت، ريتشارد إيه روسون، مايكل جيه ماكان، والتر لينج", "desc": "كتيب نشرات للعميل في برنامج ماتريكس للعلاج المكثف في العيادات الخارجية لاضطرابات تعاطي المنشطات، يضم نشرات الجلسات الفردية/المشتركة ومهارات التعافي المبكر والوقاية من الانتكاس وجلسات اختيارية.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [0, 2], "page_labels": False, "cover_spread": False},
    {"slug": "matrix-family-education", "file": "matrix-family-education.json", "title": "دليل المرشد في التوعية الأسرية", "orig": "Counselor's Family Education Manual: Matrix Intensive Outpatient Treatment for People With Stimulant Use Disorders", "authors": "SAMHSA", "authors_ar": "مركز علاج تعاطي المواد المخدرة", "desc": "دليل المرشد لمجموعة التوعية الأسرية ضمن نموذج مصفوفة العلاج المكثف ماتريكس، يقدم تعليمات اثنتي عشرة جلسة للعملاء وأسرهم حول المحفزات والاشتياق والكحول والمنشطات والانتكاس وإعادة بناء الثقة والتواصل، مع النشرات والملاحق.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [0, 1], "page_labels": False, "cover_spread": False},
    {"slug": "matrix-women", "file": "matrix-women.json", "title": "إستخدام مصفوفة ماتريكس مع النساء", "orig": "Using Matrix with Women Clients", "authors": "SAMHSA", "authors_ar": "إدارة \"خدمات إساءة استعمال المواد المخدرة والصحة العقلية\" (SAMHSA)", "desc": "مكمل لمصفوفة العلاج المكثف للمرضى الخارجيين ممن يعانون من اضطرابات استخدام المنشطات، يقدم جلسات جماعية للنساء فقط حول العلاقات والإساءة والعنف والعواطف والأمومة وصورة الجسد والحمل، مع نشرات للمشاركات.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [1, 2], "page_labels": False, "cover_spread": False},
    {"slug": "matrix-client-pocket-guide", "file": "matrix-client-pocket-guide.json", "title": "كُتيب جيب العميل", "orig": "Client's Treatment Companion", "authors": "SAMHSA", "authors_ar": "", "desc": "كتيب شخصي ضمن نموذج مصفوفة العلاج المكثف ماتريكس في العيادات الخارجية للأشخاص الذين يعانون من اضطرابات تعاطي المنشطات، يتيح للعميل تدوين أفكاره عن المحفزات وأهداف التعافي والعلاقات ومبررات الانتكاسة.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [], "page_labels": False, "cover_spread": False},
    {"slug": "therapeutic-community-trainers", "file": "therapeutic-community-trainers.json", "title": "منهج المجتمع العلاجي: دليل المُدربين", "orig": "Therapeutic Community Curriculum: Trainer's Manual", "authors": "Center for Substance Abuse Treatment, Substance Abuse and Mental Health Services Administration (U.S. Department of Health and Human Services)", "authors_ar": "مركز علاج ادمان المخدرات – إدارة علاج الإدمان وخدمات الصحة العقلية", "desc": "دليل للمدربين يقدم منهج المجتمع العلاجي في أحد عشر نموذجاً تدريبياً، تشمل تاريخه وتطوره، والمجتمع بوصفه أسلوباً منهجياً، وبنيته الاجتماعية، ودور فريق العمل، وطرق العلاج، ومراحل البرنامج وكيف يتغير النزلاء.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [0], "page_labels": False, "cover_spread": False},
    {"slug": "advanced-curriculum-1", "file": "advanced-curriculum-1.json", "title": "المنهج التدريبي ذو المستوى المتقدم لمرشد مدمني المخدرات – الكتيب الأول: مقدمة في العمل المهني الخاص بتعاطي المخدرات", "orig": "", "authors": "", "authors_ar": "مكتب الأمم المتحدة المعني بالمخدرات والجريمة؛ المؤلف الرئيسي: ويندي دود", "desc": "يقدم مدخلاً إلى فهم إدمان المخدرات ونُهج العلاج القائمة على الأدلة ونهج الإرشاد وخطط الرعاية وقضايا الممارسة المهنية في العمل مع مدمني المخدرات.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [], "page_labels": False, "cover_spread": True},
    {"slug": "advanced-curriculum-2", "file": "advanced-curriculum-2.json", "title": "المنهج التدريبي ذو المستوى المتقدم لمرشد مدمني المخدرات – الكتيب ٢: التدبير العلاجي للعملاء الخاص بخدمات تعاطي المخدرات", "orig": "", "authors": "", "authors_ar": "مكتب الأمم المتحدة المعني بالمخدرات والجريمة؛ المؤلف الرئيسي: ويندي دود", "desc": "يتناول قضايا الممارسات المهنية والأخلاقيات، وتقييم العملاء وفرزهم وإحالتهم، وتخطيط الرعاية وخطط العلاج الفردي الشاملة، والإشراف، مع مسرد وأداة لخطة العلاج الفردي.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [], "page_labels": False, "cover_spread": True},
    {"slug": "advanced-curriculum-3", "file": "advanced-curriculum-3.json", "title": "المنهج التدريبي ذو المستوى المتقدم لمرشد مدمني المخدرات – الكتيب ٣: مهارات وأساليب الإرشاد", "orig": "", "authors": "", "authors_ar": "مكتب الأمم المتحدة المعني بالمخدرات والجريمة؛ المؤلف الرئيسي: ويندي دود", "desc": "يعرض مهارات الاتصال الأساسية ومهارات الاستماع وحواجز التواصل، ومفهوم الإرشاد وأهدافه وأخلاقياته وحل المشكلات وإنهاء العلاقة الإرشادية.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [], "page_labels": False, "cover_spread": True},
    {"slug": "advanced-curriculum-4", "file": "advanced-curriculum-4.json", "title": "المنهج التدريبي ذو المستوى المتقدم لمرشد مدمني المخدرات – الكتيب ٤: علم الأدوية والصحة النفسية والحد من الأضرار", "orig": "", "authors": "", "authors_ar": "مكتب الأمم المتحدة المعني بالمخدرات والجريمة؛ المؤلف الرئيسي: ويندي دود", "desc": "يغطي نماذج تعاطي المخدرات والاعتماد عليها، وعلم الأدوية الأساسي، وقضايا الصحة النفسية، والتدبير العلاجي للانسحاب، والحد من الأضرار والحقن الآمن والفيروسات المنقولة بالدم والجرعة الزائدة.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [], "page_labels": False, "cover_spread": True},
    {"slug": "advanced-curriculum-5", "file": "advanced-curriculum-5.json", "title": "المنهج التدريبي ذو المستوى المتقدم لمرشد مدمني المخدرات – الكتيب ٥: الأدلة الموجزة للممارسات بشأن العلاجات الخاصة بإرشاد مدمني المخدرات", "orig": "", "authors": "", "authors_ar": "مكتب الأمم المتحدة المعني بالمخدرات والجريمة؛ المؤلف الرئيسي: ويندي دود", "desc": "يعرض أدلة موجزة للمقابلات التحفيزية والعلاج المرتكز على الحل والعلاج المعرفي السلوكي والعلاج الأسري والإرشاد الجماعي والوقاية من الانتكاس وبرامج المساعدة الذاتية.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [], "page_labels": False, "cover_spread": True},
    {"slug": "twelve-step-facilitation", "file": "twelve-step-facilitation.json", "title": "العلاج التيسيري ذو الاثنى عشر خطوة لتعاطي المخدرات والاعتماد عليها", "orig": "", "authors": "U.S. Department of Health and Human Services, Public Health Service, National Institutes of Health", "authors_ar": "ستيوارت ام بيكر", "desc": "دليل علاجي فردي قصير الأمد يُقدَّم في جلسات منظمة لتيسير الامتناع عن المخدرات والكحول عبر المشاركة الفعالة في برامج الاثنتي عشرة خطوة، ويتناول الموضوعات الأساسية والاختيارية والبرنامج المشترك وتدريب المعالجين.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [0, 1], "page_labels": False, "cover_spread": True},
    {"slug": "group-therapy-substance-abuse", "file": "group-therapy-substance-abuse.json", "title": "العلاج الجمعي لإساءة استخدام العقاقير المخدرة: الدليل العلاجي لمراحل التغيير", "orig": "Group Treatment for Substance Abuse: A Stages-of-Change Therapy Manual", "authors": "Mary Marden Velasquez, Gaylyn Gaddy Maurer, Cathy Crouch, Carlo C. DiClemente", "authors_ar": "ماري ماردن فيلاسكيز، جيليان جادي مايرر، كاثي كروش", "desc": "دليل علاجي للمتخصصين يقدم ٢٩ جلسة جماعية قائمة على نموذج مراحل التغيير والمقابلة التحفيزية، مقسمة إلى متواليتين: التفكير في تغيير تعاطي العقاقير ثم تنفيذ التغيير والمحافظة عليه.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [0, 2], "page_labels": False, "cover_spread": True},
    {"slug": "motivational-enhancement-therapy", "file": "motivational-enhancement-therapy.json", "title": "دليل العلاج التحفيزي بزيادة الدافعية", "orig": "", "authors": "National Institute on Alcohol Abuse and Alcoholism", "authors_ar": "وليام ر. ميلر، ألين زويبن، كارلو سي ديكليمنت، روبرت ج. ريتشتاريك", "desc": "دليل بحث إكلينيكي ضمن مشروع (ماتش) يشرح العلاج التحفيزي بزيادة الدافعية لمن يتعاطون الكحول ويدمنونه: أسسه ومبادئه واستراتيجياته العملية وبنية جلساته الأربع والتعامل مع المشكلات الخاصة.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [1], "page_labels": False, "cover_spread": True},
    {"slug": "therapeutic-community-participants", "file": "therapeutic-community-participants.json", "title": "منهج المجتمع العلاجي: دليل المشاركين", "orig": "Therapeutic Community Curriculum: Participant's Manual", "authors": "U.S. Department of Health and Human Services, Substance Abuse and Mental Health Services Administration, Center for Substance Abuse Treatment", "authors_ar": "مركز علاج تعاطي المواد المخدرة", "desc": "دليل تدريبي للمشاركين يعرّف بمنهج المجتمع العلاجي في علاج الإدمان، عبر أحد عشر نموذجاً تتناول تاريخه ورؤيته للعلاج والشفاء وبنيته الاجتماعية ودور فريق العمل وطرق العلاج ومراحل البرنامج وكيفية تغير النزلاء.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [], "page_labels": False, "cover_spread": True},
    {"slug": "addiction-counseling-curriculum", "file": "addiction-counseling-curriculum.json", "title": "المنهج التدريبي للإرشادات الخاصة بعلاج إدمان المخدرات: دليل المُشاركين", "orig": "", "authors": "Robert Ali; Voung Thi Huong Thu; Nguyen To Nhu; pham Thi Huong; kevein Mulvey; Hong Nam Thi; Daniel Levitt (editor)", "authors_ar": "د/ روبرت علي، أ/ فونج ثاي هونج ثو، د/ نجوين تو نهو، أ/ فام ثاي هونج، د/ كيفين مولفاي، د/ هونج نام ثاي، دانيال ليفيت (محرر)", "desc": "منهج تدريبي لمرشدي علاج إدمان المخدرات في تسعة فصول، يغطي مبادئ الإرشاد ومهاراته، والمقابلات التحفيزية، والوقاية من الانتكاسة، والتعامل مع العدوانية، والفئات الخاصة، والإشراف العيادي.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [], "page_labels": False, "cover_spread": True},
    {"slug": "anger-management-therapist", "file": "anger-management-therapist.json", "title": "مهارات إدارة الغضب لمتعافي اضطراب إدمان المخدرات وعملاء الصحة النفسية: دليل العلاج السلوكي المعرفي", "orig": "", "authors": "", "authors_ar": "باتريك إم رايلي، مايكل إس شوبشاير", "desc": "دليل للمعالجين لتقديم علاج سلوكي معرفي جماعي لإدارة الغضب على مدى ١٢ جلسة أسبوعية مدة كل منها ٩٠ دقيقة، مع إرشادات لقادة المجموعة وإجراءات تسجيل الحضور وواجبات منزلية لكل جلسة.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [1, 3], "page_labels": False, "cover_spread": True},
    {"slug": "anger-management-client", "file": "anger-management-client.json", "title": "مهارات إدارة الغضب لمتعافي اضطراب إدمان المخدرات وعملاء الصحة النفسية: دليل العميل", "orig": "Anger Management for Substance Use Disorder and Mental Health Clients: Participant Workbook (Updated 2019)", "authors": "Patrick M. Reilly, Ph.D.; Michael S. Shopshire, Ph.D.; Timothy C. Durazzo, Ph.D.; Torri A. Campbell, Ph.D.", "authors_ar": "رايلي بي. إم.، و شوبشاير إم. إس، و دورازو تي. سي.، و كامبيل بي. إيه.", "desc": "دليل للمشاركين في دورة علاج جماعي لإدارة الغضب مدتها ١٢ أسبوعاً لمتعافي إدمان المخدرات وعملاء الصحة النفسية، يلخص المفاهيم الأساسية لكل جلسة مع أوراق عمل وواجبات منزلية ومساحة للملاحظات.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [1], "page_labels": False, "cover_spread": True},
    {"slug": "anger-management-participant", "file": "anger-management-participant.json", "title": "مهارات إدارة الغضب لمتعافي اضطراب إدمان المخدرات وعملاء الصحة النفسية: كتيب المُشارك (تحديث ٢٠١٩)", "orig": "", "authors": "", "authors_ar": "رايلي بي. إم.، و شوبشاير إم. إس، و دورازو تي. سي.، و كامبيل بي. إيه.", "desc": "كتيب للمشاركين في دورة علاج جماعي لإدارة الغضب مدتها ١٢ أسبوعاً لمتعافي إدمان المخدرات وعملاء الصحة العقلية، يقدم ملخصاً للمفاهيم الأساسية وأوراق عمل للواجبات المنزلية ومساحة للملاحظات في كل جلسة.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [1], "page_labels": False, "cover_spread": True},
    {"slug": "principles-of-addiction-treatment", "file": "principles-of-addiction-treatment.json", "title": "مبادىء علاج الإدمان: دليل قائم على البحث", "orig": "Principles of Drug Addiction Treatment: A Research-Based Guide (Third Edition)", "authors": "National Institute on Drug Abuse, National Institutes of Health, U.S. Department of Health and Human Services", "authors_ar": "", "desc": "دليل قائم على البحث يعرض مبادئ المعالجة الفعالة لإدمان المخدرات، ويجيب عن الأسئلة الشائعة حول العلاج، ويصف أنواع برامج العلاج والمناهج الدوائية والسلوكية القائمة على الأدلة.", "credit": "تمت الترجمة لجمعية المشعل الخيرية وقويم. ترجمة وتدقيق: شركة جوجان لخدمات الأعمال", "preview": [0, 2], "page_labels": False, "cover_spread": True},
]

# Subject categories (shown as sections on /books/ and as their own pages /books/c/<key>/).
# Add a new subject here, then give each book "category": "<key>" and a "type" from TYPES.
CATEGORIES = {
    "addiction": ("الإدمان والتعافي", "أدلة علاجية وكتيبات ومناهج تدريبية في علاج الإدمان والوقاية من الانتكاسة، للمعالجين والمرشدين والمتعافين وأسرهم."),
}
TYPES = {   # order = display order inside a category
    "therapist": "أدلة للمعالجين والمرشدين",
    "client": "كتيبات للمتعافين والمشاركين",
    "training": "مناهج تدريبية",
    "reference": "مراجع ومبادئ عامة",
}
BOOK_TYPE = {
    "staying-sober": "client", "relapse-prevention-workbook": "client", "matrix-client-handbook": "client",
    "matrix-client-pocket-guide": "client", "anger-management-client": "client", "anger-management-participant": "client",
    "therapy-manual-cbt-cocaine": "therapist", "cbt-coping-skills": "therapist", "matrix-counselor-manual": "therapist",
    "matrix-family-education": "therapist", "matrix-women": "therapist", "twelve-step-facilitation": "therapist",
    "group-therapy-substance-abuse": "therapist", "motivational-enhancement-therapy": "therapist", "anger-management-therapist": "therapist",
    "therapeutic-community-trainers": "training", "therapeutic-community-participants": "training", "addiction-counseling-curriculum": "training",
    "advanced-curriculum-1": "training", "advanced-curriculum-2": "training", "advanced-curriculum-3": "training",
    "advanced-curriculum-4": "training", "advanced-curriculum-5": "training",
    "principles-of-addiction-treatment": "reference",
}
for _b in BOOKS:
    _b.setdefault("category", "addiction")
    _b.setdefault("type", BOOK_TYPE.get(_b["slug"], "reference"))


def cover_card(bk, esc, npg=None):
    n = f'<small>{npg} صفحة</small>' if npg else ""
    return (f'<li><a class="bk-tile" href="/books/{bk["slug"]}/"><img src="/books/{bk["slug"]}/pages/001.webp" alt="" loading="lazy" width="180" height="255">'
            f'<strong>{esc(bk["title"])}</strong>{n}</a></li>')


def category_sections(esc, books=None, counts=None, heading="h2", limit=None):
    """HTML: one block per category, grouped by type. Used by /books/, category pages and the library home."""
    books = books or BOOKS
    out = []
    for key, (name, intro) in CATEGORIES.items():
        bs = [b for b in books if b["category"] == key]
        if not bs:
            continue
        groups = []
        for t, tname in TYPES.items():
            tb = [b for b in bs if b["type"] == t]
            if tb:
                n = len(tb)
                tb = tb[:limit] if limit else tb
                groups.append(f'<h3 class="bk-type">{tname} <span>({n})</span></h3><ul class="bk-tiles">{"".join(cover_card(b, esc, (counts or {}).get(b["slug"])) for b in tb)}</ul>')
        out.append(f'<section class="bk-cat" id="c-{key}"><div class="sec-head"><{heading}>{name} <span class="bk-count">{len(bs)} كتاباً</span></{heading}><a class="link" href="/books/c/{key}/">كل كتب التصنيف</a></div><p class="bk-hint">{intro}</p>{"".join(groups)}</section>')
    return "".join(out)


FIX = [(re.compile(r'([.،:؛])(?=[ء-ي])'), r'\1 '), (re.compile(r'([ً-ْ])\1+'), r'\1')]


def clean(t):
    for rx, rep in FIX:
        t = rx.sub(rep, t)
    return t


def render(blocks, esc, limit=None):
    out, words = [], 0
    for kind, txt in blocks:
        if limit and words > limit:
            break
        words += len(txt.split())
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
        from PIL import Image
        with Image.open(imgs / "002.webp") as im0:
            ratio = round(im0.height / im0.width, 4)
        base = f"/books/{bk['slug']}/"
        read = base + "read/"
        shutil.copytree(imgs, root / bk["slug"] / "pages")
        credit = f'<p class="bk-credit">{icon("book")}<span>{esc(bk["credit"])}. <a href="{transl}">googantranslation.com</a></span></p>'
        toc_cards = "".join(
            f'<li><a href="{read}#p={s["page"]}"><span class="bk-ch">{esc(s["title"])}</span>{"<b>" + esc(s["sub"]) + "</b>" if s.get("sub") else ""}{"<small>صفحة " + str(s.get("printed", s["page"] - 1)) + "</small>" if bk.get("page_labels", True) else ""}</a></li>'
            for s in secs)
        pv = bk.get("preview", PREVIEW)
        spread = bk.get("cover_spread", True)   # book 1: PDF page 1 was a front+back cover spread
        npg = npages - 2 if spread else npages
        preview = "".join(f'<section class="bk-pre"><h2>{esc(label(secs[i]))}</h2><div class="prose bk-text">{render(secs[i]["blocks"], esc, 900)}</div></section>' for i in pv)
        pre_html = (f"""<div class="wrap narrow bk-preview"><h2 class="bk-pre-h">من الصفحات الأولى</h2>{preview}
<p class="bk-go"><a class="btn" href="{read}#p={secs[pv[-1] + 1]['page'] if pv[-1] + 1 < len(secs) else secs[-1]['page']}">أكمل القراءة في الكتاب</a></p>{credit}</div>""" if pv else "")
        orig_row = f'<div><dt>العنوان الأصلي</dt><dd dir="ltr">{esc(bk["orig"])}</dd></div>' if bk.get("orig") else ""
        who = " ".join(x for x in (esc(bk.get("authors_ar", "")), f'<span dir="ltr">({esc(bk["authors"])})</span>' if bk.get("authors") else "") if x)
        who_row = f'<div><dt>{"المؤلفان" if bk.get("page_labels", True) else "التأليف"}</dt><dd>{who}</dd></div>' if who else ""
        info = f"""<dl class="bk-info">{orig_row}{who_row}<div><dt>الترجمة والتدقيق</dt><dd>شركة جوجان لخدمات الأعمال، لجمعية المشعل الخيرية وقويم</dd></div><div><dt>التصنيف</dt><dd><a href="/books/c/{bk['category']}/">{CATEGORIES[bk["category"]][0]}</a>، {TYPES[bk["type"]]}</dd></div><div><dt>عدد الصفحات</dt><dd>{npg} صفحة</dd></div><div><dt>الإتاحة</dt><dd>قراءة مجانية على الموقع بتقليب الصفحات</dd></div></dl>"""
        body = banner(esc(bk["title"]), esc(bk["desc"]), crumbs([(short, "/"), ("مكتبة الكتب", "/books/"), (CATEGORIES[bk["category"]][0], f"/books/c/{bk['category']}/"), (bk["title"], None)])) + f"""
<div class="wrap bk-top"><a class="bk-cover" href="{read}#p=1"><img src="{base}pages/001.webp" alt="غلاف كتاب {esc(bk['title'])}" width="420" height="625"></a>
<div class="bk-top-copy">{info}<p class="bk-go"><a class="btn" href="{read}">{icon('book')}اقرأ الكتاب</a></p>{credit}</div></div>
<div class="wrap bk-contents"><h2>فهرس الكتاب</h2><p class="bk-hint">اختر فصلاً ليُفتح الكتاب على صفحته مباشرة.</p><ol class="bk-chs">{toc_cards}</ol></div>
{pre_html}"""
        (root / bk["slug"]).mkdir(parents=True, exist_ok=True)
        ld = [{"@context": "https://schema.org", "@type": "Book", "name": bk["title"], "inLanguage": "ar", "numberOfPages": npg,
               "author": [{"@type": "Person", "name": n.strip()} for n in bk["authors"].split("&")],
               "translator": {"@type": "Organization", "name": "شركة جوجان لخدمات الأعمال"}, "workTranslation": None,
               "translationOfWork": {"@type": "Book", "name": bk["orig"], "inLanguage": "en"}, "url": page.__globals__["SITE"] + base,
               "image": page.__globals__["SITE"] + base + "pages/001.webp"}]
        ld[0].pop("workTranslation")
        (root / bk["slug"] / "index.html").write_text(page(f"{bk['title']} | {short}", bk["desc"], base, body, ld=ld, og_image=page.__globals__["SITE"] + base + "pages/001.webp"), encoding="utf-8")
        urls.append(base)
        opts = "".join(f'<option value="{s["page"]}">{esc(label(s))}</option>' for s in secs)
        rbody = f"""<div class="rd" data-reader data-pages="{npages}" data-ratio="{ratio}" data-spread="{1 if spread else 0}" style="--rd-ratio:{ratio}" data-dir="{base}pages/" data-slug="{bk['slug']}">
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
        cards.append(f'<li class="bk-card"><a href="{base}"><img src="{base}pages/001.webp" alt="" width="120" height="179" loading="lazy"><span><strong>{esc(bk["title"])}</strong><span>{esc(bk["authors_ar"])}</span><span>{npg} صفحة</span></span></a></li>')
    counts = {b["slug"]: len(list((HERE / "content" / "books" / f"{b['slug']}-pages").glob("*.webp"))) - (2 if b.get("cover_spread", True) else 0) for b in BOOKS}
    chips = "".join(f'<a class="bk-chip" href="/books/c/{k}/">{v[0]} <span>{sum(1 for b in BOOKS if b["category"] == k)}</span></a>' for k, v in CATEGORIES.items() if any(b["category"] == k for b in BOOKS))
    body = banner("مكتبة الكتب", f"{len(BOOKS)} كتاباً ترجمها قسم الترجمة في جوجان، تُقرأ كاملة ومجاناً على الموقع بتقليب الصفحات.", crumbs([(short, "/"), ("مكتبة الكتب", None)])) + \
        f'<div class="wrap"><nav class="bk-chips" aria-label="تصنيفات الكتب">{chips}</nav>{category_sections(esc, counts=counts)}</div>'
    (root / "index.html").write_text(page(f"مكتبة الكتب | {short}", "كتب مترجمة تُقرأ مجاناً بتقليب الصفحات، مصنفة حسب الموضوع ونوع الكتاب.", "/books/", body), encoding="utf-8")
    for key, (name, intro) in CATEGORIES.items():
        bs = [b for b in BOOKS if b["category"] == key]
        if not bs:
            continue
        body = banner(name, intro, crumbs([(short, "/"), ("مكتبة الكتب", "/books/"), (name, None)])) + f'<div class="wrap">{category_sections(esc, bs, counts)}</div>'
        (root / "c" / key).mkdir(parents=True, exist_ok=True)
        (root / "c" / key / "index.html").write_text(page(f"{name}: كتب مترجمة | {short}", intro, f"/books/c/{key}/", body), encoding="utf-8")
        urls.append(f"/books/c/{key}/")
    return urls, redirects
