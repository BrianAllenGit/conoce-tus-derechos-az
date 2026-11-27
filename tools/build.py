#!/usr/bin/env python3
"""Builds index.html and docs/SOURCES.md from one list of facts.

Run:  python3 tools/build.py
No dependencies. The output files are committed, so the site itself has no build step.
Every fact people may act on lives in SOURCES or ORGS below, with the page it was read on.
"""
import json
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKED = "2026-11-27"
CHECKED_TXT = {"es": "27 de noviembre de 2026", "en": "November 27, 2026"}
SITE_URL = "https://brianallengit.github.io/conoce-tus-derechos-az/"

# id -> (url, Spanish label, English label, what we took from it)
SOURCES = {
    "aclu": (
        "https://www.aclu.org/know-your-rights/immigrants-rights",
        "ACLU: Derechos de los inmigrantes (en inglés, con versión en español)",
        "ACLU: Know Your Rights, Immigrants' Rights",
        "Quoted word for word, whole scenarios, no edits: overview; law enforcement asks about my immigration status; stopped by police or ICE; "
        "police or ICE at my home; I need a lawyer; stopped in transit; detained while my case is underway; ICE at my place of business with a search warrant or subpoena. "
        "Linked: all other scenarios.",
    ),
    "aclu_es": (
        "https://www.aclu.org/know-your-rights/derechos-de-los-inmigrantes",
        "ACLU: Conozca sus derechos, derechos de los inmigrantes (en español)",
        "ACLU: Know Your Rights, Immigrants' Rights (Spanish version)",
        "Spanish version of the ACLU page, quoted word for word in the Spanish half of this page (the matching scenarios, in ACLU's own Spanish). Linked for all other scenarios.",
    ),
    "acluaz_work": (
        "https://www.acluaz.org/know-your-rights/know-your-rights-during-and-after-workplace-raid/",
        "ACLU de Arizona: Sus derechos antes, durante y después de una redada en el trabajo",
        "ACLU of Arizona: Know Your Rights Before, During, and After a Workplace Raid",
        "Quoted word for word: the \"Plan for your family\", \"Find an attorney\" and \"Know where important documents are\" passages, and the two workplace "
        "questions about entering a workplace and being detained during a search. Linked: the rest of the page.",
    ),
    "acluaz_work_es": (
        "https://www.acluaz.org/es/know-your-rights/conozca-sus-derechos-antes-durante-y-despues-de-una-redada-en-el-lugar-de-trabajo/",
        "ACLU de Arizona: Conozca sus derechos antes, durante y después de una redada en el lugar de trabajo (en español)",
        "ACLU of Arizona: Know Your Rights Before, During, and After a Workplace Raid (Spanish version)",
        "Quoted word for word: the family plan, important documents, finding an attorney, and workplace entry and detention passages, in Spanish.",
    ),
    "ars": (
        "https://azleg.gov/ars/13/02412.htm",
        "Legislatura de Arizona: A.R.S. 13-2412 (en inglés)",
        "Arizona Legislature: A.R.S. 13-2412",
        "The statute on refusing to provide a truthful name when lawfully detained, quoted word for word.",
    ),
    "ilrc_red": (
        "https://www.ilrc.org/red-cards-tarjetas-rojas",
        "ILRC: Tarjetas Rojas (Red Cards)",
        "ILRC: Red Cards / Tarjetas Rojas",
        "Link only. The ILRC allows hyperlinks, so no ILRC text or card artwork is copied here.",
    ),
    "ilrc_red_es": (
        "https://www.ilrc.org/sites/default/files/2025-01/Artwork%20for%20Printing%20Your%20Own%20Red%20Cards%20-%20Spanish.pdf",
        "ILRC: Tarjeta Roja en español para imprimir (PDF en ilrc.org)",
        "ILRC: Printable red card, Spanish (PDF on ilrc.org)",
        "Official printable file. Linked, not rehosted.",
    ),
    "ilrc_red_en": (
        "https://www.ilrc.org/sites/default/files/documents/red_card-self_srv-english.pdf",
        "ILRC: Tarjeta Roja en inglés para imprimir (PDF en ilrc.org)",
        "ILRC: Printable red card, English (PDF on ilrc.org)",
        "Official printable file. Linked, not rehosted.",
    ),
    "ilrc_plan": (
        "https://www.ilrc.org/community-resources/know-your-rights/step-step-family-preparedness-plan",
        "ILRC: Plan de Preparación Familiar paso a paso (inglés y español)",
        "ILRC: Step-by-Step Family Preparedness Plan (English and Spanish)",
        "Link only (full plan). No ILRC text is copied here.",
    ),
    "ilrc_plan_es": (
        "https://www.ilrc.org/community-resources/plan-de-preparaci%C3%B3n-familiar",
        "ILRC: Plan de Preparación Familiar (en español, para descargar)",
        "ILRC: Family Preparedness Plan (Spanish download page)",
        "Spanish family preparedness packet. Linked, not rehosted.",
    ),
    "ice_locator": (
        "https://locator.ice.gov/odls/",
        "ICE: Localizador de personas detenidas (sitio oficial del gobierno)",
        "ICE: Online Detainee Locator System (official government site)",
        "Link only. Official tool to find a person in ICE custody; no description of its inputs is repeated here.",
    ),
    "eoir_phone": (
        "https://www.justice.gov/eoir/customer-service-initiatives",
        "Departamento de Justicia (EOIR): información automática de casos",
        "Department of Justice (EOIR): automated case information",
        "The court information line 1-800-898-7180, in English and Spanish, 24 hours a day, 7 days a week; "
        "it needs the A-number.",
    ),
    "eoir_probono": (
        "https://www.justice.gov/eoir/list-pro-bono-legal-service-providers",
        "Departamento de Justicia (EOIR): lista de proveedores de servicios legales gratuitos",
        "Department of Justice (EOIR): List of Pro Bono Legal Service Providers",
        "Official list by immigration court, including Eloy, Florence, Phoenix and Tucson. EOIR says it does not endorse the organizations.",
    ),
    "eoir_roster": (
        "https://www.justice.gov/eoir/recognition-accreditation-roster-reports",
        "Departamento de Justicia (EOIR): organizaciones reconocidas y representantes acreditados",
        "Department of Justice (EOIR): Recognized Organizations and Accredited Representatives roster",
        "Official roster to check whether a non-lawyer is allowed to represent you.",
    ),
    "ian": (
        "https://www.immigrationadvocates.org/legaldirectory/search?state=AZ",
        "Immigration Advocates Network: directorio de servicios legales en Arizona",
        "Immigration Advocates Network: legal services directory, Arizona",
        "National directory that lists only nonprofits with free or low-cost immigration legal services.",
    ),
    "firrp": (
        "https://firrp.org/getinvolved/contact/",
        "Florence Project: página de contacto",
        "Florence Project: contact page",
        "Phone numbers (520) 777-5600 Tucson and (602) 307-1008 Phoenix; clients are people who are detained; no walk-ins.",
    ),
    "firrp_faq": (
        "https://firrp.org/faq/",
        "Florence Project: preguntas frecuentes",
        "Florence Project: frequently asked questions",
        "The Florence Project does not charge fees; how families can look for a detained person.",
    ),
    "plan": (
        "https://planphx.org/legal-services",
        "Phoenix Legal Action Network (PLAN): servicios legales",
        "Phoenix Legal Action Network (PLAN): legal services",
        "Free representation for non-detained, low-income immigrants in Maricopa County or with cases in the Phoenix Immigration Court.",
    ),
    "plan_contact": (
        "https://planphx.org/contact",
        "Phoenix Legal Action Network (PLAN): contacto",
        "Phoenix Legal Action Network (PLAN): contact",
        "Phone 602-730-1726; office by appointment only.",
    ),
    "fh": (
        "https://friendlyhouse.org/immigration-legal-services/",
        "Friendly House: servicios legales de inmigración",
        "Friendly House: Immigration and Legal Services",
        "Phone 602-416-7200; 802 S. 1st Ave, Suite 1, Phoenix; describes its services as affordable.",
    ),
    "cc": (
        "https://www.catholiccharitiesaz.org/immigration-legal-services",
        "Catholic Charities Community Services: servicios legales de inmigración",
        "Catholic Charities Community Services: Immigration Legal Services",
        "Phones 602-749-4415 and toll-free 855-316-2229; 5151 N. 19th Avenue, Phoenix; deportation defense and asylum listed; "
        "staff includes DOJ accredited representatives.",
    ),
    "irc": (
        "https://www.rescue.org/united-states/phoenix-az",
        "International Rescue Committee (IRC) en Phoenix",
        "International Rescue Committee (IRC) in Phoenix",
        "Phone (602) 433-2440; 4425 West Olive Avenue, Suite 400, Glendale; describes low-cost immigration legal services.",
    ),
    "azlh": (
        "https://www.azlawhelp.org/",
        "AZLawHelp (Arizona Bar Foundation)",
        "AZLawHelp (Arizona Bar Foundation)",
        "Phone 866-637-5341 to check if you qualify for free or reduced fee legal help.",
    ),
}

