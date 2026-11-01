"""HTTP client for the public 3Cat JSON APIs used by www.3cat.cat.

Catalog and search come from api.3cat.cat. Stream URLs come from the media
endpoint (api-media.3cat.cat). Only clear HLS, DASH and progressive MP4
addresses returned by that endpoint are used.
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from resources.lib.strings import category_title
from resources.lib.parsing import (
    allowed_url,
    art_from_images,
    as_list,
    clean_text,
    clean_title,
    ensure_params,
    keep_shelf,
    parse_duration,
    plot_of,
    season_number,
    choose_stream,
    with_page,
)


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
# The catalogue is edited in Catalan. Ask for that language so a localized
# response cannot rename sections.
API_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ca",
    "Referer": "https://www.3cat.cat/",
}

API = "https://api.3cat.cat"
MEDIA_HOSTS = (
    "https://api-media.3cat.cat/pvideo/media.jsp",
    "https://api-media.ccma.cat/pvideo/media.jsp",
)
GEO_URL = "https://dinamics.ccma.cat/geo.json"
TEMATIQUES_URL = (
    "https://statics.3cat.cat/recursos/3play/tires/3play_home_tematiques_web_v1.json"
)

# Slug used on 3cat.cat -> editorial frontal that lists that section's rows.
SECTION_FRONTALS = {
    "series": "trescat-tresplwapp-series",
    "pellicules": "trescat-tresplwapp-pelicules",
    "documentals-i-reportatges": "trescat-tresplwapp-documental",
    "sx3": "trescat-tresplwapp-sx3",
    "actualitat": "trescat-tresplwapp-actualitat",
    "cultura": "trescat-tresplwapp-cultura",
    "esports": "trescat-tresplwapp-esports",
    "musica": "trescat-tresplwapp-musica",
    "cuines": "trescat-tresplwapp-cuines",
    "campus": "trescat-tresplwapp-campus",
}

# Sections whose frontal was empty, but a tematica filter still lists programs.
TEMATICA_FALLBACK = {
    "entreteniment": "PUENTRETENIM",
}

SKIP_CATEGORY_SLUGS = frozenset({"podcasts", "colleccions"})

MAIN_CHANNELS = (
    {
        "id": "tv3",
        "title": "TV3",
        "plot": "La televisió pública de Catalunya.",
        "logo": "https://statics.3cat.cat/img/logos/tv3.png",
    },
    {
        "id": "324",
        "title": "3CatInfo",
        "plot": "Informatius en directe, el canal 3/24.",
        "logo": "https://statics.3cat.cat/img/logos/324.png",
    },
    {
        "id": "sx3",
        "title": "SX3",
        "plot": "El canal infantil.",
        "logo": "https://statics.3cat.cat/recursos/3play/img/logo-sx3.png",
    },
    {
        "id": "c33",
        "title": "33",
        "plot": "Canal 33.",
        "logo": "https://statics.3cat.cat/img/logos/33.png",
    },
    {
        "id": "esport3",
        "title": "Esport3",
        "plot": "Esports en directe.",
        "logo": "https://statics.3cat.cat/img/logos/esport3.png",
    },
    {
        "id": "tvi",
        "title": "TV3CAT",
        "plot": "Senyal internacional de TV3.",
        "logo": "https://statics.3cat.cat/img/logos/tv3cat.png",
    },
)

LATEST_FRONTAL = "trescat-tresplay-novtotsmar"
RANKING_FRONTAL = "trescat-tresplwapp-mestop"
FAST_FRONTAL = "trescat-tresplay-fastchanne"


class ApiError(Exception):
    """The 3Cat API could not be read."""


def default_fetch(url, timeout=25):
    request = Request(url, headers=API_HEADERS)
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except HTTPError as exc:
        detail = exc.read(240).decode("utf-8", "replace")
        raise ApiError("HTTP %s for %s (%s)" % (exc.code, url, detail)) from exc
    except URLError as exc:
        raise ApiError("Network error for %s (%s)" % (url, exc.reason)) from exc
    try:
        return json.loads(raw.decode("utf-8"))
    except ValueError as exc:
        raise ApiError("Invalid JSON from %s" % url) from exc


class Client:
    def __init__(self, fetch=None, cache=None, ttl=1800):
        self.fetch = fetch or default_fetch
        self.cache = cache
        self.ttl = ttl

    def get_json(self, url, ttl=None):
        if not allowed_url(url):
            raise ApiError("Refused URL outside the 3Cat APIs")
        use_ttl = self.ttl if ttl is None else ttl
        if self.cache is not None and use_ttl:
            cached = self.cache.get(url)
            if cached is not None:
                return cached
        data = self.fetch(url)
        if self.cache is not None and use_ttl:
            self.cache.set(url, data, use_ttl)
        return data

    def _items(self, url, ttl=None):
        data = self.get_json(url, ttl=ttl)
        resposta = data.get("resposta") if isinstance(data, dict) else None
        if not isinstance(resposta, dict):
            raise ApiError("Unexpected API payload")
        items = as_list(resposta.get("items"))
        page = resposta.get("paginacio") or {}
        return items, page

    def geo(self):
        try:
            data = self.get_json(GEO_URL, ttl=3600)
        except ApiError:
            return "TOTS"
        if isinstance(data, dict) and data.get("geo"):
            return str(data["geo"]).upper()
        return "TOTS"

    def categories(self):
        data = self.get_json(TEMATIQUES_URL, ttl=6 * 3600)
        resposta = data.get("resposta") if isinstance(data, dict) else {}
        found = []
        for item in as_list((resposta or {}).get("items")):
            slug = item.get("slug")
            if not slug or slug in SKIP_CATEGORY_SLUGS:
                continue
            if slug not in SECTION_FRONTALS and slug not in TEMATICA_FALLBACK:
                continue
            art = art_from_images(item.get("imatges"))
            thumb = item.get("img_pastilla") or art.get("thumb")
            fanart = art.get("fanart") or thumb
            found.append(
                {
                    "slug": slug,
                    "title": category_title(
                        slug, item.get("titol_pastilla") or item.get("titol") or ""
                    ),
                    "plot": clean_text(item.get("entradeta")),
                    "art": {
                        "thumb": thumb,
                        "poster": fanart or thumb,
                        "fanart": fanart,
                        "icon": thumb,
                    },
                    "fallback_tematica": TEMATICA_FALLBACK.get(slug),
                    "has_frontal": slug in SECTION_FRONTALS,
                }
            )
        return found

    def section_rows(self, slug):
        frontal = SECTION_FRONTALS.get(slug)
        if not frontal:
            return []
        return self._rows(frontal)

    def ranking_rows(self):
        return self._rows(RANKING_FRONTAL)

    def _rows(self, frontal):
        rows = []
        page = 1
        while page <= 6:
            query = urlencode(
                {
                    "_format": "json",
                    "origen": "frontal",
                    "frontal": frontal,
                    "items_pagina": 40,
                    "pagina": page,
                    "version": "2.0",
                }
            )
            items, pagination = self._items("%s/tiracontinguts?%s" % (API, query))
            rows.extend(item for item in items if keep_shelf(item))
            total_pages = int(pagination.get("total_pagines") or 1)
            if page >= total_pages:
                break
            page += 1
        return rows

    def listing(self, url, page=1):
        if not allowed_url(url):
            raise ApiError("Refused URL outside the 3Cat APIs")
        target = ensure_params(with_page(url, page))
        return self._items(target)

    def programs(self, page=1, page_size=24, tematica=None, canal=None, lletra=None, codi_etic=None):
        params = {
            "_format": "json",
            "agrupar": "false",
            "items_pagina": page_size,
            "pagina": page,
            "sdom": "img",
            "version": "2.0",
            "https": "true",
            "master": "yes",
        }
        if tematica:
            params["tematica"] = tematica
        if canal:
            params["canal"] = canal
        if lletra:
            params["lletra"] = lletra
        if codi_etic:
            params["codi_etic"] = codi_etic
        return self._items("%s/programestv?%s" % (API, urlencode(params)))

    def latest(self, page=1, page_size=24):
        params = {
            "_format": "json",
            "frontal": LATEST_FRONTAL,
            "origen": "frontal",
            "items_pagina": page_size,
            "pagina": page,
            "sdom": "img",
            "version": "2.0",
            "https": "true",
            "master": "yes",
        }
        return self._items("%s/videos?%s" % (API, urlencode(params)))

    def search(self, text, kind="program", page=1, page_size=24):
        typology = "PTVC_PROGRAMA" if kind == "program" else "DTY_VIDEO_MM"
        params = {
            "_format": "json",
            "text": text,
            "tipologia": typology,
            "items_pagina": page_size,
            "pagina": page,
            "sdom": "img",
            "version": "2.0",
            "https": "true",
            "master": "yes",
        }
        return self._items("%s/cercador/tot?%s" % (API, urlencode(params)))

    def program(self, program_id):
        params = urlencode(
            {
                "_format": "json",
                "sdom": "img",
                "version": "2.0",
                "https": "true",
                "master": "yes",
            }
        )
        data = self.get_json("%s/programestv/%s/?%s" % (API, program_id, params))
        resposta = data.get("resposta") if isinstance(data, dict) else None
        item = (resposta or {}).get("item")
        if not isinstance(item, dict):
            raise ApiError("Program %s was not found" % program_id)
        return item

    def seasons(self, program_id):
        """Seasons that actually have episodes.

        The program document usually lists only the current season. Older
        seasons are still addressable as PUTEMP_n, so those ids are probed.
        """
        detail = self.program(program_id)
        known = {}
        for entry in detail.get("temporades") or []:
            if not isinstance(entry, dict) or not entry.get("id"):
                continue
            number = season_number(entry.get("id"))
            known[str(entry["id"])] = {
                "id": str(entry["id"]),
                "number": number,
                "title": clean_text(entry.get("desc")),
                "episodes": None,
            }
        numbers = [item["number"] for item in known.values() if item["number"]]
        upper = max(numbers) + 2 if numbers else 6
        upper = max(upper, 6)
        totals = {}
        start = 1
        while start <= upper and start <= 40:
            batch = list(range(start, min(upper, 40) + 1))
            totals.update(self._probe_seasons(program_id, batch))
            top = batch[-1]
            if totals.get(top, 0) > 0 and upper < 40:
                upper = min(40, top + 4)
                start = top + 1
            else:
                break
        for number, total in totals.items():
            if total <= 0:
                continue
            season_id = "PUTEMP_%s" % number
            current = known.get(season_id, {})
            known[season_id] = {
                "id": season_id,
                "number": number,
                "title": current.get("title") or "",
                "episodes": total,
            }
        # Keep seasons that have episodes. If every probe failed, fall back
        # to the seasons advertised on the program document.
        kept = []
        for item in known.values():
            number = item.get("number")
            total = totals.get(number) if number is not None else None
            if total:
                item["episodes"] = total
                kept.append(item)
            elif number is None:
                kept.append(item)
            elif number not in totals and item.get("episodes") not in (0, None):
                kept.append(item)
        if not kept and known:
            kept = list(known.values())
        kept.sort(key=lambda item: (item.get("number") is None, item.get("number") or 0))
        return detail, kept

    def _probe_seasons(self, program_id, numbers):
        totals = {}
        workers = min(6, max(1, len(numbers)))
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {
                pool.submit(self._season_total, program_id, number): number for number in numbers
            }
            for future in as_completed(futures):
                number = futures[future]
                try:
                    totals[number] = future.result()
                except Exception:
                    totals[number] = 0
        return totals

    def _season_total(self, program_id, number):
        _items, page = self.episodes(program_id, "PUTEMP_%s" % number, page=1, page_size=1)
        try:
            return int(page.get("total_items") or 0)
        except (TypeError, ValueError):
            return 0

    def episodes(self, program_id, season_id, page=1, page_size=24, newest_first=False):
        params = {
            "_format": "json",
            "ordre": "-capitol" if newest_first else "capitol",
            "origen": "llistat",
            "perfil": "pc",
            "programatv_id": program_id,
            "tipus_contingut": "PPD",
            "items_pagina": page_size,
            "pagina": page,
            "sdom": "img",
            "version": "2.0",
            "temporada": season_id,
            "https": "true",
            "master": "yes",
            "no_agrupacio": "PUAGR_LLSIGN",
        }
        return self._items("%s/videos?%s" % (API, urlencode(params)))

    def live_channels(self, include_fast=True):
        now = self._now_playing()
        channels = []
        seen = set()
        for spec in MAIN_CHANNELS:
            channels.append(self._channel_from_spec(spec, now.get(spec["id"])))
            seen.add(spec["id"])
        if include_fast:
            for channel in self.fast_channels():
                if channel["id"] in seen:
                    continue
                seen.add(channel["id"])
                channels.append(channel)
        return channels

    def _now_playing(self):
        query = urlencode(
            {
                "_format": "json",
                "tipus": "tv",
                "version": "1.0",
                "https": "true",
                "master": "yes",
            }
        )
        try:
            data = self.get_json("%s/arafem?%s" % (API, query), ttl=120)
        except ApiError:
            return {}
        indexed = {}
        for entry in data.get("canal") or []:
            if not isinstance(entry, dict):
                continue
            current = entry.get("ara_fem") or {}
            code = current.get("codi_canal") or entry.get("name")
            if code:
                indexed[str(code).lower()] = current
        return indexed

    def _channel_from_spec(self, spec, current):
        art = {"icon": spec["logo"], "clearlogo": spec["logo"], "poster": spec["logo"], "thumb": spec["logo"]}
        plot = spec.get("plot") or ""
        duration = None
        if isinstance(current, dict) and current.get("titol_programa"):
            program_art = art_from_images(current.get("imatges"))
            if program_art.get("thumb"):
                art["thumb"] = program_art["thumb"]
            if program_art.get("fanart"):
                art["fanart"] = program_art["fanart"]
                art["landscape"] = program_art["fanart"]
            if program_art.get("poster"):
                art["poster"] = program_art["poster"]
            show = clean_text(current.get("titol_programa"))
            chapter = clean_text(current.get("titol_capitol"))
            headline = " — ".join(part for part in (show, chapter) if part)
            synopsis = clean_text(current.get("sinopsi"))
            plot = "\n\n".join(part for part in (headline, synopsis) if part)
            duration = parse_duration(current.get("durada"))
        elif spec.get("logo"):
            art["fanart"] = spec["logo"]
        return {
            "id": spec["id"],
            "title": spec["title"],
            "plot": plot,
            "art": art,
            "duration": duration,
            "live": True,
        }

    def fast_channels(self):
        params = urlencode(
            {
                "_format": "json",
                "frontal": FAST_FRONTAL,
                "origen": "frontal",
                "sdom": "img",
                "version": "2.0",
                "https": "true",
                "master": "yes",
            }
        )
        try:
            items, _page = self._items("%s/destacats?%s" % (API, params), ttl=600)
        except ApiError:
            return []
        channels = []
        for item in items:
            canals = item.get("canals") or []
            if not canals or not isinstance(canals[0], dict):
                continue
            code = str(canals[0].get("id") or "").lower()
            if not code:
                continue
            art = art_from_images(item.get("imatges"))
            channels.append(
                {
                    "id": code,
                    "title": clean_title(item.get("titol") or code.upper()),
                    "plot": clean_text(item.get("avantitol")),
                    "art": art,
                    "duration": None,
                    "live": True,
                    "fast": True,
                }
            )
        return channels

    def resolve(self, video_id=None, channel_id=None, mode="auto"):
        """Return {ok, reason, stream}. reason is drm, empty or error."""
        if not video_id and not channel_id:
            return {"ok": False, "reason": "empty", "stream": None}
        params = {
            "media": "video",
            "versio": "vast",
            "idint": channel_id or video_id,
            "profile": "pc_3cat",
        }
        if channel_id:
            params["format"] = "HLS"
            params["desplacament"] = "0"
            ttl = 90
        else:
            params["format"] = "dm"
            ttl = 600
        query = urlencode(params)
        data = None
        last_error = None
        for host in MEDIA_HOSTS:
            try:
                data = self.get_json("%s?%s" % (host, query), ttl=ttl)
                break
            except ApiError as exc:
                last_error = exc
        if data is None:
            raise last_error or ApiError("Media API unavailable")
        if not isinstance(data, dict):
            return {"ok": False, "reason": "empty", "stream": None}
        subtitles = []
        for sub in data.get("subtitols") or []:
            if isinstance(sub, dict) and sub.get("url"):
                subtitles.append(
                    {
                        "url": sub["url"],
                        "lang": sub.get("iso") or "",
                        "label": clean_text(sub.get("text")),
                    }
                )
        subtitles.sort(key=lambda sub: {"ca": 0, "es": 1, "en": 2}.get(sub["lang"], 9))
        stream = choose_stream(data.get("media"), self.geo(), mode=mode)
        if stream is None:
            reason = "drm" if _payload_looks_like_drm(data.get("media")) else "empty"
            return {"ok": False, "reason": reason, "stream": None}
        info = data.get("informacio") if isinstance(data.get("informacio"), dict) else {}
        images = info.get("imatges") if isinstance(info.get("imatges"), dict) else {}
        stream["subtitles"] = subtitles
        stream["title"] = clean_text(info.get("titol_complet") or info.get("titol"))
        stream["plot"] = clean_text(info.get("descripcio"))
        stream["image"] = images.get("url") if isinstance(images, dict) else None
        stream["duration"] = parse_duration((info.get("durada") or {}))
        stream["program_id"] = info.get("programa_id") or ""
        stream["show"] = clean_text(info.get("programa"))
        theme = info.get("tematica") if isinstance(info.get("tematica"), dict) else {}
        stream["tematica"] = theme.get("id") or ""
        return {"ok": True, "reason": None, "stream": stream}


def _payload_looks_like_drm(media):
    blob = json.dumps(media or "", ensure_ascii=False).lower()
    return any(token in blob for token in ("widevine", "playready", "clearkey"))
