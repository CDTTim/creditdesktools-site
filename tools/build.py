#!/usr/bin/env python3
"""Builds the static site for creditdesktools.com into public/ (the Cloudflare Pages output folder).

Run from the repo root:  python3 tools/build.py
Then test the math:      node tools/test_calcs.js

Pages are plain HTML so Cloudflare Pages serves them with no build step.
Edit content in tools/content.py, layout here, math in assets/calc.js.
"""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import CALCS, GROUPS, TEMPLATES, ETSY_SHOP

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(REPO, "public")  # Cloudflare Pages output directory
SITE = "https://creditdesktools.com"
UPDATED = "2026-11-16"
CONTACT = "hello@creditdesktools.com"
WFS_EMAIL = "wisefinancialsvcs@gmail.com"
BY_SLUG = {c["slug"]: c for c in CALCS}
e = html.escape

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:wght@600&display=swap" rel="stylesheet">')


def layout(path, title, desc, body, schema=None, active=""):
    url = SITE + path
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    def nav(href, label, key, cls=""):
        cur = ' aria-current="page"' if key == active else ""
        c = f' class="{cls}"' if cls else ""
        return f'<a href="{href}"{cur}{c}>{label}</a>'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/icon-512.png">
<meta name="theme-color" content="#1f3a5f">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="/assets/style.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
 <div class="wrap">
  <a class="brand" href="/"><img src="/assets/img/cdt-icon-96.png" alt="" width="36" height="36"><span>Credit Desk <span class="tools">Tools</span></span></a>
  <nav class="nav" aria-label="Main">
   {nav("/#calculators", "Calculators", "calcs")}
   {nav(ETSY_SHOP, "Templates", "tpl", "hide-sm")}
   {nav("/about/", "About", "about", "hide-sm")}
   {nav("/contact/", "Contact", "contact")}
  </nav>
 </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
 <div class="wrap">
  <div>
   <h3>Credit Desk Tools</h3>
   <p>Free small business finance calculators and ready-to-use Excel templates, built by lending and accounting professionals.</p>
   <p>Calculators are for education and planning, not financial, legal or tax advice. © 2026 Credit Desk Tools.</p>
  </div>
  <div>
   <h3>Calculators</h3>
   <ul>
    <li><a href="/business-loan-calculator/">Business loan</a></li>
    <li><a href="/dscr-calculator/">DSCR</a></li>
    <li><a href="/mca-apr-calculator/">MCA true APR</a></li>
    <li><a href="/cash-conversion-cycle-calculator/">Cash conversion cycle</a></li>
    <li><a href="/#calculators">All calculators</a></li>
   </ul>
  </div>
  <div>
   <h3>Company</h3>
   <ul>
    <li><a href="/about/">About</a></li>
    <li><a href="/contact/">Contact</a></li>
    <li><a href="{ETSY_SHOP}">Templates on Etsy</a></li>
    <li><a href="/privacy/">Privacy</a></li>
    <li><a href="/terms/">Terms</a></li>
    <li><a href="/disclosure/">Affiliate disclosure</a></li>
   </ul>
  </div>
 </div>
</footer>
<script src="/assets/calc.js" defer></script>
</body>
</html>
"""


def fmt_default(x):
    if isinstance(x, float) and not x.is_integer():
        return f"{x:,.2f}".rstrip("0").rstrip(".") if x < 1000 else f"{x:,.2f}"
    return f"{int(x):,}"


def field_html(f):
    name, label, pre, suf, default, hint, optional = f
    cls = "input" + (" has-pre" if pre else "") + (" has-suf" if suf else "")
    opt = " data-optional" if optional else ""
    req = "" if optional else " required"
    hint_html = f'<span class="hint">{e(hint)}</span>' if hint else ""
    lab = e(label) + (' <span class="hint" style="display:inline">(optional)</span>' if optional else "")
    return f"""<div class="field">
 <label for="f-{name}">{lab}</label>
 <div class="{cls}">{f'<span class="pre">{pre}</span>' if pre else ''}<input id="f-{name}" name="{name}" type="text" inputmode="decimal" autocomplete="off" value="{fmt_default(default)}"{opt}{req}>{f'<span class="suf">{suf}</span>' if suf else ''}</div>
 {hint_html}