# Organizations. Every phone number below was read on the organization's own page on CHECKED.
ORGS = [
    {
        "name": "Florence Immigrant & Refugee Rights Project (Florence Project)",
        "es": "Ayuda legal y social gratuita para adultos y niños <strong>detenidos por inmigración en Arizona</strong>. No cobra. "
              "No atiende visitas sin cita: trabaja dentro de los centros de detención.",
        "en": "Free legal and social services for adults and children <strong>detained by immigration in Arizona</strong>. It does not charge fees. "
              "It cannot help walk-in visitors: it works inside the detention centers.",
        "phones": [("(602) 307-1008", "+16023071008", "Phoenix"), ("(520) 777-5600", "+15207775600", "Tucson")],
        "site": "https://firrp.org/",
        "src": ["firrp", "firrp_faq"],
    },
    {
        "name": "Phoenix Legal Action Network (PLAN)",
        "es": "Representación gratuita para inmigrantes de bajos ingresos que <strong>no están detenidos</strong> y viven en el condado de Maricopa "
              "o tienen su caso en la Corte de Inmigración de Phoenix. Atiende solo con cita.",
        "en": "Free representation for low-income immigrants who are <strong>not detained</strong> and live in Maricopa County "
              "or have a case in the Phoenix Immigration Court. By appointment only.",
        "phones": [("602-730-1726", "+16027301726", "")],
        "site": "https://planphx.org/",
        "src": ["plan", "plan_contact"],
    },
    {
        "name": "Friendly House",
        "es": "Consultas y servicios legales de inmigración a costo accesible. 802 S. 1st Ave, Suite 1, Phoenix. Pregunta por el costo cuando llames.",
        "en": "Affordable immigration consultations and legal services. 802 S. 1st Ave, Suite 1, Phoenix. Ask about the cost when you call.",
        "phones": [("602-416-7200", "+16024167200", "")],
        "site": "https://friendlyhouse.org/immigration-legal-services/",
        "src": ["fh"],
    },
    {
        "name": "Catholic Charities Community Services",
        "es": "Servicios legales de inmigración con representantes acreditados por el Departamento de Justicia. Su página incluye defensa contra "
              "la deportación y asilo. 5151 N. 19th Avenue, Phoenix. Pregunta por el costo cuando llames.",
        "en": "Immigration legal services with Department of Justice accredited representatives. Its page lists deportation defense "
              "and asylum. 5151 N. 19th Avenue, Phoenix. Ask about the cost when you call.",
        "phones": [("602-749-4415", "+16027494415", ""), ("855-316-2229", "+18553162229", {"es": "gratis", "en": "toll-free"})],
        "site": "https://www.catholiccharitiesaz.org/immigration-legal-services",
        "src": ["cc"],
    },
    {
        "name": "International Rescue Committee (IRC) Phoenix",
        "es": "Servicios legales de inmigración de bajo costo (residencia, ciudadanía, reunificación familiar, DACA). "
              "4425 West Olive Avenue, Suite 400, Glendale.",
        "en": "Low-cost immigration legal services (green cards, citizenship, family reunification, DACA). "
              "4425 West Olive Avenue, Suite 400, Glendale.",
        "phones": [("(602) 433-2440", "+16024332440", "")],
        "site": "https://www.rescue.org/united-states/phoenix-az",
        "src": ["irc"],
    },
    {
        "name": "AZLawHelp (Arizona Bar Foundation)",
        "es": "Para ver si calificas para ayuda legal gratuita o de costo reducido en Arizona (ayuda legal en general, no solo inmigración).",
        "en": "To check if you qualify for free or reduced fee legal help in Arizona (legal help in general, not only immigration).",
        "phones": [("866-637-5341", "+18666375341", "")],
        "site": "https://www.azlawhelp.org/",
        "src": ["azlh"],
    },
]

