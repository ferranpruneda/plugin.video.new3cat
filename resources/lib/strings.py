"""UI strings for the addon.

Kodi translates strings.po with the interface language, so a Spanish Kodi
would show Spanish menus. These tables are what the addon actually displays:
Catalan unless the user asks to follow Kodi's language.
"""

from __future__ import annotations

# Stable names for the sections on 3cat.cat. The JSON is Catalan today; this
# map keeps the buttons in Catalan if a response ever arrives in another language.
CATEGORY_TITLES = {
    "actualitat": "Actualitat",
    "campus": "Campus",
    "cuines": "Cuines",
    "cultura": "Cultura i divulgació",
    "documentals-i-reportatges": "Documentals",
    "entreteniment": "Entreteniment",
    "esports": "Esports",
    "eva": "EVA",
    "musica": "Música",
    "pellicules": "Pel·lícules",
    "series": "Sèries",
    "sx3": "SX3",
}

STRINGS = {
    "ca": {
        30100: "Directes",
        30101: "El més vist",
        30102: "Novetats",
        30103: "Categories",
        30104: "Catàleg",
        30105: "Cerca",
        30106: "Pàgina següent (%s/%s)",
        30109: "Temporada %s",
        30110: "Capítol %s",
        30112: "No hi ha resultats.",
        30113: "Aquest contingut no està disponible.",
        30114: "Aquest contingut pot estar limitat a Catalunya o a Espanya.",
        30115: "Aquest vídeo està protegit amb DRM i no es pot reproduir.",
        30116: "No s'ha pogut connectar amb 3Cat. Torna-ho a provar.",
        30117: "Cal el complement inputstream.adaptive per reproduir aquest format.",
        30118: "Tots els programes",
        30119: "Cerca de programes",
        30120: "Cerca de vídeos",
        30121: "Text a cercar",
        30123: "Aquesta secció no està disponible.",
        30124: "Directe",
        30125: "Temporada",
        30130: "Infantil",
        30131: "SX3 en directe",
        30132: "Programes del SX3",
        30133: "Per edats",
        30134: "Els més petits",
        30135: "Tots els públics",
        30136: "A partir de 7 anys",
        30137: "A partir de 10 anys",
        30138: "Destacats del SX3",
        30139: "Racó dels petits: el SX3 en directe i els programes infantils.",
        30140: "El canal infantil SX3, en directe.",
        30141: "Programes emesos al canal SX3.",
        30142: "Classificació per edat: el codi Infantil i les franges del canal SX3.",
        30143: "Programes amb el codi ètic Infantil de 3Cat.",
        30144: "Programes del SX3 marcats com a tots els públics.",
        30145: "Programes del SX3 recomanats a partir de 7 anys.",
        30146: "Programes del SX3 recomanats a partir de 10 anys.",
        30147: "Files destacades del web del SX3.",
        30150: "Cerca per veu",
        30151: "Prem el micròfon del teclat o del comandament i digues el programa.",
        30152: "Continua mirant",
        30153: "Et pot agradar",
        30154: "Encara no has mirat res en aquest dispositiu.",
        30155: "Historial esborrat. Només estava en aquest dispositiu.",
        30156: "Reprèn a %s",
        30157: "L'historial està desactivat en aquest dispositiu.",
        30160: "Els canals de televisió que ara mateix són en antena.",
        30161: "Les files del que més s'ha mirat: sèries, pel·lícules, documentals i més.",
        30162: "Els vídeos que s'acaben de publicar al web.",
        30163: "Les seccions del web, de les sèries als esports i a la cultura.",
        30164: "Tots els programes, o només els d'una lletra.",
        30165: "Escriu un títol i tria si busques programes o vídeos.",
        30166: "Dicta un títol amb el micròfon del teclat o del comandament.",
        30167: "El que has començat a veure en aquest aparell, per reprendre-ho.",
        30168: "El catàleg sencer, sense filtrar per la lletra inicial.",
        30169: "Programes el títol dels quals comença per un número o un signe.",
        30170: "Programes el títol dels quals comença per %s.",
        30171: "Programes que coincideixen amb «%s».",
        30172: "Vídeos i capítols que coincideixen amb «%s».",
        30173: "Programes i vídeos de la secció «%s».",
        30174: "Programes aplegats a «%s».",
        30175: "Els canals en directe d'aquesta secció.",
        30176: "Les categories que pengen d'aquesta secció.",
        30177: "Canals temàtics que emeten en directe.",
        30178: "Altres programes de la mateixa temàtica que els que has mirat.",
        30179: "Emissió en directe d'aquest canal.",
        30180: "Informatius, entrevistes i el que està passant.",
        30181: "Continguts per aprendre i per a l'escola.",
        30182: "Receptes, cuiners i programes de cuina.",
        30183: "Cultura, divulgació i programes per entendre el món.",
        30184: "Documentals i reportatges per mirar sencers.",
        30185: "Programes d'entreteniment, humor i varietats.",
        30186: "Competicions, retransmissions i programes d'esport.",
        30187: "Concerts, sessions i programes de música.",
        30188: "Pel·lícules i telefilms del catàleg.",
        30189: "Sèries de ficció, amb les temporades i els capítols.",
        30190: "Sèries i programes del canal infantil SX3.",
        30191: "Vídeos aplegats a «%s».",
        30192: "La classificació «%s».",
        30193: "El destacat «%s».",
        30194: "Continguts aplegats a «%s».",
    },
    "es": {
        30100: "Directos",
        30101: "Lo más visto",
        30102: "Novedades",
        30103: "Categorías",
        30104: "Catálogo",
        30105: "Buscar",
        30106: "Página siguiente (%s/%s)",
        30109: "Temporada %s",
        30110: "Capítulo %s",
        30112: "No hay resultados.",
        30113: "Este contenido no está disponible.",
        30114: "Este contenido puede estar limitado a Cataluña o a España.",
        30115: "Este vídeo está protegido con DRM y no se puede reproducir.",
        30116: "No se ha podido conectar con 3Cat. Inténtalo de nuevo.",
        30117: "Hace falta el complemento inputstream.adaptive para reproducir este formato.",
        30118: "Todos los programas",
        30119: "Buscar programas",
        30120: "Buscar vídeos",
        30121: "Texto a buscar",
        30123: "Esta sección no está disponible.",
        30124: "Directo",
        30125: "Temporada",
        30130: "Infantil",
        30131: "SX3 en directo",
        30132: "Programas del SX3",
        30133: "Por edades",
        30134: "Los más pequeños",
        30135: "Todos los públicos",
        30136: "A partir de 7 años",
        30137: "A partir de 10 años",
        30138: "Destacados del SX3",
        30139: "Rincón de los pequeños: el SX3 en directo y los programas infantiles.",
        30140: "El canal infantil SX3, en directo.",
        30141: "Programas emitidos en el canal SX3.",
        30142: "Clasificación por edad: el código Infantil y las franjas del canal SX3.",
        30143: "Programas con el código ético Infantil de 3Cat.",
        30144: "Programas del SX3 marcados como todos los públicos.",
        30145: "Programas del SX3 recomendados a partir de 7 años.",
        30146: "Programas del SX3 recomendados a partir de 10 años.",
        30147: "Filas destacadas de la web del SX3.",
        30150: "Buscar por voz",
        30151: "Pulsa el micrófono del teclado o del mando y di el programa.",
        30152: "Seguir viendo",
        30153: "Te puede gustar",
        30154: "Todavía no has visto nada en este dispositivo.",
        30155: "Historial borrado. Solo estaba en este dispositivo.",
        30156: "Seguir en %s",
        30157: "El historial está desactivado en este dispositivo.",
        30160: "Los canales de televisión que están emitiendo ahora.",
        30161: "Las filas de lo más visto: series, películas, documentales y más.",
        30162: "Los vídeos que se acaban de publicar en la web.",
        30163: "Las secciones de la web, de las series a los deportes y la cultura.",
        30164: "Todos los programas, o solo los de una letra.",
        30165: "Escribe un título y elige si buscas programas o vídeos.",
        30166: "Dicta un título con el micrófono del teclado o del mando.",
        30167: "Lo que has empezado a ver en este aparato, para retomarlo.",
        30168: "El catálogo entero, sin filtrar por la letra inicial.",
        30169: "Programas cuyo título empieza por un número o un signo.",
        30170: "Programas cuyo título empieza por %s.",
        30171: "Programas que coinciden con «%s».",
        30172: "Vídeos y capítulos que coinciden con «%s».",
        30173: "Programas y vídeos de la sección «%s».",
        30174: "Programas reunidos en «%s».",
        30175: "Los canales en directo de esta sección.",
        30176: "Las categorías de esta sección.",
        30177: "Canales temáticos que emiten en directo.",
        30178: "Otros programas de la misma temática que los que has visto.",
        30179: "Emisión en directo de este canal.",
        30180: "Informativos, entrevistas y lo que está pasando.",
        30181: "Contenidos para aprender y para la escuela.",
        30182: "Recetas, cocineros y programas de cocina.",
        30183: "Cultura, divulgación y programas para entender el mundo.",
        30184: "Documentales y reportajes para ver enteros.",
        30185: "Programas de entretenimiento, humor y variedades.",
        30186: "Competiciones, retransmisiones y programas de deporte.",
        30187: "Conciertos, sesiones y programas de música.",
        30188: "Películas y telefilmes del catálogo.",
        30189: "Series de ficción, con las temporadas y los capítulos.",
        30190: "Series y programas del canal infantil SX3.",
        30191: "Vídeos reunidos en «%s».",
        30192: "La clasificación «%s».",
        30193: "El destacado «%s».",
        30194: "Contenidos reunidos en «%s».",
    },
    "en": {
        30100: "Live TV",
        30101: "Most watched",
        30102: "Latest",
        30103: "Categories",
        30104: "Catalog",
        30105: "Search",
        30106: "Next page (%s/%s)",
        30109: "Season %s",
        30110: "Episode %s",
        30112: "No results.",
        30113: "This video is not available.",
        30114: "This stream may only play in Catalonia or Spain.",
        30115: "This video is DRM-protected and cannot be played.",
        30116: "Could not reach 3Cat. Try again.",
        30117: "inputstream.adaptive is required to play this format.",
        30118: "All programmes",
        30119: "Search programmes",
        30120: "Search videos",
        30121: "Search text",
        30123: "This section is not available.",
        30124: "Live",
        30125: "Season",
        30130: "Kids",
        30131: "SX3 live",
        30132: "SX3 programmes",
        30133: "By age",
        30134: "The youngest",
        30135: "All audiences",
        30136: "From age 7",
        30137: "From age 10",
        30138: "SX3 highlights",
        30139: "For children: SX3 live and programmes marked for kids.",
        30140: "The SX3 children's channel, live.",
        30141: "Programmes shown on the SX3 channel.",
        30142: "Age bands: the Infantil rating and the SX3 channel ratings.",
        30143: "Programmes with 3Cat's Infantil rating.",
        30144: "SX3 programmes rated suitable for all audiences.",
        30145: "SX3 programmes recommended from age 7.",
        30146: "SX3 programmes recommended from age 10.",
        30147: "Highlighted rows from the SX3 website.",
        30150: "Voice search",
        30151: "Press the microphone on the keyboard or remote and say the programme.",
        30152: "Continue watching",
        30153: "You may like",
        30154: "Nothing has been watched on this device yet.",
        30155: "History cleared. It was only stored on this device.",
        30156: "Resume at %s",
        30157: "Watch history is turned off on this device.",
        30160: "Television channels that are on the air right now.",
        30161: "Rows of what people watch most: series, films, documentaries and more.",
        30162: "Videos just published on the website.",
        30163: "The website sections, from series to sport and culture.",
        30164: "Every programme, or only those under one letter.",
        30165: "Type a title and choose programmes or videos.",
        30166: "Say a title with the keyboard or remote microphone.",
        30167: "What you have started on this device, so you can pick it up again.",
        30168: "The whole catalogue, not filtered by the first letter.",
        30169: "Programmes whose title starts with a number or a symbol.",
        30170: "Programmes whose title starts with %s.",
        30171: "Programmes that match «%s».",
        30172: "Videos and episodes that match «%s».",
        30173: "Programmes and videos in the «%s» section.",
        30174: "Programmes gathered under «%s».",
        30175: "Live channels in this section.",
        30176: "The categories under this section.",
        30177: "Thematic channels that are broadcasting live.",
        30178: "Other programmes in the same theme as the ones you have watched.",
        30179: "This channel's live broadcast.",
        30180: "News, interviews and what is happening now.",
        30181: "Programmes for learning and for school.",
        30182: "Recipes, cooks and cooking shows.",
        30183: "Culture, explainers and programmes about the world.",
        30184: "Documentaries and reports to watch in full.",
        30185: "Entertainment, comedy and variety shows.",
        30186: "Competitions, live sport and sports programmes.",
        30187: "Concerts, sessions and music programmes.",
        30188: "Films and TV movies in the catalogue.",
        30189: "Fiction series, with their seasons and episodes.",
        30190: "Series and programmes from the SX3 children's channel.",
        30191: "Videos gathered under «%s».",
        30192: "The chart «%s».",
        30193: "The highlight «%s».",
        30194: "Items gathered under «%s».",
    },
}


