/* GOOGAN library flip-book reader (RTL). Pages are fed to StPageFlip in reverse order so the
   book opens and turns like an Arabic book. Images load lazily around the current spread. */
(function () {
  var root = document.querySelector("[data-reader]");
  if (!root || !window.St) return;
  var R = +root.dataset.ratio || 1.42, N = +root.dataset.pages, dir = root.dataset.dir, key = "gr:" + root.dataset.slug;
  var book = root.querySelector(".rd-book"), counter = root.querySelector("[data-count]");
  var toc = root.querySelector("[data-toc]"), snd = root.querySelector("[data-sound]");
  var pad = function (n) { return ("00" + n).slice(-3); };
  var LTR = root.dataset.ltr === "1";   // left-to-right books (e.g. German) are fed in natural order
  var kOf = function (pos) { return LTR ? pos + 1 : N - pos; }, posOf = function (k) { return LTR ? k - 1 : N - k; };

  for (var pos = 0; pos < N; pos++) {
    var k = kOf(pos), d = document.createElement("div");
    d.className = "rd-pg";
    if (k === 1 || k === N) d.setAttribute("data-density", "hard");
    d.innerHTML = '<img alt="" draggable="false" data-src="' + dir + pad(k) + '.webp">';
    book.appendChild(d);
  }
  book.addEventListener("contextmenu", function (e) { e.preventDefault(); });

  var pf = new St.PageFlip(book, {
    width: 420, height: Math.round(420 * R), size: "stretch", minWidth: 260, maxWidth: 700, minHeight: Math.round(260 * R), maxHeight: Math.round(700 * R),
    showCover: true, usePortrait: true, mobileScrollSupport: true, maxShadowOpacity: 0.35, flippingTime: 650,
    drawShadow: true, showPageCorners: true
  });
  var pgs = book.querySelectorAll(".rd-pg");
  pf.loadFromHTML(pgs);

  function load(center) {
    var imgs = book.querySelectorAll("img[data-src]");
    for (var i = 0; i < imgs.length; i++) {
      var p = +imgs[i].closest(".rd-pg").dataset.pos;
      if (Math.abs(p - center) <= 6) { imgs[i].src = imgs[i].dataset.src; imgs[i].removeAttribute("data-src"); }
    }
  }
  for (var i = 0; i < pgs.length; i++) pgs[i].dataset.pos = i;

  var SP = root.dataset.spread !== "0";
  function label(pos) {
    var k = kOf(pos);
    if (k === 1) return "الغلاف";
    if (SP && k === N) return "الغلاف الخلفي";
    var n = SP ? k - 1 : k, tot = SP ? N - 2 : N;
    return "صفحة " + n.toLocaleString("ar-EG") + " من " + tot.toLocaleString("ar-EG");
  }
  function current() { return pf.getCurrentPageIndex(); }
  function update() {
    var pos = current(), k = kOf(pos);
    counter.textContent = label(pos);
    load(pos);
    try { localStorage.setItem(key, k); } catch (e) {}
    if (history.replaceState) history.replaceState(null, "", "#p=" + k);
    if (toc) { var v = ""; for (var j = 0; j < toc.options.length; j++) if (+toc.options[j].value && +toc.options[j].value <= k) v = toc.options[j].value; toc.value = v; }
  }

  // page-turn sound: a short filtered noise sweep made with Web Audio (no audio file)
  var ac = null, soundOn = true;
  try { soundOn = localStorage.getItem("gr:sound") !== "0"; } catch (e) {}
  function paintSound() { snd.setAttribute("aria-pressed", soundOn ? "true" : "false"); snd.title = soundOn ? "كتم صوت التقليب" : "تشغيل صوت التقليب"; }
  paintSound();
  snd.addEventListener("click", function () { soundOn = !soundOn; paintSound(); try { localStorage.setItem("gr:sound", soundOn ? "1" : "0"); } catch (e) {} });
  function swish() {
    if (!soundOn) return;
    try {
      ac = ac || new (window.AudioContext || window.webkitAudioContext)();
      var len = Math.floor(ac.sampleRate * 0.32), buf = ac.createBuffer(1, len, ac.sampleRate), ch = buf.getChannelData(0);
      for (var i = 0; i < len; i++) { var t = i / len; ch[i] = (Math.random() * 2 - 1) * Math.pow(1 - t, 2.2) * Math.min(1, t * 14); }
      var src = ac.createBufferSource(), bp = ac.createBiquadFilter(), g = ac.createGain();
      bp.type = "bandpass"; bp.Q.value = 0.8;
      bp.frequency.setValueAtTime(900, ac.currentTime); bp.frequency.exponentialRampToValueAtTime(3800, ac.currentTime + 0.28);
      g.gain.value = 0.55; src.buffer = buf; src.connect(bp); bp.connect(g); g.connect(ac.destination); src.start();
    } catch (e) {}
  }
  pf.on("changeState", function (e) { if (e.data === "flipping") swish(); });
  pf.on("flip", update);
  pf.on("changeOrientation", update);

  var start = 1, m = location.hash.match(/p=(\d+)/);
  if (m) start = +m[1]; else { try { start = +localStorage.getItem(key) || 1; } catch (e) {} }
  start = Math.min(Math.max(start, 1), N);
  load(posOf(start));
  pf.turnToPage(posOf(start));
  update();

  function next() { LTR ? pf.flipNext("bottom") : pf.flipPrev("bottom"); }
  function prev() { LTR ? pf.flipPrev("bottom") : pf.flipNext("bottom"); }
  root.querySelector("[data-next]").addEventListener("click", next);
  root.querySelector("[data-prev]").addEventListener("click", prev);
  document.addEventListener("keydown", function (e) {
    if (e.target.tagName === "SELECT") return;
    if (e.key === "ArrowLeft") { e.preventDefault(); LTR ? prev() : next(); }
    if (e.key === "ArrowRight") { e.preventDefault(); LTR ? next() : prev(); }
  });
  if (toc) toc.addEventListener("change", function () { if (toc.value) { var p = posOf(+toc.value); load(p); pf.turnToPage(p); update(); } });
  window.addEventListener("hashchange", function () { var m = location.hash.match(/p=(\d+)/); if (m) { var p = posOf(+m[1]); load(p); pf.turnToPage(p); update(); } });

  var fs = root.querySelector("[data-fs]");
  if (fs && root.requestFullscreen) fs.addEventListener("click", function () { document.fullscreenElement ? document.exitFullscreen() : root.requestFullscreen(); });
  else if (fs) fs.hidden = true;

  // zoom: show the visible page(s) at full width in a scrollable, pinch-zoomable layer
  var zoom = root.querySelector(".rd-zoom"), zin = zoom.querySelector(".rd-zoom-in");
  root.querySelector("[data-zoom]").addEventListener("click", function () {
    var pos = current(), ks = [kOf(pos)];
    if (pf.getOrientation() === "landscape" && pos > 0 && pos < N - 1) ks = [kOf(pos + 1), kOf(pos)].sort(function (a, b) { return a - b; });
    if (LTR && pf.getOrientation() === "landscape" && pos > 0 && pos < N - 1) ks = [kOf(pos - 1 + (pos % 2)), kOf(pos + (pos % 2))].sort(function (a, b) { return a - b; });
    zin.innerHTML = ks.map(function (k) { return '<img alt="" draggable="false" src="' + dir + pad(k) + '.webp">'; }).join("");
    zoom.hidden = false; zoom.focus();
  });
  zoom.querySelector("[data-close]").addEventListener("click", function () { zoom.hidden = true; });
  zoom.addEventListener("keydown", function (e) { if (e.key === "Escape") zoom.hidden = true; });
  zoom.addEventListener("contextmenu", function (e) { e.preventDefault(); });
})();
