# Website definition of done: evidence

Checklist mirrors Brian's website definition of done (vault: `me/working-together/web-definition-of-done.md`). Run on 2026-11-27, inside Docker only (Playwright image, axe-core 4.10.2 and Lighthouse 12.2.1 installed in the throwaway container). Re-run with `./tools/audit.sh` (axe, overflow, screenshots) and `./tools/dod.sh` (icons, tag validation, keyboard, text spacing, forced colors, Lighthouse).

Planned address (not live yet): https://brianallengit.github.io/conoce-tus-derechos-az/

## Language approach (hreflang)

One page, one canonical URL, both languages in the same static HTML. So `es`, `en` and `x-default` alternates all point to the same canonical URL, which is valid (one URL may be declared for several languages). A separate `?lang=en` alternate was rejected: the same file serves both URLs, so the canonical would have to point away from the English one (a conflict that makes Google drop it), and crawlers that do not run JavaScript would see Spanish at both. `?lang=en` still works as a share link for people (the toggle honors it and `app.js` switches title and description), but it is not advertised to search engines. The sitemap carries the same three alternates.

## 1. Accessibility
- [x] axe-core, 0 violations, ES and EN at 375 and 1280 (`docs/screenshots/audit-report.txt`): `axe es 375px: 0 violations, 40 rules passed, 0 incomplete`, same for es 1280, en 375, en 1280. Tags: wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa, best-practice.
- [x] Keyboard: es 77 and en 73 tab stops, 0 without a visible focus indicator, order cycles with no trap, skip link is the first stop (`docs/lighthouse/extra.txt`).
- [x] Headings and landmarks: one visible H1 per language (two in the file, one hidden at a time), `main`, `nav`, `header`, `footer`, labelled sections; no inputs; no meaningful images in the page body (the only image is the link preview).
- [x] Contrast and targets: axe color-contrast passes; overflow check also counts buttons and `.btn` under 44px tall: 0 at 320, 375, 768 (tap targets are 56px).
- [x] `prefers-reduced-motion` (rule added to `style.css`, no animation exists) and `forced-colors` (rules added: language buttons keep a visible pressed state; screenshots `docs/lighthouse/es-forced-colors-375.png`, `en-forced-colors-375.png`). JavaScript off: both languages shown, all 20 panels are in the static HTML.
- [ ] Honest note, what a machine could not verify: real screen reader pass (VoiceOver, TalkBack, NVDA), a native Spanish speaker read, an immigration-law read of the steps, real-device phone testing. All three reads are required before shipping.

## 2. Phone first
- [x] No horizontal scroll and no element past the edge at 320, 375, 768 in ES and EN (`overflow ... OK` lines in the audit report). 1280 is covered by the axe screenshots (`docs/screenshots/*-1280.png`), not by the overflow script. Screenshots: `docs/screenshots/`.
- [x] Readable without zoom (20px base text). 200 percent zoom equivalent (640 css px) has no horizontal scroll; WCAG 1.4.12 text-spacing overrides at 320 and 375 give no overflow (`docs/lighthouse/es-textspacing-320.png`, `en-textspacing-320.png`).

## 3. Languages
- [x] English and Spanish, visible ES/EN switch (button accessible names now "ES, Español" and "EN, English" so the visible label is inside the name), `lang` on `<html>` updates (axe run asserts it), hreflang in the head:
```html
<link rel="canonical" href="https://brianallengit.github.io/conoce-tus-derechos-az/">
<link rel="alternate" hreflang="es" href="https://brianallengit.github.io/conoce-tus-derechos-az/">
<link rel="alternate" hreflang="en" href="https://brianallengit.github.io/conoce-tus-derechos-az/">
<link rel="alternate" hreflang="x-default" href="https://brianallengit.github.io/conoce-tus-derechos-az/">
```