E = html.escape


def ext(url, label):
    return '<a href="%s" rel="noopener noreferrer">%s</a>' % (E(url, quote=True), label)


def sources(lang, ids, level=3):
    head = {"es": "De dónde viene esta información", "en": "Where this information comes from"}[lang]
    chk = {"es": "revisado el", "en": "checked on"}[lang]
    li = []
    for i in ids:
        if lang == "en" and i in ("aclu_es", "acluaz_work_es"):
            continue
        url, es, en, _ = SOURCES[i]
        li.append('<li>%s <span class="chk">(%s <time datetime="%s">%s</time>)</span></li>'
                  % (ext(url, E(es if lang == "es" else en)), chk, CHECKED, CHECKED_TXT[lang]))
    return '<div class="src"><h%d>%s</h%d><ul>%s</ul></div>' % (level, head, level, "".join(li))


def say(lang, text, meaning=None):
    """A sentence to say out loud, in English, with its Spanish meaning."""
    out = '<blockquote class="say"><p lang="en">%s</p>' % E(text)
    if lang == "es" and meaning:
        out += '<p class="mean">Significa: %s</p>' % E(meaning)
    return out + "</blockquote>"


with open(os.path.join(ROOT, "tools", "quotes.json"), encoding="utf-8") as _f:
    QUOTES = json.load(_f)
RETRIEVED_TXT = {"es": "27 de noviembre de 2026", "en": "November 27, 2026"}


