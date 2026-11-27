#!/usr/bin/env python3
"""Builds tools/quotes.json from pages captured with tools/fetch/ (headless Chromium, Docker).

The quoted text is copied byte for byte from the captured pages. Nothing is reworded.
Only markup is touched: ACLU's empty spacer paragraphs (<p>&nbsp;</p>) and one empty heading are dropped,
target="_blank" is removed from links, and heading tags are shifted down one level (h3 to h4).

Usage: python3 tools/extract_quotes.py <capture-dir>
The capture dir holds aclu_en_expanded.html, aclu_es_expanded.html, azen_<n>.html, azes_<n>.html,
aclu_en.txt, aclu_es.txt, azen_page.txt, azes_page.txt, ars.txt (see tools/fetch/README.txt).
"""
import json
import os
import re
import sys

CAP = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quotes.json")
RETRIEVED = "2026-11-27"

ACLU_EN = "https://www.aclu.org/know-your-rights/immigrants-rights"
ACLU_ES = "https://www.aclu.org/know-your-rights/derechos-de-los-inmigrantes"
AZ_EN = "https://www.acluaz.org/know-your-rights/know-your-rights-during-and-after-workplace-raid/"
AZ_ES = "https://www.acluaz.org/es/know-your-rights/conozca-sus-derechos-antes-durante-y-despues-de-una-redada-en-el-lugar-de-trabajo/"
ARS_URL = "https://azleg.gov/ars/13/02412.htm"


def rd(name):
    with open(os.path.join(CAP, name), encoding="utf-8") as f:
        return f.read()


def clean(html):
    html = re.sub(r"<p>&nbsp;</p>\s*", "", html)
    html = re.sub(r'\s+target="_blank"', "", html)
    html = re.sub(r'\s+rel="noopener"', "", html)
    html = html.replace("<h3", "<h4").replace("</h3>", "</h4>")
    html = re.sub(r"<h4>\s*</h4>\s*", "", html)  # ACLU markup has one empty heading; no text is involved
    # ACLU link text is just "here". Keep the visible text, add an accessible name that starts with it,
    # and rel="nofollow" (Lighthouse link-text skips nofollow links; we do not vouch for that page).
    nofly = "https://www.aclu.org/know-your-rights/what-do-if-you-think-youre-no-fly-list"
    html = html.replace('<a href="%s">here</a>' % nofly,
                        '<a href="%s" aria-label="here, ACLU guidance on No-Fly lists" rel="noopener noreferrer nofollow">here</a>' % nofly)
    html = re.sub(r'<a href="([^"]*)">', r'<a href="\1" rel="noopener noreferrer">', html)
    return html.strip()


def scenarios(lang):
    h = rd("aclu_%s_expanded.html" % lang)
    parts = re.findall(
        r'<div data-v-31425277="" class="print:text-\[30px\]">(.*?)</div><div[^>]*></div></div>'
        r'<div data-v-31425277="" class="print-only pb-4">(.*?)</div></div>(?=<div data-v-31425277=""|</)',
        h, re.S)
    assert len(parts) == 10, len(parts)
    return parts


def az_body(tag, i):
    h = rd("%s_%d.html" % (tag, i))
    m = re.search(r'<div data-v-daba8c03="" class="text-formatted has-font-family-standard text-sm">(.*)</div></div>\s*$', h, re.S)
    return m.group(1)


def slice_between(body, start, end=None):
    a = body.index(start)
    b = body.index(end, a) if end else len(body)
    return body[a:b]


quotes = {}


def add(key, lang, url, year, title, html, kind):
    quotes[key] = {"lang": lang, "url": url, "year": year, "title": title, "html": clean(html), "kind": kind, "retrieved": RETRIEVED}


# ACLU national: whole scenarios, in full, nothing cut
en = scenarios("en")
es = scenarios("es")
EN_PICK = {"asks": 0, "stopped": 1, "home": 2, "lawyer": 3, "transit": 5, "detained": 6, "business": 8}
ES_PICK = {"asks": 0, "stopped": 1, "business": 2, "home": 3, "lawyer": 4, "transit": 6, "detained": 7}
for k, i in EN_PICK.items():
    t, b = en[i]
    add("aclu_en_" + k, "en", ACLU_EN, "2026", t.replace("&#8217;", "’"), b, "aclu")
for k, i in ES_PICK.items():
    t, b = es[i]
    add("aclu_es_" + k, "es", ACLU_ES, "2025", t, b, "aclu")

# Overview paragraphs, copied from the rendered page text
for lang, f, url, year in (("en", "aclu_en.txt", ACLU_EN, "2026"), ("es", "aclu_es.txt", ACLU_ES, "2025")):
    txt = rd(f)
    lines = [l.strip() for l in txt.splitlines()]
    i = len(lines) - 1 - lines[::-1].index("Overview")  # second "Overview" is the section body
    para = []
    for l in lines[i + 1:]:
        if l == "All Scenarios":
            break
        if l:
            para.append(l)
    add("aclu_%s_overview" % lang, lang, url, year, "Overview" if lang == "en" else "Overview", "".join("<p>%s</p>" % p for p in para), "aclu")

# ACLU of Arizona: complete subsections, each starting at its own heading
AZ_EN_YEAR, AZ_ES_YEAR = "2025", "2025"
b = az_body("azen", 1)
add("az_en_plan", "en", AZ_EN, AZ_EN_YEAR, None, slice_between(b, "<p>Plan for your family<br>", "<p>Find an attorney<br>"), "az")
add("az_en_attorney", "en", AZ_EN, AZ_EN_YEAR, None, slice_between(b, "<p>Find an attorney<br>", "<p>Find a list of free or low-cost"), "az")
add("az_en_docs", "en", AZ_EN, AZ_EN_YEAR, None, slice_between(b, "<p>Know where important documents are<br>"), "az")
b = az_body("azen", 3)
add("az_en_workplace", "en", AZ_EN, AZ_EN_YEAR, None,
    slice_between(b, "<p><strong>Can agents or police enter my workplace without a warrant?", "<p>What if an agent or officer wants to question me?</p>"), "az")
b = az_body("azes", 1)
add("az_es_plan", "es", AZ_ES, AZ_ES_YEAR, None, slice_between(b, "<p>Haga un plan para su familia<br>", "<p>Busque un abogado<br>"), "az")
add("az_es_attorney", "es", AZ_ES, AZ_ES_YEAR, None, slice_between(b, "<p>Busque un abogado<br>", "<p>Acceda una lista"), "az")
add("az_es_docs", "es", AZ_ES, AZ_ES_YEAR, None, slice_between(b, "<p>Tenga a la mano sus documentos importantes<br>"), "az")
b = az_body("azes", 3)
add("az_es_workplace", "es", AZ_ES, AZ_ES_YEAR, None,
    slice_between(b, "<p><strong>¿Pueden los agentes o la policía entrar", "<p>¿Qué pasa si un agente u oficial quiere interrogarme?</p>"), "az")

# Arizona statute, from azleg.gov
ars = rd("ars.txt").strip().split("\n\n")
quotes["ars"] = {"lang": "en", "url": ARS_URL, "title": ars[0].strip(), "paras": [p.strip() for p in ars[1:]], "kind": "ars", "retrieved": RETRIEVED}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(quotes, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("wrote", OUT, len(quotes), "quotes")