## 4. Search
- [x] Title 55 characters ("Conoce tus derechos en Arizona: qué hacer y ayuda legal"; English version set by `app.js`, 54), meta description 152, canonical, `robots` meta `index,follow,max-image-preview:large` (`docs/lighthouse/validate.txt`).
- [x] `robots.txt` (allows all, names the sitemap) and `sitemap.xml` (the one public page, with es/en/x-default alternates). The page URL is the directory URL GitHub Pages serves without a redirect.
- [x] JSON-LD `@graph` in the head: `Organization` (the project name only; no person, no contact, nothing beyond what the page shows), `WebSite` (inLanguage es and en), `WebPage`. Not added: `FAQPage` and `HowTo` (the page has no real FAQ markup and Google no longer shows HowTo), `BreadcrumbList` (one page). Validated offline by `tools/validate.js`: parses, `@context` is schema.org, required `name`/`url` present on each type, every `@id` reference resolves, name and description equal the visible title and description. Run Google's Rich Results Test and the schema.org validator by hand at ship time.
- [x] Static HTML: everything, including both languages, is in `index.html` (no JavaScript needed to see content).

## 5. Link previews
- [x] Open Graph: `og:title`, `og:description`, `og:type=website`, `og:url`, `og:image` (absolute https, 1200x630 PNG, 66154 bytes), `og:image:type`, `og:image:width/height`, `og:image:alt`, `og:locale=es_US`, `og:locale:alternate=en_US`, `og:site_name`.
- [x] Twitter: `summary_large_image`, `twitter:title`, `twitter:description`, `twitter:image`, `twitter:image:alt`.
- [x] Parsed from the built HTML by `tools/validate.js` (56 checks, all PASS, `docs/lighthouse/validate.txt`). Platform debuggers (Facebook Sharing Debugger, X, LinkedIn Post Inspector, Discord) cannot read a private repo: [ ] run by hand at ship time.

## 6. AI answers
- [x] Plain "what it is, who it is for, how to use it" text at the top of the page (the lead paragraph and "Importante" notice) and the "Sobre esta página" section. A short Q&A block was not added: that would be new content, which was out of scope.
- [x] `llms.txt`: factual summary, who it is for, how to use it, key links and sources, limits. No "best" claims.

## 7. App polish
- [x] Favicon set: `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png` (180), `icon-192.png`, `icon-512.png`; `theme-color` `#0b4f8a`; `manifest.webmanifest` (CSP gained `manifest-src 'self'`).
- [x] Print styles already present (`@media print`, "Imprimir esta página" button, `docs/screenshots/es-print-preview.png`).
- [x] Lighthouse mobile in Docker (`docs/lighthouse/lighthouse.txt`):

| Page | Performance | Accessibility | Best practices | SEO |
|---|---|---|---|---|
| ES `/` | 100 | 100 | 100 | 100 |
| EN `/?lang=en` | 100 | 100 | 100 | 100 |

FCP 1.2 s, LCP 1.2 s, TBT 0 ms, CLS 0 on the simulated mobile profile. Run against a local server, so text compression and cache headers (2 informational findings) depend on GitHub Pages in production.

## 8. Trust and safety
- [x] No cookies, no storage, no analytics, no ads, no third-party requests (audit fails on any external request; 0 seen). Stated on the page and in the footer, including that GitHub Pages may keep visit logs. Strict CSP in a meta tag: `default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; manifest-src 'self'; base-uri 'none'; form-action 'none'`. A CSP meta tag cannot set `frame-ancestors`; GitHub Pages cannot send headers.
- [x] Facts come from the ACLU, ACLU of Arizona, ILRC, DOJ EOIR, ICE's detainee locator or each organization's own page, linked with the checked date 2026-11-27 (`docs/SOURCES.md`). No legal content was changed in this pass.
- [x] No link between Brian's real identity and the clan. The HTML and JSON-LD name no person. Note: the planned host `brianallengit.github.io` contains the GitHub handle, same as Fresh Start Resume, and `LICENSE` in the repo says "Copyright (c) 2026 Brian Allen" (not on the page).

## Still open (by hand, at ship time)
- [ ] Native Spanish speaker read; immigration-law read of the steps; real screen reader pass.
- [ ] Google Rich Results Test and schema.org validator on the live URL; Facebook, X, LinkedIn and Discord link debuggers.
- [ ] Check `/robots.txt`, `/sitemap.xml`, `/llms.txt` and `/manifest.webmanifest` return 200 on the live origin.
