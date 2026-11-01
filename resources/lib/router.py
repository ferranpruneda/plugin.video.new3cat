"""Kodi directory routing. This is the only module that imports xbmc."""

from __future__ import annotations

import os
import sys
import traceback
from urllib.parse import parse_qsl, urlencode

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs

from resources.lib.api import ApiError, Client
from resources.lib.cache import FileCache
from resources.lib.history import HistoryStore, format_position, should_resume
from resources.lib.matching import rank_matches, search_variants
from resources.lib.parsing import present_item
from resources.lib.strings import text as catalog_text

ADDON_ID = "plugin.video.new3cat"
FANART = "https://img.3cat.cat/multimedia/png/3/0/1697462431903_1920x1080.png"
# Official SX3 mark from 3Cat, used only as a small clearlogo. The colourful
# icons and backgrounds are original drawings in resources/media/kids.
SX3_CLEARLOGO = "https://statics.3cat.cat/recursos/3play/img/logo-sx3.png"

MIME = {
    "hls": "application/vnd.apple.mpegurl",
    "mpd": "application/dash+xml",
    "mp4": "video/mp4",
}
ISA_TYPE = {"hls": "hls", "mpd": "mpd"}


def log(message, level=xbmc.LOGINFO):
    xbmc.log("[%s] %s" % (ADDON_ID, message), level)


def build_url(base, params):
    cleaned = {key: value for key, value in params.items() if value is not None and value != ""}
    return "%s?%s" % (base, urlencode(cleaned))


def _bool_setting(addon, key, default):
    value = addon.getSetting(key)
    if value == "":
        return default
    return value == "true"


def _int_setting(addon, key, default, low, high):
    try:
        value = int(addon.getSetting(key) or default)
    except ValueError:
        value = default
    return max(low, min(high, value))


def _kodi_language():
    try:
        code = xbmc.getLanguage(xbmc.ISO_639_1)
    except Exception:
        return "ca"
    return code or "ca"


def ui_text(addon, string_id):
    """Catalan labels by default. Setting ui_language=1 follows Kodi."""
    follow = False
    try:
        follow = (addon.getSetting("ui_language") or "0") == "1"
    except Exception:
        follow = False
    return catalog_text(
        string_id,
        follow_kodi=follow,
        kodi_language=_kodi_language() if follow else "ca",
    )


