// Header state
const header = document.querySelector('.header');
const onScroll = () => header && header.classList.toggle('solid', window.scrollY > 40);
onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

// Mobile menu
const toggle = document.querySelector('.menu-toggle');
if (toggle) toggle.addEventListener('click', () => {
  document.body.classList.toggle('menu-open');
  toggle.setAttribute('aria-expanded', document.body.classList.contains('menu-open'));
});
document.querySelectorAll('.nav a').forEach(a => a.addEventListener('click', () => document.body.classList.remove('menu-open')));

// Reveal on scroll
const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .12 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Count-up stats
const cio = new IntersectionObserver(es => es.forEach(e => {
  if (!e.isIntersecting) return; cio.unobserve(e.target);
  const el = e.target, end = +el.dataset.count, t0 = performance.now(), dur = 1600;
  const step = t => { const p = Math.min((t - t0) / dur, 1); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
  requestAnimationFrame(step);
}), { threshold: .5 });
document.querySelectorAll('[data-count]').forEach(el => cio.observe(el));

// Generic filter (library + portfolio). Uses event delegation so chips added later also work.
document.addEventListener('click', e => {
  const chip = e.target.closest('[data-filter-group] .chip');
  if (!chip) return;
  const group = chip.closest('[data-filter-group]');
  const target = document.querySelector(group.dataset.filterGroup);
  group.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
  chip.classList.add('active');
  const f = chip.dataset.filter;
  if (target) target.querySelectorAll('[data-cat]').forEach(it => it.classList.toggle('hide', f !== 'all' && it.dataset.cat !== f));
  if (target && LIMITS[target.id]) { target.classList.remove('expanded'); limitGrid(target.id); }
});

// Long grids: show the first few, then a "See more" button
const LIMITS = { lib: [6, 'See more services'], vids: [8, 'See more videos'], work: [12, 'See more designs'] };
window.limitGrid = id => {
  const grid = document.getElementById(id); if (!grid || (id === 'work' && !grid.hasAttribute('data-cms-work'))) return;
  const [n, label] = LIMITS[id];
  let btn = grid.nextElementSibling;
  if (!btn || !btn.classList.contains('lib-more')) {
    btn = document.createElement('div'); btn.className = 'lib-more';
    btn.innerHTML = `<button class="btn btn-primary" type="button">${label}</button>`;
    grid.after(btn);
    btn.querySelector('button').addEventListener('click', () => { grid.classList.add('expanded'); limitGrid(id); });
  }
  const items = [...grid.querySelectorAll('[data-cat]')];
  const shown = items.filter(it => !it.classList.contains('hide'));
  const open = grid.classList.contains('expanded');
  items.forEach(it => it.classList.remove('clip'));
  shown.forEach((it, i) => it.classList.toggle('clip', !open && i >= n));
  btn.hidden = open || shown.length <= n;
};
window.limitLib = () => limitGrid('lib');
Object.keys(LIMITS).forEach(limitGrid);

// Video library: play a Google Drive video in a pop-up
const vm = document.querySelector('.vid-modal');
if (vm) {
  const frame = vm.querySelector('.vid-frame'), cap = vm.querySelector('.vid-cap');
  const close = () => { vm.classList.remove('open'); frame.innerHTML = ''; document.documentElement.classList.remove('vid-lock'); };
  document.addEventListener('click', e => {
    const v = e.target.closest('[data-vid]'); if (!v) return;
    const id = encodeURIComponent(v.dataset.vid);
    frame.innerHTML = `<iframe src="https://drive.google.com/file/d/${id}/preview" allow="autoplay; fullscreen" allowfullscreen title="Video"></iframe>`;
    cap.textContent = v.querySelector('.vid-info')?.innerText.replace(/\n+/, ' · ') || '';
    vm.classList.add('open'); document.documentElement.classList.add('vid-lock');
  });
  vm.querySelector('.vid-close').onclick = close;
  vm.addEventListener('click', e => { if (e.target === vm) close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && vm.classList.contains('open')) close(); });
}

// Portfolio: placeholder when an image is missing (also for images added later)
window.markMissingWork = (root = document) => root.querySelectorAll('.work img').forEach(img => {
  const mark = () => img.closest('.work').classList.add('missing');
  if (img.complete && img.naturalWidth === 0) mark(); else img.addEventListener('error', mark);
});
markMissingWork();

