"""Turn one Googan training course into encyclopedia course data.

  python3 tools/course_tools/make_course.py META.json COURSE.pdf

META.json: slug, title, subtitle, desc, intro[], audience[], outcomes[], units[], updates[], category.
COURSE.pdf: the course converted from Word AFTER the header logo/site were replaced (see README).
Writes tools/content/courses/<slug>.json and <slug>-pages/NNN.webp (page 1 = designed cover).
"""
import json, re, subprocess, sys, tempfile
from pathlib import Path
import fitz
from PIL import Image

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
sys.path.insert(0, str(TOOLS))
import courses as C

ICONS = {  # 24x24 stroke paths
 "feasibility-studies-course": "M3 20h18M6 17v-5M10 17V8M14 17v-7M18 17V5M15.5 4.5l2.5-1 1 2.5",
 "project-management-course": "M4 5h16v15H4zM4 9h16M8 3v4M16 3v4M7 13h4M7 16h7",
 "iso-certification-course": "M12 3l2.4 4.9 5.4.8-3.9 3.8.9 5.4-4.8-2.5-4.8 2.5.9-5.4L4.2 8.7l5.4-.8zM9.5 12l1.8 1.8 3.4-3.4",
 "performance-improvement-course": "M3 18l6-6 4 4 8-8M15 8h6v6",
 "team-building-course": "M8 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM16 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM2 20c0-3.3 2.7-6 6-6s6 2.7 6 6M12 20c0-3.3 1.8-6 4-6s6 2.7 6 6",
 "meetings-management-course": "M3 6h18v10H3zM8 20h8M12 16v4M7 10h4M7 13h7",
 "time-management-course": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 7v5l3.5 2",
 "priorities-course": "M4 6h10M4 12h7M4 18h4M17 4v16M14 17l3 3 3-3",
 "customer-service-course": "M4 13a8 8 0 0 1 16 0M4 13v4a2 2 0 0 0 2 2h1v-6H4M20 13v4a2 2 0 0 1-2 2h-1v-6h3M17 19c0 1.1-1.8 2-4 2",
 "persuasion-influence-course": "M4 5h12v8H9l-4 3v-3H4zM14 13v2h5l3 3V10h-3",
 "internet-marketing-course": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3",
 "advertising-campaigns-course": "M3 10v4h3l7 4V6L6 10zM16 9a4 4 0 0 1 0 6M18.5 6.5a7.5 7.5 0 0 1 0 11",
 "trade-exhibitions-course": "M3 9l9-5 9 5v11H3zM8 20v-6h8v6M3 9h18",
 "communication-technology-course": "M7 3h10v18H7zM10 18h4M2 9a6 6 0 0 1 3-5M22 9a6 6 0 0 0-3-5",
 "work-stress-course": "M12 3c3 3 5 5.6 5 9a5 5 0 0 1-10 0c0-1.7.6-3.2 1.6-4.4.4 1.5 1.4 2.4 2.4 2.4 0-2.6.3-4.6 1-7z",
 "thinking-skills-course": "M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z",
 "tourism-marketing-course": "M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21zM12 12a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z",
 "tourism-programs-planning-course": "M3 6l6-3 6 3 6-3v15l-6 3-6-3-6 3zM9 3v15M15 6v15",
 "tour-guiding-course": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM15.5 8.5l-2 5-5 2 2-5z",
 "press-writing-course": "M4 4h13v16H6a2 2 0 0 1-2-2zM17 8h3v10a2 2 0 0 1-2 2M7 8h7M7 11h7M7 14h4",
 "press-interview-course": "M12 3a3 3 0 0 1 3 3v5a3 3 0 0 1-6 0V6a3 3 0 0 1 3-3zM6 11a6 6 0 0 0 12 0M12 17v4M9 21h6",
 "classroom-management-course": "M3 5h18v11H3zM8 20l4-4 4 4M7 9h6M7 12h4",
 "study-skills-course": "M3 6c3-1.2 6-1.2 9 .9 3-2.1 6-2.1 9-.9v13c-3-1.2-6-1.2-9 .9-3-2.1-6-2.1-9-.9zM12 6.9v13",
 "dealing-with-teenagers-course": "M9 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM17 11a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zM3 21c0-3.9 2.7-7 6-7s6 3.1 6 7M14 21c.2-2.9 1.4-5 3-5s3.5 2.1 4 5",
}
MARK = '<svg viewBox="0 0 64 64" width="54" height="54"><rect width="64" height="64" rx="14" fill="#fff" fill-opacity=".12"/><path d="M12 46 L22 26 L32 46 Z M32 46 L42 26 L52 46 Z" fill="none" stroke="#f2b632" stroke-width="3.5" stroke-linejoin="round"/><path d="M22 26 L32 12 L42 26" fill="none" stroke="#fff" stroke-width="3.5" stroke-linejoin="round"/></svg>'


