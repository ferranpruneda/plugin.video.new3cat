"""Pure helpers for 3Cat JSON: artwork, durations, listings and stream choice.

Nothing in this module imports Kodi or touches the network. Stream selection
only returns URLs the API already exposes. It never requests a DRM license.
"""

from __future__ import annotations

import html
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


_TAG = re.compile(r"<[^>]+>")
_SPACE = re.compile(r"\s+")
_DIMS = re.compile(r"(\d+)\s*x\s*(\d+)", re.I)
_HEIGHT = re.compile(r"(\d{3,4})\s*p", re.I)
_EPISODE_CODE = re.compile(r"T\d+xC\d+", re.I)
_SEASON_ID = re.compile(r"(\d+)$")

ALLOWED_HOSTS = frozenset(
    {
        "api.3cat.cat",
        "api.ccma.cat",
        "statics.3cat.cat",
        "api-media.3cat.cat",
        "api-media.ccma.cat",
        "dinamics.ccma.cat",
    }
)

# When the viewer's region has no exact match, try a wider signal first.
_GEO_FALLBACK = {
    "CATALUNYA": ("TOTS", "ESPANYA"),
    "ESPANYA": ("TOTS", "CATALUNYA"),
    "TOTS": ("ESPANYA", "CATALUNYA"),
    "ANDORRA": ("TOTS", "ESPANYA", "CATALUNYA"),
}

_DRM_TOKENS = ("widevine", "playready", "clearkey", "skd:", "contentprotection")


def clean_text(value):
    if not value:
        return ""
    text = html.unescape(_TAG.sub(" ", str(value)))
    text = text.replace("\xa0", " ")
    return _SPACE.sub(" ", text).strip()


def clean_title(value):
    return clean_text(value).replace("*", "").strip()


def parse_duration(value):
    """Return seconds. Accepts HH:MM:SS[:FF], a media dict, or a number of seconds."""
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, dict):
        millis = value.get("milisegons")
        if isinstance(millis, (int, float)):
            return int(millis / 1000)
        return parse_duration(value.get("text"))
    parts = str(value).strip().split(":")
    if len(parts) < 3:
        return None
    try:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(float(parts[2]))
    except ValueError:
        return None
    return hours * 3600 + minutes * 60 + seconds


def parse_date(value):
    """Normalize DD/MM/YYYY or ISO dates to YYYY-MM-DD."""
    if not value:
        return None
    text = str(value).strip()
    match = re.match(r"(\d{2})/(\d{2})/(\d{4})", text)
    if match:
        day, month, year = match.groups()
        return "%s-%s-%s" % (year, month, day)
    match = re.match(r"(\d{4}-\d{2}-\d{2})", text)
    if match:
        return match.group(1)
    return None


def year_of(premiered):
    if premiered and len(premiered) >= 4 and premiered[:4].isdigit():
        return int(premiered[:4])
    return None


def season_number(season_id):
    if not season_id:
        return None
    match = _SEASON_ID.search(str(season_id))
    if not match:
        return None
    return int(match.group(1))


def as_list(value):
    """Normalize the API's item / single-object / letter-group shapes."""
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        letters = value.get("lletra")
        nested = value.get("item")
        if isinstance(letters, list) and not isinstance(nested, list):
            items = []
            for group in letters:
                if isinstance(group, dict):
                    items.extend(as_list(group.get("item")))
            return items
        # Listing containers are {"num", "item"} or {"valor", "item"}.
        # A normal programme never uses "item" as its only payload key.
        if isinstance(nested, list) and set(value) <= {"item", "num", "lletra", "valor"}:
            return as_list(nested)
        if isinstance(nested, dict) and "num" in value:
            return [nested]
        return [value]
    return []


def _dims(mida):
    if not mida:
        return None
    match = _DIMS.search(str(mida))
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def _image_score(image):
    mida = str(image.get("mida") or "")
    rel = str(image.get("rel_name") or "").lower()
    dims = _dims(mida)
    if mida.upper() == "MASTER" or mida == "":
        score = 5000000
    elif dims:
        score = dims[0] * dims[1]
    else:
        score = 1
    if any(token in rel for token in ("imatge_169", "169", "keyvideo")):
        score += 1000000
    if "1014" in mida or "1920" in mida:
        score += 100000
    return score


