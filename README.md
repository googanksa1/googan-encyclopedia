# موسوعة جوجان — www.bloggoogan.com

Static site served by Cloudflare Pages.

- `site/` — the published website (Cloudflare Pages build output directory). No build command.
- `tools/` — generator scripts used to rebuild `site/` from the Blogger export.

Cloudflare Pages settings: Framework preset **None**, Build command **(empty)**, Build output directory **site**.

## Rebuild

    python3 tools/build4.py --snapshot site

`tools/content/legacy.json` holds the cleaned original Blogger articles. New articles go in
`tools/content/posts/*.md` with a front-matter block:

    ---
    title: عنوان المقال
    slug: english-url-slug
    topic: feasibility
    date: 2026-11-05 09:00
    description: وصف قصير اختياري
    ---
    نص المقال بصيغة Markdown…

A post goes live at `/YYYY/MM/slug.html` on the first rebuild after its date (Riyadh time).
