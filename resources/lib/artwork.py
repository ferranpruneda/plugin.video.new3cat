"""Local posters and fanart for menus, categories, letters and thematic channels.

Menu tiles are 2:3 posters only. Adult sections have no separate icons.
Main live channels keep the on-air picture and the official logo; this
module only supplies posters for the thematic (FAST) channels.
"""

from __future__ import annotations

import os
import re

ADDON_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Shipped files under resources/media. Tests compare the tree with this list.
SHIPPED_MEDIA = (
    "categories/fanart-actualitat.jpg",
    "categories/fanart-campus.jpg",
    "categories/fanart-cuines.jpg",
    "categories/fanart-cultura.jpg",
    "categories/fanart-documentals-i-reportatges.jpg",
    "categories/fanart-entreteniment.jpg",
    "categories/fanart-esports.jpg",
    "categories/fanart-eva.jpg",
    "categories/fanart-generic.jpg",
    "categories/fanart-musica.jpg",
    "categories/fanart-pellicules.jpg",
    "categories/fanart-series.jpg",
    "categories/poster-actualitat.png",
    "categories/poster-campus.png",
    "categories/poster-cuines.png",
    "categories/poster-cultura.png",
    "categories/poster-documentals-i-reportatges.png",
    "categories/poster-entreteniment.png",
    "categories/poster-esports.png",
    "categories/poster-eva.png",
    "categories/poster-generic.png",
    "categories/poster-musica.png",
    "categories/poster-pellicules.png",
    "categories/poster-series.png",
    "common/poster-fallback.png",
    "common/poster-next-page.png",
    "kids/banner.png",
    "kids/fanart.png",
    "kids/icon-age10.png",
    "kids/icon-age7.png",
    "kids/icon-ages.png",
    "kids/icon-highlights.png",
    "kids/icon-home.png",
    "kids/icon-live.png",
    "kids/icon-petits.png",
    "kids/icon-programmes.png",
    "kids/icon-tots.png",
    "kids/poster-age10.png",
    "kids/poster-age7.png",
    "kids/poster-ages.png",
    "kids/poster-highlights.png",
    "kids/poster-home.png",
    "kids/poster-live.png",
    "kids/poster-petits.png",
    "kids/poster-programmes.png",
    "kids/poster-tots.png",
    "letters/poster-all.png",
    "letters/poster-letter-a.png",
    "letters/poster-letter-b.png",
    "letters/poster-letter-c.png",
    "letters/poster-letter-d.png",
    "letters/poster-letter-e.png",
    "letters/poster-letter-f.png",
    "letters/poster-letter-g.png",
    "letters/poster-letter-h.png",
    "letters/poster-letter-hash.png",
    "letters/poster-letter-i.png",
    "letters/poster-letter-j.png",
    "letters/poster-letter-k.png",
    "letters/poster-letter-l.png",
    "letters/poster-letter-m.png",
    "letters/poster-letter-n.png",
    "letters/poster-letter-o.png",
    "letters/poster-letter-p.png",
    "letters/poster-letter-q.png",
    "letters/poster-letter-r.png",
    "letters/poster-letter-s.png",
    "letters/poster-letter-t.png",
    "letters/poster-letter-u.png",
    "letters/poster-letter-v.png",
    "letters/poster-letter-w.png",
    "letters/poster-letter-x.png",
    "letters/poster-letter-y.png",
    "letters/poster-letter-z.png",
    "letters/poster-letter.png",
    "live/poster-fast-beauties.png",
    "live/poster-fast-generic.png",
    "live/poster-fast-pucfc1.png",
    "live/poster-fast-pucfc2.png",
    "live/poster-fast-pucfc3.png",
    "live/poster-fast-pucfc4.png",
    "live/poster-fast-tem1.png",
    "live/poster-fast-tem2.png",
    "menu/fanart-categories.jpg",
    "menu/fanart-continue.jpg",
    "menu/fanart-latest.jpg",
    "menu/fanart-letters.jpg",
    "menu/fanart-live.jpg",
    "menu/fanart-rankings.jpg",
    "menu/fanart-search.jpg",
    "menu/fanart-voice.jpg",
    "menu/poster-categories.png",
    "menu/poster-continue.png",
    "menu/poster-latest.png",
    "menu/poster-letters.png",
    "menu/poster-live.png",
    "menu/poster-rankings.png",
    "menu/poster-search.png",
    "menu/poster-similar.png",
    "menu/poster-voice.png",
    "search/poster-programmes.png",
    "search/poster-videos.png",
)