class Router:
    def __init__(self, handle, base, params, addon, client, profile):
        self.handle = handle
        self.base = base
        self.params = params
        self.addon = addon
        self.client = client
        self.profile = profile
        self.history = HistoryStore(profile)
        self._items = []

    def tr(self, string_id):
        return ui_text(self.addon, string_id)

    def notify(self, message):
        xbmcgui.Dialog().notification(self.addon.getAddonInfo("name"), message, xbmcgui.NOTIFICATION_INFO, 6000)

    def url(self, **params):
        return build_url(self.base, params)

    def page_size(self):
        return _int_setting(self.addon, "page_size", 24, 8, 60)

    def newest_first(self):
        return (self.addon.getSetting("episode_order") or "0") == "1"

    def stream_mode(self):
        value = self.addon.getSetting("stream_mode") or "0"
        return {"0": "auto", "1": "dash", "2": "mp4"}.get(value, "auto")

    def dispatch(self):
        action = self.params.get("action") or "root"
        method = getattr(self, "action_" + action, None)
        if method is None:
            method = self.action_root
        try:
            method()
        except ApiError as exc:
            log("API error: %s" % exc, xbmc.LOGERROR)
            self._fail(self.tr(30116))

    def _fail(self, message):
        self.notify(message)
        if self.params.get("action") == "play":
            xbmcplugin.setResolvedUrl(self.handle, False, xbmcgui.ListItem())
        else:
            xbmcplugin.endOfDirectory(self.handle, succeeded=False)

    def add(self, url, title, art=None, info=None, folder=True, playable=False, label2=""):
        item = xbmcgui.ListItem(label=title or "3Cat", label2=label2 or "")
        merged = {"fanart": FANART}
        if art:
            merged.update({key: value for key, value in art.items() if value})
        item.setArt(merged)
        if info:
            _apply_info(item, info)
        if playable:
            item.setProperty("IsPlayable", "true")
        self._items.append((url, item, folder))

    def finish(self, content, category, cache=True, fanart=None):
        xbmcplugin.setPluginCategory(self.handle, category)
        xbmcplugin.setPluginFanart(self.handle, fanart or FANART)
        if content:
            xbmcplugin.setContent(self.handle, content)
        if content == "episodes":
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_EPISODE)
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_DATE)
        elif content == "tvshows":
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_UNSORTED)
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_TITLE)
        elif content == "movies":
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_UNSORTED)
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_TITLE)
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_VIDEO_YEAR)
        else:
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_UNSORTED)
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.addDirectoryItems(self.handle, self._items)
        xbmcplugin.endOfDirectory(self.handle, succeeded=True, cacheToDisc=cache)
        self._items = []

    def action_root(self):
        name = self.addon.getAddonInfo("name")
        entries = (
            ("live", 30100, "https://statics.3cat.cat/img/logos/tv3.png"),
        )
        rest = (
            ("latest", 30102, "https://statics.3cat.cat/recursos/3play/img/series_960x540.jpg"),
            ("rankings", 30101, "https://apptv.3cat.cat/apptv/_resources/imatges/tematiques/superdestacat/pelicules_960x540.jpg"),
            ("categories", 30103, "https://apptv.3cat.cat/apptv/_resources/imatges/tematiques/superdestacat/documentals_960x540.jpg"),
            ("letters", 30104, "https://statics.3cat.cat/recursos/3play/img/series_960x540.jpg"),
            ("continue", 30152, FANART),
            ("search", 30105, FANART),
            ("voice", 30150, FANART),
        )
        for action, label, image in entries:
            art = {"thumb": image, "poster": image, "fanart": image, "icon": image}
            self.add(self.url(action=action), self.tr(label), art=art, info={"mediatype": "video", "plot": self.tr(label)})
        self.add(
            self.url(action="kids"),
            self.tr(30130),
            art=_kids_art("home"),
            info={"mediatype": "tvshow", "plot": self.tr(30139)},
        )
        for action, label, image in rest:
            art = {"thumb": image, "poster": image, "fanart": image, "icon": image}
            self.add(self.url(action=action), self.tr(label), art=art, info={"mediatype": "video", "plot": self.tr(label)})
        self.finish("videos", name, cache=False)

    def action_kids(self):
        self.add(
            self.url(action="play", channel_id="sx3", title=self.tr(30131)),
            self.tr(30131),
            art=_kids_art("live"),
            info={"mediatype": "video", "plot": self.tr(30140), "genre": [self.tr(30124)]},
            folder=False,
            playable=True,
        )
        self._add_kids_folder(self.tr(30132), self.tr(30141), canal="PUC_S3", kind="programmes")
        self.add(
            self.url(action="kids_ages"),
            self.tr(30133),
            art=_kids_art("ages"),
            info={"mediatype": "tvshow", "plot": self.tr(30142)},
        )
        self.add(
            self.url(action="kids_shelves"),
            self.tr(30138),
            art=_kids_art("highlights"),
            info={"mediatype": "tvshow", "plot": self.tr(30147)},
        )
        self.finish("tvshows", self.tr(30130), fanart=_kids_file("fanart.png"))

    def action_kids_ages(self):
        bands = (
            (30134, 30143, "", "CE_IN", "petits"),
            (30135, 30144, "PUC_S3", "CE_TP", "tots"),
            (30136, 30145, "PUC_S3", "CE_07", "age7"),
            (30137, 30146, "PUC_S3", "CE_10", "age10"),
        )
        for title_id, plot_id, canal, code, kind in bands:
            self._add_kids_folder(
                self.tr(title_id), self.tr(plot_id), canal=canal, codi_etic=code, kind=kind
            )
        self.finish("tvshows", self.tr(30133), fanart=_kids_file("fanart.png"))

    def action_kids_shelves(self):
        rows = self.client.section_rows("sx3")
        if not rows:
            self.notify(self.tr(30112))
        self._add_shelves(rows, self.tr(30138), fanart=_kids_file("fanart.png"), kids=True)

    def _add_kids_folder(self, title, plot, canal="", codi_etic="", kind="home"):
        self.add(
            self.url(
                action="programs",
                title=title,
                canal=canal,
                codi_etic=codi_etic,
                kids="1",
            ),
            title,
            art=_kids_art(kind),
            info={"mediatype": "tvshow", "plot": plot},
        )

    def action_live(self):
        include_fast = _bool_setting(self.addon, "fast_channels", True)
        for channel in self.client.live_channels(include_fast=include_fast):
            self.add(
                self.url(action="play", channel_id=channel["id"], title=channel["title"]),
                channel["title"],
                art=channel.get("art"),
                info={
                    "mediatype": "video",
                    "plot": channel.get("plot") or "",
                    "duration": channel.get("duration"),
                    "genre": [self.tr(30124)],
                },
                folder=False,
                playable=True,
            )
        self.finish("videos", self.tr(30100), cache=False)

    def action_latest(self):
        page = _page(self.params)
        items, pagination = self.client.latest(page=page, page_size=self.page_size())
        self._add_catalog(items, "videos")
        self._add_next(pagination, action="latest")
        if not self._items:
            self.notify(self.tr(30112))
        self.finish(self._content_for(items), self.tr(30102))

    def action_rankings(self):
        self._add_shelves(self.client.ranking_rows(), self.tr(30101))

    def action_categories(self):
        for category in self.client.categories():
            self.add(
                self.url(action="category", slug=category["slug"], title=category["title"]),
                category["title"],
                art=category.get("art"),
                info={"mediatype": "tvshow", "plot": category.get("plot") or ""},
            )
        if not self._items:
            self.notify(self.tr(30123))
        self.finish("tvshows", self.tr(30103))

    def action_category(self):
        slug = self.params.get("slug") or ""
        title = self.params.get("title") or slug
        categories = {item["slug"]: item for item in self.client.categories()}
        category = categories.get(slug, {})
        fanart = (category.get("art") or {}).get("fanart")
        if category and not category.get("has_frontal") and category.get("fallback_tematica"):
            self.params["tematica"] = category["fallback_tematica"]
            self.params["title"] = title
            self.action_programs()
            return
        rows = self.client.section_rows(slug) if category.get("has_frontal") or slug else []
        if not rows and category.get("fallback_tematica"):
            self.params["tematica"] = category["fallback_tematica"]
            self.params["title"] = title
            self.action_programs()
            return
        if not rows:
            self.notify(self.tr(30123))
            self.finish("videos", title)
            return
        self._add_shelves(rows, title, fanart=fanart)

    def action_letters(self):
        self.add(self.url(action="programs", title=self.tr(30118)), self.tr(30118))
        self.add(self.url(action="programs", lletra="#", title="#"), "#")
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.add(self.url(action="programs", lletra=letter, title=letter), letter)
        self.finish("videos", self.tr(30104))

    def action_programs(self):
        page = _page(self.params)
        title = self.params.get("title") or self.tr(30107)
        items, pagination = self.client.programs(
            page=page,
            page_size=self.page_size(),
            tematica=self.params.get("tematica"),
            lletra=self.params.get("lletra"),
            canal=self.params.get("canal"),
            codi_etic=self.params.get("codi_etic"),
        )
        self._add_catalog(items, "tvshows")
        extra = {
            "action": "programs",
            "title": title,
            "tematica": self.params.get("tematica"),
            "lletra": self.params.get("lletra"),
            "canal": self.params.get("canal"),
            "codi_etic": self.params.get("codi_etic"),
            "kids": self.params.get("kids"),
        }
        self._add_next(pagination, **extra)
        if not self._items:
            self.notify(self.tr(30112))
        fanart = _kids_file("fanart.png") if self.params.get("kids") == "1" else None
        self.finish("tvshows", title, fanart=fanart)

    def action_shelf(self):
        page = _page(self.params)
        title = self.params.get("title") or "3Cat"
        url = self.params.get("url") or ""
        items, pagination = self.client.listing(url, page=page)
        content = self._content_for(items)
        self._add_catalog(items, content)
        self._add_next(pagination, action="shelf", url=url, title=title, kids=self.params.get("kids"))
        if not self._items:
            self.notify(self.tr(30112))
        background = _kids_file("fanart.png") if self.params.get("kids") == "1" else None
        self.finish(content, title, fanart=background)

    def action_program(self):
        program_id = self.params.get("program_id")
        detail, seasons = self.client.seasons(program_id)
        shown = present_item(detail)
        art = shown["art"]
        title = shown["title"] or self.params.get("title") or "3Cat"
        if len(seasons) == 1:
            self.params["season"] = seasons[0]["id"]
            self.params["season_number"] = str(seasons[0].get("number") or "")
            self.params["title"] = title
            self.action_episodes()
            return
        if not seasons:
            self.notify(self.tr(30113))
            self.finish("seasons", title, fanart=self._section_fanart(art.get("fanart")))
            return
        for season in seasons:
            number = season.get("number")
            label = self.tr(30109) % number if number else (season.get("title") or self.tr(30125))
            plot = shown["plot"]
            if season.get("episodes"):
                plot = "%s\n%s" % (label, plot) if plot else label
            self.add(
                self.url(
                    action="episodes",
                    program_id=program_id,
                    season=season["id"],
                    season_number=number or "",
                    title=title,
                    kids=self.params.get("kids"),
                ),
                label,
                art=art,
                info={
                    "mediatype": "season",
                    "title": label,
                    "tvshowtitle": title,
                    "season": number,
                    "plot": shown["plot"],
                    "premiered": shown["premiered"],
                    "year": shown["year"],
                },
            )
        self.finish("seasons", title, fanart=self._section_fanart(art.get("fanart")))

    def action_episodes(self):
        page = _page(self.params)
        program_id = self.params.get("program_id")
        season_id = self.params.get("season")
        show = self.params.get("title") or ""
        try:
            season_number = int(self.params.get("season_number") or 0) or None
        except ValueError:
            season_number = None
        detail = self.client.program(program_id)
        show_art = present_item(detail)["art"]
        show_title = present_item(detail)["title"] or show
        items, pagination = self.client.episodes(
            program_id,
            season_id,
            page=page,
            page_size=self.page_size(),
            newest_first=self.newest_first(),
        )
        for raw in items:
            shown = present_item(raw)
            if shown["kind"] == "skip" or not shown["id"]:
                continue
            title = shown["title"]
            if shown["generic_episode"] and shown["episode"]:
                title = self.tr(30110) % shown["episode"]
            art = dict(show_art)
            art.update(shown["art"])
            self.add(
                self._play_url(shown["id"], title, art, program_id=program_id, show=show_title, raw=raw),
                title,
                art=art,
                info={
                    "mediatype": "episode",
                    "title": title,
                    "tvshowtitle": show_title,
                    "plot": shown["plot"],
                    "duration": shown["duration"],
                    "premiered": shown["premiered"],
                    "year": shown["year"],
                    "season": shown["season"] or season_number,
                    "episode": shown["episode"],
                    "mpaa": shown["mpaa"],
                    "genre": shown["genres"],
                },
                folder=False,
                playable=True,
                label2=shown["premiered"] or "",
            )
        self._add_next(
            pagination,
            action="episodes",
            program_id=program_id,
            season=season_id,
            season_number=season_number or "",
            title=show_title,
            kids=self.params.get("kids"),
        )
        if not self._items:
            self.notify(self.tr(30112))
        self.finish("episodes", show_title, fanart=self._section_fanart(show_art.get("fanart")))

    def action_search(self):
        query = self.params.get("q") or ""
        kind = self.params.get("kind") or ""
        query = query.strip()[:80]
        if not query:
            keyboard = xbmc.Keyboard("", self.tr(30121))
            keyboard.doModal()
            if not keyboard.isConfirmed():
                xbmcplugin.endOfDirectory(self.handle, succeeded=False)
                return
            query = keyboard.getText().strip()[:80]
            if not query:
                xbmcplugin.endOfDirectory(self.handle, succeeded=False)
                return
        if kind not in ("program", "video"):
            self.add(
                self.url(action="search", q=query, kind="program"),
                self.tr(30119),
                info={"plot": query},
            )
            self.add(
                self.url(action="search", q=query, kind="video"),
                self.tr(30120),
                info={"plot": query},
            )
            self.finish("videos", self.tr(30105))
            return
        page = _page(self.params)
        items, pagination = self.client.search(query, kind=kind, page=page, page_size=self.page_size())
        content = "tvshows" if kind == "program" else self._content_for(items)
        self._add_catalog(items, content)
        self._add_next(pagination, action="search", q=query, kind=kind)
        title = self.tr(30119) if kind == "program" else self.tr(30120)
        if not self._items:
            self.notify(self.tr(30112))
        self.finish(content, "%s: %s" % (title, query))

    def action_voice(self):
        query = (self.params.get("q") or "").strip()
        if not query:
            typed = xbmcgui.Dialog().input(self.tr(30151), type=xbmcgui.INPUT_ALPHANUM)
            query = (typed or "").strip()
        if not query:
            xbmcplugin.endOfDirectory(self.handle, succeeded=False)
            return
        found = []
        seen = set()
        for variant in search_variants(query):
            for kind in ("program", "video"):
                try:
                    batch, _page = self.client.search(variant, kind=kind, page=1, page_size=self.page_size())
                except ApiError:
                    if found:
                        break
                    raise
                for item in batch:
                    identity = item.get("id")
                    if identity in seen:
                        continue
                    seen.add(identity)
                    found.append(item)
            if len(found) >= 12:
                break
        found = rank_matches(query, found)
        self._add_catalog(found, self._content_for(found))
        if not self._items:
            self.notify(self.tr(30112))
        self.finish(self._content_for(found) if self._items else "videos", "%s: %s" % (self.tr(30150), query))

    def action_continue(self):
        items = self.history.recent(self.page_size()) if self._remember() else []
        if not items:
            self.notify(self.tr(30154) if self._remember() else self.tr(30157))
        for entry in items:
            title = entry.get("title") or entry.get("show") or "3Cat"
            show = entry.get("show") or ""
            label = title if not show or show == title else "%s — %s" % (show, title)
            art = {}
            if entry.get("thumb"):
                art["thumb"] = entry["thumb"]
                art["poster"] = entry["thumb"]
            if entry.get("fanart"):
                art["fanart"] = entry["fanart"]
                art["landscape"] = entry["fanart"]
            label2 = ""
            if should_resume(entry):
                label2 = self.tr(30156) % format_position(entry.get("position"))
            item_url = self.url(
                action="play",
                video_id=entry.get("video_id"),
                title=title,
                program_id=entry.get("program_id"),
                show=show,
                tematica=entry.get("tematica"),
                thumb=entry.get("thumb"),
                fanart=entry.get("fanart"),
            )
            self.add(
                item_url,
                label,
                art=art,
                info={
                    "mediatype": "episode",
                    "title": label,
                    "tvshowtitle": show,
                    "plot": entry.get("plot") or label2,
                    "duration": entry.get("duration"),
                    "resume": entry.get("position") if should_resume(entry) else None,
                },
                folder=False,
                playable=True,
                label2=label2,
            )
        if items:
            self.add(
                self.url(action="similar"),
                self.tr(30153),
                info={"mediatype": "tvshow", "plot": self.tr(30153)},
            )
        self.finish("episodes", self.tr(30152), cache=False)

    def action_similar(self):
        collected = []
        seen = set(self.history.program_ids(20))
        codes = []
        for program_id in self.history.program_ids(3):
            try:
                detail = self.client.program(program_id)
            except ApiError:
                continue
            for theme in detail.get("tematiques") or []:
                code = theme.get("id") if isinstance(theme, dict) else None
                if code and code not in codes:
                    codes.append(code)
        for code in codes[:2]:
            batch, _page = self.client.programs(page=1, page_size=15, tematica=code)
            for item in batch:
                identity = item.get("id")
                if identity in seen:
                    continue
                seen.add(identity)
                collected.append(item)
        if not collected:
            recent = self.history.recent(1)
            hint = ""
            if recent:
                hint = recent[0].get("show") or recent[0].get("title") or ""
            if hint:
                batch, _page = self.client.search(hint, kind="program", page=1, page_size=12)
                for item in batch:
                    if item.get("id") not in seen:
                        collected.append(item)
        self._add_catalog(collected, "tvshows")
        if not self._items:
            self.notify(self.tr(30112))
        self.finish("tvshows", self.tr(30153))

    def action_clear_history(self):
        self.history.clear()
        self.notify(self.tr(30155))

    def action_play(self):
        result = self.client.resolve(
            video_id=self.params.get("video_id"),
            channel_id=self.params.get("channel_id"),
            mode=self.stream_mode(),
        )
        if not result.get("ok"):
            reason = result.get("reason")
            self.notify(self.tr(30115) if reason == "drm" else self.tr(30113))
            xbmcplugin.setResolvedUrl(self.handle, False, xbmcgui.ListItem())
            return
        stream = result["stream"]
        protocol = stream["protocol"]
        media_url = stream["url"]
        use_isa = _has_inputstream()
        if protocol == "mpd" and not use_isa:
            if stream.get("fallback_mp4"):
                protocol = "mp4"
                media_url = stream["fallback_mp4"]
            else:
                self.notify(self.tr(30117))
                xbmcplugin.setResolvedUrl(self.handle, False, xbmcgui.ListItem())
                return
        # inputstream.adaptive reads headers from its own properties. The
        # pipe syntax is for Kodi's ffmpeg demuxer (MP4 and HLS without ISA).
        if protocol in ("hls", "mpd") and use_isa:
            play_url = media_url
        else:
            play_url = _with_ffmpeg_headers(media_url)
        if stream.get("limited") and _bool_setting(self.addon, "geo_warning", True):
            self.notify(self.tr(30114))
        item = xbmcgui.ListItem(label=self.params.get("title") or stream.get("title") or "3Cat", path=play_url)
        item.setMimeType(MIME.get(protocol, "video/mp4"))
        item.setContentLookup(False)
        if protocol in ("hls", "mpd") and use_isa:
            item.setProperty("inputstream", "inputstream.adaptive")
            item.setProperty("inputstream.adaptive.manifest_type", ISA_TYPE[protocol])
            header = "User-Agent=Mozilla/5.0&Referer=https://www.3cat.cat/"
            item.setProperty("inputstream.adaptive.manifest_headers", header)
            item.setProperty("inputstream.adaptive.stream_headers", header)
        if self.params.get("channel_id"):
            item.setProperty("IsLive", "true")
        subtitles = [sub["url"] for sub in stream.get("subtitles") or [] if sub.get("url")]
        if subtitles:
            item.setSubtitles(subtitles)
        if stream.get("image"):
            item.setArt({"thumb": stream["image"], "fanart": stream["image"]})
        self._note_playback(stream, media_url)
        xbmcplugin.setResolvedUrl(self.handle, True, item)

    def _play_url(self, video_id, title, art, program_id="", show="", raw=None):
        raw = raw or {}
        theme = self.params.get("tematica") or _first_id(raw.get("tematiques"))
        program = program_id or _first_id(raw.get("programes_tv"))
        return self.url(
            action="play",
            video_id=video_id,
            title=title,
            program_id=program,
            show=show or raw.get("programa") or "",
            tematica=theme,
            thumb=(art or {}).get("thumb") or (art or {}).get("poster") or "",
            fanart=(art or {}).get("fanart") or "",
            kids=self.params.get("kids"),
        )

    def _remember(self):
        return _bool_setting(self.addon, "remember_history", True)

    def _note_playback(self, stream, media_url):
        if self.params.get("channel_id") or not self.params.get("video_id") or not self._remember():
            return
        record = {
            "video_id": self.params.get("video_id"),
            "program_id": self.params.get("program_id") or stream.get("program_id") or "",
            "title": self.params.get("title") or stream.get("title") or "",
            "show": self.params.get("show") or stream.get("show") or "",
            "plot": stream.get("plot") or "",
            "thumb": self.params.get("thumb") or stream.get("image") or "",
            "fanart": self.params.get("fanart") or stream.get("image") or "",
            "tematica": self.params.get("tematica") or stream.get("tematica") or "",
            "position": 0,
            "duration": stream.get("duration") or 0,
            "stream_url": media_url,
        }
        previous = self.history.get(record["video_id"])
        if previous and should_resume(previous):
            record["position"] = previous.get("position") or 0
            record["duration"] = previous.get("duration") or record["duration"]
        self.history.remember(record)
        self.history.write_pending(record)

    def _section_fanart(self, fallback):
        if self.params.get("kids") == "1":
            return _kids_file("fanart.png")
        return fallback

    def _add_shelves(self, rows, title, fanart=None, kids=False):
        for row in rows:
            name = row.get("nom") or title
            name = name.replace("*", "").strip() or title
            tipus = str(row.get("tipus") or "").upper()
            art = _kids_art("highlights") if kids else ({"fanart": fanart} if fanart else None)
            if tipus == "DIRECTES":
                target = self.url(action="live")
            elif tipus == "FAST_CHANNEL":
                target = self.url(action="live")
            elif tipus == "TEMATIQUES":
                target = self.url(action="categories")
            else:
                target = self.url(
                    action="shelf",
                    url=row.get("url_dades"),
                    title=name,
                    kids="1" if kids else None,
                )
            self.add(target, name, art=art, info={"plot": name, "mediatype": "tvshow"})
        self.finish("tvshows" if kids else "videos", title, fanart=fanart)

    def _add_catalog(self, items, content):
        for raw in items:
            shown = present_item(raw)
            if shown["kind"] == "skip" or not shown["id"]:
                continue
            if shown["kind"] == "program":
                self.add(
                    self.url(
                        action="program",
                        program_id=shown["id"],
                        title=shown["title"],
                        kids=self.params.get("kids"),
                        tematica=_first_id(raw.get("tematiques")),
                    ),
                    shown["title"],
                    art=shown["art"],
                    info={
                        "mediatype": "tvshow",
                        "title": shown["title"],
                        "tvshowtitle": shown["title"],
                        "plot": shown["plot"],
                        "premiered": shown["premiered"],
                        "year": shown["year"],
                        "mpaa": shown["mpaa"],
                        "genre": shown["genres"],
                    },
                    label2=shown["premiered"] or "",
                )
                continue
            title = shown["title"]
            if shown["generic_episode"] and shown["episode"]:
                title = self.tr(30110) % shown["episode"]
            mediatype = "movie" if shown["film"] or content == "movies" else "episode" if shown["episode"] else "video"
            info = {
                "mediatype": mediatype,
                "title": title,
                "plot": shown["plot"],
                "duration": shown["duration"],
                "premiered": shown["premiered"],
                "year": shown["year"],
                "mpaa": shown["mpaa"],
                "genre": shown["genres"],
            }
            if mediatype == "episode":
                info["tvshowtitle"] = shown["show"]
                info["season"] = shown["season"]
                info["episode"] = shown["episode"]
            self.add(
                self._play_url(shown["id"], title, shown["art"], show=shown.get("show"), raw=raw),
                title,
                art=shown["art"],
                info=info,
                folder=False,
                playable=True,
                label2=shown["premiered"] or "",
            )

    def _add_next(self, pagination, **params):
        try:
            current = int(pagination.get("pagina_actual") or _page(self.params))
            total = int(pagination.get("total_pagines") or 1)
        except (TypeError, ValueError):
            return
        if current >= total:
            return
        self.add(
            self.url(page=current + 1, **params),
            self.tr(30106) % (current + 1, total),
            info={"plot": self.tr(30106) % (current + 1, total)},
        )

    def _content_for(self, items):
        shown = [present_item(item) for item in items]
        shown = [item for item in shown if item["kind"] != "skip"]
        if not shown:
            return "videos"
        if all(item["kind"] == "program" for item in shown):
            return "tvshows"
        if all(item["kind"] == "video" and item["film"] for item in shown):
            return "movies"
        if all(item["kind"] == "video" and item["episode"] for item in shown):
            return "episodes"
        return "videos"


