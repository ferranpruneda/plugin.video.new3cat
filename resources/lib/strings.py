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


def category_title(slug, api_title=""):
    """Catalan label for a known section. Unknown sections keep the API name."""
    if slug in CATEGORY_TITLES:
        return CATEGORY_TITLES[slug]
    title = (api_title or "").replace("*", "").strip()
    return title or (slug or "")
