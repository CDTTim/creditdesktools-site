# Credit Desk Tools: operating brief

Read this first on every run. It is the standing context for anyone (human or Claude) working on this repo.

## What the business is
creditdesktools.com is a free small-business finance calculator site. Each page gives away a working calculator plus a plain-English guide, and earns when visitors want more:
- Excel/Google Sheets templates (Etsy shop CreditDeskTools; Payhip store to be added)
- Affiliate referrals (lending marketplace, accounting software) once approved
- Bookkeeping referrals to Wise Financial Services (wisefinancialsvcs@gmail.com), a related firm

Owner: Tim. He reviews and merges every change. Contact address on the site: hello@creditdesktools.com.

## Audience
Small business owners, bookkeepers and borrowers preparing to talk to a lender. Not finance professionals by default: explain terms the first time they appear.

## Voice
- Plain English, short sentences, specific numbers. Credible lender's perspective, never salesy.
- No hype, no emoji, no "unlock" or "supercharge."
- Never give individualized financial, legal or tax advice. Never imply an offer of credit.
- Avoid current market figures (prime rate, SBA fee percentages, specific lender rates) unless verified that day and dated; they go stale. Prefer "check the current schedule."

## Rules for every page
1. Every calculator shows its formula on the page ("How it's calculated").
2. Every calculator has at least 3 hand-checked test cases in tools/test_calcs.js. Work expected values out by hand or with an independent script, never by running calc.js. `node tools/test_calcs.js` must pass before a pull request.
3. Footer disclaimer and page disclaimer stay on every calculator page.
4. Any page with an affiliate link links to /disclosure/ near the link.
5. The Wise Financial Services box appears only on cash-flow, cost, pricing and month-end pages (`wfs=True`), and follows that firm's brand guide (navy #0F2A4A, gold #B88A3E accent only, Source Serif 4 heading, Inter body). Use the supplied icon file; never redraw it.
6. Credit Desk Tools brand: navy #1F3A5F, deep navy #172A45, gold #E8B04B, Inter.

## How the site is built
- Content: `tools/content.py` (one dict per calculator). Layout: `tools/build.py`. Math: `public/assets/calc.js` (same slug as the content entry).
- Build: `python3 tools/build.py` writes HTML into `public/`. Commit the built files.
- Cloudflare Pages deploys `public/` from the `main` branch. Nothing outside `public/` is published.

## Workflow limits for scheduled runs
- Work on a new branch; open a pull request; never merge, never push to main.
- Never change prices, affiliate links, legal pages (privacy, terms, disclosure) or the Wise Financial box without Tim asking.
- Append one dated line to ops/LOG.md per run.