def quote(lang, key):
    """A passage copied word for word from its source, with the notice the source's terms require.

    The ACLU and ACLU of Arizona user agreements allow copying text for noncommercial use with no editorial
    changes, no misleading excerpts, and this notice. Nothing inside q["html"] is ever edited by hand.
    """
    q = QUOTES[key]
    kind = q["kind"]
    es = lang == "es"
    url = q["url"]
    link = '<a href="%s" rel="noopener noreferrer">%s</a>' % (E(url, quote=True), E(url))
    if kind == "ars":
        label = "Texto de la ley, sin cambios" if es else "Text of the law, unchanged"
        body = "<h4>%s</h4>%s" % (E(q["title"]), "".join("<p>%s</p>" % E(p) for p in q["paras"]))
        notice = ("Arizona Revised Statutes 13-2412. Leído en %s el %s." if es else "Arizona Revised Statutes 13-2412. Read at %s on %s.") % (link, RETRIEVED_TXT[lang])
    else:
        who = "American Civil Liberties Union" if kind == "aclu" else "ACLU of Arizona"
        short = "ACLU" if kind == "aclu" else "ACLU of Arizona"
        label = ("Cita de la %s, palabra por palabra y sin cambios" if es else "Quoted from the %s, word for word and unchanged") % short
        title = ""
        if kind == "aclu" and q.get("title") and not key.endswith("_overview"):
            title = "<h3>%s</h3>" % E(q["title"])
        body = title + q["html"]
        notice = "Copyright %s %s. Originally posted by the %s at %s." % (
            q["year"], who, "ACLU" if kind == "aclu" else "ACLU of Arizona", link)
        notice += " " + (("Leído el %s." if es else "Read on %s.") % RETRIEVED_TXT[lang])
    return '<figure class="quote" lang="%s"><p class="qlabel" lang="%s">%s</p><div class="qbody">%s</div><figcaption>%s</figcaption></figure>' % (
        q["lang"], lang, E(label), body, notice)


def orgs(lang):
    out = []
    web = {"es": "Sitio web", "en": "Website"}[lang]
    call = {"es": "Llamar al", "en": "Call"}[lang]
    for o in ORGS:
        ph = []
        for num, tel, note in o["phones"]:
            if isinstance(note, dict):
                note = note[lang]
            label = "%s %s" % (call, num) + (" (%s)" % note if note else "")
            ph.append('<a class="btn call" href="tel:%s">%s</a>' % (tel, E(label)))
        out.append(
            '<article class="org"><h4>%s</h4><p>%s</p><div class="calls">%s</div><p class="orgweb">%s: %s</p>%s</article>'
            % (E(o["name"]), o[lang], "".join(ph), web, ext(o["site"], E(o["site"].split("/")[2].replace("www.", ""))), sources(lang, o["src"], 5))
        )
    return "".join(out)


