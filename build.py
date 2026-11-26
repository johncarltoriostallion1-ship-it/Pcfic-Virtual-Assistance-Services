"""Builds the static multi-page site. Edit the CONFIG block, then run:  python build.py"""
import os, html, time
from icons import I

HERE = os.path.dirname(os.path.abspath(__file__))
e = html.escape
V = str(int(time.time()))  # cache-buster: browsers load fresh CSS/JS after every build

# ============================== CONFIG ==============================
BRAND = "PCFIC"                            # short wordmark
BRAND_FULL = "PCFIC Virtual Assistance Services"
TAGLINE = "Virtual Assistance Services"
WA_NUMBER = "16717888712"                   # WhatsApp number, digits only (country code first)
WA_DISPLAY = "+1 (671) 788-8712"
EMAIL = "pcficvaservices@gmail.com"
LOCATION = "Tamuning, Guam"
FB_URL = "https://www.facebook.com/PacificVirtualAssistanceServ"
OWNER_1 = ("Jimmy Barriga", "Co-Founder · Accounting Lead")
OWNER_2 = ("Janna Amarante", "Co-Founder · Creative & Social Lead")

# Clients with logos -> each gets its own page: client-<slug>.html
CLIENTS = [
  dict(slug="hsp", name="Health Services of the Pacific", short="HSP", logo="hsp.png", industry="Healthcare", location="Dededo, Guam",
       about="A Guam medical clinic offering geriatric care, women's health, diabetes care, wound care and immunizations — plus provider home visits, at-home lab draws and medical equipment for homebound patients.",
       services=["Social media content", "Health awareness campaigns", "Graphic design", "Patient-focused copywriting"], website=""),
  dict(slug="career-tech-high", name="Career Tech High Academy Charter School", short="Career Tech High", logo="career-tech-high-badge.png", industry="Education", location="Guam",
       about="A Guam charter school focused on career and technical education — certificate courses taught on-prem, hybrid and face to face, with a proud student-athlete community.",
       services=["Social media content", "Event & sports graphics", "Enrollment campaigns", "Leadership series"], website=""),
  dict(slug="upkey-aesthetics", name="Upkey Aesthetics", short="Upkey Aesthetics", logo="upkey-aesthetics.png", industry="Beauty & Aesthetics", location="Menlo Park, CA",
       about="An aesthetics studio offering salt facials, vitamin B12 + MIC injections, DiolazeXL laser hair removal and Ultherapy non-surgical lifting.",
       services=["Social media content", "Luxury brand design", "Treatment carousels", "Copywriting"], website=""),
  dict(slug="regenerative-research", name="Regenerative Research Institute of Silicon Valley", short="Regenerative Research", logo="regenerative-research.png", industry="Health & Research", location="Silicon Valley, CA",
       about="An institute that educates patients about regenerative medicine — cellular therapy, heart health, sports injury recovery and how the body renews itself.",
       services=["Educational content", "Social media design", "Health awareness posts"], website="https://regenerativeresearchsv.com"),
  dict(slug="adj-auto", name="ADJ Automotive Repair Services, LLC", short="ADJ Automotive", logo="adj-auto.png", industry="Automotive", location="Guam",
       about="An automotive repair shop serving drivers across Guam.",
       services=["Social media content", "Graphic design"], website="https://adjauto.com"),
  dict(slug="24seven", name="24Seven Gym & Sport", short="24Seven Gym", logo="24seven.png", industry="Fitness & Sports", location="",
       about="A gym and sports brand.", services=["Social media content", "Graphic design"], website=""),
  dict(slug="revival-solutions", name="Revival Solutions", short="Revival Solutions", logo="revival.png", industry="Business Services", location="",
       about="A business solutions brand.", services=["Social media content", "Graphic design"], website=""),
  dict(slug="the-light", name="The Light A/C & Electrical Services", short="The Light", logo="the-light.png", industry="A/C & Electrical", location="",
       about="Air-conditioning and electrical services.", services=["Social media content", "Graphic design"], website=""),
  dict(slug="lt", name="LT", short="LT", logo="lt.png", industry="", location="",
       about="", services=["Social media content", "Graphic design"], website=""),
]
# Every brand in the Canva portfolio (assets/img/work/<page>.jpg)
BRANDS = [
  ("guam-essential", "Guam Essential Services", range(1, 6)),
  ("smash-daddys", "Smash Daddy's", range(6, 8)),
  ("cabalen", "Cabalen Fast Food", range(8, 12)),
  ("bezon-buildz", "Bezon Buildz", range(12, 17)),
  ("upkey-aesthetics", "Upkey Aesthetics", range(17, 21)),
  ("regenerative-research", "Regenerative Research", range(21, 25)),
  ("wil-castro", "Wil Castro Campaign", range(25, 29)),
  ("career-tech-high", "Career Tech High", range(29, 33)),
  ("hsp", "HSP", range(33, 38)),
]
FEATURED = [1, 9, 13, 17, 21, 29, 33, 7]   # home page "featured work"
# ====================================================================