def _first_id(entries):
    for entry in entries or []:
        if isinstance(entry, dict) and entry.get("id"):
            return entry.get("id")
    return ""


def _kids_file(name):
    root = xbmcvfs.translatePath(xbmcaddon.Addon(ADDON_ID).getAddonInfo("path"))
    return os.path.join(root, "resources", "media", "kids", name)


def _kids_art(kind):
    """Poster-friendly art for one Infantil folder. Shared colourful background."""
    icon = _kids_file("icon-%s.png" % kind)
    poster = _kids_file("poster-%s.png" % kind)
    background = _kids_file("fanart.png")
    return {
        "icon": icon,
        "thumb": icon,
        "poster": poster,
        "fanart": background,
        "landscape": background,
        "banner": _kids_file("banner.png"),
        "clearlogo": SX3_CLEARLOGO,
    }


def _page(params):
    try:
        return max(1, int(params.get("page") or 1))
    except ValueError:
        return 1


def _apply_info(item, info):
    tag = item.getVideoInfoTag()
    title = info.get("title")
    if title:
        tag.setTitle(title)
    plot = info.get("plot")
    if plot:
        tag.setPlot(plot)
    if info.get("duration"):
        tag.setDuration(int(info["duration"]))
    if info.get("premiered"):
        tag.setPremiered(info["premiered"])
    if info.get("year"):
        tag.setYear(int(info["year"]))
    if info.get("mediatype"):
        tag.setMediaType(info["mediatype"])
    if info.get("tvshowtitle"):
        tag.setTvShowTitle(info["tvshowtitle"])
    if info.get("season") not in (None, ""):
        tag.setSeason(int(info["season"]))
    if info.get("episode") not in (None, ""):
        tag.setEpisode(int(info["episode"]))
    if info.get("mpaa"):
        tag.setMpaa(info["mpaa"])
    if info.get("genre"):
        tag.setGenres(list(info["genre"]))
    if info.get("resume") and info.get("duration"):
        try:
            tag.setResumePoint(float(info["resume"]), float(info["duration"]))
        except Exception:
            item.setProperty("ResumeTime", str(int(float(info["resume"]))))
            item.setProperty("TotalTime", str(int(float(info["duration"]))))
    tag.setStudios(["3Cat"])


