var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// .wrangler/tmp/bundle-VGVxwe/strip-cf-connecting-ip-header.js
function stripCfConnectingIPHeader(input, init) {
  const request = new Request(input, init);
  request.headers.delete("CF-Connecting-IP");
  return request;
}
__name(stripCfConnectingIPHeader, "stripCfConnectingIPHeader");
globalThis.fetch = new Proxy(globalThis.fetch, {
  apply(target, thisArg, argArray) {
    return Reflect.apply(target, thisArg, [
      stripCfConnectingIPHeader.apply(null, argArray)
    ]);
  }
});

// .wrangler/tmp/pages-ogx4uy/bundledWorker-0.03928718180638846.mjs
var __defProp2 = Object.defineProperty;
var __name2 = /* @__PURE__ */ __name((target, value) => __defProp2(target, "name", { value, configurable: true }), "__name");
function stripCfConnectingIPHeader2(input, init) {
  const request = new Request(input, init);
  request.headers.delete("CF-Connecting-IP");
  return request;
}
__name(stripCfConnectingIPHeader2, "stripCfConnectingIPHeader");
__name2(stripCfConnectingIPHeader2, "stripCfConnectingIPHeader");
globalThis.fetch = new Proxy(globalThis.fetch, {
  apply(target, thisArg, argArray) {
    return Reflect.apply(target, thisArg, [
      stripCfConnectingIPHeader2.apply(null, argArray)
    ]);
  }
});
var REDIRECTS = { "/2012/08/blog-post_2656.html": "/", "/2012/06/blog-post.html": "/", "/2025/06/best-certified-feasibility-study-office.html": "/topics/feasibility/", "/2025/01/body-font-family-arial-sans-serif.html": "/2026/08/feasibility-study-office-riyadh.html", "/2026/08/about-googan.html": "/about/", "/2026/08/2026.html": "/topics/feasibility/", "/2026/08/90.html": "/topics/sectors/", "/2012/02/blog-post_22.html": "/topics/management/", "/2013/02/blog-post_24.html": "/", "/2012/08/blog-post_7690.html": "/", "/2012/07/blog-post_18.html": "/", "/2012/02/wmv.html": "/topics/legal-translation/", "/2011/08/blog-post_27.html": "/", "/2025/05/blog-post.html": "/topics/feasibility/", "/2013/02/blog-post_264.html": "/topics/languages/", "/2014/06/blog-post_23.html": "/", "/2012/04/blog-post.html": "/", "/2026/08/blog-post.html": "/topics/saudi-investment/", "/2011/04/blog-post_8233.html": "/topics/market-research/", "/2011/06/9-essential-skills-of-human-resources_15.html": "/topics/management/", "/2012/12/blog-post_31.html": "/", "/2014/06/blog-post_3071.html": "/", "/2011/05/blog-post_3124.html": "/topics/certified-translation/", "/2012/11/blog-post_7.html": "/topics/certified-translation/", "/2012/02/persian-translation.html": "/topics/languages/", "/p/blog-page.html": "/about/", "/2026/08/feasibility-study-office-riyadh_0179658900.html": "/2026/08/feasibility-study-office-riyadh.html", "/2011/05/blog-post_13.html": "/topics/certified-translation/", "/2014/06/blog-post.html": "/", "/2025/05/blog-post_119.html": "/topics/saudi-investment/", "/2012/02/training-courses.html": "/", "/2011/04/blog-post_9922.html": "/", "/2012/02/blog-post_2611.html": "/topics/certified-translation/", "/2025/06/blog-post_62.html": "/2025/06/blog-post_78.html", "/2011/08/blog-post_21.html": "/", "/2011/10/blog-post_26.html": "/", "/2025/01/what-is-devaluation.html": "/topics/financial-analysis/", "/2025/05/blog-post_63.html": "/topics/certified-translation/", "/2012/09/blog-post_4005.html": "/", "/2012/03/blog-post_25.html": "/topics/market-research/", "/2025/02/blog-post_17.html": "/topics/feasibility/", "/2026/08/5-2026.html": "/topics/saudi-investment/", "/2014/12/blog-post_5.html": "/", "/2011/06/9-essential-skills-of-human-resources_1126.html": "/topics/management/", "/2012/11/blog-post_5.html": "/topics/financial-analysis/", "/2012/02/blog-post.html": "/topics/feasibility/", "/2013/02/blog-post_122.html": "/", "/2011/04/blog-post_8584.html": "/", "/2025/06/httpsgoogan.coarticlewhy-do-projects-fail-an-inside-look-from-a-feasibility-study-perspective-complete-guid_01892806155.html": "/2025/06/httpsgoogan.coarticlewhy-do-projects-fail-an-inside-look-from-a-feasibility-study-perspective-complete-guid.html", "/2026/08/chinese-certified-translation-riyadh.html": "/topics/languages/", "/2011/09/change-management.html": "/topics/management/", "/2012/04/blog-post_7476.html": "/topics/languages/", "/2011/09/blog-post_2913.html": "/", "/2014/06/blog-post_1315.html": "/", "/2025/06/blog-post_67.html": "/2025/06/blog-post_57.html", "/2025/05/blog-post_13.html": "/topics/certified-translation/", "/2012/11/blog-post_10.html": "/topics/certified-translation/", "/2012/06/blog-post_06.html": "/topics/languages/", "/2025/05/body-font-family-segoe-ui-tahoma-geneva_75.html": "/2025/05/blog-post_31.html", "/2013/09/100.html": "/", "/2012/02/ukrainian-translation.html": "/topics/languages/", "/2012/02/legal-translation.html": "/topics/legal-translation/", "/2012/12/blog-post_25.html": "/", "/2025/02/blog-post_22.html": "/topics/feasibility/", "/2014/12/blog-post.html": "/", "/2012/08/5562.html": "/", "/2025/01/blog-post_21.html": "/topics/feasibility/", "/2012/02/blog-post_16.html": "/topics/feasibility/", "/2012/06/blog-post_5959.html": "/topics/languages/", "/2012/08/blog-post_6086.html": "/", "/2012/02/blog-post_8927.html": "/topics/languages/", "/2025/05/httpsgoogan.coarticlefeasibility-study-office-presents-20-new-project-ideas-in-super-artificial-intelligence-currently-unavailable.html": "/topics/feasibility/", "/2026/08/urdu-certified-translation-riyadh.html": "/topics/languages/", "/2011/04/blog-post_29.html": "/topics/market-research/", "/2013/12/blog-post.html": "/topics/management/", "/2025/06/blog-post_71.html": "/topics/industry/", "/2026/08/2026_02136478444.html": "/topics/industry/", "/2012/08/blog-post_3897.html": "/", "/2026/08/french-certified-translation-riyadh.html": "/topics/languages/", "/2012/02/blog-post_8046.html": "/topics/certified-translation/", "/2014/12/blog-post_30.html": "/", "/2012/04/blog-post_05.html": "/topics/management/", "/2013/03/blog-post.html": "/", "/2011/06/9-essential-skills-of-human-resources.html": "/topics/management/", "/2013/02/blog-post_14.html": "/topics/market-research/", "/2012/02/blog-post_18.html": "/", "/2012/01/blog-post.html": "/", "/2025/05/httpsgoogan.coarticlewhy-do-some-projects-fail-despite-sufficient-funding-a-study-of-the-hidden-causes.html": "/2025/05/blog-post_43.html", "/2026/08/from-10000-sar-to-business-success-story.html.html": "/topics/feasibility/", "/2012/07/blog-post_6552.html": "/", "/2024/12/blog-post_25.html": "/", "/2012/09/blog-post_1978.html": "/", "/2011/04/blog-post_1795.html": "/", "/2012/08/blog-post_6729.html": "/topics/financial-analysis/", "/2012/08/blog-post_862.html": "/topics/sectors/", "/2025/06/top-10-feasibility-study-questions.html": "/topics/feasibility/", "/2025/06/blog-post_61.html": "/2025/06/blog-post_19.html", "/2026/08/invest-in-saudi-arabia.html": "/topics/saudi-investment/", "/2026/08/economic-feasibility-study.html": "/2025/05/blog-post_98.html", "/p/blog-page_25.html": "/2026/08/feasibility-study-office-riyadh.html", "/2025/06/blog-post_30.html": "/2026/08/feasibility-study-office-riyadh.html", "/2025/01/blog-post_22.html": "/2026/08/feasibility-study-office-riyadh.html", "/2011/05/blog-post.html": "/2026/08/certified-translation-riyadh.html" };
var KEY = /* @__PURE__ */ __name2((p) => p.replace(/^\/+/, "").replace(/\.html$/, "").replace(/[^A-Za-z0-9_-]/g, "_"), "KEY");
var worker_default = {
  async fetch(request, env) {
    const url = new URL(request.url);
    let path;
    try {
      path = decodeURIComponent(url.pathname);
    } catch (e) {
      path = url.pathname;
    }
    const go = /* @__PURE__ */ __name2((to, code = 301) => Response.redirect(new URL(to, url.origin).toString(), code), "go");
    const notFound = /* @__PURE__ */ __name2(async () => {
      const nf = await env.ASSETS.fetch(new Request(new URL("/404.html", url.origin)));
      return new Response(request.method === "HEAD" ? null : nf.body, { status: 404, headers: { "content-type": "text/html; charset=utf-8" } });
    }, "notFound");
    if (url.hostname === "bloggoogan.com")
      return go("https://www.bloggoogan.com" + url.pathname + url.search);
    if (REDIRECTS[path])
      return go(REDIRECTS[path]);
    if (!path.endsWith(".html") && REDIRECTS[path + ".html"])
      return go(REDIRECTS[path + ".html"]);
    if (path === "/search" || path.startsWith("/search/"))
      return go("/topics/");
    if (/^\/\d{4}\/(\d{2}\/?)?$/.test(path))
      return go("/topics/");
    if (/_archive\.html$/.test(path))
      return go("/topics/");
    if (path === "/feeds/posts/summary" || path === "/feeds/posts/default/")
      return go("/feeds/posts/default");
    if (path.startsWith("/_posts/"))
      return notFound();
    if (path.endsWith(".html") && path !== "/404.html" && path !== "/index.html") {
      const r = await env.ASSETS.fetch(new Request(new URL("/_posts/" + KEY(path), url.origin), { method: "GET" }));
      if (r.status === 200) {
        const h = new Headers(r.headers);
        h.set("content-type", "text/html; charset=utf-8");
        h.set("cache-control", "public, max-age=600");
        return new Response(request.method === "HEAD" ? null : r.body, { status: 200, headers: h });
      }
      const alt = await env.ASSETS.fetch(new Request(new URL("/_posts/" + KEY(path + ".html"), url.origin), { method: "GET" }));
      if (alt.status === 200)
        return go(path + ".html");
      return notFound();
    }
    if (/^\/(\d{4}\/\d{2}|p)\/[^/]+$/.test(path)) {
      const r = await env.ASSETS.fetch(new Request(new URL("/_posts/" + KEY(path), url.origin), { method: "GET" }));
      if (r.status === 200)
        return go(path + ".html");
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
};
var drainBody = /* @__PURE__ */ __name2(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } finally {
    try {
      if (request.body !== null && !request.bodyUsed) {
        const reader = request.body.getReader();
        while (!(await reader.read()).done) {
        }
      }
    } catch (e) {
      console.error("Failed to drain the unused request body.", e);
    }
  }
}, "drainBody");
var middleware_ensure_req_body_drained_default = drainBody;
function reduceError(e) {
  return {
    name: e?.name,
    message: e?.message ?? String(e),
    stack: e?.stack,
    cause: e?.cause === void 0 ? void 0 : reduceError(e.cause)
  };
}
__name(reduceError, "reduceError");
__name2(reduceError, "reduceError");
var jsonError = /* @__PURE__ */ __name2(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } catch (e) {
    const error = reduceError(e);
    return Response.json(error, {
      status: 500,
      headers: { "MF-Experimental-Error-Stack": "true" }
    });
  }
}, "jsonError");
var middleware_miniflare3_json_error_default = jsonError;
var __INTERNAL_WRANGLER_MIDDLEWARE__ = [
  middleware_ensure_req_body_drained_default,
  middleware_miniflare3_json_error_default
];
var middleware_insertion_facade_default = worker_default;
var __facade_middleware__ = [];
function __facade_register__(...args) {
  __facade_middleware__.push(...args.flat());
}
__name(__facade_register__, "__facade_register__");
__name2(__facade_register__, "__facade_register__");
function __facade_invokeChain__(request, env, ctx, dispatch, middlewareChain) {
  const [head, ...tail] = middlewareChain;
  const middlewareCtx = {
    dispatch,
    next(newRequest, newEnv) {
      return __facade_invokeChain__(newRequest, newEnv, ctx, dispatch, tail);
    }
  };
  return head(request, env, ctx, middlewareCtx);
}
__name(__facade_invokeChain__, "__facade_invokeChain__");
__name2(__facade_invokeChain__, "__facade_invokeChain__");
function __facade_invoke__(request, env, ctx, dispatch, finalMiddleware) {
  return __facade_invokeChain__(request, env, ctx, dispatch, [
    ...__facade_middleware__,
    finalMiddleware
  ]);
}
__name(__facade_invoke__, "__facade_invoke__");
__name2(__facade_invoke__, "__facade_invoke__");
var __Facade_ScheduledController__ = /* @__PURE__ */ __name(class {
  constructor(scheduledTime, cron, noRetry) {
    this.scheduledTime = scheduledTime;
    this.cron = cron;
    this.#noRetry = noRetry;
  }
  #noRetry;
  noRetry() {
    if (!(this instanceof __Facade_ScheduledController__)) {
      throw new TypeError("Illegal invocation");
    }
    this.#noRetry();
  }
}, "__Facade_ScheduledController__");
__name2(__Facade_ScheduledController__, "__Facade_ScheduledController__");
function wrapExportedHandler(worker) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return worker;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  const fetchDispatcher = /* @__PURE__ */ __name2(function(request, env, ctx) {
    if (worker.fetch === void 0) {
      throw new Error("Handler does not export a fetch() function.");
    }
    return worker.fetch(request, env, ctx);
  }, "fetchDispatcher");
  return {
    ...worker,
    fetch(request, env, ctx) {
      const dispatcher = /* @__PURE__ */ __name2(function(type, init) {
        if (type === "scheduled" && worker.scheduled !== void 0) {
          const controller = new __Facade_ScheduledController__(
            Date.now(),
            init.cron ?? "",
            () => {
            }
          );
          return worker.scheduled(controller, env, ctx);
        }
      }, "dispatcher");
      return __facade_invoke__(request, env, ctx, dispatcher, fetchDispatcher);
    }
  };
}
__name(wrapExportedHandler, "wrapExportedHandler");
__name2(wrapExportedHandler, "wrapExportedHandler");
function wrapWorkerEntrypoint(klass) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return klass;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  return class extends klass {
    #fetchDispatcher = (request, env, ctx) => {
      this.env = env;
      this.ctx = ctx;
      if (super.fetch === void 0) {
        throw new Error("Entrypoint class does not define a fetch() function.");
      }
      return super.fetch(request);
    };
    #dispatcher = (type, init) => {
      if (type === "scheduled" && super.scheduled !== void 0) {
        const controller = new __Facade_ScheduledController__(
          Date.now(),
          init.cron ?? "",
          () => {
          }
        );
        return super.scheduled(controller);
      }
    };
    fetch(request) {
      return __facade_invoke__(
        request,
        this.env,
        this.ctx,
        this.#dispatcher,
        this.#fetchDispatcher
      );
    }
  };
}
__name(wrapWorkerEntrypoint, "wrapWorkerEntrypoint");
__name2(wrapWorkerEntrypoint, "wrapWorkerEntrypoint");
var WRAPPED_ENTRY;
if (typeof middleware_insertion_facade_default === "object") {
  WRAPPED_ENTRY = wrapExportedHandler(middleware_insertion_facade_default);
} else if (typeof middleware_insertion_facade_default === "function") {
  WRAPPED_ENTRY = wrapWorkerEntrypoint(middleware_insertion_facade_default);
}
var middleware_loader_entry_default = WRAPPED_ENTRY;

