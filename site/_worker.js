// GOOGAN Encyclopedia v4 — Cloudflare Pages advanced-mode worker.
// 1) 301-redirects retired posts (duplicates, thin or off-topic) to their closest page.
// 2) Serves every kept Blogger URL (/YYYY/MM/slug.html, /p/slug.html) with 200 at its exact path.
// 3) Handles Blogger legacy paths (/search, archives, feeds, ?m=1).
// 4) Serves library.bloggoogan.com (books and translated studies) from the /_library/ build folder.
const REDIRECTS = {"/2012/08/blog-post_2656.html": "/", "/2012/06/blog-post.html": "/", "/2025/06/best-certified-feasibility-study-office.html": "/topics/feasibility/", "/2025/01/body-font-family-arial-sans-serif.html": "/2026/08/feasibility-study-office-riyadh.html", "/2026/08/about-googan.html": "/about/", "/2026/08/2026.html": "/topics/feasibility/", "/2026/08/90.html": "/topics/sectors/", "/2012/02/blog-post_22.html": "/topics/management/", "/2013/02/blog-post_24.html": "/", "/2012/08/blog-post_7690.html": "/", "/2012/07/blog-post_18.html": "/", "/2012/02/wmv.html": "/topics/legal-translation/", "/2011/08/blog-post_27.html": "/", "/2025/05/blog-post.html": "/topics/feasibility/", "/2013/02/blog-post_264.html": "/topics/languages/", "/2014/06/blog-post_23.html": "/", "/2012/04/blog-post.html": "/", "/2026/08/blog-post.html": "/topics/saudi-investment/", "/2011/04/blog-post_8233.html": "/topics/market-research/", "/2011/06/9-essential-skills-of-human-resources_15.html": "/topics/management/", "/2012/12/blog-post_31.html": "/", "/2014/06/blog-post_3071.html": "/", "/2011/05/blog-post_3124.html": "/topics/certified-translation/", "/2012/11/blog-post_7.html": "/topics/certified-translation/", "/2012/02/persian-translation.html": "/topics/languages/", "/p/blog-page.html": "/about/", "/2026/08/feasibility-study-office-riyadh_0179658900.html": "/2026/08/feasibility-study-office-riyadh.html", "/2011/05/blog-post_13.html": "/topics/certified-translation/", "/2014/06/blog-post.html": "/", "/2025/05/blog-post_119.html": "/topics/saudi-investment/", "/2012/02/training-courses.html": "/", "/2011/04/blog-post_9922.html": "/", "/2012/02/blog-post_2611.html": "/topics/certified-translation/", "/2025/06/blog-post_62.html": "/2025/06/blog-post_78.html", "/2011/08/blog-post_21.html": "/", "/2011/10/blog-post_26.html": "/", "/2025/01/what-is-devaluation.html": "/topics/financial-analysis/", "/2025/05/blog-post_63.html": "/topics/certified-translation/", "/2012/09/blog-post_4005.html": "/", "/2012/03/blog-post_25.html": "/topics/market-research/", "/2025/02/blog-post_17.html": "/topics/feasibility/", "/2026/08/5-2026.html": "/topics/saudi-investment/", "/2014/12/blog-post_5.html": "/", "/2011/06/9-essential-skills-of-human-resources_1126.html": "/topics/management/", "/2012/11/blog-post_5.html": "/topics/financial-analysis/", "/2012/02/blog-post.html": "/topics/feasibility/", "/2013/02/blog-post_122.html": "/", "/2011/04/blog-post_8584.html": "/", "/2025/06/httpsgoogan.coarticlewhy-do-projects-fail-an-inside-look-from-a-feasibility-study-perspective-complete-guid_01892806155.html": "/2025/06/httpsgoogan.coarticlewhy-do-projects-fail-an-inside-look-from-a-feasibility-study-perspective-complete-guid.html", "/2026/08/chinese-certified-translation-riyadh.html": "/topics/languages/", "/2011/09/change-management.html": "/topics/management/", "/2012/04/blog-post_7476.html": "/topics/languages/", "/2011/09/blog-post_2913.html": "/", "/2014/06/blog-post_1315.html": "/", "/2025/06/blog-post_67.html": "/2025/06/blog-post_57.html", "/2025/05/blog-post_13.html": "/topics/certified-translation/", "/2012/11/blog-post_10.html": "/topics/certified-translation/", "/2012/06/blog-post_06.html": "/topics/languages/", "/2025/05/body-font-family-segoe-ui-tahoma-geneva_75.html": "/2025/05/blog-post_31.html", "/2013/09/100.html": "/", "/2012/02/ukrainian-translation.html": "/topics/languages/", "/2012/02/legal-translation.html": "/topics/legal-translation/", "/2012/12/blog-post_25.html": "/", "/2025/02/blog-post_22.html": "/topics/feasibility/", "/2014/12/blog-post.html": "/", "/2012/08/5562.html": "/", "/2025/01/blog-post_21.html": "/topics/feasibility/", "/2012/02/blog-post_16.html": "/topics/feasibility/", "/2012/06/blog-post_5959.html": "/topics/languages/", "/2012/08/blog-post_6086.html": "/", "/2012/02/blog-post_8927.html": "/topics/languages/", "/2025/05/httpsgoogan.coarticlefeasibility-study-office-presents-20-new-project-ideas-in-super-artificial-intelligence-currently-unavailable.html": "/topics/feasibility/", "/2026/08/urdu-certified-translation-riyadh.html": "/topics/languages/", "/2011/04/blog-post_29.html": "/topics/market-research/", "/2013/12/blog-post.html": "/topics/management/", "/2025/06/blog-post_71.html": "/topics/industry/", "/2026/08/2026_02136478444.html": "/topics/industry/", "/2012/08/blog-post_3897.html": "/", "/2026/08/french-certified-translation-riyadh.html": "/topics/languages/", "/2012/02/blog-post_8046.html": "/topics/certified-translation/", "/2014/12/blog-post_30.html": "/", "/2012/04/blog-post_05.html": "/topics/management/", "/2013/03/blog-post.html": "/", "/2011/06/9-essential-skills-of-human-resources.html": "/topics/management/", "/2013/02/blog-post_14.html": "/topics/market-research/", "/2012/02/blog-post_18.html": "/", "/2012/01/blog-post.html": "/", "/2025/05/httpsgoogan.coarticlewhy-do-some-projects-fail-despite-sufficient-funding-a-study-of-the-hidden-causes.html": "/2025/05/blog-post_43.html", "/2026/08/from-10000-sar-to-business-success-story.html.html": "/topics/feasibility/", "/2012/07/blog-post_6552.html": "/", "/2024/12/blog-post_25.html": "/", "/2012/09/blog-post_1978.html": "/", "/2011/04/blog-post_1795.html": "/", "/2012/08/blog-post_6729.html": "/topics/financial-analysis/", "/2012/08/blog-post_862.html": "/topics/sectors/", "/2025/06/top-10-feasibility-study-questions.html": "/topics/feasibility/", "/2025/06/blog-post_61.html": "/2025/06/blog-post_19.html", "/2026/08/invest-in-saudi-arabia.html": "/topics/saudi-investment/", "/2026/08/economic-feasibility-study.html": "/2025/05/blog-post_98.html", "/p/blog-page_25.html": "/2026/08/feasibility-study-office-riyadh.html", "/2025/06/blog-post_30.html": "/2026/08/feasibility-study-office-riyadh.html", "/2025/01/blog-post_22.html": "/2026/08/feasibility-study-office-riyadh.html", "/2011/05/blog-post.html": "/2026/08/certified-translation-riyadh.html", "/books/staying-sober/01/": "/books/staying-sober/read/#p=10", "/books/staying-sober/01": "/books/staying-sober/read/#p=10", "/books/staying-sober/02/": "/books/staying-sober/read/#p=12", "/books/staying-sober/02": "/books/staying-sober/read/#p=12", "/books/staying-sober/03/": "/books/staying-sober/read/#p=14", "/books/staying-sober/03": "/books/staying-sober/read/#p=14", "/books/staying-sober/04/": "/books/staying-sober/read/#p=18", "/books/staying-sober/04": "/books/staying-sober/read/#p=18", "/books/staying-sober/05/": "/books/staying-sober/read/#p=22", "/books/staying-sober/05": "/books/staying-sober/read/#p=22", "/books/staying-sober/06/": "/books/staying-sober/read/#p=32", "/books/staying-sober/06": "/books/staying-sober/read/#p=32", "/books/staying-sober/07/": "/books/staying-sober/read/#p=38", "/books/staying-sober/07": "/books/staying-sober/read/#p=38", "/books/staying-sober/08/": "/books/staying-sober/read/#p=58", "/books/staying-sober/08": "/books/staying-sober/read/#p=58", "/books/staying-sober/09/": "/books/staying-sober/read/#p=84", "/books/staying-sober/09": "/books/staying-sober/read/#p=84", "/books/staying-sober/10/": "/books/staying-sober/read/#p=104", "/books/staying-sober/10": "/books/staying-sober/read/#p=104", "/books/staying-sober/11/": "/books/staying-sober/read/#p=114", "/books/staying-sober/11": "/books/staying-sober/read/#p=114", "/books/staying-sober/12/": "/books/staying-sober/read/#p=130", "/books/staying-sober/12": "/books/staying-sober/read/#p=130", "/books/staying-sober/13/": "/books/staying-sober/read/#p=158", "/books/staying-sober/13": "/books/staying-sober/read/#p=158", "/books/staying-sober/14/": "/books/staying-sober/read/#p=172", "/books/staying-sober/14": "/books/staying-sober/read/#p=172", "/books/staying-sober/15/": "/books/staying-sober/read/#p=192", "/books/staying-sober/15": "/books/staying-sober/read/#p=192", "/books/staying-sober/16/": "/books/staying-sober/read/#p=206", "/books/staying-sober/16": "/books/staying-sober/read/#p=206", "/books/staying-sober/17/": "/books/staying-sober/read/#p=210", "/books/staying-sober/17": "/books/staying-sober/read/#p=210"};
const LIBRARY = "https://library.bloggoogan.com";
const LIBRARY_LIVE = false;
const LIB_REDIRECTS = {"/books/staying-sober/01/": "/books/staying-sober/read/#p=10", "/books/staying-sober/01": "/books/staying-sober/read/#p=10", "/books/staying-sober/02/": "/books/staying-sober/read/#p=12", "/books/staying-sober/02": "/books/staying-sober/read/#p=12", "/books/staying-sober/03/": "/books/staying-sober/read/#p=14", "/books/staying-sober/03": "/books/staying-sober/read/#p=14", "/books/staying-sober/04/": "/books/staying-sober/read/#p=18", "/books/staying-sober/04": "/books/staying-sober/read/#p=18", "/books/staying-sober/05/": "/books/staying-sober/read/#p=22", "/books/staying-sober/05": "/books/staying-sober/read/#p=22", "/books/staying-sober/06/": "/books/staying-sober/read/#p=32", "/books/staying-sober/06": "/books/staying-sober/read/#p=32", "/books/staying-sober/07/": "/books/staying-sober/read/#p=38", "/books/staying-sober/07": "/books/staying-sober/read/#p=38", "/books/staying-sober/08/": "/books/staying-sober/read/#p=58", "/books/staying-sober/08": "/books/staying-sober/read/#p=58", "/books/staying-sober/09/": "/books/staying-sober/read/#p=84", "/books/staying-sober/09": "/books/staying-sober/read/#p=84", "/books/staying-sober/10/": "/books/staying-sober/read/#p=104", "/books/staying-sober/10": "/books/staying-sober/read/#p=104", "/books/staying-sober/11/": "/books/staying-sober/read/#p=114", "/books/staying-sober/11": "/books/staying-sober/read/#p=114", "/books/staying-sober/12/": "/books/staying-sober/read/#p=130", "/books/staying-sober/12": "/books/staying-sober/read/#p=130", "/books/staying-sober/13/": "/books/staying-sober/read/#p=158", "/books/staying-sober/13": "/books/staying-sober/read/#p=158", "/books/staying-sober/14/": "/books/staying-sober/read/#p=172", "/books/staying-sober/14": "/books/staying-sober/read/#p=172", "/books/staying-sober/15/": "/books/staying-sober/read/#p=192", "/books/staying-sober/15": "/books/staying-sober/read/#p=192", "/books/staying-sober/16/": "/books/staying-sober/read/#p=206", "/books/staying-sober/16": "/books/staying-sober/read/#p=206", "/books/staying-sober/17/": "/books/staying-sober/read/#p=210", "/books/staying-sober/17": "/books/staying-sober/read/#p=210"};
const KEY = (p) => p.replace(/^\/+/, "").replace(/\.html$/, "").replace(/[^A-Za-z0-9_-]/g, "_");

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    let path;
    try { path = decodeURIComponent(url.pathname); } catch (e) { path = url.pathname; }
    const go = (to, code = 301) => Response.redirect(new URL(to, url.origin).toString(), code);
    const notFound = async () => {
      const nf = await env.ASSETS.fetch(new Request(new URL("/404.html", url.origin)));
      return new Response(request.method === "HEAD" ? null : nf.body, { status: 404, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } });
    };

    if (url.hostname === "bloggoogan.com") return go("https://www.bloggoogan.com" + url.pathname + url.search);
    if (url.hostname.startsWith("library.")) return library(request, env, url, path);
    if (path.startsWith("/_library/") || path === "/_library") return notFound();
    if (REDIRECTS[path]) return go(REDIRECTS[path]);
    if (!path.endsWith(".html") && REDIRECTS[path + ".html"]) return go(REDIRECTS[path + ".html"]);
    if (LIBRARY_LIVE && (path === "/books" || path.startsWith("/books/"))) return go(LIBRARY + path + url.search);
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