WORK = [(slug, name, n) for slug, name, r in BRANDS for n in r]
WORK_BY = {slug: list(r) for slug, name, r in BRANDS}
BRAND_NAME = {slug: name for slug, name, r in BRANDS}
BLANK = 'target="_blank" rel="noopener"'
WA = f"https://wa.me/{WA_NUMBER}?text=" + "Hi%21%20I%27d%20like%20to%20check%20in%20about%20your%20services."
SVC_PAGES = ("accounting.html", "social-media.html")

def header(active):
    links = []
    for href, label in [("index.html", "Home"), ("services.html", "Services"), ("clients.html", "Clients"), ("about.html", "About"), ("contact.html", "Contact")]:
        on = href == active or (href == "services.html" and active in SVC_PAGES) or (href == "clients.html" and active.startswith("client-"))
        cls = ' class="active"' if on else ""
        links.append(f'<a href="{href}"{cls}>{label}</a>')
    return f'''<header class="header">
  <div class="container">
    <a href="index.html" class="brand" aria-label="{BRAND_FULL} home"><span class="brand-logo"><img src="assets/img/logo-pcfic-sm.png" alt="{BRAND} logo"></span><span class="brand-text"><strong>{BRAND}</strong><small>{TAGLINE}</small></span></a>
    <nav class="nav">{''.join(links)}<a class="btn btn-wa" href="{WA}" {BLANK}>{I["wa"]} Check in</a></nav>
    <button class="menu-toggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>'''

def footer():
    return f'''<section class="cta-band">
  <div class="container">
    <div class="cta-box reveal">
      <div><span class="eyebrow" style="color:#9DBBFF">Let's talk</span><h2>Ready to get your books clean and your brand seen?</h2><p>Send us a quick WhatsApp check-in. A real person replies — usually within the same business day.</p></div>
      <div class="hero-ctas"><a class="btn btn-white btn-wa" href="{WA}" {BLANK}>{I["wa"]} WhatsApp check-in</a><a class="btn btn-ghost" href="services.html">See services {I["arrow"]}</a></div>
    </div>
  </div>
</section>
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a href="index.html" class="brand"><span class="brand-logo"><img src="assets/img/logo-pcfic-sm.png" alt="{BRAND} logo"></span><span class="brand-text"><strong>{BRAND}</strong><small style="color:rgba(255,255,255,.55)">{TAGLINE}</small></span></a>
        <p>Accounting, social media and digital marketing support for businesses across Guam and the Pacific — so owners can focus on running the business.</p>
        <div class="socials"><a href="{FB_URL}" {BLANK} aria-label="Facebook" data-cms-fb>{I["fb"]}</a><a href="{WA}" {BLANK} aria-label="WhatsApp">{I["wa"]}</a></div>
      </div>
      <div><h4>Services</h4><ul><li><a href="accounting.html">Accounting Services</a></li><li><a href="social-media.html">Social Media Services</a></li><li><a href="services.html">Service Library</a></li><li><a href="social-media.html#portfolio">Our Work</a></li></ul></div>
      <div><h4>Company</h4><ul><li><a href="about.html">About Us</a></li><li><a href="clients.html">Our Clients</a></li><li><a href="contact.html">Contact</a></li></ul></div>
      <div><h4>Get in touch</h4><ul><li><a href="{WA}" {BLANK}>WhatsApp: <span data-cms="whatsapp_display">{WA_DISPLAY}</span></a></li><li><a href="mailto:{EMAIL}" data-cms-mail><span data-cms="email">{EMAIL}</span></a></li><li>{LOCATION}</li></ul></div>
    </div>
    <div class="footer-partner" data-cms-partners hidden></div>
    <div class="footer-bottom"><span>© <span data-year></span> {BRAND_FULL}. All rights reserved.</span><span>Serving Guam & the Pacific</span></div>
  </div>
</footer>
<a class="wa-float" href="{WA}" {BLANK} aria-label="WhatsApp check-in"><span class="bubble">Check in with us on WhatsApp</span><span class="btn-round">{I["wa"]}</span></a>'''

LIGHTBOX = f'<div class="lightbox" aria-hidden="true"><button class="lb-close" aria-label="Close">{I["close"]}</button><button class="lb-prev" aria-label="Previous">{I["left"]}</button><img alt=""><button class="lb-next" aria-label="Next">{I["right"]}</button></div>'

