# Conoce tus derechos · Arizona

Know your rights and where to get help. A free, ad-free, zero-tracking, Spanish-first page (Spanish and English) for immigrants and families in Arizona, with a focus on Tempe and Phoenix.

Status: private draft. Not published. Planned address once shipped: https://brianallengit.github.io/conoce-tus-derechos-az/

## What is on the page

- Short, plain steps for when immigration agents or police come to the door, stop you in public, stop your car, or come to your work, and what families can do if someone is detained.
- Links to the official ILRC Red Cards (linked on ilrc.org, not copied here).
- Free or low-cost immigration legal help in Arizona, each with a phone number read on the organization's own page.
- A family plan checklist and an important documents list that can be printed.
- A clear note: general information, not legal advice.

## Where the facts come from

Every fact comes from the ACLU, the ACLU of Arizona, the Immigrant Legal Resource Center (ILRC), the U.S. Department of Justice (EOIR), ICE's official detainee locator, or the organization's own page. Each one is linked on the page with the date it was checked (2026-11-27). The full list is in [docs/SOURCES.md](docs/SOURCES.md), including what was looked for and left out because it could not be verified.

Before publishing: have a native Spanish speaker read the Spanish, and have someone who knows immigration law read the steps.

## Privacy promise

- No cookies, no localStorage, no accounts, no forms, no analytics, no ads, no third-party fonts or scripts.
- A strict Content Security Policy blocks every outside request. The page only loads its own HTML, CSS and one small script.
- The language choice lives only in the page address (`?lang=en`).
- Links and phone buttons leave the site. Other sites have their own privacy rules.
- GitHub Pages, the planned host, may keep standard visit logs; the page cannot see or control those, and adds nothing.

## Accessibility

- WCAG 2.2 AA target. axe-core reports 0 violations in Spanish and English at 375px and 1280px.
- No sideways scroll at 320px, 375px or 768px. Large text, one column, tap targets of 56px.
- Works without JavaScript: both languages are shown.
- Screenshots and the audit report are in [docs/screenshots](docs/screenshots).
- Website definition of done: all items checked with evidence in [docs/DEFINITION-OF-DONE.md](docs/DEFINITION-OF-DONE.md). Lighthouse mobile 100/100/100/100.

## Run it

Open `index.html` in a browser. There is nothing to install.

## Change the content

All text, links and phone numbers live in `tools/build.py`. Edit them there, then run:

```
python3 tools/build.py     # rewrites index.html and docs/SOURCES.md
./tools/audit.sh           # axe, overflow check and screenshots, inside Docker only
```

When a fact is checked again, update `CHECKED` in `tools/build.py`.

## Deploy to GitHub Pages (only when the owner says so)

1. Make the repository public.
2. Settings, Pages, Source: "Deploy from a branch", branch `main`, folder `/ (root)`.
3. If the address changes, update `SITE_URL` in `tools/build.py` and rebuild.

## Why

Built to help families who are scared know what to do and who to call. Free forever. A sibling of Fresh Start Resume.

## License

MIT for the code and the page's own wording, see `LICENSE`. The organizations named own their own names, materials and Red Cards; this page is not affiliated with them.