// library.bloggoogan.com: every path maps to /_library/<path>; shared /assets/ come from the site root.
async function library(request, env, url, path) {
  const fetchAsset = (p) => env.ASSETS.fetch(new Request(new URL(p, url.origin), { method: "GET", headers: request.headers }));
  const send = (r, status, extra = {}) => {
    const h = new Headers(r.headers);
    for (const [k, v] of Object.entries(extra)) h.set(k, v);
    return new Response(request.method === "HEAD" ? null : r.body, { status, headers: h });
  };
  if (path.startsWith("/_library")) return Response.redirect(new URL(path.replace(/^\/_library/, "") || "/", url.origin).toString(), 301);
  const to = LIB_REDIRECTS[path];
  if (to) return Response.redirect(new URL(to, url.origin).toString(), 301);
  let r = await fetchAsset("/_library" + path);
  if (r.status === 404 && path.startsWith("/assets/")) return env.ASSETS.fetch(request);
  // Pages normalises /x/index.html -> /x/ with a redirect; strip our internal prefix from it.
  if (r.status >= 300 && r.status < 400) {
    const loc = r.headers.get("location") || "/";
    const dest = new URL(loc, url.origin);
    return Response.redirect(new URL(dest.pathname.replace(/^\/_library/, "") + dest.search, url.origin).toString(), r.status === 308 ? 301 : r.status);
  }
  if (r.status === 200) {
    if (path === "/feed.xml") return send(r, 200, { "content-type": "application/atom+xml; charset=utf-8" });
    return send(r, 200);
  }
  const nf = await fetchAsset("/_library/404.html");
  return send(nf, 404, { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" });
}