def art_from_images(images):
    """Pick poster, landscape, thumb and clearlogo URLs from an imatges array."""
    posters = []
    landscapes = []
    logos = []
    for image in images or []:
        if not isinstance(image, dict):
            continue
        url = image.get("text") or image.get("url")
        if not url or not str(url).startswith("http"):
            continue
        rel = str(image.get("rel_name") or "").lower()
        dims = _dims(image.get("mida"))
        score = _image_score(image)
        if "logo" in rel and "iptv" not in rel and "bravia" not in rel:
            logos.append((score, url))
            continue
        portrait = bool(dims and dims[1] > dims[0] * 1.15)
        if "poster" in rel or portrait:
            posters.append((score, url))
        else:
            landscapes.append((score, url))

    def best(pairs):
        if not pairs:
            return None
        pairs.sort(key=lambda item: item[0], reverse=True)
        return pairs[0][1]

    landscape = best(landscapes)
    poster = best(posters) or landscape
    logo = best(logos)
    art = {}
    if landscape:
        art["thumb"] = landscape
        art["fanart"] = landscape
        art["landscape"] = landscape
    if poster:
        art["poster"] = poster
        if "thumb" not in art:
            art["thumb"] = poster
    if logo:
        art["clearlogo"] = logo
    return art


def plot_of(item):
    for key in ("entradeta", "descripcio", "sinopsi", "entradeta_promo"):
        text = clean_text((item or {}).get(key))
        if text:
            return text
    return ""


def rating_of(item):
    for entry in (item or {}).get("codis_etics") or []:
        if isinstance(entry, dict) and entry.get("desc"):
            return clean_text(entry["desc"])
    return ""


def genres_of(item):
    genres = []
    for key in ("tematiques", "formats"):
        for entry in (item or {}).get(key) or []:
            if isinstance(entry, dict) and entry.get("desc"):
                label = clean_text(entry["desc"])
                if label and label not in genres:
                    genres.append(label)
    return genres


def is_film(item):
    for entry in (item or {}).get("formats") or []:
        if not isinstance(entry, dict):
            continue
        code = str(entry.get("id") or "")
        label = str(entry.get("desc") or "").lower()
        if code == "PUFF_FILM" or "pel·l" in label or "pelic" in label or "telefilm" in label:
            return True
    return False


def classify(item):
    """Return program, video or skip."""
    if not isinstance(item, dict):
        return "skip"
    typology = str(item.get("tipologia") or "").upper()
    if any(token in typology for token in ("NOTICIA", "NOT_", "AUDIO", "RADIO", "PODCAST")):
        return "skip"
    if typology == "PTVC_PROGRAMA":
        return "program"
    if "VIDEO" in typology or item.get("durada"):
        return "video"
    if item.get("nombonic") and item.get("titol"):
        return "program"
    if item.get("id") and item.get("titol"):
        return "program"
    return "skip"


def is_generic_episode_title(title):
    return bool(_EPISODE_CODE.fullmatch(clean_title(title)))


def present_item(item):
    kind = classify(item)
    title = clean_title(item.get("titol") or "")
    premiered = parse_date(item.get("data_emissio") or item.get("data_publicacio"))
    episode = item.get("capitol_temporada")
    if episode in (None, ""):
        episode = item.get("capitol")
    try:
        episode = int(episode) if episode not in (None, "") else None
    except (TypeError, ValueError):
        episode = None
    seasons = item.get("temporades") or []
    season = None
    if seasons and isinstance(seasons[0], dict):
        season = season_number(seasons[0].get("id"))
    show = clean_text(item.get("programa") or item.get("avantitol") or "")
    return {
        "kind": kind,
        "id": item.get("id"),
        "title": title,
        "generic_episode": kind == "video" and is_generic_episode_title(title),
        "plot": plot_of(item),
        "art": art_from_images(item.get("imatges")),
        "duration": parse_duration(item.get("durada")),
        "premiered": premiered,
        "year": year_of(premiered),
        "season": season,
        "episode": episode,
        "show": show,
        "film": is_film(item),
        "mpaa": rating_of(item),
        "genres": genres_of(item),
    }


def keep_shelf(row):
    if not isinstance(row, dict):
        return False
    tipus = str(row.get("tipus") or "").upper()
    name = clean_title(row.get("nom") or "").lower()
    fmt = str(row.get("format") or "").upper()
    if tipus in ("PROGRAMES_RADIO", "ESTAS_VEIENT"):
        return False
    if fmt == "QUADRAT":
        return False
    if any(token in name for token in ("escoltat", "pòdcast", "podcast", "ràdio", "radio", "àudio", "audio")):
        return False
    if tipus in ("DIRECTES", "FAST_CHANNEL", "TEMATIQUES"):
        return True
    return bool(row.get("url_dades"))


def allowed_url(url):
    try:
        parts = urlsplit(url)
    except ValueError:
        return False
    return parts.scheme == "https" and parts.hostname in ALLOWED_HOSTS


def ensure_params(url):
    parts = urlsplit(url)
    pairs = parse_qsl(parts.query, keep_blank_values=True)
    keys = {key for key, _ in pairs}
    for key, value in (
        ("_format", "json"),
        ("sdom", "img"),
        ("version", "2.0"),
        ("https", "true"),
        ("master", "yes"),
    ):
        if key not in keys:
            pairs.append((key, value))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(pairs), ""))