# Folded shelf name -> one category. Longer or more specific markers first.
# A shelf that matches two categories keeps the rankings art.
_SHELF_MARKERS = (
    ("documentals-i-reportatges", ["documental"]),
    ("pellicules", ["pel ?licul"]),
    ("entreteniment", ["entreteniment"]),
    ("actualitat", ["actualitat"]),
    ("esports", ["(?:^| )esport"]),
    ("campus", ["campus"]),
    ("cultura", ["cultura"]),
    ("musica", ["musica"]),
    ("cuines", ["(?:^| )cuin"]),
    ("series", ["(?:^| )serie"]),
    ("sx3", ["sx3", "(?:^| )infantil(?: |$)"]),
    ("eva", ["(?:^| )eva(?: |$)"]),
)


def addon_path(*parts):
    return os.path.join(ADDON_ROOT, *parts)


def media_path(*parts):
    return addon_path("resources", "media", *parts)


def addon_fanart():
    return addon_path("fanart.jpg")


def poster_fallback():
    return media_path("common", "poster-fallback.png")


def next_page_art():
    return {"poster": media_path("common", "poster-next-page.png")}


def menu_art(action):
    """Poster and section fanart for one main-menu entry. No landscape, no icon file."""
    poster = media_path("menu", "poster-%s.png" % action)
    fanart = media_path("menu", "fanart-%s.jpg" % action)
    art = {"poster": poster}
    if os.path.isfile(fanart):
        art["fanart"] = fanart
    return art


def category_art(slug):
    """Poster and fanart for a category slug. Unknown slugs use the generic pair.

    SX3 reuses the Infantil home poster and background.
    """
    if slug == "sx3":
        return {
            "poster": media_path("kids", "poster-home.png"),
            "icon": media_path("kids", "icon-home.png"),
            "fanart": media_path("kids", "fanart.png"),
        }
    poster = media_path("categories", "poster-%s.png" % (slug or "generic"))
    fanart = media_path("categories", "fanart-%s.jpg" % (slug or "generic"))
    if not os.path.isfile(poster):
        poster = media_path("categories", "poster-generic.png")
        fanart = media_path("categories", "fanart-generic.jpg")
    elif not os.path.isfile(fanart):
        fanart = media_path("categories", "fanart-generic.jpg")
    return {"poster": poster, "fanart": fanart}


def letter_art(label):
    """Engraved milestone for # and A-Z. «Tots els programes» has its own poster."""
    if label == "#":
        name = "poster-letter-hash.png"
    elif label and len(label) == 1 and label.isalpha():
        name = "poster-letter-%s.png" % label.lower()
    else:
        name = "poster-all.png"
    path = media_path("letters", name)
    if not os.path.isfile(path):
        path = media_path("letters", "poster-letter.png")
    return {"poster": path, "fanart": media_path("menu", "fanart-letters.jpg")}


def search_art(kind):
    name = "poster-programmes.png" if kind == "program" else "poster-videos.png"
    return {
        "poster": media_path("search", name),
        "fanart": media_path("menu", "fanart-search.jpg"),
    }


def similar_art():
    return {
        "poster": media_path("menu", "poster-similar.png"),
        "fanart": media_path("menu", "fanart-continue.jpg"),
    }


def fast_poster(channel_id):
    """Thematic-channel poster, or the generic cabin when the id is new."""
    token = re.sub(r"[^a-z0-9]", "", (channel_id or "").lower())
    generic = media_path("live", "poster-fast-generic.png")
    if not token:
        return generic
    specific = media_path("live", "poster-fast-%s.png" % token)
    if os.path.isfile(specific):
        return specific
    return generic


def live_art(channel):
    """Keep main-channel art. Thematic channels use the local poster.

    Official logos stay on clearlogo and, when the API sent one, on icon.
    """
    art = dict((channel or {}).get("art") or {})
    if not (channel or {}).get("fast"):
        return art
    art["poster"] = fast_poster((channel or {}).get("id"))
    if art.get("clearlogo"):
        art["icon"] = art["clearlogo"]
    return art


def shelf_slug(name):
    """Category slug for a rankings row, or None when it is not exactly one category."""
    from resources.lib.matching import fold

    folded = fold(name)
    if not folded:
        return None
    hits = []
    for slug, patterns in _SHELF_MARKERS:
        if any(re.search(pattern, folded) for pattern in patterns):
            hits.append(slug)
    if len(hits) == 1:
        return hits[0]
    return None


def ranking_row_art(name):
    slug = shelf_slug(name)
    if slug:
        return category_art(slug)
    return menu_art("rankings")
