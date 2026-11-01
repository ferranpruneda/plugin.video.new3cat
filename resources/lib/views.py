"""Default poster and wall views for Kodi's Estuary skin.

Verified in skin.estuary MyVideoNav.xml on the Nexus (Kodi 20) and Omega
(Kodi 21) branches: the window lists views 50, 51, 52, 53, 54, 55, 500, 501
and 502. Wall is control 500 and Poster is control 51. InfoWall is 54.

Wall and InfoWall are allowed for movies, tvshows, seasons, episodes and the
generic "videos" type. Poster is only allowed for movies, sets, tvshows,
seasons and games, so other lists fall back to the wall.
"""

from __future__ import annotations

ESTUARY_WALL = 500
ESTUARY_POSTER = 51
ESTUARY_INFOWALL = 54

POSTER_CONTENT = frozenset({"movies", "sets", "tvshows", "seasons", "games"})

VIEW_TYPES = ("wall", "poster", "infowall")


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
    return {"wall": ESTUARY_WALL, "poster": ESTUARY_POSTER, "infowall": ESTUARY_INFOWALL}[choice]


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