def language_code(code):
    """Map a Kodi language tag to ca, es or en. Anything else stays Catalan."""
    primary = (code or "").lower().replace("_", "-").split("-", 1)[0]
    if primary in STRINGS:
        return primary
    return "ca"


def text(string_id, follow_kodi=False, kodi_language="ca"):
    lang = language_code(kodi_language) if follow_kodi else "ca"
    table = STRINGS.get(lang) or STRINGS["ca"]
    return table.get(string_id) or STRINGS["ca"].get(string_id, "")


# Root menu action -> description. The title ids stay 30100 and neighbours.
ROOT_MENU_PLOTS = {
    "live": 30160,
    "rankings": 30161,
    "latest": 30162,
    "categories": 30163,
    "letters": 30164,
    "search": 30165,
    "voice": 30166,
    "continue": 30167,
}

CATEGORY_PLOT_IDS = {
    "actualitat": 30180,
    "campus": 30181,
    "cuines": 30182,
    "cultura": 30183,
    "documentals-i-reportatges": 30184,
    "entreteniment": 30185,
    "esports": 30186,
    "musica": 30187,
    "pellicules": 30188,
    "series": 30189,
    "sx3": 30190,
}

_SHELF_PLOT_IDS = {
    "PROGRAMES": 30174,
    "VIDEOS": 30191,
    "RANQUING": 30192,
    "DESTACAT": 30193,
}