// Lightbox (delegated, works for tiles added later)
const lb = document.querySelector('.lightbox');
if (lb) {
  const lbImg = lb.querySelector('img'); let list = [], idx = 0;
  const show = i => { idx = (i + list.length) % list.length; lbImg.src = list[idx].src; lbImg.alt = list[idx].alt; };
  document.addEventListener('click', e => {
    const w = e.target.closest('.work');
    if (!w || w.classList.contains('missing')) return;
    list = [...document.querySelectorAll('.work:not(.hide):not(.missing) img')];
    show(list.indexOf(w.querySelector('img'))); lb.classList.add('open');
  });
  lb.querySelector('.lb-close').onclick = () => lb.classList.remove('open');
  lb.querySelector('.lb-prev').onclick = e => { e.stopPropagation(); show(idx - 1); };
  lb.querySelector('.lb-next').onclick = e => { e.stopPropagation(); show(idx + 1); };
  lb.addEventListener('click', e => { if (e.target === lb) lb.classList.remove('open'); });
  document.addEventListener('keydown', e => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') lb.classList.remove('open');
    if (e.key === 'ArrowLeft') show(idx - 1);
    if (e.key === 'ArrowRight') show(idx + 1);
  });
}

// WhatsApp check-in form -> opens WhatsApp with a pre-filled message
const form = document.querySelector('#checkin-form');
if (form) form.addEventListener('submit', e => {
  e.preventDefault();
  const d = new FormData(form);
  const services = d.getAll('service').join(', ') || 'Not sure yet';
  const msg = `Hi! I'd like to check in.\n\nName: ${d.get('name')}\nBusiness: ${d.get('business') || '-'}\nEmail: ${d.get('email') || '-'}\nInterested in: ${services}\n\n${d.get('message') || ''}`;
  window.open(`https://wa.me/${form.dataset.wa}?text=${encodeURIComponent(msg)}`, '_blank');
});

document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());

// 3D tilt on logo medallions (delegated)
if (matchMedia('(hover:hover)').matches) {
  document.addEventListener('mousemove', e => {
    const m = e.target.closest && e.target.closest('.medal'); if (!m) return;
    const t = m.querySelector('.tile'); if (!t) return;
    const r = t.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
    t.style.transform = `rotateY(${x * 22}deg) rotateX(${-y * 22}deg) translateY(-4px)`;
  });
  document.addEventListener('mouseout', e => {
    const m = e.target.closest && e.target.closest('.medal');
    if (m && !m.contains(e.relatedTarget)) { const t = m.querySelector('.tile'); if (t) t.style.transform = ''; }
  });
}

// Deep-link a brand filter on the portfolio: portfolio.html#brand-hsp
window.applyBrandHash = () => {
  const h = location.hash.replace('#', '');
  if (!h.startsWith('brand-')) return;
  const chip = document.querySelector(`.chip[data-filter="${h.slice(6)}"]`);
  if (chip) { chip.click(); document.querySelector('#portfolio')?.scrollIntoView({ behavior: 'smooth' }); }
};
applyBrandHash(); window.addEventListener('hashchange', applyBrandHash);

// Deep-link a service group in the library: services.html#svc-creative
window.applySvcHash = () => {
  const h = location.hash.replace('#', '');
  if (!h.startsWith('svc-')) return;
  const chip = document.querySelector(`[data-filter-group="#lib"] .chip[data-filter="${h.slice(4)}"]`);
  if (chip) { chip.click(); document.querySelector('#lib')?.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
};
applySvcHash(); window.addEventListener('hashchange', applySvcHash);

/* Founder avatars: show the icon until the photo file exists */
document.querySelectorAll('.f2-av').forEach(function(img){
  function miss(){ img.setAttribute('data-missing',''); }
  if (img.complete && img.naturalWidth === 0) miss(); else img.addEventListener('error', miss);
});

// Video thumbnails: our saved frame first, then Google Drive's own thumbnail, then a plain colour tile
document.addEventListener('error', e => {
  const img = e.target;
  if (!(img instanceof HTMLImageElement) || !img.closest('.vid-thumb')) return;
  const id = img.closest('[data-vid]')?.dataset.vid;
  if (id && !img.dataset.fb) { img.dataset.fb = '1'; img.src = `https://drive.google.com/thumbnail?id=${encodeURIComponent(id)}&sz=w640`; }
  else img.remove();
}, true);
