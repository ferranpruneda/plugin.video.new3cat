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
    "menu": "poster",
    "video": "widelist",
    "programme": "wall",
}
SECTION_DEFAULT_INDEX = {
    "menu": "1",
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


# Video window (MyVideoNav). The plugin records which section is on screen.
VIDEO_NAV_WINDOW = 10025
VIEW_SECTION_PROPERTY = "new3cat.section"
VIEW_APPLIED_PROPERTY = "new3cat.applied"
VIEW_PICKED_SETTING = {
    "menu": "view_picked_menu",
    "video": "view_picked_video",
    "programme": "view_picked_programme",
}
# v1.0.3 forced InfoWall on menus. A stored 54 is that default, not a
# later manual choice, until this epoch has been applied once.
MENU_VIEW_EPOCH = "1.0.4"
MENU_VIEW_EPOCH_SETTING = "view_menu_epoch"
OLD_MENU_FORCED_VIEW = ESTUARY_INFOWALL
SUPPRESS_MENU_VIEW_PROPERTY = "new3cat.suppress_menu_view"


def parse_viewmode(value):
    """Container.Viewmode as an int, or None when it is missing or a label."""
    text = str(value or "").strip()
    if not text.isdigit():
        return None
    number = int(text)
    if number < 1 or number > 9999:
        return None
    return number


def manual_view_update(previous_section, applied_view, current_viewmode, suppress_view=None):
    """Return (section, view id) when the visible view is not the one we set.

    previous_section and applied_view are what the plugin stored on the
    video window. current_viewmode is Container.Viewmode while that
    directory is still the one on screen. The same id means the user
    left the view alone. suppress_view skips the old forced menu id
    while an upgrade is still showing it.
    """
    if previous_section not in VIEW_PICKED_SETTING:
        return None
    current = parse_viewmode(current_viewmode)
    if current is None:
        return None
    if previous_section == "menu" and current == parse_viewmode(suppress_view):
        return None
    applied = parse_viewmode(applied_view)
    if applied is not None and current == applied:
        return None
    return (previous_section, current)


def migrate_picked_menu(saved, epoch):
    """Drop a stored InfoWall (54) left by v1.0.3, once.

    Returns (saved_value, epoch, suppress_view_id_or_None). Other saved
    ids, including a later manual 54, stay. An empty saved value is left
    empty so the new poster default is used while forcing is on.
    """
    if epoch == MENU_VIEW_EPOCH:
        return saved or "", epoch, None
    if parse_viewmode(saved) == OLD_MENU_FORCED_VIEW:
        return "", MENU_VIEW_EPOCH, OLD_MENU_FORCED_VIEW
    return saved or "", MENU_VIEW_EPOCH, None


def resolve_directory_view(skin_dir, force, default_view_id, saved_view_id):
    """View id to apply for this directory, or None to leave the skin alone.

    Forcing uses the section default, including after Back. Otherwise a
    view the user chose for this section type is applied again. With no
    saved choice the skin is not overwritten. Other skins are never forced.
    """
    if not str(skin_dir or "").startswith("skin.estuary"):
        return None
    if force:
        return default_view_id
    return parse_viewmode(saved_view_id)


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


def fill_art(art, fallback="", fanart_fallback=""):
    """Make sure a wall or poster has an image even if the API sent only one.

    fallback is the poster used when the item has no picture at all.
    fanart_fallback is the wide background used when the item has no fanart.
    """
    filled = {key: value for key, value in (art or {}).items() if value}
    picture = (
        filled.get("poster")
        or filled.get("thumb")
        or filled.get("icon")
        or filled.get("landscape")
        or filled.get("fanart")
        or fallback
    )
    wide = filled.get("fanart") or filled.get("landscape") or filled.get("banner") or fanart_fallback or picture
    if picture:
        filled.setdefault("poster", picture)
        filled.setdefault("thumb", picture)
        filled.setdefault("icon", picture)
    if wide:
        filled.setdefault("fanart", wide)
        filled.setdefault("landscape", wide)
        filled.setdefault("banner", wide)
    return filled
