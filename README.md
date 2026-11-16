# creditdesktools.com

Free small business finance calculators. Static HTML, deployed by Cloudflare Pages.

- `public/` is the website (Cloudflare Pages output directory). Built files are committed.
- `tools/content.py` holds page content; `tools/build.py` generates the HTML; `public/assets/calc.js` holds the calculator math.
- `tools/test_calcs.js` holds hand-checked test cases for every calculator.
- `ops/` holds the operating brief, product catalog, backlog and run log.

## Build and test

```
python3 tools/build.py
node tools/test_calcs.js
```

To preview locally: `cd public && python3 -m http.server 8000`, then open http://localhost:8000.

## Cloudflare Pages settings

- Production branch: `main`
- Framework preset: None
- Build command: (leave empty)
- Build output directory: `public`