def cover_html(m):
    name, _, col = C.CATS[m["category"]]
    path = ICONS.get(m["slug"], "M5 4h10l4 4v12H5zM15 4v4h4M8 12h8M8 15.5h8")
    fonts = TOOLS / "book_tools" / "fonts"
    return f"""<html dir="rtl"><head><meta charset="utf-8"><style>
@font-face{{font-family:A;src:url({fonts}/cairo-ar-700.ttf)}}@font-face{{font-family:AR;src:url({fonts}/cairo-ar-400.ttf)}}@font-face{{font-family:L;src:url({fonts}/cairo-la-700.ttf)}}
body{{margin:0}}.p{{width:794px;height:1123px;position:relative;overflow:hidden;color:#fff;font-family:A,L;background:radial-gradient(circle at 18% 64%,{col} 0,transparent 55%),linear-gradient(155deg,{col} 0%,#16153a 70%,#0f0e28 100%)}}
.pat{{position:absolute;inset:0;opacity:.09}}
.ring{{position:absolute;border-radius:50%;border:2px solid rgba(255,255,255,.14)}}
.top{{position:absolute;top:54px;right:60px;left:60px;display:flex;align-items:center;gap:16px;font-size:22px}}.top span small{{display:block;font-family:L;font-size:15px;opacity:.75;margin-top:2px}}
.head{{position:absolute;top:168px;right:60px;left:80px;display:flex;flex-direction:column;align-items:flex-start;gap:22px}}
.tag{{background:#f2b705;color:#16153a;font-size:21px;padding:6px 22px;border-radius:30px}}
h1{{margin:0;font-size:{64 if len(m['title'])<34 else 54}px;line-height:1.3;text-shadow:0 2px 18px rgba(0,0,0,.25)}}
.sub{{margin:0;font-family:AR;font-size:25px;line-height:1.7;opacity:.9;max-width:600px}}
.ill{{position:absolute;left:-40px;bottom:150px;width:500px;height:500px;border-radius:50%;background:radial-gradient(circle,rgba(242,183,5,.22),rgba(255,255,255,.05) 62%,transparent 72%);display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 26px rgba(255,255,255,.04),0 0 0 60px rgba(255,255,255,.025)}}
.ill svg{{width:250px;height:250px;filter:drop-shadow(0 6px 22px rgba(242,183,5,.35))}}
.wm{{position:absolute;right:-90px;bottom:-120px;width:520px;height:520px;opacity:.06}}
.bot{{position:absolute;bottom:54px;right:60px;left:60px;display:flex;justify-content:space-between;align-items:flex-end;font-size:19px}}.bot small{{display:block;font-family:L;font-size:15px;opacity:.8}}
.line{{position:absolute;bottom:118px;right:60px;width:120px;height:5px;background:#f2b705;border-radius:3px}}
</style></head><body><div class="p">
<svg class="pat" width="794" height="1123"><defs><pattern id="t" width="70" height="60" patternUnits="userSpaceOnUse"><path d="M0 60L17.5 30L35 60ZM35 60L52.5 30L70 60ZM17.5 30L35 0L52.5 30Z" fill="none" stroke="#fff" stroke-width="1.3"/></pattern></defs><rect width="794" height="1123" fill="url(#t)"/></svg>
<div class="ring" style="width:760px;height:760px;left:-260px;bottom:-60px"></div><div class="ring" style="width:980px;height:980px;left:-370px;bottom:-170px"></div>
<div class="top">{MARK}<span>شركة جوجان لخدمات الأعمال<small>googanconsult.com</small></span></div>
<div class="head"><div class="tag">دورة تدريبية · {name}</div><h1>{m['title']}</h1><p class="sub">{m['subtitle']}</p></div>
<svg class="wm" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1"><path d="{path}"/></svg>
<div class="ill"><svg viewBox="0 0 24 24" fill="none" stroke="#f6c64a" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"><path d="{path}"/></svg></div>
<div class="line"></div>
<div class="bot"><span>موسوعة جوجان<small>bloggoogan.com/courses</small></span><span style="text-align:left;font-family:AR">قراءة مجانية</span></div>
</div></body></html>"""


def main(meta_path, pdf_path):
    m = json.load(open(meta_path, encoding="utf-8"))
    slug = m["slug"]
    tmp = Path(tempfile.mkdtemp())
    (tmp / "c.html").write_text(cover_html(m), encoding="utf-8")
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
          f"await p.goto('file://{tmp}/c.html');await p.waitForTimeout(700);await p.pdf({{path:'{tmp}/c.pdf',width:'794px',height:'1123px',printBackground:true,pageRanges:'1'}});await b.close();}})()")
    subprocess.run(["node", "-e", js], check=True)
    doc = fitz.open(tmp / "c.pdf"); body = fitz.open(pdf_path)
    cw = doc[0].rect.width; bw = body[0].rect.width
    doc.insert_pdf(body)
    out_dir = C.DATA / f"{slug}-pages"; out_dir.mkdir(parents=True, exist_ok=True)
    for f in out_dir.glob("*.webp"): f.unlink()
    for i, pg in enumerate(doc):
        zoom = 900 / pg.rect.width
        pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        if i > 0 and abs(im.width / im.height - 794 / 1123) > .02:   # letterbox odd sizes to the cover ratio
            H = round(im.width * 1123 / 794); bg = Image.new("RGB", (im.width, H), "white"); bg.paste(im, (0, (H - im.height) // 2)); im = bg
        im.save(out_dir / f"{i+1:03d}.webp", "WEBP", quality=74)
    toc = body.get_toc(simple=True)
    lvl1 = [(t, p) for l, t, p in toc if l == 1 and t.strip()]
    if len(lvl1) < 3:
        lvl1 = [(t, p) for l, t, p in toc if l <= 2 and t.strip()]
    secs, seen = [], set()
    for t, p in lvl1:
        t = re.sub(r"\s+", " ", t).strip(" :-–.").replace("", "")
        if len(t) < 3 or t in seen or p < 1:
            continue
        seen.add(t); secs.append({"title": t[:90], "page": p + 1})
    if not secs or secs[0]["page"] > 2:
        secs.insert(0, {"title": "بداية الدورة", "page": 2})
    words = sum(len(pg.get_text().split()) for pg in body)
    m.update(pages=doc.page_count, minutes=max(10, round(words / 180 / 5) * 5), sections=secs[:24])
    json.dump(m, open(C.DATA / f"{slug}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{slug}: {doc.page_count} pages, {len(secs)} sections, ~{m['minutes']} min")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
