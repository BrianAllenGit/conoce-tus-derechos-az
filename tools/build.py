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
        "Steps for ICE or police at the home, stopped in public, stopped in a car, checkpoints, arrest or detention, "
        "the right to remain silent, refusing searches, warrants signed by a judge, Form I-205, the sentences to say out loud, "
        "right to a lawyer at your own cost, consulate contact, A-number, fear of return, probation search condition.",
    ),
    "aclu_es": (
        "https://www.aclu.org/know-your-rights/derechos-de-los-inmigrantes",
        "ACLU: Conozca sus derechos, derechos de los inmigrantes (en español)",
        "ACLU: Know Your Rights, Immigrants' Rights (Spanish version)",
        "Spanish version of the ACLU page, linked for Spanish readers.",
    ),
    "acluaz_work": (
        "https://www.acluaz.org/know-your-rights/know-your-rights-during-and-after-workplace-raid/",
        "ACLU de Arizona: Sus derechos antes, durante y después de una redada en el trabajo",
        "ACLU of Arizona: Know Your Rights Before, During, and After a Workplace Raid",
        "Workplace steps (do not run, ask if free to leave, remain silent, do not sign), when agents may enter a workplace, "
        "the Arizona rule on giving your name, family plan items (extra keys, trusted person, power of attorney, medications), "
        "important documents list, warning about notaries.",
    ),
    "ilrc_red": (
        "https://www.ilrc.org/red-cards-tarjetas-rojas",
        "ILRC: Tarjetas Rojas (Red Cards)",
        "ILRC: Red Cards / Tarjetas Rojas",
        "What red cards are, that they are free, that they can be printed at home, that they are not individual legal advice, "
        "and the five points printed on the card.",
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
        "Family plan: back-up caregiver, medical information, passports for children, school emergency contacts, "
        "ICE detainee locator and A-number, consulate number, who may give immigration legal advice, what to carry.",
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
        "Official tool to find a person in ICE custody.",
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
    A('<section class="notice" aria-labelledby="%s-imp-h"><h2 id="%s-imp-h">%s</h2><p>%s</p></section>' % (
        p, p, T("Importante", "Important"),
        T("Esta página da <strong>información general</strong>. <strong>No es consejo legal.</strong> Cada caso es distinto. "
          "Habla con un abogado o con un representante acreditado sobre tu situación. "
          "Esta página no guarda ni recoge ningún dato tuyo. Los enlaces te llevan a otros sitios.",
          "This page gives <strong>general information</strong>. <strong>It is not legal advice.</strong> Every case is different. "
          "Talk to a lawyer or an accredited representative about your situation. "
          "This page does not save or collect any information about you. Links take you to other sites.")))

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
    sec("basics", T("Lo más importante", "The most important things"),
        "<p>%s</p><ol class=\"steps\">%s</ol>%s" % (
            T("Todas las personas en los Estados Unidos tienen ciertos derechos, sin importar su estatus migratorio.",
              "All people in the United States have certain rights, regardless of immigration status."),
            "".join("<li>%s</li>" % x for x in (T([
                "<strong>Mantén la calma.</strong> No corras, no discutas y no te resistas.",
                "<strong>No abras la puerta</strong> si un agente de inmigración está tocando.",
                "<strong>Tienes derecho a guardar silencio.</strong> No tienes que contestar preguntas de un agente de inmigración.",
                "<strong>No firmes nada</strong> sin hablar antes con un abogado.",
                "Fuera de tu casa, <strong>pregunta si puedes irte</strong>. Si te dicen que sí, vete con calma.",
                "<strong>No mientas</strong> y no muestres documentos falsos.",
            ], [
                "<strong>Stay calm.</strong> Do not run, argue, or resist.",
                "<strong>Do not open the door</strong> if an immigration agent is knocking.",
                "<strong>You have the right to remain silent.</strong> You do not have to answer questions from an immigration agent.",
                "<strong>Do not sign anything</strong> without first speaking to a lawyer.",
                "Outside your home, <strong>ask if you are free to leave</strong>. If they say yes, leave calmly.",
                "<strong>Do not lie</strong> and do not show false documents.",
            ]))),
            sources(lang, ["ilrc_red", "aclu"] + (["aclu_es"] if es else []))))

    # 2 Home
    sec("home", T("Si ICE o la policía tocan a tu puerta", "If ICE or the police come to your door"),
        "<ol class=\"steps\">%s</ol>%s%s%s%s" % (
            "".join("<li>%s</li>" % x for x in (T([
                "<strong>Mantén la calma y deja la puerta cerrada.</strong> Es más seguro hablar a través de la puerta.",
                "Pregunta si son agentes de inmigración y a qué vienen. Pide que te muestren su placa o identificación por la ventana o la mirilla.",
                "Pregunta si tienen una <strong>orden firmada por un juez</strong>. Si dicen que sí, pide que la pasen por debajo de la puerta o la pongan contra la ventana.",
                "No abras la puerta a menos que te muestren una orden judicial de registro o de arresto que nombre a una persona que vive en tu casa o las áreas de tu domicilio que van a registrar.",
                "Una orden de deportación (formulario I-205) <strong>no</strong> les permite entrar a una casa sin permiso.",
                "Si no muestran una orden judicial, deja la puerta cerrada y di la primera frase de abajo.",
                "Si entran a la fuerza, <strong>no te resistas</strong>. Di la segunda frase de abajo.",
                "No mientas, no muestres documentos falsos y no firmes nada sin hablar antes con un abogado.",
            ], [
                "<strong>Stay calm and keep the door closed.</strong> It is safer to speak through the door.",
                "Ask if they are immigration agents and what they are there for. Ask them to show a badge or identification through the window or peephole.",
                "Ask if they have a <strong>warrant signed by a judge</strong>. If they say yes, ask them to slide it under the door or hold it up to a window.",
                "Do not open the door unless they show you a judicial search or arrest warrant that names a person in your residence or the areas to be searched at your address.",
                "A warrant of removal or deportation (Form I-205) does <strong>not</strong> allow officers to enter a home without consent.",
                "If they do not show a judicial warrant, keep the door closed and say the first sentence below.",
                "If agents force their way in, <strong>do not resist</strong>. Say the second sentence below.",
                "Do not lie, do not show false documents, and do not sign anything without speaking with a lawyer first.",
            ]))),
            "<h3>%s</h3>" % T("Qué decir (en inglés)", "What to say"),
            say(lang, "I do not consent to your entry.", "No doy permiso para que entren."),
            say(lang, "I do not consent to your entry or to your search of these premises. I am exercising my right to remain silent. I wish to speak with a lawyer as soon as possible.",
                "No doy permiso para que entren ni para que registren este lugar. Estoy usando mi derecho a guardar silencio. Quiero hablar con un abogado lo antes posible."),
            "<p class=\"tip\">%s</p>%s" % (
                T("Ojo: si la policía tiene una orden de arresto, puede entrar a la casa de la persona nombrada en la orden si cree que está adentro. "
                  "Si estás en libertad condicional (probation) con una condición de registro, la policía puede entrar a tu casa.",
                  "Note: if police have an arrest warrant, they are allowed to enter the home of the person on the warrant if they believe that person is inside. "
                  "If you are on probation with a search condition, law enforcement is allowed to enter your home."),
                sources(lang, ["aclu"] + (["aclu_es"] if es else []) + ["ilrc_red"]))))

    # 3 Public
    sec("public", T("Si te paran en la calle o en un lugar público", "If you are stopped in public"),
        "<ol class=\"steps\">%s</ol><h3>%s</h3><p>%s</p><h3>%s</h3>%s%s" % (
            "".join("<li>%s</li>" % x for x in (T([
                "<strong>Mantén la calma.</strong> No corras, no discutas, no te resistas y no estorbes al agente. Mantén las manos donde las puedan ver.",
                "<strong>Pregunta si puedes irte.</strong> Si te dicen que sí, vete con calma.",
                "<strong>Tienes derecho a guardar silencio.</strong> Si quieres usar ese derecho, dilo en voz alta.",
                "No tienes que contestar dónde naciste, si eres ciudadano o cómo entraste al país. (Hay reglas distintas en la frontera, en aeropuertos y para algunas personas con ciertas visas.)",
                "No tienes que dar permiso para que te registren a ti o tus cosas. La policía sí puede tocar tu ropa por fuera si sospecha que llevas un arma.",
                "<strong>No mientas</strong> sobre tu estatus y no muestres documentos falsos.",
                "Si no eres ciudadano y un agente de inmigración te pide tus documentos de inmigración, debes mostrarlos si los llevas contigo. Si no tienes documentos de inmigración, di que quieres guardar silencio.",
                "Si te arrestan o te detienen: di que quieres guardar silencio y pide un abogado. No des explicaciones y no firmes nada.",
            ], [
                "<strong>Stay calm.</strong> Do not run, argue, resist, or obstruct the officer. Keep your hands where they can see them.",
                "<strong>Ask if you are free to leave.</strong> If they say yes, leave calmly.",
                "<strong>You have the right to remain silent.</strong> If you wish to use that right, say so out loud.",
                "You do not have to answer questions about where you were born, whether you are a U.S. citizen, or how you entered the country. (Separate rules apply at borders and airports, and for some people on certain visas.)",
                "You do not have to consent to a search of yourself or your belongings. Police may pat down your clothing if they suspect a weapon.",
                "<strong>Do not lie</strong> about your status and do not show false documents.",
                "If you are not a U.S. citizen and an immigration agent asks for your immigration papers, you must show them if you have them with you. If you do not have immigration papers, say you want to remain silent.",
                "If you are arrested or detained: say you wish to remain silent and ask for a lawyer. Do not give explanations and do not sign anything.",
            ]))),
            T("Tu nombre, en Arizona", "Your name, in Arizona"),
            T("Según la ACLU de Arizona: no estás obligado a dar tu nombre a agentes federales como ICE. Si un policía local o estatal que investiga un delito te pide tu nombre, "
              "la ley de Arizona te obliga a decir tu nombre legal completo y verdadero, pero no tienes que dar más información.",
              "According to the ACLU of Arizona: you are not required to give your name to federal law enforcement such as ICE. If a local or state police officer who is investigating a crime asks for your name, "
              "Arizona law requires you to state your true full legal name, but you do not have to give any further information."),
            T("Qué decir (en inglés)", "What to say"),
            say(lang, "Am I free to leave?", "¿Puedo irme?") +
            say(lang, "I am exercising my right to remain silent. I wish to speak with a lawyer.", "Estoy usando mi derecho a guardar silencio. Quiero hablar con un abogado."),
            sources(lang, ["aclu"] + (["aclu_es"] if es else []) + ["acluaz_work", "ilrc_red"])))

    # 4 Car
    sec("car", T("Si te paran en el carro", "If you are stopped in a car"),
        "<ol class=\"steps\">%s</ol>%s" % (
            "".join("<li>%s</li>" % x for x in (T([
                "Detente en un lugar seguro lo más pronto posible. Apaga el motor, prende la luz de adentro, baja la ventana un poco y pon las manos en el volante.",
                "Si la policía te los pide, muestra tu licencia de manejar, el registro del carro y el comprobante de seguro.",
                "<strong>El conductor y los pasajeros tienen derecho a guardar silencio.</strong> No tienes que contestar preguntas sobre tu estatus migratorio.",
                "Si eres pasajero, puedes preguntar si puedes irte. Si te dicen que sí, vete con calma.",
                "Si un oficial o agente pide revisar tu carro, <strong>puedes decir que no das permiso</strong>. Pero si la policía cree que tu carro tiene pruebas de un delito, puede revisarlo sin tu permiso.",
                "<strong>Nunca huyas</strong> de un retén (punto de control) de inmigración. En un retén los agentes pueden pararte y hacer preguntas breves.",
                "No mientas y no muestres documentos falsos.",
            ], [
                "Pull over in a safe place as quickly as possible. Turn off the engine, turn on the inside light, open the window part way, and put your hands on the wheel.",
                "If police ask, show your driver's license, registration, and proof of insurance.",
                "<strong>Drivers and passengers have the right to remain silent.</strong> You do not have to answer questions about your immigration status.",
                "If you are a passenger, you can ask if you are free to leave. If the officer says yes, leave calmly.",
                "If an officer or agent asks to look inside your car, <strong>you can refuse to consent to the search</strong>. But if police believe your car contains evidence of a crime, they can search it without your consent.",
                "<strong>Never flee</strong> from an immigration checkpoint. At a checkpoint, agents can stop you and ask brief questions.",
                "Do not lie and do not show false documents.",
            ]))),
            sources(lang, ["aclu"] + (["aclu_es"] if es else []))))

    # 5 Work
    sec("work", T("Si inmigración llega a tu trabajo", "If immigration comes to your work"),
        "<ol class=\"steps\">%s</ol><h3>%s</h3><ul class=\"list\">%s</ul>%s" % (
            "".join("<li>%s</li>" % x for x in (T([
                "<strong>No corras.</strong> Puedes preguntar si puedes irte.",
                "<strong>Tienes derecho a guardar silencio</strong>, aunque tengas miedo.",
                "Puedes decirle al oficial que quieres hablar con un abogado.",
                "No tienes que contestar preguntas sobre tu estatus migratorio, dónde naciste o cómo entraste al país.",
                "<strong>No mientas</strong> y no le des documentos falsos al oficial.",
                "<strong>No firmes nada</strong> antes de consultar con un abogado.",
                "Si los agentes tienen una orden para registrar el lugar, pueden pedirte que te quedes en un área mientras hacen el registro.",
            ], [
                "<strong>Do not run.</strong> You may ask if you are free to leave.",
                "<strong>You have the right to remain silent</strong>, even if you are scared.",
                "You may tell the officer that you wish to speak to a lawyer.",
                "You do not have to answer questions about your immigration status, where you were born, or how you entered the country.",
                "<strong>Do not lie</strong> or give the officer fake documents.",
                "<strong>Do not sign anything</strong> before consulting with a lawyer.",
                "If the agents have a warrant to search the place, they may ask you to stay in one area while they search.",
            ]))),
            T("Bueno saber", "Good to know"),
            "".join("<li>%s</li>" % x for x in (T([
                "Los agentes pueden entrar sin orden a las áreas abiertas al público (por ejemplo, el comedor de un restaurante) o si el empleador les da permiso.",
                "Para entrar a un área que no es pública sin permiso del empleador, la regla general es que necesitan una orden firmada por un juez.",
                "Antes de que pase algo: habla con compañeros de confianza sobre mantener la calma, no correr y el derecho a guardar silencio. Si tienes sindicato, pregunta si puede ayudar.",
            ], [
                "Agents may enter without a warrant in areas open to the public (for example, the dining area of a restaurant) or if the employer gives permission.",
                "To enter a non-public area without the employer's permission, the general rule is that they need a warrant signed by a judge.",
                "Before anything happens: talk to trusted co-workers about staying calm, not running, and the right to remain silent. If you belong to a union, ask if it can help.",
            ]))),
            sources(lang, ["acluaz_work"])))

    # 6 Detained
    sec("detained", T("Si detienen a alguien de tu familia", "If someone in your family is detained"),
        "<h3>%s</h3><ul class=\"list\">%s</ul><h3>%s</h3><ul class=\"list\">%s</ul><div class=\"calls\"><a class=\"btn call\" href=\"tel:+18008987180\">%s</a></div>%s" % (
            T("La persona detenida", "The person who is detained"),
            "".join("<li>%s</li>" % x for x in (T([
                "Tiene derecho a hablar con un abogado, pero el gobierno no tiene que darle uno. Puede pedir una lista de opciones gratuitas o de bajo costo.",
                "No debe firmar nada ni tomar decisiones sin un abogado.",
                "Tiene derecho a comunicarse con el consulado de su país.",
                "Si tiene miedo de regresar a su país, debe decírselo a un oficial y contactar a un abogado de inmediato.",
                "Debe recordar su número de inmigración (número A) y dárselo a su familia.",
            ], [
                "Has the right to talk to a lawyer, but the government does not have to provide one. They can ask for a list of free or low-cost options.",
                "Should not sign anything or make decisions without a lawyer.",
                "Has the right to contact their country's consulate.",
                "If they fear returning to their country, they should tell an officer and contact a lawyer immediately.",
                "Should remember their immigration number (A-number) and give it to their family.",
            ]))),
            T("La familia", "The family"),
            "".join("<li>%s</li>" % x for x in (T([
                "Busca a la persona en el %s. Necesitas su nombre completo y su país de nacimiento, más su número A o su fecha de nacimiento." % ext(SOURCES["ice_locator"][0], "localizador oficial de personas detenidas de ICE"),
                "Para saber la fecha y el lugar de la próxima audiencia en la corte de inmigración, llama a la línea automática del Departamento de Justicia. Atiende en español e inglés, las 24 horas, y pide el número A.",
                "Llama a una organización de %s." % ('<a href="#%s-legal">ayuda legal</a>' % p),
            ], [
                "Look for the person in the %s. You need their full name and country of birth, plus their A-number or their date of birth." % ext(SOURCES["ice_locator"][0], "official ICE detainee locator"),
                "To learn the date and place of the next immigration court hearing, call the Department of Justice automated line. It works in English and Spanish, 24 hours a day, and asks for the A-number.",
                "Call a %s organization." % ('<a href="#%s-legal">legal help</a>' % p),
            ]))),
            T("Llamar al 1-800-898-7180 (corte de inmigración)", "Call 1-800-898-7180 (immigration court)"),
            sources(lang, ["aclu", "ice_locator", "eoir_phone", "firrp_faq", "ilrc_plan"])))

    # 7 Red cards
    sec("cards", T("Tarjetas Rojas (Red Cards)", "Red Cards (Tarjetas Rojas)"),
        "<div class=\"redcard\"><p>%s</p><p>%s</p></div><div class=\"calls\">%s%s%s</div><p class=\"hint\">%s</p>%s" % (
            T("Las Tarjetas Rojas del Immigrant Legal Resource Center (ILRC) te ayudan a usar tus derechos. Un lado te recuerda tus derechos en español. "
              "El otro lado, en inglés, es para mostrarlo o dárselo al agente: lo puedes pasar por debajo de la puerta o mostrarlo por la ventana.",
              "Red Cards from the Immigrant Legal Resource Center (ILRC) help you use your rights. One side reminds you of your rights. "
              "The other side, in English, is for showing or handing to the agent: you can slide it under the door or show it through the window."),
            T("<strong>Son gratis.</strong> Nunca pagues por ellas. Puedes imprimirlas en casa, en una biblioteca o en una copiadora.",
              "<strong>They are free.</strong> Never pay for them. You can print them at home, at a library, or at a copy shop."),
            '<a class="btn primary" href="%s" rel="noopener noreferrer">%s</a>' % (E(SOURCES["ilrc_red_es"][0], True), T("Imprimir tarjeta en español (PDF del ILRC)", "Print card in Spanish (ILRC PDF)")),
            '<a class="btn primary" href="%s" rel="noopener noreferrer">%s</a>' % (E(SOURCES["ilrc_red_en"][0], True), T("Imprimir tarjeta en inglés (PDF del ILRC)", "Print card in English (ILRC PDF)")),
            '<a class="btn secondary" href="%s" rel="noopener noreferrer">%s</a>' % (E(SOURCES["ilrc_red"][0], True), T("Ver todas las tarjetas e idiomas en ilrc.org", "See all cards and languages on ilrc.org")),
            T("Estos botones abren archivos en el sitio oficial del ILRC. Esta página no copia ni guarda sus archivos.",
              "These buttons open files on the official ILRC site. This page does not copy or host their files."),
            sources(lang, ["ilrc_red", "ilrc_red_es", "ilrc_red_en"])))

    # 8 Legal help
    sec("legal", T("Ayuda legal gratuita o de bajo costo en Arizona", "Free or low-cost legal help in Arizona"),
        "<p class=\"tip\">%s</p><h3>%s</h3>%s<h3>%s</h3><ul class=\"list\">%s</ul>%s" % (
            T("<strong>Cuidado con el fraude.</strong> En los Estados Unidos un «notario» no es abogado. Solo un abogado con licencia o un representante acreditado por el "
              "Departamento de Justicia (que trabaja en una organización reconocida) puede darte consejo legal de inmigración.",
              "<strong>Watch out for fraud.</strong> In the United States a \"notario\" or notary is not a lawyer. Only a licensed attorney or a Department of Justice "
              "accredited representative (who works at a recognized organization) can give you immigration legal advice."),
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
            sources(lang, ["ian", "eoir_probono", "eoir_roster", "ilrc_plan", "acluaz_work"])))

    # 9 Family plan
    def checks(xs):
        return '<ul class="check">%s</ul>' % "".join("<li>%s</li>" % x for x in xs)
    sec("plan", T("Plan para tu familia", "Family plan"),
        "<p>%s</p><h3>%s</h3>%s<h3>%s</h3>%s<h3>%s</h3>%s<div class=\"calls\">%s</div>%s" % (
            T("Tener un plan baja el estrés de lo inesperado. Ojalá nunca lo necesites. Puedes imprimir esta página y marcar cada cosa.",
              "Having a plan lowers the stress of the unexpected. We hope you never need it. You can print this page and check off each item."),
            T("Lista del plan familiar", "Family plan checklist"),
            checks(T([
                "Elegir a un adulto de confianza que cuide a mis hijos si yo no puedo, y hablar con esa persona.",
                "Poner al día los contactos de emergencia en la escuela y la guardería.",
                "Escribir las condiciones médicas, alergias, medicinas, doctor y seguro de mis hijos, y darle una copia a la persona que los va a cuidar.",
                "Memorizar los teléfonos de mi familia y de mi abogado.",
                "Darle un juego extra de llaves a alguien de confianza.",
                "Elegir a alguien de confianza que pueda tomar decisiones por mí si me detienen. Preguntarle a un abogado si me conviene una carta poder (power of attorney).",
                "Asegurarme de que mi familia sepa mi número A, si tengo uno, y cómo usar el localizador de ICE.",
                "Anotar el teléfono del consulado de mi país más cercano.",
                "Explicarles el plan a mis hijos con calma: quién los va a cuidar y que van a estar bien.",
                "Practicar en familia: no abrir la puerta, guardar silencio, mostrar la Tarjeta Roja.",
                "Pedir una consulta con un proveedor legal de confianza para saber qué opciones tengo.",
            ], [
                "Choose a trusted adult to care for my children if I cannot, and talk with that person.",
                "Update emergency contacts at school and day care.",
                "Write down my children's medical conditions, allergies, medications, doctor and insurance, and give a copy to the person who will care for them.",
                "Memorize the phone numbers of my family and my lawyer.",
                "Give an extra set of keys to someone I trust.",
                "Choose someone I trust to make decisions for me if I am detained. Ask a lawyer whether a power of attorney makes sense for me.",
                "Make sure my family knows my A-number, if I have one, and how to use the ICE locator.",
                "Write down the phone number of my country's nearest consulate.",
                "Calmly explain the plan to my children: who will care for them and that they will be okay.",
                "Practice as a family: do not open the door, remain silent, show the Red Card.",
                "Get a consultation with a trusted legal provider to learn what options I have.",
            ])),
            T("Documentos importantes para juntar", "Important documents to gather"),
            "<p>%s</p>%s" % (
                T("Guárdalos en un lugar seguro al que tu familia pueda llegar fácilmente. Dale copias a una persona de confianza.",
                  "Keep them in a secure place your family can reach easily. Give copies to a person you trust."),
                checks(T([
                    "Actas de nacimiento.",
                    "Acta de matrimonio.",
                    "Pasaportes (también los de mis hijos).",
                    "Papeles de la corte.",
                    "Copia de todos los papeles que he presentado a inmigración.",
                    "Mi número A, si tengo uno.",
                    "Información médica y de la escuela de mis hijos.",
                    "Lista de todos los abogados que me han representado y cómo contactarlos.",
                ], [
                    "Birth certificates.",
                    "Marriage certificate.",
                    "Passports (my children's too).",
                    "Court papers.",
                    "A copy of all papers I have filed with immigration.",
                    "My A-number, if I have one.",
                    "My children's medical and school information.",
                    "A list of all the lawyers who have represented me and how to contact them.",
                ]))),
            T("Qué llevar contigo y qué no", "What to carry and what not to carry"),
            "<ul class=\"list\">%s</ul>" % "".join("<li>%s</li>" % x for x in (T([
                "Lleva una Tarjeta Roja.",
                "Lleva el teléfono de alguien que pueda poner tu plan en marcha y llamar a tu abogado.",
                "Si tienes estatus legal, puedes llevar tu permiso de trabajo o tarjeta de residencia válidos.",
                "<strong>No lleves</strong> documentos de identidad o de inmigración falsos.",
                "<strong>No lleves</strong> documentos sobre tu país de origen. Pregúntale a un representante legal local qué documentos son seguros para llevar.",
            ], [
                "Carry a Red Card.",
                "Carry the phone number of someone who can put your plan into action and call your lawyer.",
                "If you have lawful status, you can carry your valid work permit or green card.",
                "<strong>Do not carry</strong> false identity or immigration documents.",
                "<strong>Do not carry</strong> documents about your country of origin. Ask a local legal representative which documents are safe to carry.",
            ]))),
            '<a class="btn primary" href="%s" rel="noopener noreferrer">%s</a>' % (
                E(SOURCES["ilrc_plan_es" if es else "ilrc_plan"][0], True),
                T("Plan de Preparación Familiar completo (ILRC)", "Full Family Preparedness Plan (ILRC)")),
            sources(lang, ["ilrc_plan", "ilrc_plan_es", "acluaz_work", "aclu"])))

    # 10 About
    sec("about", T("Sobre esta página", "About this page"),
        "<ul class=\"list\">%s</ul><div class=\"calls no-print\"><button type=\"button\" class=\"btn primary big js-print\">%s</button></div>" % (
            "".join("<li>%s</li>" % x for x in (T([
                "<strong>No es consejo legal.</strong> Es información general tomada de organizaciones establecidas y de sitios oficiales. Las leyes y las prácticas cambian. Habla con un abogado o un representante acreditado sobre tu caso.",
                "<strong>No recogemos datos.</strong> Esta página no tiene analíticas, anuncios, cookies, formularios ni cuentas, y no guarda nada.",
                "<strong>Los enlaces salen de este sitio.</strong> Los otros sitios tienen sus propias reglas de privacidad. Los botones de teléfono usan la aplicación de llamadas de tu teléfono.",
                "Cada enlace y cada teléfono se revisó el <time datetime=\"%s\">%s</time> en la página oficial de cada organización. Antes de ir a una oficina, llama para confirmar." % (CHECKED, CHECKED_TXT["es"]),
                "Esta página no está afiliada a ninguna de las organizaciones nombradas ni al gobierno.",
                "En un teléfono o computadora compartidos, el historial del navegador puede mostrar que visitaste esta página.",
                "Es gratis y siempre lo será.",
            ], [
                "<strong>This is not legal advice.</strong> It is general information taken from established organizations and official sites. Laws and practices change. Talk to a lawyer or an accredited representative about your case.",
                "<strong>We collect no data.</strong> This page has no analytics, ads, cookies, forms or accounts, and it saves nothing.",
                "<strong>Links leave this site.</strong> Other sites have their own privacy rules. Phone buttons use your phone's calling app.",
                "Every link and phone number was checked on <time datetime=\"%s\">%s</time> on each organization's official page. Before going to an office, call to confirm." % (CHECKED, CHECKED_TXT["en"]),
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
            "- State Bar of Arizona phone number for checking a lawyer's license: seen only on the ACLU of Arizona page, not on the State Bar's own page, so it is left out.",
            "- EOIR hotline number printed on the ACLU of Arizona page, (800) 568-5157: it differs from the number on EOIR's own page, so only EOIR's own number, 1-800-898-7180, is used.",
            "- Arizona State University immigration clinic: the page tried returned 404, left out.",
            "- Chicanos Por La Causa immigration services: its own page lists only Tucson, Somerton and Nogales offices and says it does not represent people in immigration court, so it is left out of a Phoenix-area list.",
            "- Arizona court form for delegating parental powers: not found on azcourts.gov tonight, so the site only says to ask a lawyer about a power of attorney.",
            "- Detention facility phone numbers shown on the Florence Project FAQ: that page still uses old facility names, so they are left out.",
            "", "## Notes for the reviewer", "",
            "- The Spanish text was written by an AI and needs a read by a native speaker before the site goes public.",
            "- ILRC red card files are linked on ilrc.org, not copied. ILRC's site says \"All rights reserved\" and has a reprint permission form.",
            "- The legal steps paraphrase the ACLU, ACLU of Arizona and ILRC pages in plain words. The sentences to say out loud are quoted from the ACLU page.",
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
