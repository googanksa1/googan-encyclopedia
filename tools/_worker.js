// GOOGAN Encyclopedia v4 — Cloudflare Pages advanced-mode worker.
// 1) 301-redirects retired posts (duplicates, thin or off-topic) to their closest page.
// 2) Serves every kept Blogger URL (/YYYY/MM/slug.html, /p/slug.html) with 200 at its exact path.
// 3) Handles Blogger legacy paths (/search, archives, feeds, ?m=1).
const REDIRECTS = /*REDIRECTS*/{};
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