def content(lang):
    es = lang == "es"
    p = lang  # id prefix
    T = lambda a, b: a if es else b  # noqa: E731
    h = []
    A = h.append

    # Intro and disclaimer
    A('<section class="notice" aria-labelledby="%s-imp-h"><h2 id="%s-imp-h">%s</h2><p>%s</p><div class="calls no-print">%s%s</div></section>' % (
        p, p, T("Importante", "Important"),
        T("Esta página da <strong>información general</strong>. <strong>No es consejo legal.</strong> Cada caso es distinto. "
          "Habla con un abogado o con un representante acreditado sobre tu situación. "
          "Esta página no guarda ni recoge ningún dato tuyo. Los enlaces te llevan a otros sitios.",
          "This page gives <strong>general information</strong>. <strong>It is not legal advice.</strong> Every case is different. "
          "Talk to a lawyer or an accredited representative about your situation. "
          "This page does not save or collect any information about you. Links take you to other sites."),
        '<a class="btn primary" href="%s" rel="noopener noreferrer">%s</a>' % (E(SOURCES["aclu_es"][0], True), T("ACLU: Derechos de los inmigrantes (en español)", "ACLU: Immigrants' Rights (Spanish)")),
        '<a class="btn primary" href="%s" rel="noopener noreferrer" lang="en">%s</a>' % (E(SOURCES["aclu"][0], True), T("ACLU: Immigrants' Rights (en inglés)", "ACLU: Immigrants' Rights (English)"))))

    # Jump menu
    items = [
        ("basics", T("Lo más importante", "The most important things")),
        ("home", T("Si tocan a tu puerta", "If they knock on your door")),
        ("public", T("En la calle", "In public")),
        ("car", T("En el carro", "In a car")),
        ("work", T("En el trabajo", "At work")),
        ("detained", T("Si detienen a alguien", "If someone is detained")),
        ("cards", T("Tarjetas Rojas", "Red Cards")),
        ("legal", T("Ayuda legal en Arizona", "Legal help in Arizona")),
        ("plan", T("Plan para tu familia", "Family plan")),
        ("about", T("Sobre esta página", "About this page")),
    ]
    A('<nav class="jump no-print" aria-labelledby="%s-jump-h"><h2 id="%s-jump-h">%s</h2><ul>%s</ul></nav>' % (
        p, p, T("¿Qué necesitas?", "What do you need?"),
        "".join('<li><a class="btn secondary" href="#%s-%s">%s</a></li>' % (p, i, t) for i, t in items)))

    def sec(i, title, body):
        A('<section class="panel" id="%s-%s" aria-labelledby="%s-%s-h" tabindex="-1"><h2 id="%s-%s-h">%s</h2>%s</section>'
          % (p, i, p, i, p, i, title, body))

    # 1 Basics
    sec("basics", T("Empieza aquí", "Start here"),
        "%s%s<div class=\"calls\">%s%s</div>%s" % (
            quote(lang, "aclu_%s_overview" % lang),
            quote(lang, "aclu_%s_asks" % lang),
            '<a class="btn primary" href="%s" rel="noopener noreferrer">%s</a>' % (E(SOURCES["aclu_es"][0], True), T("Todos los escenarios de la ACLU, en español", "All ACLU scenarios, in Spanish")),
            '<a class="btn primary" href="%s" rel="noopener noreferrer" lang="en">%s</a>' % (E(SOURCES["aclu"][0], True), T("Todos los escenarios de la ACLU, en inglés", "All ACLU scenarios, in English")),
            sources(lang, ["aclu", "aclu_es"])))

    # 2 Home
    sec("home", T("Si ICE o la policía tocan a tu puerta", "If ICE or the police come to your door"),
        quote(lang, "aclu_%s_home" % lang) + sources(lang, ["aclu", "aclu_es"]))

    # 3 Public
    sec("public", T("Si te paran en la calle o en un lugar público", "If you are stopped in public"),
        "%s<h3>%s</h3><p>%s</p>%s%s" % (
            quote(lang, "aclu_%s_stopped" % lang),
            T("La ley de Arizona sobre dar tu nombre", "Arizona law on giving your name"),
            T("Este es el texto de la ley de Arizona, copiado sin cambios de la página oficial de la Legislatura de Arizona. Está en inglés. "
              "Si tienes preguntas sobre cómo aplica a ti, habla con un abogado.",
              "This is the text of the Arizona law, copied without changes from the Arizona Legislature's official page. "
              "If you have questions about how it applies to you, talk to a lawyer."),
            quote(lang, "ars"),
            sources(lang, ["aclu", "aclu_es", "ars"])))

    # 4 Car
    sec("car", T("Si te paran en el carro", "If you are stopped in a car"),
        quote(lang, "aclu_%s_transit" % lang) + sources(lang, ["aclu", "aclu_es"]))

    # 5 Work
    sec("work", T("Si inmigración llega a tu trabajo", "If immigration comes to your work"),
        "%s%s<div class=\"calls\"><a class=\"btn secondary\" href=\"%s\" rel=\"noopener noreferrer\">%s</a></div>%s" % (
            quote(lang, "aclu_%s_business" % lang),
            quote(lang, "az_%s_workplace" % lang),
            E(SOURCES["acluaz_work_es" if es else "acluaz_work"][0], True),
            T("Leer toda la página de la ACLU de Arizona sobre redadas en el trabajo", "Read the whole ACLU of Arizona page on workplace raids"),
            sources(lang, ["aclu", "aclu_es", "acluaz_work", "acluaz_work_es"])))

    # 6 Detained
    sec("detained", T("Si detienen a alguien de tu familia", "If someone in your family is detained"),
        "%s%s<h3>%s</h3><ul class=\"list\">%s</ul><div class=\"calls\"><a class=\"btn call\" href=\"tel:+18008987180\">%s</a></div>%s" % (
            quote(lang, "aclu_%s_detained" % lang),
            quote(lang, "aclu_%s_lawyer" % lang),
            T("Buscar a la persona y su caso", "Finding the person and the case"),
            "".join("<li>%s</li>" % x for x in (T([
                "Localizador oficial de personas detenidas de ICE: %s." % ext(SOURCES["ice_locator"][0], "locator.ice.gov"),
                "Línea automática del Departamento de Justicia (EOIR) sobre casos en la corte de inmigración, en español e inglés, las 24 horas. Pide el número A.",
                "Organizaciones de %s." % ('<a href="#%s-legal">ayuda legal</a>' % p),
            ], [
                "Official ICE detainee locator: %s." % ext(SOURCES["ice_locator"][0], "locator.ice.gov"),
                "Department of Justice (EOIR) automated line about immigration court cases, in English and Spanish, 24 hours a day. It asks for the A-number.",
                "%s organizations." % ('<a href="#%s-legal">Legal help</a>' % p),
            ]))),
            T("Llamar al 1-800-898-7180 (corte de inmigración)", "Call 1-800-898-7180 (immigration court)"),
            sources(lang, ["aclu", "aclu_es", "ice_locator", "eoir_phone"])))

    # 7 Red cards (links only: ILRC allows hyperlinks, not copies)
    sec("cards", T("Tarjetas Rojas (Red Cards)", "Red Cards (Tarjetas Rojas)"),
        "<div class=\"redcard\"><p>%s</p></div><div class=\"calls\">%s%s%s</div><p class=\"hint\">%s</p>%s" % (
            T("Las Tarjetas Rojas son un recurso del Immigrant Legal Resource Center (ILRC). Los archivos y las instrucciones están en el sitio del ILRC.",
              "Red Cards are a resource from the Immigrant Legal Resource Center (ILRC). The files and the instructions are on the ILRC site."),
            '<a class="btn primary" href="%s" rel="noopener noreferrer">%s</a>' % (E(SOURCES["ilrc_red_es"][0], True), T("Tarjeta en español (PDF del ILRC)", "Card in Spanish (ILRC PDF)")),
            '<a class="btn primary" href="%s" rel="noopener noreferrer">%s</a>' % (E(SOURCES["ilrc_red_en"][0], True), T("Tarjeta en inglés (PDF del ILRC)", "Card in English (ILRC PDF)")),
            '<a class="btn secondary" href="%s" rel="noopener noreferrer">%s</a>' % (E(SOURCES["ilrc_red"][0], True), T("Todas las tarjetas e idiomas en ilrc.org", "All cards and languages on ilrc.org")),
            T("Estos botones abren archivos en el sitio oficial del ILRC. Esta página no copia ni guarda sus archivos ni su texto.",
              "These buttons open files on the official ILRC site. This page does not copy or host their files or their text."),
            sources(lang, ["ilrc_red", "ilrc_red_es", "ilrc_red_en"])))

    # 8 Legal help
    sec("legal", T("Ayuda legal gratuita o de bajo costo en Arizona", "Free or low-cost legal help in Arizona"),
        "%s<h3>%s</h3>%s<h3>%s</h3><ul class=\"list\">%s</ul>%s" % (
            quote(lang, "az_%s_attorney" % lang),
            T("Organizaciones", "Organizations"),
            orgs(lang),
            T("Listas oficiales y directorios", "Official lists and directories"),
            "".join("<li>%s</li>" % x for x in (T([
                "%s: organizaciones sin fines de lucro con servicios gratuitos o de bajo costo." % ext(SOURCES["ian"][0], "Directorio de Arizona de Immigration Advocates Network"),
                "%s, por corte (Eloy, Florence, Phoenix, Tucson). El gobierno aclara que no recomienda a ninguna organización de la lista." % ext(SOURCES["eoir_probono"][0], "Lista del Departamento de Justicia de proveedores gratuitos (pro bono)"),
                "%s: para confirmar que alguien que no es abogado está autorizado." % ext(SOURCES["eoir_roster"][0], "Organizaciones reconocidas y representantes acreditados"),
            ], [
                "%s: nonprofits with free or low-cost services." % ext(SOURCES["ian"][0], "Immigration Advocates Network directory for Arizona"),
                "%s, by court (Eloy, Florence, Phoenix, Tucson). The government says it does not endorse any organization on the list." % ext(SOURCES["eoir_probono"][0], "Department of Justice list of pro bono legal service providers"),
                "%s: to confirm that a non-lawyer is authorized." % ext(SOURCES["eoir_roster"][0], "Recognized organizations and accredited representatives"),
            ]))),
            sources(lang, ["acluaz_work", "acluaz_work_es", "ian", "eoir_probono", "eoir_roster"])))

    # 9 Family plan: ACLU of Arizona text, plus a link to the ILRC plan
    sec("plan", T("Plan para tu familia", "Family plan"),
        "%s%s<div class=\"calls\">%s</div>%s" % (
            quote(lang, "az_%s_plan" % lang),
            quote(lang, "az_%s_docs" % lang),
            '<a class="btn primary" href="%s" rel="noopener noreferrer">%s</a>' % (
                E(SOURCES["ilrc_plan_es" if es else "ilrc_plan"][0], True),
                T("Plan de Preparación Familiar completo (ILRC)", "Full Family Preparedness Plan (ILRC)")),
            sources(lang, ["acluaz_work", "acluaz_work_es", "ilrc_plan", "ilrc_plan_es"])))

    # 10 About
    sec("about", T("Sobre esta página", "About this page"),
        "<ul class=\"list\">%s</ul><div class=\"calls no-print\"><button type=\"button\" class=\"btn primary big js-print\">%s</button></div>" % (
            "".join("<li>%s</li>" % x for x in (T([
                "<strong>No es consejo legal.</strong> Es información general citada de organizaciones establecidas y de sitios oficiales. Las leyes y las prácticas cambian. Habla con un abogado o un representante acreditado sobre tu caso.",
                "<strong>No recogemos datos.</strong> Esta página no tiene analíticas, anuncios, cookies, formularios ni cuentas, y no guarda nada.",
                "<strong>Los enlaces salen de este sitio.</strong> Los otros sitios tienen sus propias reglas de privacidad. Los botones de teléfono usan la aplicación de llamadas de tu teléfono.",
                "Cada enlace y cada teléfono se revisó el <time datetime=\"%s\">%s</time> en la página oficial de cada organización. Antes de ir a una oficina, llama para confirmar." % (CHECKED, CHECKED_TXT["es"]),
                "Los textos de la ACLU y de la ACLU de Arizona se copian <strong>palabra por palabra y sin cambios</strong>, con el aviso de derechos de autor que piden esos sitios, para uso no comercial. El texto de la ley de Arizona se copia del sitio de la Legislatura. Los títulos, botones y avisos que no están en un recuadro de cita son de esta página.",
                "Esta página no está afiliada a ninguna de las organizaciones nombradas ni al gobierno.",
                "En un teléfono o computadora compartidos, el historial del navegador puede mostrar que visitaste esta página.",
                "Es gratis y siempre lo será.",
            ], [
                "<strong>This is not legal advice.</strong> It is general information quoted from established organizations and official sites. Laws and practices change. Talk to a lawyer or an accredited representative about your case.",
                "<strong>We collect no data.</strong> This page has no analytics, ads, cookies, forms or accounts, and it saves nothing.",
                "<strong>Links leave this site.</strong> Other sites have their own privacy rules. Phone buttons use your phone's calling app.",
                "Every link and phone number was checked on <time datetime=\"%s\">%s</time> on each organization's official page. Before going to an office, call to confirm." % (CHECKED, CHECKED_TXT["en"]),
                "Text from the ACLU and the ACLU of Arizona is copied <strong>word for word and unchanged</strong>, with the copyright notice those sites require, for noncommercial use. The Arizona law text is copied from the Legislature's site. Headings, buttons and notices that are not inside a quote box are this page's own.",
                "This page is not affiliated with any of the organizations named or with the government.",
                "On a shared phone or computer, the browser history can show that you visited this page.",
                "It is free and always will be.",
            ]))),
            T("Imprimir esta página", "Print this page")))
    return "\n".join(h)


