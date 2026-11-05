// GOOGAN Encyclopedia — instant search over /assets/search.json (no dependencies).
(function () {
  var index = null, loading = null;
  function norm(s) {
    return (s || "").toLowerCase()
      .replace(/[ً-ْـ]/g, "")
      .replace(/[إأآا]/g, "ا").replace(/ى/g, "ي").replace(/ة/g, "ه").replace(/ؤ/g, "و").replace(/ئ/g, "ي")
      .replace(/\s+/g, " ").trim();
  }
  function load() {
    if (index) return Promise.resolve(index);
    if (!loading) {
      loading = fetch("/assets/search.json").then(function (r) { return r.json(); }).then(function (d) {
        index = d.map(function (x) { x.n = norm(x.t + " " + x.c); return x; });
        return index;
      }).catch(function () { index = []; return index; });
    }
    return loading;
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function find(q) {
    var words = norm(q).split(" ").filter(function (w) { return w.length > 1; });
    if (!words.length) return [];
    return index.map(function (x) {
      var s = 0;
      words.forEach(function (w) { if (x.n.indexOf(w) > -1) s += 1; });
      return [s, x];
    }).filter(function (a) { return a[0] === words.length || (words.length > 2 && a[0] >= words.length - 1); })
      .sort(function (a, b) { return b[0] - a[0]; }).slice(0, 8).map(function (a) { return a[1]; });
  }
  document.querySelectorAll("[data-search]").forEach(function (form) {
    var input = form.querySelector("[data-q]"), box = form.querySelector(".results");
    function render() {
      var q = input.value;
      if (norm(q).length < 2) { box.hidden = true; box.innerHTML = ""; return; }
      load().then(function () {
        var r = find(q);
        box.innerHTML = r.length
          ? r.map(function (x) { return '<a role="option" href="' + x.u + '"><b>' + esc(x.t) + "</b><span>" + esc(x.c) + "</span></a>"; }).join("")
          : '<p class="none">لا توجد نتائج مطابقة. جرّب كلمة أخرى.</p>';
        box.hidden = false;
      });
    }
    input.addEventListener("input", render);
    input.addEventListener("focus", function () { load(); if (input.value) render(); });
    form.addEventListener("submit", function (e) {
      var first = box.querySelector("a");
      if (first) { e.preventDefault(); location.href = first.getAttribute("href"); return; }
    });
    input.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { box.hidden = true; }
      if (e.key === "ArrowDown") { var a = box.querySelector("a"); if (a) { e.preventDefault(); a.focus(); } }
    });
    box.addEventListener("keydown", function (e) {
      var items = Array.prototype.slice.call(box.querySelectorAll("a")), i = items.indexOf(document.activeElement);
      if (e.key === "ArrowDown" && i < items.length - 1) { e.preventDefault(); items[i + 1].focus(); }
      if (e.key === "ArrowUp") { e.preventDefault(); (i > 0 ? items[i - 1] : input).focus(); }
      if (e.key === "Escape") { box.hidden = true; input.focus(); }
    });
    document.addEventListener("click", function (e) { if (!form.contains(e.target)) box.hidden = true; });
  });
})();
(function () {
  if (window.matchMedia && window.matchMedia("(max-width: 860px)").matches) {
    document.querySelectorAll("details.toc[open]").forEach(function (d) { d.removeAttribute("open"); });
  }
})();
// Retry an image once if it fails to load (e.g. a slow first request), instead of leaving a blank box until refresh.
(function () {
  document.addEventListener("error", function (e) {
    var img = e.target;
    if (!img || img.tagName !== "IMG" || img.dataset.retried) return;
    img.dataset.retried = "1";
    setTimeout(function () {
      var s = img.getAttribute("src") || "";
      img.src = s + (s.indexOf("?") < 0 ? "?" : "&") + "r=" + Date.now();
    }, 900);
  }, true);
})();