def with_page(url, page):
    parts = urlsplit(url)
    pairs = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True) if key != "pagina"]
    pairs.append(("pagina", str(page)))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(pairs), ""))


def _protocol(entry):
    label = str(entry.get("label") or "")
    fmt = str(entry.get("format") or "")
    file_url = str(entry.get("file") or "").split("?", 1)[0].lower()
    upper = (label + " " + fmt).upper()
    if label.upper() == "DASH" or file_url.endswith(".mpd") or "DASH" in upper:
        return "mpd"
    if "HLS" in upper or file_url.endswith(".m3u8"):
        return "hls"
    if file_url.endswith(".mp4") or _HEIGHT.search(label):
        return "mp4"
    if fmt.upper() == "MP4":
        return "mp4"
    return "other"


def _height(entry):
    match = _HEIGHT.search(str(entry.get("label") or ""))
    if match:
        return int(match.group(1))
    return 0


def _is_drm(entry):
    blob = " ".join(
        str(entry.get(key) or "") for key in ("file", "format", "label", "drm", "license")
    ).lower()
    return any(token in blob for token in _DRM_TOKENS)


def iter_media(media):
    """Yield flat {geo, format, label, file, active} entries from live or VOD payloads."""
    if isinstance(media, list):
        for entry in media:
            yield from iter_media(entry)
        return
    if not isinstance(media, dict):
        return
    url = media.get("url")
    geo = media.get("geo")
    if isinstance(url, list):
        for part in url:
            if not isinstance(part, dict):
                continue
            yield {
                "geo": geo,
                "format": part.get("label") or media.get("format"),
                "label": part.get("label") or "",
                "file": part.get("file") or "",
                "active": part.get("active", True),
            }
        return
    if isinstance(url, str) and url:
        yield {
            "geo": geo,
            "format": media.get("format"),
            "label": media.get("format") or "",
            "file": url,
            "active": True,
        }


def _geo_rank(entry_geo, user_geo):
    entry_geo = (entry_geo or "").upper()
    user_geo = (user_geo or "TOTS").upper()
    if entry_geo == user_geo:
        return 0
    order = _GEO_FALLBACK.get(user_geo, ("TOTS", "ESPANYA", "CATALUNYA"))
    if entry_geo in order:
        return 1 + order.index(entry_geo)
    return 99


def choose_stream(media, user_geo, mode="auto"):
    """Pick one playable URL.

    `mode` is auto, dash or mp4. DASH and HLS here are the clear manifests the
    media endpoint already returns. Entries that look like DRM are ignored.
    Returns None when nothing clear is available.
    """
    entries = []
    for entry in iter_media(media):
        if not entry.get("file") or _is_drm(entry):
            continue
        proto = _protocol(entry)
        if proto == "other":
            continue
        item = dict(entry)
        item["protocol"] = proto
        item["height"] = _height(entry)
        item["rank"] = _geo_rank(entry.get("geo"), user_geo)
        entries.append(item)
    if not entries:
        return None

    best_rank = min(entry["rank"] for entry in entries)
    pool = [entry for entry in entries if entry["rank"] == best_rank]

    def score(entry):
        proto = entry["protocol"]
        active = 1 if entry.get("active", True) else 0
        if mode == "mp4":
            if proto != "mp4":
                return None
            return (active, entry["height"])
        if mode == "dash":
            if proto == "mpd":
                return (2, entry["height"], active)
            if proto == "mp4":
                return (1, entry["height"], active)
            return None
        order = {"mpd": 3, "hls": 2, "mp4": 1}
        return (order.get(proto, 0), entry["height"], active)

    ranked = []
    for entry in pool:
        value = score(entry)
        if value is not None:
            ranked.append((value, entry))
    if not ranked:
        return None
    ranked.sort(key=lambda item: item[0], reverse=True)
    chosen = ranked[0][1]

    def best_mp4(candidates):
        mp4s = [entry for entry in candidates if entry["protocol"] == "mp4"]
        if not mp4s:
            return None
        mp4s.sort(key=lambda entry: (1 if entry.get("active", True) else 0, entry["height"]), reverse=True)
        return mp4s[0]["file"]

    fallback = best_mp4(pool) or best_mp4(entries)
    if chosen["protocol"] == "mp4":
        fallback = None
    chosen_geo = (chosen.get("geo") or "").upper()
    user = (user_geo or "TOTS").upper()
    limited = chosen_geo not in (user, "TOTS")
    return {
        "url": chosen["file"],
        "protocol": chosen["protocol"],
        "height": chosen["height"],
        "geo": chosen_geo,
        "limited": limited,
        "fallback_mp4": fallback,
    }
