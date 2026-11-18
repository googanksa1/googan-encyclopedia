// GOOGAN Encyclopedia v4 — Cloudflare Pages advanced-mode worker.
// 1) 301-redirects retired posts (duplicates, thin or off-topic) to their closest page.
// 2) Serves every kept Blogger URL (/YYYY/MM/slug.html, /p/slug.html) with 200 at its exact path.
// 3) Handles Blogger legacy paths (/search, archives, feeds, ?m=1).
// 4) Serves library.bloggoogan.com (books and translated studies) from the /_library/ build folder.
// 5) Adds security headers to every response (both hostnames).
// 6) Fills the public contact e-mail from the Cloudflare env var SITE_CONTACT_EMAIL into
//    <a data-ce> links (the address is kept out of the repo). Without the variable the links
//    fall back to the About page contact section.
const REDIRECTS = /*REDIRECTS*/{};
const LIBRARY = /*LIBRARY*/"";
const LIBRARY_LIVE = /*LIBRARY_LIVE*/false;
const LIB_REDIRECTS = /*LIB_REDIRECTS*/{};
// Books withdrawn at the owner's request: answer 410 Gone (and never from cache) so no stale copy is served.
const LIB_GONE = /*LIB_GONE*/[];
// Old Blogger posts with no replacement (owner decision 18 Nov 2026): 410 Gone.
const GONE = new Set(/*GONE*/[]);
const KEY = (p) => p.replace(/^\/+/, "").replace(/\.html$/, "").replace(/[^A-Za-z0-9_-]/g, "_");

const SECURITY = {
  "Strict-Transport-Security": "max-age=31536000",
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "SAMEORIGIN",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=(), browsing-topics=()",
  "Cross-Origin-Opener-Policy": "same-origin",
};
const CSP = [
  "default-src 'self'",
  "script-src 'self' 'unsafe-inline'",
  "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
  "font-src 'self' data: https://fonts.gstatic.com",
  "img-src 'self' data: https:",
  "media-src 'self'",
  "connect-src 'self'",
  "frame-src https://www.youtube.com https://www.youtube-nocookie.com",
  "frame-ancestors 'self'",
  "form-action 'self' https://www.google.com",
  "base-uri 'self'",
  "object-src 'none'",
  "upgrade-insecure-requests",
].join("; ");
const EMAIL_OK = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

export default {
  async fetch(request, env) {
    const res = await route(request, env);
    return harden(res, env);
  },
};

function harden(res, env) {
  const out = new Response(res.body, res);
  for (const [k, v] of Object.entries(SECURITY)) out.headers.set(k, v);
  if (!(out.headers.get("content-type") || "").includes("text/html")) return out;
  out.headers.set("Content-Security-Policy", CSP);
  const email = String((env && env.SITE_CONTACT_EMAIL) || "").trim();
  if (!out.body || !EMAIL_OK.test(email)) return out;
  return new HTMLRewriter()
    .on("a[data-ce]", { element(e) { e.setAttribute("href", "mailto:" + email); e.removeAttribute("data-ce"); } })
    .on("[data-ce-text]", { element(e) { e.setInnerContent(email); e.setAttribute("dir", "ltr"); e.removeAttribute("data-ce-text"); } })
    .transform(out);
}

async function route(request, env) {
  {
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
    // Blogger mobile variant (?m=1 / ?m=0): one 301 straight to the final clean URL (no chain).
    if (url.searchParams.has("m")) {
      const q = new URLSearchParams(url.search); q.delete("m");
      const rest = q.toString() ? "?" + q.toString() : "";
      return go((REDIRECTS[path] || url.pathname) + (REDIRECTS[path] ? "" : rest));
    }
    // Old Blogger URLs that never had a replacement: 410 Gone so Google drops them faster than a 404.
    const PAGED = ["updated-max", "updated-min", "max-results", "start", "by-date", "reverse-paginate"].some((k) => url.searchParams.has(k));
    if (GONE.has(path) || ((path === "/search" || path.startsWith("/search/")) && PAGED) || /^\/feeds\/\d+\/comments\//.test(path) || /^\/2025\/05\/article\d+\.html$/.test(path) || path === "/projects" || path === "/projects/") {
      const nf = await env.ASSETS.fetch(new Request(new URL("/404.html", url.origin)));
      return new Response(request.method === "HEAD" ? null : nf.body, { status: 410, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex" } });
    }
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
  }
}

// library.bloggoogan.com: every path maps to /_library/<path>; shared /assets/ come from the site root.
async function library(request, env, url, path) {
  const fetchAsset = (p) => env.ASSETS.fetch(new Request(new URL(p, url.origin), { method: "GET", headers: request.headers }));
  const send = (r, status, extra = {}) => {
    const h = new Headers(r.headers);
    for (const [k, v] of Object.entries(extra)) h.set(k, v);
    return new Response(request.method === "HEAD" ? null : r.body, { status, headers: h });
  };
  if (path.startsWith("/_library")) return Response.redirect(new URL(path.replace(/^\/_library/, "") || "/", url.origin).toString(), 301);
  if (LIB_GONE.some((g) => path === g.slice(0, -1) || path.startsWith(g))) {
    const nf = await fetchAsset("/_library/404.html");
    return send(nf, 410, { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" });
  }
  const to = LIB_REDIRECTS[path];
  if (to) return Response.redirect(new URL(to, url.origin).toString(), 301);
  // Search Console verification files: Pages strips ".html" with a redirect, but Google needs a direct 200.
  if (/^\/google[0-9a-f]+\.html$/.test(path)) {
    const v = await fetchAsset("/_library" + path.slice(0, -5));
    if (v.status === 200) return send(v, 200, { "content-type": "text/html; charset=utf-8" });
  }
  let r = await fetchAsset("/_library" + path);
  if (r.status === 404 && path.startsWith("/assets/")) return env.ASSETS.fetch(request);
  // Pages normalises /x/index.html -> /x/ with a redirect; strip our internal prefix from it.
  // 304 Not Modified (browser revalidating a cached file) is not a redirect: pass it through.
  if (r.status === 304) return new Response(null, { status: 304, headers: r.headers });
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