// ../../.npm-global/lib/node_modules/wrangler/templates/middleware/middleware-ensure-req-body-drained.ts
var drainBody2 = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } finally {
    try {
      if (request.body !== null && !request.bodyUsed) {
        const reader = request.body.getReader();
        while (!(await reader.read()).done) {
        }
      }
    } catch (e) {
      console.error("Failed to drain the unused request body.", e);
    }
  }
}, "drainBody");
var middleware_ensure_req_body_drained_default2 = drainBody2;

// ../../.npm-global/lib/node_modules/wrangler/templates/middleware/middleware-miniflare3-json-error.ts
function reduceError2(e) {
  return {
    name: e?.name,
    message: e?.message ?? String(e),
    stack: e?.stack,
    cause: e?.cause === void 0 ? void 0 : reduceError2(e.cause)
  };
}
__name(reduceError2, "reduceError");
var jsonError2 = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } catch (e) {
    const error = reduceError2(e);
    return Response.json(error, {
      status: 500,
      headers: { "MF-Experimental-Error-Stack": "true" }
    });
  }
}, "jsonError");
var middleware_miniflare3_json_error_default2 = jsonError2;

// .wrangler/tmp/bundle-VGVxwe/middleware-insertion-facade.js
var __INTERNAL_WRANGLER_MIDDLEWARE__2 = [
  middleware_ensure_req_body_drained_default2,
  middleware_miniflare3_json_error_default2
];
var middleware_insertion_facade_default2 = middleware_loader_entry_default;

