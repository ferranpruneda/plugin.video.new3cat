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