def page(fname, title, desc, body, main_attr=""):
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="assets/img/hero-guam.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400;1,800&display=swap" rel="stylesheet">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="stylesheet" href="assets/css/style.css?v={V}">
</head>
<body>
{header(fname)}
<main{main_attr}>
{body}
</main>
{footer()}
<script src="assets/js/main.js?v={V}"></script>
<script src="assets/js/icons.js?v={V}"></script>
<script src="assets/js/cms-config.js?v={V}"></script>
<script src="assets/js/content.js?v={V}"></script>
</body>
</html>'''
    with open(os.path.join(HERE, fname), "w", encoding="utf-8") as f:
        f.write(doc)

import random as _r
def particles(n=34, seed=7):
    _r.seed(seed)
    return "".join(f'<i style="left:{_r.uniform(0,100):.1f}%;top:{_r.uniform(0,100):.1f}%;--s:{_r.uniform(2,5):.1f}px;--d:{_r.uniform(5,12):.1f}s;--dl:-{_r.uniform(0,10):.1f}s"></i>' for _ in range(n))

def page_hero(crumb, eyebrow, h1, lead, ctas=True, curve="#fff", extra=""):
    c = f'<div class="hero-ctas"><a class="btn btn-primary btn-wa" href="{WA}" {BLANK}>{I["wa"]} WhatsApp check-in</a></div>' if ctas else ""
    return f'''<section class="ph" style="--curve:{curve}">
  <div class="ph-glow" aria-hidden="true"></div>
  <div class="container ph-in">
    {extra}<span class="ph-pill"><span class="dot"></span>{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>{c}
  </div>
  <div class="ph-curve" aria-hidden="true"></div>
</section>'''

def medal(c, big=False, link=True):
    inner = f'<span class="tile"><img src="assets/img/clients/{c["logo"]}" alt="{e(c["name"])} logo"></span><span class="floor"></span>'
    if big:
        return f'<div class="medal">{inner}</div>'
    return f'''<a class="medal reveal" href="client-{c["slug"]}.html" aria-label="See our work for {e(c["name"])}">{inner}
      <span class="name">{e(c["short"])}<span class="view">View work →</span></span></a>'''

def work_tile(slug, n, cap=True):
    name = BRAND_NAME[slug]
    return f'''<div class="work reveal" data-cat="{slug}"><img src="assets/img/work/{n}.jpg" alt="{e(name)} social media design" loading="lazy">
  <div class="ph">{I["image"]}<b>Design {n}</b><small>{e(name)}</small></div>{f'<span class="cap">{e(name)}</span>' if cap else ''}</div>'''

PROOF = f'''<section class="proof">
  <div class="container center">
    <span class="eyebrow reveal">Our clients</span>
    <h2 class="reveal d1">Trusted by businesses <b>across Guam.</b></h2>
    <p class="lead reveal d2">Clinics, schools, studios and service brands — tap any logo to see the work we've created for them.</p>
    <div class="medals" data-cms-medals>{''.join(medal(c) for c in CLIENTS)}</div>
    <p class="proof-note reveal">Real clients · Real work · Locally made</p>
  </div>
</section>'''

SVC_CARDS = f'''<div class="svc-grid three">
  <a href="accounting.html" class="svc-card reveal">
    <span class="num">01</span><div class="ic">{I["calc"]}</div>
    <h3>Accounting Services</h3>
    <p>Clean books, on-time payroll and reports you can actually read — so every decision is backed by real numbers.</p>
    <ul data-svc-list="accounting"><li>Bookkeeping</li><li>Payroll</li><li>Financial statements</li><li>Tax-ready records</li><li>Accounts payable & receivable</li><li>Software setup</li></ul>
    <span class="btn btn-primary">Explore accounting {I["arrow"]}</span>
  </a>
  <a href="social-media.html" class="svc-card dark reveal d2">
    <span class="num">02</span><div class="ic">{I["social"]}</div>
    <h3>Social Media Services</h3>
    <p>Scroll-stopping content, consistent posting and ads that bring real customers through your door.</p>
    <ul data-svc-list="social"><li>Content calendar</li><li>Graphic design</li><li>Copywriting</li><li>Page management</li><li>Paid ads</li><li>Monthly reports</li></ul>
    <span class="btn btn-white">Explore social media {I["arrow"]}</span>
  </a>
  <a href="services.html#svc-creative" class="svc-card reveal d3">
    <span class="num">03</span><div class="ic">{I["web"]}</div>
    <h3>Web &amp; Creative</h3>
    <p>Websites, logos and videos that make your brand look professional everywhere customers find you.</p>
    <ul data-svc-list="creative"><li>Website development</li><li>Professional logo design</li><li>Video editing</li></ul>
    <span class="btn btn-primary">See web &amp; creative {I["arrow"]}</span>
  </a>
</div>'''

def owners_block(full=False):
    btn = '' if full else f'<a class="btn btn-primary" href="about.html">Our story {I["arrow"]}</a>'
    return f'''<div class="founders2">
  <div class="f2-text reveal">
    <span class="eyebrow">Meet the founders</span>
    <h2>Two specialists. <span class="text-blue">One team</span> behind your business.</h2>
    <p class="lead">One of us keeps your numbers accurate. The other makes sure the right people see your brand. Together we cover the two things most owners never have time for.</p>
    <div class="f2-people">
      <div class="f2-p"><img class="f2-av" src="assets/img/founder-jimmy.jpg" alt="{OWNER_1[0]}"><span class="f2-ic">{I["calc"]}</span><div><b>{OWNER_1[0]}</b><small>{OWNER_1[1]}</small></div></div>
      <div class="f2-p"><img class="f2-av" src="assets/img/founder-janna.jpg" alt="{OWNER_2[0]}"><span class="f2-ic">{I["social"]}</span><div><b>{OWNER_2[0]}</b><small>{OWNER_2[1]}</small></div></div>
    </div>
    {btn}
  </div>
  <figure class="f2-photo reveal d2">
    <img src="assets/img/owners.jpg" alt="The founders of {BRAND_FULL}">
    <span class="f-chip">{I["heart"]} Locally owned · Guam</span>
  </figure>
</div>'''

def logo_marquee():
    items = "".join(f'''<a class="mq-item" href="client-{c["slug"]}.html"><span class="mq-tile"><img src="assets/img/clients/{c["logo"]}" alt="{e(c["name"])} logo" loading="lazy"></span><span class="mq-name">{e(c["short"])}</span></a>''' for c in CLIENTS)
    return f'''<section class="logo-band" id="work-band" aria-label="Our clients">
  <div class="container center"><p class="mq-caption">Trusted by clinics, schools and growing brands across Guam</p></div>
  <div class="mq"><div class="mq-track" data-cms-marquee>{items}<span class="mq-dup" aria-hidden="true">{items}</span></div></div>
</section>'''

def brand_of(n):
    for slug, name, r in BRANDS:
        if n in r: return slug

# ------------------------------- HOME -------------------------------
home = f'''<section class="hero">
  <div class="hero-bg"></div><div class="hero-glow" aria-hidden="true"></div>
  <div class="container">
    <div class="hero-main">
      <div class="seal reveal" aria-hidden="true">
        <svg viewBox="0 0 200 200" class="seal-ring"><defs><path id="sealpath" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>
          <circle cx="100" cy="100" r="96" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="1"/>
          <circle cx="100" cy="100" r="62" fill="none" stroke="rgba(255,255,255,.25)" stroke-width="1"/>
          <text><textPath href="#sealpath" textLength="480">{BRAND} · VIRTUAL ASSISTANCE SERVICES · GUAM ·</textPath></text></svg>
        <span class="seal-mark"><img src="assets/img/logo-pcfic.png" alt=""></span>
      </div>
      <h1 class="reveal d1"><span data-cms="hero_line1">Clean books.</span><span data-cms="hero_line2">Bold brands.</span><span class="accent" data-cms="hero_line3">Island grown.</span></h1>
      <p class="lead reveal d2" data-cms="hero_lead">Guam's locally owned accounting and social media team. <br>Bookkeeping, payroll and content that brings customers in.</p>
      <div class="hero-ctas reveal d3">
        <a class="btn btn-primary btn-wa" href="{WA}" {BLANK}>{I["wa"]} WhatsApp check-in</a>
        <a class="text-link" href="clients.html">See our clients {I["arrow"]}</a>
      </div>
    </div>
  </div>
  <a class="scroll-cue" href="#work-band" aria-label="Scroll down"></a>
</section>
{logo_marquee()}
<div data-cms-partner-band></div>
<section class="bg-sky">
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">What we do</span><h2>Two services. <span class="text-blue">One partner.</span></h2><p class="lead">Most small businesses juggle an accountant, a designer and a page manager. We bring it under one roof.</p></div>
    {SVC_CARDS}
  </div>
</section>
<div id="clients">{PROOF}</div>
<section class="stats section-sm">
  <div class="container stats-grid">
    <div class="stat reveal"><b><span data-count="{len(CLIENTS)}" data-cms-stat="clients">0</span><em>+</em></b><span class="lbl">Business clients</span></div>
    <div class="stat reveal d1"><b><span data-count="{len(WORK)}" data-cms-stat="designs">0</span><em>+</em></b><span class="lbl">Social designs delivered</span></div>
    <div class="stat reveal d2"><b><span data-count="{len(BRANDS)}" data-cms-stat="brands">0</span></b><span class="lbl">Brands in our portfolio</span></div>
    <div class="stat reveal d3"><b><span data-count="3">0</span></b><span class="lbl">Service areas, one team</span></div>
  </div>
</section>
<section>
  <div class="container">
    <div class="section-head reveal" style="display:flex;justify-content:space-between;align-items:end;gap:30px;flex-wrap:wrap">
      <div><span class="eyebrow">Featured work</span><h2>Content made for real brands</h2></div>
      <a class="btn btn-outline" href="social-media.html#portfolio">View full portfolio {I["arrow"]}</a>
    </div>
    <div class="feat-work" data-cms-featured>{''.join(work_tile(brand_of(n), n) for n in FEATURED)}</div>
  </div>
</section>
<section class="fb-band">
  <div class="container fb-grid">
    <div class="fb-text reveal">
      <span class="eyebrow">Follow us</span>
      <h2>Fresh from our <span class="text-blue">Facebook page.</span></h2>
      <p class="lead">Helping brands grow with smart ads, strong visuals and real results. See our latest posts, tips and client work as soon as we publish them.</p>
      <ul class="fb-points">
        <li>{I["social"]} Social media management</li>
        <li>{I["target"]} Facebook ads management</li>
        <li>{I["web"]} Website development</li>
        <li>{I["pen"]} Professional logo design</li>
        <li>{I["video"]} Video editing</li>
      </ul>
      <a class="btn btn-primary" href="{FB_URL}" {BLANK} data-cms-fb-link>{I["fb"]} Follow us on Facebook</a>
    </div>
    <div class="fb-frame reveal d2">
      <iframe title="PCFIC on Facebook" loading="lazy" allow="encrypted-media" data-fb-embed
        src="https://www.facebook.com/plugins/page.php?href={FB_URL.replace(':', '%3A').replace('/', '%2F')}&amp;tabs=timeline&amp;width=500&amp;height=640&amp;small_header=true&amp;adapt_container_width=true&amp;hide_cover=false&amp;show_facepile=false"></iframe>
    </div>
  </div>
</section>
<section class="bg-sky">
  <div class="container">{owners_block()}</div>
</section>
<section>
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">How it works</span><h2>Getting started is simple</h2></div>
    <div class="steps">
      <div class="step reveal"><h3>Check in on WhatsApp</h3><p>Tell us what you need. No forms, no waiting on hold.</p></div>
      <div class="step reveal d1"><h3>Free discovery call</h3><p>We learn your business, goals and current setup.</p></div>
      <div class="step reveal d2"><h3>Clear proposal</h3><p>A simple plan and a fixed monthly fee. No surprises.</p></div>
      <div class="step reveal d3"><h3>We get to work</h3><p>Regular updates and reports so you always know where things stand.</p></div>
    </div>
  </div>
</section>
{LIGHTBOX}'''
page("index.html", f"{BRAND_FULL} | Accounting & Social Media Services in Guam",
     "Bookkeeping, payroll and social media management for businesses in Guam. Check in with us on WhatsApp.", home)

# ------------------------------- SERVICE LIBRARY -------------------------------
LIB = [
 ("accounting", "Accounting", "Monthly Bookkeeping", "Every transaction recorded, categorized and reconciled against your bank each month."),
 ("accounting", "Accounting", "Payroll Processing", "Accurate, on-time payroll with pay stubs and the records you need for filings."),
 ("accounting", "Accounting", "Financial Statements", "Profit & loss, balance sheet and cash flow — explained in plain language."),
 ("accounting", "Accounting", "Tax-Ready Records", "Organized books and documents so tax season is fast and stress-free for your CPA."),
 ("accounting", "Accounting", "Payables & Receivables", "Bills paid on time, invoices sent and followed up so cash keeps flowing."),
 ("accounting", "Accounting", "Software Setup & Clean-up", "Set up or untangle your accounting software and catch up on past months."),
 ("social", "Social Media", "Content Calendar", "A month of planned posts aligned with your promos, seasons and goals."),
 ("social", "Social Media", "Graphic Design", "On-brand posts, flyers and carousels designed to stop the scroll."),
 ("social", "Social Media", "Copywriting & Captions", "Captions and calls-to-action written to get comments, clicks and calls."),
 ("social", "Social Media", "Page Management", "Consistent posting plus replies to comments and messages on your pages."),
 ("social", "Social Media", "Paid Ads", "Targeted Facebook & Instagram ads that reach customers in Guam."),
 ("social", "Social Media", "Monthly Reports", "Reach, engagement and leads — what worked and what we'll do next."),
 ("creative", "Web & Creative", "Website Development", "Fast, mobile-friendly websites that turn visitors into inquiries and bookings."),
 ("creative", "Web & Creative", "Professional Logo Design", "A clean, memorable logo and brand look that makes your business stand out."),
 ("creative", "Web & Creative", "Video Editing", "Short videos and reels edited for Facebook, Instagram and TikTok."),
]
SVC_HREF = {"accounting": "accounting.html", "social": "social-media.html", "creative": "contact.html"}
lib_items = "".join(f'''<a class="lib-item reveal" data-cat="{c}" href="{SVC_HREF[c]}">
  <span class="tag">{e(t)}</span><h3>{e(h)}</h3><p>{p}</p><span class="more">Learn more {I["arrow"]}</span></a>''' for c, t, h, p in LIB)
services = f'''{page_hero('<span>Services</span>', 'Service library', 'Everything we do, <em>in one place.</em>', 'Browse our full library of accounting, social media, web and creative services. Each one can stand alone or be bundled into a monthly plan.')}
<section><div class="container">{SVC_CARDS}</div></section>
<section class="bg-sky">
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">The library</span><h2>Browse by service</h2></div>
    <div class="lib-filter" data-filter-group="#lib"><button class="chip active" data-filter="all">All services</button><button class="chip" data-filter="accounting">Accounting</button><button class="chip" data-filter="social">Social Media</button><button class="chip" data-filter="creative">Web &amp; Creative</button></div>
    <div class="lib-grid" id="lib" data-svc-lib>{lib_items}</div>
  </div>
</section>
<section>
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">Better together</span><h2>Why bundle both services?</h2></div>
    <div class="feat-grid">
      <div class="feat reveal"><div class="ic">{I["users"]}</div><h3>One point of contact</h3><p>One team, one WhatsApp thread. No chasing three different vendors.</p></div>
      <div class="feat reveal d1"><div class="ic">{I["chart"]}</div><h3>Marketing tied to numbers</h3><p>We see what your ads spend and what they bring in — so budget goes where it works.</p></div>
      <div class="feat reveal d2"><div class="ic">{I["card"]}</div><h3>One simple monthly fee</h3><p>Bundled plans cost less than hiring each service separately.</p></div>
    </div>
  </div>
</section>'''
page("services.html", f"Service Library | {BRAND_FULL}", "Accounting and social media services for Guam businesses.", services)

# ------------------------------- ACCOUNTING -------------------------------
acct = f'''{page_hero('<a href="services.html">Services</a><span>/</span><span>Accounting</span>', 'Accounting services', 'Clean books. Clear numbers. <em>Zero stress.</em>', 'We keep your records accurate and up to date every month — so you always know where your money is going, and tax season is never a scramble.')}
<section>
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">What's included</span><h2>Everything your books need</h2></div>
    <div class="feat-grid" data-svc-feat="accounting">
      <div class="feat reveal"><div class="ic">{I["book"]}</div><h3>Monthly Bookkeeping</h3><p>Transactions recorded, categorized and reconciled with your bank and card statements.</p></div>
      <div class="feat reveal d1"><div class="ic">{I["users"]}</div><h3>Payroll Processing</h3><p>Employees paid correctly and on time, with pay stubs and payroll records kept in order.</p></div>
      <div class="feat reveal d2"><div class="ic">{I["chart"]}</div><h3>Financial Statements</h3><p>Monthly P&L, balance sheet and cash flow — with a short summary of what they mean.</p></div>
      <div class="feat reveal"><div class="ic">{I["file"]}</div><h3>Tax-Ready Records</h3><p>Year-round organization so your CPA gets clean, complete books when it's time to file.</p></div>
      <div class="feat reveal d1"><div class="ic">{I["card"]}</div><h3>Payables & Receivables</h3><p>Track bills and invoices, send reminders and keep your cash flow healthy.</p></div>
      <div class="feat reveal d2"><div class="ic">{I["calc"]}</div><h3>Setup & Catch-up</h3><p>Behind on your books? We clean up past months and set you up properly going forward.</p></div>
    </div>
  </div>
</section>
<section class="bg-sky">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Who it's for</span><h2>Built for busy owners, not accountants</h2>
      <ul class="checks">
        <li><span class="tick">{I["check"]}</span><div>Owners doing their own books at night<span>Get your evenings back.</span></div></li>
        <li><span class="tick">{I["check"]}</span><div>Growing teams with payroll to run<span>Pay people right, every time.</span></div></li>
        <li><span class="tick">{I["check"]}</span><div>Businesses months behind on records<span>We catch you up without judgment.</span></div></li>
        <li><span class="tick">{I["check"]}</span><div>Anyone applying for a loan or grant<span>Lenders want clean statements — we prepare them.</span></div></li>
      </ul>
      <a class="btn btn-primary btn-wa" href="{WA}" {BLANK}>{I["wa"]} Ask about accounting</a>
    </div>
    <div class="reveal d2">
      <div class="steps" style="grid-template-columns:1fr 1fr">
        <div class="step"><h3>Check in</h3><p>Message us on WhatsApp.</p></div>
        <div class="step"><h3>Review</h3><p>We look at your current books.</p></div>
        <div class="step"><h3>Plan</h3><p>Fixed monthly fee, clear scope.</p></div>
        <div class="step"><h3>Monthly close</h3><p>Reports in your inbox every month.</p></div>
      </div>
    </div>
  </div>
</section>
<section>
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">FAQ</span><h2>Common questions</h2></div>
    <div class="faq reveal">
      <details><summary>Do I need to be in Guam to work with you?</summary><p>No. Most of the work happens online. We're based in Guam, but we can support businesses anywhere in the Pacific.</p></details>
      <details><summary>What software do you use?</summary><p>We work with the major cloud accounting platforms and can set one up if you don't have one yet.</p></details>
      <details><summary>How do I send you receipts and statements?</summary><p>Through a shared folder or straight on WhatsApp — whatever is easiest for you. We'll organize it from there.</p></details>
      <details><summary>Do you file taxes?</summary><p>We keep your records tax-ready all year and work alongside your CPA. Message us to discuss what your business needs.</p></details>
      <details><summary>How is pricing set?</summary><p>A fixed monthly fee based on transaction volume and services included. You'll know the price before we start.</p></details>
    </div>
  </div>
</section>'''
page("accounting.html", f"Accounting Services in Guam | {BRAND_FULL}", "Bookkeeping, payroll, financial statements and tax-ready records for Guam businesses.", acct)

# ------------------------------- SOCIAL MEDIA -------------------------------
chips = '<button class="chip active" data-filter="all">All work</button>' + "".join(f'<button class="chip" data-filter="{slug}">{e(name)}</button>' for slug, name, r in BRANDS)
social = f'''{page_hero('<a href="services.html">Services</a><span>/</span><span>Social Media</span>', 'Social media services', 'Content that stops the scroll — and <em>brings in customers.</em>', 'We plan, design, write and post for you, then run the ads that turn followers into paying customers.')}
<section>
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">What's included</span><h2>Your full social media team</h2></div>
    <div class="feat-grid" data-svc-feat="social">
      <div class="feat reveal"><div class="ic">{I["cal"]}</div><h3>Content Calendar</h3><p>A month of posts planned around your promos, events and seasons.</p></div>
      <div class="feat reveal d1"><div class="ic">{I["pen"]}</div><h3>Graphic Design</h3><p>On-brand posts, carousels and flyers — see real examples below.</p></div>
      <div class="feat reveal d2"><div class="ic">{I["file"]}</div><h3>Copywriting</h3><p>Captions and calls-to-action written to get comments, clicks and calls.</p></div>
      <div class="feat reveal"><div class="ic">{I["social"]}</div><h3>Page Management</h3><p>Consistent posting and replies to comments and messages.</p></div>
      <div class="feat reveal d1"><div class="ic">{I["target"]}</div><h3>Paid Ads</h3><p>Facebook & Instagram ads targeted to the customers you want in Guam.</p></div>
      <div class="feat reveal d2"><div class="ic">{I["chart"]}</div><h3>Monthly Reports</h3><p>Reach, engagement and leads — and what we'll improve next month.</p></div>
    </div>
  </div>
</section>
<section class="bg-sky" id="portfolio">
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">Our work</span><h2>Designs we've made for real clients</h2><p class="lead">Filter by brand. Tap any design to view it larger.</p></div>
    <div class="lib-filter" data-filter-group="#work" data-cms-work-chips>{chips}</div>
    <div class="work-grid" id="work" data-cms-work>{''.join(work_tile(s, n) for s, name, n in WORK)}</div>
  </div>
</section>
<section>
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">FAQ</span><h2>Common questions</h2></div>
    <div class="faq reveal">
      <details><summary>Which platforms do you manage?</summary><p>Mainly Facebook and Instagram, plus TikTok and LinkedIn when they fit your audience.</p></details>
      <details><summary>Do I get to approve posts first?</summary><p>Yes. You'll see each month's content before anything goes live.</p></details>
      <details><summary>Is the ad budget included?</summary><p>Our fee covers managing the ads. The ad spend itself is paid directly to the platform, so you stay in control of it.</p></details>
      <details><summary>How many posts do I get per month?</summary><p>It depends on the plan. Message us and we'll recommend a posting schedule that fits your goals and budget.</p></details>
    </div>
  </div>
</section>
{LIGHTBOX}'''
page("social-media.html", f"Social Media Services in Guam | {BRAND_FULL}", "Social media content, design, page management and ads for Guam businesses.", social)

# ------------------------------- CLIENTS -------------------------------
logo_slugs = {c["slug"] for c in CLIENTS}
others = "".join(f'<a href="social-media.html#brand-{slug}">{e(name)}</a>' for slug, name, r in BRANDS if slug not in logo_slugs)
cl = "".join(f'''<a class="client reveal{' d'+str(i%3) if i%3 else ''}" href="client-{c['slug']}.html">
  <div class="logo"><img src="assets/img/clients/{c['logo']}" alt="{e(c['name'])} logo" loading="lazy"></div>
  <div class="body"><div><h3>{e(c['name'])}</h3><small>{e(c['industry'] or 'View work')}</small></div><span class="go">{I["arrow"]}</span></div></a>''' for i, c in enumerate(CLIENTS))
clients = f'''{page_hero('<span>Clients</span>', 'Our clients', "Businesses we're <em>proud to work with.</em>", 'Clinics, schools, studios and service brands. Tap a client to see what they do and the work we created for them.', ctas=False)}
{PROOF.replace('<span class="eyebrow reveal">Our clients</span>','').replace('<p class="lead reveal d2">Clinics, schools, studios and service brands — tap any logo to see the work we\'ve created for them.</p>','<p class="lead reveal d2">Tap any logo to see the work.</p>').replace('class="proof"','class="proof proof-page"')}
<section class="bg-sky section-sm">
  <div class="container center">
    <span class="eyebrow reveal">More from our portfolio</span>
    <h2 class="reveal">Other brands we've designed for</h2>
    <div class="brand-chips reveal" data-cms-others>{others}</div>
  </div>
</section>'''
page("clients.html", f"Our Clients | {BRAND_FULL}", "Businesses across Guam that trust us with their accounting and social media.", clients)

# ------------------------------- CLIENT DETAIL PAGES -------------------------------
for i, c in enumerate(CLIENTS):
    prev_c, next_c = CLIENTS[i - 1], CLIENTS[(i + 1) % len(CLIENTS)]
    facts = "".join(f'<span><b>{k}</b>{e(v)}</span>' for k, v in [("Industry", c["industry"]), ("Location", c["location"])] if v)
    if c["website"]:
        facts += f'<span><b>Website</b><a href="{c["website"]}" {BLANK}>{e(c["website"].replace("https://", ""))}</a></span>'
    work = WORK_BY.get(c["slug"], [])
    if work:
        gallery = f'<div class="client-work">{"".join(work_tile(c["slug"], n, cap=False) for n in work)}</div>'
    else:
        gallery = f'''<div class="empty-work reveal"><div class="ic">{I["image"]}</div><h3>Work samples coming soon</h3>
          <p>We're preparing a showcase of the content we've made for {e(c["short"])}.</p></div>'''
    about = e(c["about"]) if c["about"] else f"{e(c['name'])} is one of the businesses we support with content and design."
    site_btn = f'<a class="btn btn-ghost" href="{c["website"]}" {BLANK}>Visit their website {I["out"]}</a>' if c["website"] else ""
    meta = " · ".join(v for v in [c["industry"], c["location"]] if v)
    site_link = f'<a class="ch-site" href="{c["website"]}" {BLANK}>{e(c["website"].replace("https://", ""))} {I["out"]}</a>' if c["website"] else ""
    logo_tile = f'<span class="ch-logo"><img src="assets/img/clients/{c["logo"]}" alt="{e(c["name"])} logo"></span>'
    sub = e(c["about"]) if c["about"] else f"Content and design we've created for {e(c['short'])}."
    if site_link: sub += f'<br><span class="ph-site">{site_link}</span>'
    body = f'''{page_hero("", e(meta) if meta else "Client spotlight", e(c["name"]), sub, ctas=False, curve="#F5F8FF", extra=logo_tile)}
<section class="ch-work" id="work">
  <div class="container">
    <div class="ch-head"><h2>Work for {e(c["short"])}</h2><div class="svc-tags small">{"".join(f"<span>{e(t)}</span>" for t in c["services"])}</div></div>
    {gallery}
  </div>
</section>
<section class="section-sm" style="padding-top:0">
  <div class="container client-nav">
    <a href="client-{prev_c["slug"]}.html"><img src="assets/img/clients/{prev_c["logo"]}" alt=""><div><small>← Previous client</small><b>{e(prev_c["short"])}</b></div></a>
    <a class="next" href="client-{next_c["slug"]}.html"><div><small>Next client →</small><b>{e(next_c["short"])}</b></div><img src="assets/img/clients/{next_c["logo"]}" alt=""></a>
  </div>
</section>
{LIGHTBOX}'''
    page(f"client-{c['slug']}.html", f"{c['name']} | Client Work | {BRAND_FULL}", f"See the content and design work we created for {c['name']}.", body, main_attr=f' data-client="{c["slug"]}"')

# Generic client page for clients added in the admin panel: client.html?c=<slug>
page("client.html", f"Client Work | {BRAND_FULL}", "Content and design work we created for our clients.",
     f'<section class="section"><div class="container center"><p class="lead">Loading…</p></div></section>{LIGHTBOX}', main_attr=' data-client=""')

# ------------------------------- ABOUT -------------------------------
about = f'''{page_hero('<span>About</span>', 'About us', 'A local team that treats your business <em>like our own.</em>', 'We started with one idea: owners should spend their time growing their business, not buried in spreadsheets and posting schedules.', ctas=False)}
<section><div class="container">{owners_block(full=True)}</div></section>
<section class="bg-sky">
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">Our values</span><h2>What you can expect from us</h2></div>
    <div class="feat-grid">
      <div class="feat reveal"><div class="ic">{I["shield"]}</div><h3>Confidential</h3><p>Your financial data stays private and secure. Always.</p></div>
      <div class="feat reveal d1"><div class="ic">{I["clock"]}</div><h3>Responsive</h3><p>Message us on WhatsApp and get a real reply — fast.</p></div>
      <div class="feat reveal d2"><div class="ic">{I["heart"]}</div><h3>Local & personal</h3><p>We know Guam's businesses and community because we're part of it.</p></div>
    </div>
  </div>
</section>'''
page("about.html", f"About Us | {BRAND_FULL}", "Meet the locally owned team behind our accounting and social media services.", about)

# ------------------------------- CONTACT -------------------------------
contact = f'''{page_hero('<span>Contact</span>', 'WhatsApp check-in', "Let's talk about <em>your business.</em>", "Fill in a few details and we'll open WhatsApp with your message ready to send. Or just tap the button and say hi.", ctas=False)}
<section>
  <div class="container contact-grid">
    <div class="wa-card reveal">
      <h3>Prefer to chat directly?</h3>
      <p>Tap below to start a WhatsApp conversation with our team.</p>
      <a class="btn btn-white btn-wa" href="{WA}" {BLANK}>{I["wa"]} Open WhatsApp</a>
      <div class="info">
        <div><span class="ic">{I["wa"]}</span><div><small>WhatsApp</small><b data-cms="whatsapp_display">{WA_DISPLAY}</b></div></div>
        <div><span class="ic">{I["mail"]}</span><div><small>Email</small><b data-cms="email">{EMAIL}</b></div></div>
        <div><span class="ic">{I["pin"]}</span><div><small>Location</small><b>{LOCATION}</b></div></div>
        <div><span class="ic">{I["clock"]}</span><div><small>Hours</small><b>Mon–Fri · 8:00 AM – 5:00 PM ChST</b></div></div>
      </div>
    </div>
    <form class="form-card reveal d2" id="checkin-form" data-wa="{WA_NUMBER}">
      <h3>Quick check-in</h3><p>Takes less than a minute.</p>
      <div class="form-row">
        <div class="field"><label for="name">Your name *</label><input id="name" name="name" required placeholder="Your full name"></div>
        <div class="field"><label for="business">Business name</label><input id="business" name="business" placeholder="Your business"></div>
      </div>
      <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" placeholder="you@business.com"></div>
      <div class="field"><label>I'm interested in</label>
        <div class="opt-group"><label><input type="checkbox" name="service" value="Accounting"><span>Accounting</span></label><label><input type="checkbox" name="service" value="Social Media"><span>Social Media</span></label><label><input type="checkbox" name="service" value="Both"><span>Both</span></label></div>
      </div>
      <div class="field"><label for="message">Message</label><textarea id="message" name="message" placeholder="Tell us a bit about your business and what you need."></textarea></div>
      <button class="btn btn-primary btn-wa" type="submit">{I["wa"]} Send via WhatsApp</button>
      <p class="form-note">Your message opens in WhatsApp — nothing is sent until you tap send.</p>
    </form>
  </div>
</section>'''
page("contact.html", f"Contact | {BRAND_FULL}", "Check in with us on WhatsApp about accounting or social media services.", contact)
print("built", len(CLIENTS), "client pages")