// ../../.npm-global/lib/node_modules/wrangler/templates/middleware/common.ts
var __facade_middleware__2 = [];
function __facade_register__2(...args) {
  __facade_middleware__2.push(...args.flat());
}
__name(__facade_register__2, "__facade_register__");
function __facade_invokeChain__2(request, env, ctx, dispatch, middlewareChain) {
  const [head, ...tail] = middlewareChain;
  const middlewareCtx = {
    dispatch,
    next(newRequest, newEnv) {
      return __facade_invokeChain__2(newRequest, newEnv, ctx, dispatch, tail);
    }
  };
  return head(request, env, ctx, middlewareCtx);
}
__name(__facade_invokeChain__2, "__facade_invokeChain__");
function __facade_invoke__2(request, env, ctx, dispatch, finalMiddleware) {
  return __facade_invokeChain__2(request, env, ctx, dispatch, [
    ...__facade_middleware__2,
    finalMiddleware
  ]);
}
__name(__facade_invoke__2, "__facade_invoke__");

// .wrangler/tmp/bundle-VGVxwe/middleware-loader.entry.ts
var __Facade_ScheduledController__2 = class {
  constructor(scheduledTime, cron, noRetry) {
    this.scheduledTime = scheduledTime;
    this.cron = cron;
    this.#noRetry = noRetry;
  }
  #noRetry;
  noRetry() {
    if (!(this instanceof __Facade_ScheduledController__2)) {
      throw new TypeError("Illegal invocation");
    }
    this.#noRetry();
  }
};
__name(__Facade_ScheduledController__2, "__Facade_ScheduledController__");
function wrapExportedHandler2(worker) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__2 === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__2.length === 0) {
    return worker;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__2) {
    __facade_register__2(middleware);
  }
  const fetchDispatcher = /* @__PURE__ */ __name(function(request, env, ctx) {
    if (worker.fetch === void 0) {
      throw new Error("Handler does not export a fetch() function.");
    }
    return worker.fetch(request, env, ctx);
  }, "fetchDispatcher");
  return {
    ...worker,
    fetch(request, env, ctx) {
      const dispatcher = /* @__PURE__ */ __name(function(type, init) {
        if (type === "scheduled" && worker.scheduled !== void 0) {
          const controller = new __Facade_ScheduledController__2(
            Date.now(),
            init.cron ?? "",
            () => {
            }
          );
          return worker.scheduled(controller, env, ctx);
        }
      }, "dispatcher");
      return __facade_invoke__2(request, env, ctx, dispatcher, fetchDispatcher);
    }
  };
}
__name(wrapExportedHandler2, "wrapExportedHandler");
function wrapWorkerEntrypoint2(klass) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__2 === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__2.length === 0) {
    return klass;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__2) {
    __facade_register__2(middleware);
  }
  return class extends klass {
    #fetchDispatcher = (request, env, ctx) => {
      this.env = env;
      this.ctx = ctx;
      if (super.fetch === void 0) {
        throw new Error("Entrypoint class does not define a fetch() function.");
      }
      return super.fetch(request);
    };
    #dispatcher = (type, init) => {
      if (type === "scheduled" && super.scheduled !== void 0) {
        const controller = new __Facade_ScheduledController__2(
          Date.now(),
          init.cron ?? "",
          () => {
          }
        );
        return super.scheduled(controller);
      }
    };
    fetch(request) {
      return __facade_invoke__2(
        request,
        this.env,
        this.ctx,
        this.#dispatcher,
        this.#fetchDispatcher
      );
    }
  };
}
__name(wrapWorkerEntrypoint2, "wrapWorkerEntrypoint");
var WRAPPED_ENTRY2;
if (typeof middleware_insertion_facade_default2 === "object") {
  WRAPPED_ENTRY2 = wrapExportedHandler2(middleware_insertion_facade_default2);
} else if (typeof middleware_insertion_facade_default2 === "function") {
  WRAPPED_ENTRY2 = wrapWorkerEntrypoint2(middleware_insertion_facade_default2);
}
var middleware_loader_entry_default2 = WRAPPED_ENTRY2;
export {
  __INTERNAL_WRANGLER_MIDDLEWARE__2 as __INTERNAL_WRANGLER_MIDDLEWARE__,
  middleware_loader_entry_default2 as default
};
//# sourceMappingURL=bundledWorker-0.03928718180638846.js.map