</div>"""


def select_html(s):
    name, label, opts, hint = s
    o = "".join(f'<option value="{v}">{e(t)}</option>' for v, t in opts)
    return f"""<div class="field">
 <label for="f-{name}">{e(label)}</label>
 <div class="input"><select id="f-{name}" name="{name}">{o}</select></div>
 <span class="hint">{e(hint)}</span>
</div>"""


def wfs_box():
    subject = "Bookkeeping%20help%20(via%20Credit%20Desk%20Tools)"
    return f"""<aside class="wfs" aria-label="Bookkeeping help from Wise Financial Services">
 <img src="/assets/img/wise-financial-icon-128.png" alt="Wise Financial Services" width="64" height="64">
 <div>
  <p class="label">Need help with your books?</p>
  <h2>Wise Financial Services</h2>
  <p>Clean monthly books make every number on this page easier to trust. Wise Financial Services handles bookkeeping, reconciliations and month-end close for small businesses.</p>
  <a class="wfs-btn" href="mailto:{WFS_EMAIL}?subject={subject}">Email Wise Financial Services</a>
 </div>
</aside>"""


def calc_page(c):
    slug = c["slug"]
    path = f"/{slug}/"
    fields = "\n".join(field_html(f) for f in c["fields"])
    if c.get("select"):
        fields += "\n" + select_html(c["select"])
    res = "\n".join(
        f'<div class="result {style}"><span>{e(label)}</span><output data-out="{key}">—</output></div>'
        for key, label, style in c["results"])
    table = (f'<h2 style="font-size:20px;margin:6px 0 10px">Yearly amortization schedule</h2>'
             f'<div class="table-wrap"><table class="sched" data-table="{slug}"></table></div>') if c.get("table") else ""
    tname, turl = TEMPLATES[c["template"]]
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in c["faqs"])
    related = "".join(
        f'<a class="card" href="/{r}/"><strong>{e(BY_SLUG[r]["h1"])}</strong><span>{e(BY_SLUG[r]["card"])}</span></a>'
        for r in c["related"])
    body = f"""<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <a href="/#calculators">Calculators</a> › {e(c["h1"])}</nav>
<div class="page-head"><h1>{e(c["h1"])}</h1><p>{e(c["intro"])}</p></div>
<div class="calc">
 <form data-calc="{slug}" novalidate>
{fields}
 </form>
 <div class="results" data-results="{slug}" aria-live="polite">
  <h2>Results</h2>
  <p class="error" data-error hidden></p>
{res}
 </div>
</div>
{table}
<div class="formula"><h2>How it's calculated</h2><code>{e(c["formula"])}</code></div>
<div class="cta"><p><strong>Want the full worksheet?</strong> The {e(tname)} template does this and more in Excel or Google Sheets, with room for your real numbers.</p><a class="btn" href="{turl}" rel="noopener">See the template</a></div>
<article class="article">
{c["guide"].strip()}
<h2>Frequently asked questions</h2>
<div class="faq">{faq_html}</div>
</article>
{wfs_box() if c.get("wfs") else ""}
<section class="related"><h2 style="font-size:20px">Related calculators</h2><div class="cards">{related}</div></section>
<p class="disclaimer">This calculator gives estimates for education and planning. It is not financial, legal or tax advice, and it is not an offer of credit. Actual terms come from your lender or provider. Last reviewed {UPDATED}.</p>
</div>"""
    schema = [
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faqs"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": c["h1"], "item": SITE + path}]},
    ]
    return path, layout(path, c["title"], c["desc"], body, schema, "calcs")


def home():
    groups = ""
    for gname, slugs in GROUPS:
        cards = "".join(
            f'<a class="card" href="/{s}/"><strong>{e(BY_SLUG[s]["h1"])}</strong><span>{e(BY_SLUG[s]["card"])}</span></a>'
            for s in slugs)
        groups += f'<h3 class="group-title">{e(gname)}</h3><div class="cards">{cards}</div>'
    tpl = "".join(f'<a class="card" href="{u}" rel="noopener"><strong>{e(n)}</strong><span>Excel + Google Sheets</span></a>'
                  for n, u in TEMPLATES.values())
    body = f"""<section class="hero"><div class="wrap">
 <p class="eyebrow">Underwriter-built finance tools</p>
 <h1>Know your numbers before the lender does.</h1>
 <p>Free calculators for loan payments, DSCR, financing costs and cash flow, built the way commercial lenders actually run the math.</p>
 <a class="btn" href="#calculators">Browse calculators</a><a class="btn btn-ghost" href="{ETSY_SHOP}" rel="noopener">Excel templates</a>
