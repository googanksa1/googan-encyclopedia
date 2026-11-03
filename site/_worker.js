// GOOGAN Encyclopedia v4 — Cloudflare Pages advanced-mode worker.
// 1) 301-redirects retired posts (duplicates, thin or off-topic) to their closest page.
// 2) Serves every kept Blogger URL (/YYYY/MM/slug.html, /p/slug.html) with 200 at its exact path.
// 3) Handles Blogger legacy paths (/search, archives, feeds, ?m=1).
const REDIRECTS = {"/2012/08/blog-post_2656.html": "/", "/2012/06/blog-post.html": "/", "/2025/06/best-certified-feasibility-study-office.html": "/topics/feasibility/", "/2025/01/body-font-family-arial-sans-serif.html": "/2025/01/blog-post_22.html", "/2026/08/about-googan.html": "/about/", "/2026/08/2026.html": "/topics/feasibility/", "/2026/08/90.html": "/topics/sectors/", "/2012/02/blog-post_22.html": "/topics/management/", "/2013/02/blog-post_24.html": "/", "/2012/08/blog-post_7690.html": "/", "/2012/07/blog-post_18.html": "/", "/2012/02/wmv.html": "/topics/legal-translation/", "/2011/08/blog-post_27.html": "/", "/2025/05/blog-post.html": "/topics/feasibility/", "/2013/02/blog-post_264.html": "/topics/languages/", "/2014/06/blog-post_23.html": "/", "/2012/04/blog-post.html": "/", "/2026/08/blog-post.html": "/topics/saudi-investment/", "/2011/04/blog-post_8233.html": "/topics/market-research/", "/2011/06/9-essential-skills-of-human-resources_15.html": "/topics/management/", "/2012/12/blog-post_31.html": "/", "/2014/06/blog-post_3071.html": "/", "/2011/05/blog-post_3124.html": "/topics/certified-translation/", "/2012/11/blog-post_7.html": "/topics/certified-translation/", "/2012/02/persian-translation.html": "/topics/languages/", "/p/blog-page.html": "/about/", "/2026/08/feasibility-study-office-riyadh_0179658900.html": "/2026/08/feasibility-study-office-riyadh.html", "/2011/05/blog-post_13.html": "/topics/certified-translation/", "/2014/06/blog-post.html": "/", "/2025/05/blog-post_119.html": "/topics/saudi-investment/", "/2012/02/training-courses.html": "/", "/2011/04/blog-post_9922.html": "/", "/2012/02/blog-post_2611.html": "/topics/certified-translation/", "/2025/06/blog-post_62.html": "/2025/06/blog-post_78.html", "/2011/08/blog-post_21.html": "/", "/2011/10/blog-post_26.html": "/", "/2025/01/what-is-devaluation.html": "/topics/financial-analysis/", "/2025/05/blog-post_63.html": "/topics/certified-translation/", "/2012/09/blog-post_4005.html": "/", "/2012/03/blog-post_25.html": "/topics/market-research/", "/2025/02/blog-post_17.html": "/topics/feasibility/", "/2026/08/5-2026.html": "/topics/saudi-investment/", "/2014/12/blog-post_5.html": "/", "/2011/06/9-essential-skills-of-human-resources_1126.html": "/topics/management/", "/2012/11/blog-post_5.html": "/topics/financial-analysis/", "/2012/02/blog-post.html": "/topics/feasibility/", "/2013/02/blog-post_122.html": "/", "/2011/04/blog-post_8584.html": "/", "/2025/06/httpsgoogan.coarticlewhy-do-projects-fail-an-inside-look-from-a-feasibility-study-perspective-complete-guid_01892806155.html": "/2025/06/httpsgoogan.coarticlewhy-do-projects-fail-an-inside-look-from-a-feasibility-study-perspective-complete-guid.html", "/2026/08/chinese-certified-translation-riyadh.html": "/topics/languages/", "/2011/09/change-management.html": "/topics/management/", "/2012/04/blog-post_7476.html": "/topics/languages/", "/2011/09/blog-post_2913.html": "/", "/2014/06/blog-post_1315.html": "/", "/2025/06/blog-post_67.html": "/2025/06/blog-post_57.html", "/2025/05/blog-post_13.html": "/topics/certified-translation/", "/2012/11/blog-post_10.html": "/topics/certified-translation/", "/2012/06/blog-post_06.html": "/topics/languages/", "/2025/05/body-font-family-segoe-ui-tahoma-geneva_75.html": "/2025/05/blog-post_31.html", "/2013/09/100.html": "/", "/2012/02/ukrainian-translation.html": "/topics/languages/", "/2012/02/legal-translation.html": "/topics/legal-translation/", "/2012/12/blog-post_25.html": "/", "/2025/02/blog-post_22.html": "/topics/feasibility/", "/2014/12/blog-post.html": "/", "/2012/08/5562.html": "/", "/2025/01/blog-post_21.html": "/topics/feasibility/", "/2012/02/blog-post_16.html": "/topics/feasibility/", "/2012/06/blog-post_5959.html": "/topics/languages/", "/2012/08/blog-post_6086.html": "/", "/2012/02/blog-post_8927.html": "/topics/languages/", "/2025/05/httpsgoogan.coarticlefeasibility-study-office-presents-20-new-project-ideas-in-super-artificial-intelligence-currently-unavailable.html": "/topics/feasibility/", "/2026/08/urdu-certified-translation-riyadh.html": "/topics/languages/", "/2011/04/blog-post_29.html": "/topics/market-research/", "/2013/12/blog-post.html": "/topics/management/", "/2025/06/blog-post_71.html": "/topics/industry/", "/2026/08/2026_02136478444.html": "/topics/industry/", "/2012/08/blog-post_3897.html": "/", "/2026/08/french-certified-translation-riyadh.html": "/topics/languages/", "/2012/02/blog-post_8046.html": "/topics/certified-translation/", "/2014/12/blog-post_30.html": "/", "/2012/04/blog-post_05.html": "/topics/management/", "/2013/03/blog-post.html": "/", "/2011/06/9-essential-skills-of-human-resources.html": "/topics/management/", "/2013/02/blog-post_14.html": "/topics/market-research/", "/2012/02/blog-post_18.html": "/", "/2012/01/blog-post.html": "/", "/2025/05/httpsgoogan.coarticlewhy-do-some-projects-fail-despite-sufficient-funding-a-study-of-the-hidden-causes.html": "/2025/05/blog-post_43.html", "/2026/08/from-10000-sar-to-business-success-story.html.html": "/topics/feasibility/", "/2012/07/blog-post_6552.html": "/", "/2024/12/blog-post_25.html": "/", "/2012/09/blog-post_1978.html": "/", "/2011/04/blog-post_1795.html": "/", "/2012/08/blog-post_6729.html": "/topics/financial-analysis/", "/2012/08/blog-post_862.html": "/topics/sectors/", "/2025/06/top-10-feasibility-study-questions.html": "/topics/feasibility/"};
const KEY = (p) => p.replace(/^\/+/, "").replace(/\.html$/, "").replace(/[^A-Za-z0-9_-]/g, "_");

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    let path;
    try { path = decodeURIComponent(url.pathname); } catch (e) { path = url.pathname; }
    const go = (to, code = 301) => Response.redirect(new URL(to, url.origin).toString(), code);
    const notFound = async () => {
      const nf = await env.ASSETS.fetch(new Request(new URL("/404.html", url.origin)));
      return new Response(request.method === "HEAD" ? null : nf.body, { status: 404, headers: { "content-type": "text/html; charset=utf-8" } });
    };

    if (url.hostname === "bloggoogan.com") return go("https://www.bloggoogan.com" + url.pathname + url.search);
    if (REDIRECTS[path]) return go(REDIRECTS[path]);
    if (!path.endsWith(".html") && REDIRECTS[path + ".html"]) return go(REDIRECTS[path + ".html"]);
    if (path === "/search" || path.startsWith("/search/")) return go("/topics/");
    if (/^\/\d{4}\/(\d{2}\/?)?$/.test(path)) return go("/topics/");
    if (/_archive\.html$/.test(path)) return go("/topics/");
    if (path === "/feeds/posts/summary" || path === "/feeds/posts/default/") return go("/feeds/posts/default");
    if (path.startsWith("/_posts/")) return notFound();

    if (path.endsWith(".html") && path !== "/404.html" && path !== "/index.html") {
      const r = await env.ASSETS.fetch(new Request(new URL("/_posts/" + KEY(path), url.origin), { method: "GET" }));
      if (r.status === 200) {
        const h = new Headers(r.headers);
        h.set("content-type", "text/html; charset=utf-8");
        h.set("cache-control", "public, max-age=600");
        return new Response(request.method === "HEAD" ? null : r.body, { status: 200, headers: h });
      }
      const alt = await env.ASSETS.fetch(new Request(new URL("/_posts/" + KEY(path + ".html"), url.origin), { method: "GET" }));
      if (alt.status === 200) return go(path + ".html");
      return notFound();
    }

    // extensionless legacy form (cached 308s from an early deploy): /2011/04/x -> /2011/04/x.html
    if (/^\/(\d{4}\/\d{2}|p)\/[^/]+$/.test(path)) {
      const r = await env.ASSETS.fetch(new Request(new URL("/_posts/" + KEY(path), url.origin), { method: "GET" }));
      if (r.status === 200) return go(path + ".html");
      return notFound();
    }

    const res = await env.ASSETS.fetch(request);
    if (path.startsWith("/feeds/") && res.status === 200) {
      const h = new Headers(res.headers);
      h.set("content-type", "application/atom+xml; charset=utf-8");
      return new Response(res.body, { status: 200, headers: h });
    }
    return res;
  },
};