TEXT = {
    "title": "Conoce tus derechos en Arizona: qué hacer y ayuda legal",
    "title_en": "Know your rights in Arizona: what to do and legal help",
    "desc": "Qué hacer si llega inmigración y dónde encontrar ayuda legal gratuita en Arizona (Tempe y Phoenix). Gratis, sin anuncios, sin rastreo. Español e inglés.",
    "desc_en": "What to do if immigration comes and where to find free or low-cost legal help in Arizona (Tempe and Phoenix). Free, no ads, no tracking. Spanish and English.",
    "imgalt": "Conoce tus derechos, Arizona: qué hacer y dónde encontrar ayuda. Know your rights and where to get help. Gratis, sin rastreo. Free, no tracking.",
}


def jsonld_graph():
    # Only what is visible on the page. No person is named; the publisher is the project itself.
    return {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": SITE_URL + "#org", "name": "Conoce tus derechos · Arizona",
             "url": SITE_URL, "logo": SITE_URL + "apple-touch-icon.png",
             "description": "Free, ad-free, zero-tracking know-your-rights and legal-help information page for Arizona, in Spanish and English."},
            {"@type": "WebSite", "@id": SITE_URL + "#website", "url": SITE_URL,
             "name": "Conoce tus derechos · Arizona", "description": TEXT["desc"],
             "inLanguage": ["es", "en"], "publisher": {"@id": SITE_URL + "#org"}},
            {"@type": "WebPage", "@id": SITE_URL + "#webpage", "url": SITE_URL, "name": TEXT["title"],
             "description": TEXT["desc"], "inLanguage": ["es", "en"], "isPartOf": {"@id": SITE_URL + "#website"},
             "publisher": {"@id": SITE_URL + "#org"}, "dateModified": CHECKED,
             "primaryImageOfPage": {"@type": "ImageObject", "url": SITE_URL + "og-image.png", "width": 1200, "height": 630},
             "about": {"@type": "Thing", "name": "Know your rights and free or low-cost immigration legal help in Arizona"}},
        ],
    }