def _same_text(left, right):
    return (left or "").strip().casefold() == (right or "").strip().casefold()


def category_plot(slug, api_plot="", title="", follow_kodi=False, kodi_language="ca"):
    """Description for a category folder. The API text wins when it says more than the title."""
    cleaned = (api_plot or "").strip()
    known = category_title(slug, "")
    if cleaned and not _same_text(cleaned, title) and not _same_text(cleaned, known):
        return cleaned
    string_id = CATEGORY_PLOT_IDS.get(slug)
    if string_id:
        written = text(string_id, follow_kodi=follow_kodi, kodi_language=kodi_language)
        if written:
            return written
    label = (title or known or slug or "3Cat").strip()
    return text(30173, follow_kodi=follow_kodi, kodi_language=kodi_language) % label


def folder_plot(api_plot, name, tipus, translate):
    """Description for one folder inside a menu of folders. Never empty."""
    cleaned = (api_plot or "").strip()
    if cleaned and not _same_text(cleaned, name):
        return cleaned
    kind = (tipus or "").upper()
    if kind == "DIRECTES":
        return translate(30175)
    if kind == "TEMATIQUES":
        return translate(30176)
    if kind == "FAST_CHANNEL":
        return translate(30177)
    label = (name or "").strip()
    if not label:
        return translate(30175)
    return translate(_SHELF_PLOT_IDS.get(kind, 30194)) % label


def letter_plot(label, translate):
    """Description for one entry of the A-Z index."""
    if label == "#":
        return translate(30169)
    if label and len(label) == 1:
        return translate(30170) % label.upper()
    return translate(30168)


def search_plot(kind, query, translate):
    """Description for the programmes/videos choice after a search."""
    string_id = 30171 if kind == "program" else 30172
    return translate(string_id) % (query or "")


def category_title(slug, api_title=""):
    """Catalan label for a known section. Unknown sections keep the API name."""
    if slug in CATEGORY_TITLES:
        return CATEGORY_TITLES[slug]
    title = (api_title or "").replace("*", "").strip()
    return title or (slug or "")
