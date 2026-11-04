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
    seo: عنوان قصير لنتائج البحث (اختياري)
    slug: english-url-slug
    topic: feasibility
    date: 2026-11-05 09:00
    description: وصف قصير اختياري
    ---
    نص المقال بصيغة Markdown…

A post goes live at `/YYYY/MM/slug.html` on the first rebuild after its date (Riyadh time).

## Daily publish

Scheduled posts become visible only after a rebuild. A daily scheduled job runs
`python3 tools/build4.py --snapshot site`, commits any change to `site/`, and pushes;
Cloudflare Pages then deploys automatically.

## Library — library.bloggoogan.com

Books (`tools/books.py`) and translated studies (`topic: translated-studies`) are published on
**مكتبة جوجان** at library.bloggoogan.com, not on the encyclopedia (owner decision, 4 Nov 2026).
`tools/library.py` builds them into `site/_library/` on every rebuild; the worker serves that folder
for the `library.*` hostname. Study URLs: `/studies/<slug>/`; books: `/books/<slug>/`.

`LIBRARY_LIVE` in `tools/build4.py` stays `False` until the library hostname is connected to the
Pages project and verified. Setting it to `True` removes books and studies from the encyclopedia and
301-redirects their old URLs (`/books/…`, the old study URL, `/topics/translated-studies/`) to the library.