def page():
    foot_es = ("Este sitio no tiene analíticas y no guarda nada. Está alojado en GitHub Pages, que puede guardar registros estándar de visitas "
               "que nosotros no podemos ver ni controlar. Nosotros no agregamos nada.")
    foot_en = ("This site has no analytics and saves nothing. It is hosted on GitHub Pages, which may keep standard visit logs "
               "that we cannot see or control. We add nothing.")
    desc = TEXT["desc"]
    title = TEXT["title"]
    imgalt = TEXT["imgalt"]
    jsonld = json.dumps(jsonld_graph(), ensure_ascii=False, indent=1).replace("</", "<\\/")
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{site}">
<link rel="alternate" hreflang="es" href="{site}">
<link rel="alternate" hreflang="en" href="{site}">
<link rel="alternate" hreflang="x-default" href="{site}">
<meta property="og:site_name" content="Conoce tus derechos · Arizona">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{site}og-image.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{imgalt}">
<meta property="og:url" content="{site}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_US">
<meta property="og:locale:alternate" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{site}og-image.png">
<meta name="twitter:image:alt" content="{imgalt}">
<meta name="theme-color" content="#0b4f8a">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<script type="application/ld+json">{jsonld}</script>
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; manifest-src 'self'; base-uri 'none'; form-action 'none'">
<meta name="referrer" content="no-referrer">
<link rel="stylesheet" href="style.css">
<noscript><link rel="stylesheet" href="noscript.css"></noscript>
</head>
<body>
<a class="skip es" href="#main">Ir al contenido</a>
<a class="skip en" href="#main" lang="en">Skip to content</a>
<header class="top">
  <div class="brand">
    <h1 class="es">Conoce tus derechos <span class="where">Arizona</span></h1>
    <h1 class="en" lang="en">Know your rights <span class="where">Arizona</span></h1>
  </div>
  <div class="langs no-print" role="group" aria-label="Idioma / Language">
    <button type="button" id="lang-es" data-lang="es" lang="es" aria-label="ES, Español" aria-pressed="true">ES</button>
    <button type="button" id="lang-en" data-lang="en" lang="en" aria-label="EN, English" aria-pressed="false">EN</button>
  </div>
</header>