</div></section>
<section class="section" id="calculators"><div class="wrap">
 <h2>Free calculators</h2>
 <p class="lead">Every calculator shows its formula and works on your phone. No sign-up.</p>
 {groups}
</div></section>
<section class="section band"><div class="wrap">
 <h2>Ready-to-use templates</h2>
 <p class="lead">When a quick calculation isn't enough, these workbooks give you the full analysis with your own data.</p>
 <div class="cards">{tpl}</div>
</div></section>
<section class="section"><div class="wrap"><div class="article">
 <h2>Why these calculators are different</h2>
 <p>Most finance calculators stop at a payment amount. These are built by people who underwrite business loans and close the books, so they answer the questions a lender will ask: whether your cash flow covers the debt, what a factoring or merchant cash advance quote really costs per year, and how long your cash is tied up in inventory and receivables.</p>
 <p>Each page explains the formula in plain English, so you can check the math and use it in your own planning.</p>
</div></div></section>"""
    schema = [{"@context": "https://schema.org", "@type": "WebSite", "name": "Credit Desk Tools", "url": SITE + "/"},
              {"@context": "https://schema.org", "@type": "Organization", "name": "Credit Desk Tools", "url": SITE + "/",
               "logo": SITE + "/assets/img/icon-512.png", "email": CONTACT, "sameAs": [ETSY_SHOP]}]
    return "/", layout("/", "Credit Desk Tools: Free Small Business Finance Calculators",
                       "Free calculators for business loan payments, DSCR, factoring and MCA costs, cash flow and pricing, plus Excel templates built by lending professionals.",
                       body, schema)


def simple(path, title, desc, inner, active=""):
    body = f'<div class="wrap"><div class="page-head" style="padding-top:28px"><h1>{e(title)}</h1></div><div class="article">{inner}</div></div>'
    return path, layout(path, f"{title} | Credit Desk Tools", desc, body, None, active)


def pages():
    out = [home()] + [calc_page(c) for c in CALCS]
    out.append(simple("/about/", "About Credit Desk Tools", "Who builds Credit Desk Tools and why.", f"""
<p>Credit Desk Tools makes free finance calculators and ready-to-use Excel templates for small business owners, bookkeepers and the people who lend to them.</p>
<p>The tools are built by a commercial lending and accounting professional with years of experience underwriting purchase order financing, asset-based loans and working capital deals. Every calculator follows the same math lenders use to size and price loans, and every page shows its formula so you can check it yourself.</p>
<h2>What we believe</h2>
<ul>
 <li><strong>Know your numbers first.</strong> Owners who understand their DSCR, cash cycle and true cost of capital get better terms and avoid expensive mistakes.</li>
 <li><strong>Show the math.</strong> No black boxes. If a number matters, you should be able to see how it was calculated.</li>
 <li><strong>Plain English.</strong> Finance has enough jargon. We explain what each number means and what to do about it.</li>
</ul>
<h2>Templates</h2>
<p>For deeper analysis, our Excel and Google Sheets templates cover loan readiness, 13-week cash flow forecasting, borrowing base certificates, financial statement spreading and more. <a href="{ETSY_SHOP}">Browse the templates</a>.</p>
<h2>Contact</h2>
<p>Questions, corrections or ideas for a new calculator: <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
""", "about"))
    out.append(simple("/contact/", "Contact", "Get in touch with Credit Desk Tools.", f"""
