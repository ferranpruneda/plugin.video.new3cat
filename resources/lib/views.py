"""Default views for Kodi's Estuary skin, chosen per kind of page.

Verified on the Nexus (Kodi 20) and Omega (Kodi 21) branches of
xbmc/xbmc, file addons/skin.estuary/xml/MyVideoNav.xml. Both list the
same view ids:

    <views>50,51,52,53,54,55,500,501,502</views>

and include View_54_InfoWall and View_55_WideList.

InfoWall is control id 54 (View_54_InfoWall.xml, panel id="54"). Its
items are visible for videos, tvshows, seasons, episodes and movies
(also music, images and games). WideList is control id 55
(View_55_WideList.xml, fixedlist id="55") and lays out tvshows,
seasons, episodes, movies, videos and games. Wall is 500. Poster is
51 and only for movies, sets, tvshows, seasons and games, so a poster
choice on any other list falls back to the wall.
"""

from __future__ import annotations

ESTUARY_WALL = 500
ESTUARY_POSTER = 51
ESTUARY_INFOWALL = 54
ESTUARY_WIDELIST = 55

POSTER_CONTENT = frozenset({"movies", "sets", "tvshows", "seasons", "games"})

# Same order as the settings lvalues: Mur, Pòster, Mur amb informació, Llista ampla.
VIEW_CHOICES = ("wall", "poster", "infowall", "widelist")
VIEW_TYPES = frozenset(VIEW_CHOICES)
VIEW_IDS = {
    "wall": ESTUARY_WALL,
    "poster": ESTUARY_POSTER,
    "infowall": ESTUARY_INFOWALL,
    "widelist": ESTUARY_WIDELIST,
}

# addon setting id, and the enum index used when the user has not chosen one.
SECTION_SETTING = {
    "menu": "view_menus",
    "video": "view_videos",
    "programme": "view_programmes",
}
SECTION_DEFAULTS = {
    "menu": "infowall",
    "video": "widelist",
    "programme": "wall",
}
SECTION_DEFAULT_INDEX = {
    "menu": "2",
    "video": "3",
    "programme": "0",
}


def section_view(section, setting_value):
    """View name for a page kind. An empty setting uses that kind's default."""
    default_name = SECTION_DEFAULTS.get(section, "wall")
    if setting_value is None or str(setting_value).strip() == "":
        return default_name
    return _choice_at(setting_value, default_name)


def directory_content(section, content):
    """Content type passed to the directory.

    Estuary InfoWall (control 54) picks the tile from Container.Content.
    On Kodi 21 Omega and Kodi 20 Nexus, View_54_InfoWall.xml is the same
    shape: videos and episodes use InfoWallEpisodeLayout, a 316 by 218
    landscape image that still prefers ListItem.Art(poster) through
    InfoWallThumbVar. Tvshows, movies and seasons use InfoWallMovieLayout,
    which draws that poster at 290 by 415 with aspectratio scale. Menu
    pages therefore use tvshows so a 2:3 poster is not fitted into the
    landscape slot. Video lists and programme lists keep their own type.
    """
    if section == "menu":
        return "tvshows"
    return content or ""


def listing_section(content):
    """Programme directories keep the programme view.

    Episodes, films, clips and mixed results are video lists. A season
    directory is not passed here: those pages use the programme view.
    """
    if content == "tvshows":
        return "programme"
    return "video"


def estuary_view_id(skin_dir, force, view_type, content):
    """Return an Estuary view id, or None when the view must not be forced.

    Other skins keep their own view. A poster request on a list Estuary cannot
    show as posters (live channels, episodes, mixed videos) uses the wall.
    """
    if not force:
        return None
    if not str(skin_dir or "").startswith("skin.estuary"):
        return None
    choice = view_type if view_type in VIEW_TYPES else "wall"
    if choice == "poster" and content not in POSTER_CONTENT:
        return ESTUARY_WALL
    return VIEW_IDS[choice]


def _choice_at(value, default_name):
    try:
        index = int(value)
    except (TypeError, ValueError):
        return default_name
    if index < 0 or index >= len(VIEW_CHOICES):
        return default_name
    return VIEW_CHOICES[index]


def fill_art(art, fallback=""):
    """Make sure a wall or poster has an image even if the API sent only one."""
    filled = {key: value for key, value in (art or {}).items() if value}
    picture = (
        filled.get("poster")
        or filled.get("thumb")
        or filled.get("icon")
        or filled.get("landscape")
        or filled.get("fanart")
        or fallback
    )
    wide = filled.get("fanart") or filled.get("landscape") or filled.get("banner") or picture
    if picture:
        filled.setdefault("poster", picture)
        filled.setdefault("thumb", picture)
        filled.setdefault("icon", picture)
    if wide:
        filled.setdefault("fanart", wide)
        filled.setdefault("landscape", wide)
        filled.setdefault("banner", wide)
    return filled