<main id="main" tabindex="-1">
<div class="es wrap">
<p class="lead">Qué hacer si llega inmigración y dónde encontrar ayuda en Arizona (Tempe, Phoenix y alrededores). Gratis. Sin anuncios. Sin rastreo.</p>
<div class="calls no-print"><button type="button" class="btn secondary js-print">Imprimir esta página</button></div>
{es}
</div>
<div class="en wrap" lang="en">
<p class="lead">What to do if immigration comes, and where to find help in Arizona (Tempe, Phoenix and nearby). Free. No ads. No tracking.</p>
<div class="calls no-print"><button type="button" class="btn secondary js-print">Print this page</button></div>
{en}
</div>
</main>

<footer>
  <p class="es">{foot_es}</p>
  <p class="en" lang="en">{foot_en}</p>
  <p>Conoce tus derechos · Arizona · MIT</p>
</footer>
<script src="app.js"></script>
</body>
</html>
""".format(desc=desc, title=title, imgalt=imgalt, jsonld=jsonld, site=SITE_URL, es=content("es"), en=content("en"), foot_es=foot_es, foot_en=foot_en)


def sources_md():
    out = ["# Sources", "",
           "Every external fact on the site (organization, phone number, legal claim) with the page it was read on.",
           "All pages were read on %s. This file is generated by `tools/build.py`; edit the lists there." % CHECKED, "",
           "Rule: a phone number is on the site only if it was seen on the organization's own official page on that date.", "",
           "## Organizations and phone numbers", "",
           "| Organization | Phone numbers on the site | Read on |", "|---|---|---|"]
    for o in ORGS:
        out.append("| %s | %s | %s |" % (
            o["name"], ", ".join(n + (" (%s)" % (t["en"] if isinstance(t, dict) else t) if t else "") for n, _, t in o["phones"]),
            " ; ".join(SOURCES[s][0] for s in o["src"])))
    out.append("| U.S. Department of Justice, EOIR automated case information | 1-800-898-7180 | %s |" % SOURCES["eoir_phone"][0])
    out += ["", "## Source pages and what was taken from each", "", "| # | Source | URL | Facts taken |", "|---|---|---|---|"]
    for n, (k, (url, _es, en, facts)) in enumerate(SOURCES.items(), 1):
        out.append("| %d | %s | %s | %s |" % (n, en, url, facts))
    out += ["", "## Looked for and left out (could not be verified on %s)" % CHECKED, "",
            "- National Immigration Law Center (NILC): nilc.org answered every request with HTTP 403 to the automated check, so no NILC text or link is used. "
            "A person should open nilc.org in a browser and decide whether to add a link.",
            "- ILRC English \"Family Preparedness Plan\" landing page (ilrc.org/resources/family-preparedness-plan): HTTP 403. "
            "The ILRC step-by-step plan page and the Spanish plan page loaded and are used instead.",
            "- Consulate of Mexico in Phoenix and its emergency line: the consulate site sits behind a bot wall and could not be read, so no consulate phone number is on the site. "
            "The site only tells people to write down their own consulate's number.",
            "- State Bar of Arizona phone number, EOIR hotline (800) 568-5157 and the county phone lists printed on the ACLU of Arizona page: not quoted (the quoted passages stop before them). Only EOIR's own number, 1-800-898-7180, is used.",
            "- ACLU of Arizona answer to \"Do I have to tell an agent or officer my name?\": not quoted. The Arizona statute is quoted from azleg.gov instead.",
            "- Arizona State University immigration clinic: the page tried returned 404, left out.",
            "- Chicanos Por La Causa immigration services: its own page lists only Tucson, Somerton and Nogales offices and says it does not represent people in immigration court, so it is left out of a Phoenix-area list.",
            "- Arizona court form for delegating parental powers: not found on azcourts.gov tonight, so the site only says to ask a lawyer about a power of attorney.",
            "- Detention facility phone numbers shown on the Florence Project FAQ: that page still uses old facility names, so they are left out.",
            "", "## Notes for the reviewer", "",
            "- The Spanish headings, buttons and notices written for this page were produced by an AI and need a read by a native speaker before the site goes public. The quoted Spanish is the ACLU's own.",
            "- ILRC red card files are linked on ilrc.org, not copied. ILRC's site says \"All rights reserved\" and has a reprint permission form.",
            "- All legal wording is quoted word for word from the ACLU, the ACLU of Arizona or the Arizona Legislature (azleg.gov), each with the notice its terms require. ILRC is linked only.",
            "- ACLU terms: https://www.aclu.org/about/aclu-site-user-agreement (text may be copied for noncommercial use, with no editorial changes, no misleading excerpts, and the copyright notice). ACLU of Arizona terms: https://www.acluaz.org/user-agreement/ (same three limits).",
            "- Not quoted, and still needs a human: the headings, buttons, notices and short lead-ins written for this page (Spanish and English). A native Spanish speaker should read the Spanish ones.",
            ""]
    return "\n".join(out)


if __name__ == "__main__":
    out = page()
    assert chr(0x2014) not in out, "em dash found"
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
    md = sources_md()
    assert chr(0x2014) not in md
    with open(os.path.join(ROOT, "docs", "SOURCES.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print("built index.html (%d bytes), docs/SOURCES.md, %d sources, %d orgs" % (len(out), len(SOURCES), len(ORGS)))
