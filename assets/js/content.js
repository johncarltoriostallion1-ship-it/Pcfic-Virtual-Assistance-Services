// Loads editable content from Supabase: contact details, services and clients (logos, info, work images).
// If Supabase is unreachable or not configured, the page keeps its built-in content.
// Needs: assets/js/icons.js and assets/js/cms-config.js loaded first.
(function () {
  var cfg = window.PCFIC_CMS || {};
  if (!cfg.url || !cfg.key || cfg.key.indexOf("PASTE_") === 0) return;
  var I = window.PCFIC_ICONS || {};
  var headers = { apikey: cfg.key, Authorization: "Bearer " + cfg.key };
  var get = function (path) {
    return fetch(cfg.url + "/rest/v1/" + path, { headers: headers, cache: "no-store" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
  };
  var esc = function (t) {
    return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };
  var $$ = function (sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); };
  var safeUrl = function (u) { u = String(u || ""); return /^(https?:\/\/|assets\/)/i.test(u) ? u : ""; };
  var BLANK = ' target="_blank" rel="noopener"';

  // ---------------- settings ----------------
  function applySettings(rows) {
    var S = {};
    rows.forEach(function (r) { S[r.key] = r.value; });

    $$("[data-cms]").forEach(function (el) {
      var v = S[el.getAttribute("data-cms")];
      if (v) el.textContent = v;
    });

    if (safeUrl(S.logo_url)) $$(".brand-logo img, .seal-mark img").forEach(function (img) { img.src = S.logo_url; });

    var num = (S.whatsapp_number || "").replace(/\D/g, "");
    if (num) {
      $$('a[href^="https://wa.me/"]').forEach(function (a) {
        a.href = a.href.replace(/wa\.me\/\d*/, "wa.me/" + num);
      });
      var form = document.querySelector("#checkin-form");
      if (form) form.dataset.wa = num;
    }

    if (S.email) $$("[data-cms-mail]").forEach(function (a) { a.href = "mailto:" + S.email; });

    var fb = safeUrl(S.facebook_url);
    $$("[data-cms-fb], [data-cms-fb-link]").forEach(function (a) {
      if (fb) { a.href = fb; a.target = "_blank"; a.rel = "noopener"; }
      else if (a.getAttribute("href") === "#") a.style.display = "none";
    });
    if (fb) $$("iframe[data-fb-embed]").forEach(function (f) {
      var next = f.src.replace(/href=[^&]*/, "href=" + encodeURIComponent(fb));
      if (next !== f.src) f.src = next;
    });
  }

  // ---------------- services ----------------
  function applyServices(list) {
    if (!list.length) return;
    var tag = { accounting: "Accounting", social: "Social Media" };
    var page = { accounting: "accounting.html", social: "social-media.html" };

    $$("[data-svc-lib]").forEach(function (grid) {
      grid.innerHTML = list.map(function (s) {
        return '<a class="lib-item reveal in" data-cat="' + esc(s.category) + '" href="' + page[s.category] + '">' +
          '<span class="tag">' + tag[s.category] + "</span><h3>" + esc(s.title) + "</h3><p>" + esc(s.description) + "</p>" +
          '<span class="more">Learn more ' + (I.arrow || "") + "</span></a>";
      }).join("");
      var active = document.querySelector('[data-filter-group="#lib"] .chip.active');
      if (active) active.click();
    });

    $$("[data-svc-feat]").forEach(function (grid) {
      var cat = grid.getAttribute("data-svc-feat");
      grid.innerHTML = list.filter(function (s) { return s.category === cat; }).map(function (s, i) {
        return '<div class="feat reveal in' + ["", " d1", " d2"][i % 3] + '"><div class="ic">' + (I[s.icon] || I.book || "") + "</div><h3>" +
          esc(s.title) + "</h3><p>" + esc(s.description) + "</p></div>";
      }).join("");
    });

    $$("[data-svc-list]").forEach(function (ul) {
      var cat = ul.getAttribute("data-svc-list");
      ul.innerHTML = list.filter(function (s) { return s.category === cat; }).map(function (s) {
        return "<li>" + esc(s.title) + "</li>";
      }).join("");
    });
  }

  // ---------------- clients ----------------
  var link = function (c) { return "client.html?c=" + encodeURIComponent(c.slug); };
  var short = function (c) { return c.short_name || c.name; };
  var imgs = function (c) { return (Array.isArray(c.images) ? c.images : []).filter(safeUrl); };
  var logoImg = function (c, alt) {
    var u = safeUrl(c.logo_url);
    return u ? '<img src="' + esc(u) + '" alt="' + (alt === "" ? "" : esc(c.name) + ' logo') + '" loading="lazy">'
             : '<span style="font-weight:800;color:var(--navy);font-size:1.1rem;padding:6px;text-align:center">' + esc(short(c)) + "</span>";
  };
  var workTile = function (c, src, cap) {
    return '<div class="work reveal in" data-cat="' + esc(c.slug) + '"><img src="' + esc(src) + '" alt="' + esc(c.name) +
      ' social media design" loading="lazy"><div class="ph">' + (I.image || "") + "<b>Design</b><small>" + esc(c.name) + "</small></div>" +
      (cap ? '<span class="cap">' + esc(c.name) + "</span>" : "") + "</div>";
  };

  function applyClients(all) {
    if (!all.length) return;
    var shown = all.filter(function (c) { return c.show_on_clients; });
    var withWork = all.filter(function (c) { return imgs(c).length; });

    $$("[data-cms-medals]").forEach(function (el) {
      el.innerHTML = shown.map(function (c) {
        return '<a class="medal reveal in" href="' + link(c) + '" aria-label="See our work for ' + esc(c.name) + '">' +
          '<span class="tile">' + logoImg(c) + '</span><span class="floor"></span>' +
          '<span class="name">' + esc(short(c)) + '<span class="view">View work →</span></span></a>';
      }).join("");
    });

    $$("[data-cms-marquee]").forEach(function (el) {
      var items = shown.map(function (c) {
        return '<a class="mq-item" href="' + link(c) + '"><span class="mq-tile">' + logoImg(c) + '</span><span class="mq-name">' + esc(short(c)) + "</span></a>";
      }).join("");
      el.innerHTML = items + '<span class="mq-dup" aria-hidden="true">' + items + "</span>";
    });

    var stat = { clients: shown.length, brands: withWork.length,
                 designs: all.reduce(function (n, c) { return n + imgs(c).length; }, 0) };
    $$("[data-cms-stat]").forEach(function (el) {
      var v = stat[el.getAttribute("data-cms-stat")];
      el.setAttribute("data-count", v);
      if (el.textContent !== "0") el.textContent = v;
    });

    $$("[data-cms-featured]").forEach(function (el) {
      el.innerHTML = withWork.slice(0, 8).map(function (c) { return workTile(c, imgs(c)[0], true); }).join("");
    });

    $$("[data-cms-work-chips]").forEach(function (el) {
      el.innerHTML = '<button class="chip active" data-filter="all">All work</button>' + withWork.map(function (c) {
        return '<button class="chip" data-filter="' + esc(c.slug) + '">' + esc(c.name) + "</button>";
      }).join("");
    });
    $$("[data-cms-work]").forEach(function (el) {
      el.innerHTML = withWork.map(function (c) {
        return imgs(c).map(function (src) { return workTile(c, src, true); }).join("");
      }).join("");
    });

    $$("[data-cms-others]").forEach(function (el) {
      var others = withWork.filter(function (c) { return !c.show_on_clients; });
      el.innerHTML = others.map(function (c) {
        return '<a href="social-media.html#brand-' + esc(c.slug) + '">' + esc(c.name) + "</a>";
      }).join("");
      var sec = el.closest("section");
      if (sec) sec.style.display = others.length ? "" : "none";
    });

    var main = document.querySelector("main[data-client]");
    if (main) renderClientPage(main, all, shown);

    if (window.markMissingWork) window.markMissingWork();
    if (window.applyBrandHash) window.applyBrandHash();
  }

  function renderClientPage(main, all, shown) {
    var slug = main.getAttribute("data-client") || new URLSearchParams(location.search).get("c") || "";
    var c = all.find(function (x) { return x.slug === slug; });
    if (!c) { if (!main.getAttribute("data-client")) location.replace("clients.html"); return; }

    var ring = shown.indexOf(c) >= 0 ? shown : all;
    var i = ring.indexOf(c), prev = ring[(i - 1 + ring.length) % ring.length], next = ring[(i + 1) % ring.length];
    var meta = [c.industry, c.location].filter(Boolean).join(" · ");
    var site = safeUrl(c.website);
    var siteLink = site ? '<a class="ch-site" href="' + esc(site) + '"' + BLANK + ">" + esc(site.replace(/^https?:\/\//, "")) + " " + (I.out || "") + "</a>" : "";
    var sub = c.about ? esc(c.about) : "Content and design we've created for " + esc(short(c)) + ".";
    if (siteLink) sub += '<br><span class="ph-site">' + siteLink + "</span>";
    var work = imgs(c);
    var gallery = work.length
      ? '<div class="client-work">' + work.map(function (src) { return workTile(c, src, false); }).join("") + "</div>"
      : '<div class="empty-work reveal in"><div class="ic">' + (I.image || "") + "</div><h3>Work samples coming soon</h3><p>We're preparing a showcase of the content we've made for " + esc(short(c)) + ".</p></div>";
    var tags = (c.services || []).map(function (t) { return "<span>" + esc(t) + "</span>"; }).join("");
    var lightbox = main.querySelector(".lightbox");

    main.innerHTML =
      '<section class="ph" style="--curve:#F5F8FF"><div class="ph-glow" aria-hidden="true"></div><div class="container ph-in">' +
        '<span class="ch-logo">' + logoImg(c) + '</span><span class="ph-pill"><span class="dot"></span>' + (esc(meta) || "Client spotlight") + "</span>" +
        "<h1>" + esc(c.name) + '</h1><p class="lead">' + sub + '</p></div><div class="ph-curve" aria-hidden="true"></div></section>' +
      '<section class="ch-work" id="work"><div class="container"><div class="ch-head"><h2>Work for ' + esc(short(c)) + '</h2><div class="svc-tags small">' + tags + "</div></div>" + gallery + "</div></section>" +
      (ring.length > 1 ? '<section class="section-sm" style="padding-top:0"><div class="container client-nav">' +
        '<a href="' + link(prev) + '">' + logoImg(prev, "") + "<div><small>← Previous client</small><b>" + esc(short(prev)) + "</b></div></a>" +
        '<a class="next" href="' + link(next) + '"><div><small>Next client →</small><b>' + esc(short(next)) + "</b></div>" + logoImg(next, "") + "</a></div></section>" : "");
    if (lightbox) main.appendChild(lightbox);
    document.title = c.name + " | Client Work | PCFIC Virtual Assistance Services";
  }

  get("settings?select=key,value").then(applySettings).catch(function () {});
  get("services?select=*&order=sort_order.asc,created_at.asc").then(applyServices).catch(function () {});
  get("clients?select=*&order=sort_order.asc,created_at.asc").then(applyClients).catch(function () {
    var main = document.querySelector('main[data-client=""]');
    if (main) location.replace("clients.html");
  });
})();