<p>We handle all questions by email and reply within one business day.</p>
<p><a class="btn" href="mailto:{CONTACT}">{CONTACT}</a></p>
<h2>Template help</h2>
<p>Trouble opening or using a template you bought? Email us with the template name and what you're seeing, and we'll help.</p>
<h2>Spotted an error?</h2>
<p>If a calculator gives a result that looks wrong, tell us the inputs you used. Every calculator is tested against hand-checked cases, and we fix confirmed errors quickly.</p>
<p class="disclaimer">We can't give individual financial, legal or tax advice. For advice on your situation, talk to your accountant, attorney or lender.</p>
""", "contact"))
    out.append(simple("/privacy/", "Privacy Policy", "How Credit Desk Tools handles your information.", f"""
<p><em>Last updated {UPDATED}.</em></p>
<h2>Calculator inputs stay in your browser</h2>
<p>Every calculator runs entirely in your web browser. The numbers you type are not sent to us or stored anywhere.</p>
<h2>Analytics</h2>
<p>We use privacy-focused web analytics from Cloudflare to count page views and see which pages are useful. It does not use cookies or track you across other websites.</p>
<h2>Email</h2>
<p>If you email us, we use your address only to reply. If you join our email list, we use your address to send the newsletter, and you can unsubscribe at any time from any email.</p>
<h2>Third-party sites</h2>
<p>Template purchases happen on Etsy or our store provider, and those sites have their own privacy policies. Links to other websites, including any partner or affiliate links, are governed by those sites' policies.</p>
<h2>Contact</h2>
<p>Questions about privacy: <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
"""))
    out.append(simple("/terms/", "Terms of Use", "Terms of use for creditdesktools.com.", f"""
<p><em>Last updated {UPDATED}.</em></p>
<h2>Educational use only</h2>
<p>The calculators, guides and templates on this site are for general education and planning. They are not financial, investment, legal, tax or accounting advice, and they are not an offer or commitment to lend. Results are estimates based on the inputs you provide and simplified assumptions. Actual loan terms, costs and eligibility are set by lenders and providers.</p>
<h2>No warranty</h2>
<p>We work to keep the tools accurate, but the site is provided as is, without warranties of any kind. We are not liable for decisions made or losses incurred based on information from this site. Consult a qualified professional before making financial decisions.</p>
<h2>Content</h2>
<p>The text, calculators and design of this site are owned by Credit Desk Tools. You may use the calculators freely for your own business and share links to any page. Please don't copy the pages or code wholesale.</p>
<h2>Links</h2>
<p>We may link to other websites, including partners and affiliates. We don't control those sites and aren't responsible for their content or offers.</p>
<h2>Changes</h2>
<p>We may update these terms. The date at the top shows the latest version.</p>
<h2>Contact</h2>
<p><a href="mailto:{CONTACT}">{CONTACT}</a></p>
"""))
    out.append(simple("/disclosure/", "Affiliate Disclosure", "How Credit Desk Tools earns money.", f"""
<p>Credit Desk Tools is free to use. We earn money in three ways:</p>
<ul>
 <li><strong>Template sales:</strong> our Excel and Google Sheets templates, sold on Etsy and our own store.</li>
 <li><strong>Affiliate and referral partners:</strong> some links may go to lenders, lending marketplaces or software providers that pay us a commission or referral fee if you sign up or apply. This never changes the price you pay.</li>
 <li><strong>Referrals to related businesses:</strong> some pages mention Wise Financial Services, a bookkeeping firm related to Credit Desk Tools.</li>
</ul>
<p>Our calculators work the same whether or not a partner is involved, and we only recommend products we would consider ourselves. Partner relationships never affect a calculator's results.</p>
<p>Questions: <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
"""))
    p404 = layout("/404.html", "Page not found | Credit Desk Tools", "Page not found.",
                  '<div class="wrap" style="padding:60px 20px"><h1>Page not found</h1><p>That page doesn\'t exist. Try the <a href="/#calculators">full list of calculators</a>.</p></div>')
    return out, p404


def main():
    out, p404 = pages()
    for path, doc in out:
        target = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(doc)
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(p404)
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{UPDATED}</lastmod></url>" for p, _ in out)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"User-agent: *\nAllow: /\n\n\nSitemap: {SITE}/sitemap.xml\n")
    print(f"Built {len(out)} pages + 404")


if __name__ == "__main__":
    main()