def _has_inputstream():
    return bool(xbmc.getCondVisibility("System.HasAddon(inputstream.adaptive)"))


def _with_ffmpeg_headers(url):
    if "|" in url:
        return url
    return url + "|User-Agent=Mozilla%2F5.0&Referer=https%3A%2F%2Fwww.3cat.cat%2F"


def run(argv=None):
    argv = argv or sys.argv
    handle = int(argv[1])
    query = argv[2][1:] if len(argv) > 2 and argv[2].startswith("?") else ""
    params = dict(parse_qsl(query))
    addon = xbmcaddon.Addon(ADDON_ID)
    profile = xbmcvfs.translatePath(addon.getAddonInfo("profile"))
    client = Client(cache=FileCache(profile), ttl=_int_setting(addon, "cache_minutes", 30, 1, 240) * 60)
    base = argv[0]
    try:
        Router(handle, base, params, addon, client, profile).dispatch()
    except Exception:
        log(traceback.format_exc(), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(addon.getAddonInfo("name"), ui_text(addon, 30116), xbmcgui.NOTIFICATION_ERROR, 6000)
        if params.get("action") == "play":
            xbmcplugin.setResolvedUrl(handle, False, xbmcgui.ListItem())
        else:
            xbmcplugin.endOfDirectory(handle, succeeded=False)
