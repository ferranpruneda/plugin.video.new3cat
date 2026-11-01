# -*- coding: utf-8 -*-
"""Checks the public 3Cat endpoints this addon depends on.

These tests need network access. They only request URLs the website already
publishes and do not try to unlock DRM or geo-blocked segments.
"""

import unittest
from urllib.request import Request, urlopen

from resources.lib.api import USER_AGENT, Client
from resources.lib.cache import MemoryCache
from resources.lib.parsing import present_item


def _fetch_bytes(url, limit=1200):
    request = Request(url, headers={"User-Agent": USER_AGENT, "Referer": "https://www.3cat.cat/"})
    with urlopen(request, timeout=30) as response:
        return response.status, response.headers.get("content-type", ""), response.read(limit)


class LiveApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client(cache=MemoryCache(), ttl=120)

    def test_catalog_categories_and_search(self):
        categories = self.client.categories()
        slugs = {item["slug"] for item in categories}
        self.assertIn("series", slugs)
        self.assertIn("pellicules", slugs)
        self.assertIn("sx3", slugs)
        rows = self.client.section_rows("series")
        self.assertGreaterEqual(len(rows), 3)
        self.assertTrue(all(row.get("nom") and row.get("url_dades") for row in rows))
        programs, page = self.client.programs(page=1, page_size=5, tematica="PUFICCIO")
        self.assertGreater(page.get("total_items", 0), 0)
        self.assertGreaterEqual(len(programs), 1)
        shown = present_item(programs[0])
        self.assertEqual(shown["kind"], "program")
        self.assertTrue(shown["title"])
        found, search_page = self.client.search("crims", kind="program", page=1, page_size=5)
        self.assertGreater(search_page.get("total_items", 0), 0)
        self.assertTrue(found)

    def test_infantil_age_codes(self):
        items, page = self.client.programs(page=1, page_size=3, codi_etic="CE_IN")
        self.assertGreater(page.get("total_items", 0), 0)
        self.assertTrue(items)
        for item in items:
            codes = [entry.get("id") for entry in item.get("codis_etics") or []]
            self.assertIn("CE_IN", codes)
        older, older_page = self.client.programs(
            page=1, page_size=2, canal="PUC_S3", codi_etic="CE_07"
        )
        self.assertGreater(older_page.get("total_items", 0), 0)
        self.assertTrue(older)

    def test_latest_and_rankings(self):
        videos, page = self.client.latest(page=1, page_size=4)
        self.assertGreater(page.get("total_items", 0), 0)
        self.assertTrue(any(present_item(video)["kind"] == "video" for video in videos))
        rows = self.client.ranking_rows()
        names = " ".join((row.get("nom") or "").lower() for row in rows)
        self.assertIn("vist", names)
        self.assertNotIn("escoltat", names)

    def test_program_seasons_and_clear_vod(self):
        shows, _page = self.client.programs(page=1, page_size=8, tematica="PUFICCIO")
        opened = None
        for show in shows:
            _detail, seasons = self.client.seasons(show["id"])
            if not seasons:
                continue
            episodes, pagination = self.client.episodes(
                show["id"], seasons[-1]["id"], page=1, page_size=3
            )
            if episodes and pagination.get("total_items"):
                opened = (show, seasons, episodes)
                break
        self.assertIsNotNone(opened, "no fiction programme exposed episodes")
        _show, seasons, episodes = opened
        self.assertGreaterEqual(len(seasons), 1)
        episode = present_item(episodes[0])
        self.assertEqual(episode["kind"], "video")
        self.assertTrue(episode["art"].get("thumb") or episode["art"].get("fanart"))
        resolved = self.client.resolve(video_id=episode["id"], mode="mp4")
        self.assertTrue(resolved["ok"], resolved)
        stream = resolved["stream"]
        self.assertIn(stream["protocol"], ("mp4", "mpd", "hls"))
        status, content_type, body = _fetch_bytes(stream["url"])
        self.assertIn(status, (200, 206))
        if stream["protocol"] == "mp4":
            self.assertIn(b"ftyp", body[:32])
        elif stream["protocol"] == "mpd":
            text = body.decode("utf-8", "replace")
            self.assertIn("<MPD", text)
            self.assertNotIn("ContentProtection", text)

    def test_live_playlists(self):
        geo = self.client.geo()
        channels = {channel["id"]: channel for channel in self.client.live_channels(include_fast=True)}
        for channel_id in ("tv3", "324", "sx3", "c33", "esport3"):
            self.assertIn(channel_id, channels)
        info = self.client.resolve(channel_id="324", mode="auto")
        tv3 = self.client.resolve(channel_id="tv3", mode="auto")
        self.assertTrue(info["ok"])
        self.assertEqual(info["stream"]["protocol"], "hls")
        self.assertEqual(info["stream"]["geo"], "TOTS")
        self.assertFalse(info["stream"]["limited"])
        self.assertTrue(tv3["ok"])
        self.assertEqual(tv3["stream"]["protocol"], "hls")
        # limited is true only when the chosen variant is narrower than the
        # viewer. A worldwide (TOTS) address is not limited.
        chosen_geo = tv3["stream"]["geo"]
        if chosen_geo in (geo, "TOTS"):
            self.assertFalse(tv3["stream"]["limited"])
        else:
            self.assertTrue(tv3["stream"]["limited"])
        status, content_type, body = _fetch_bytes(info["stream"]["url"])
        self.assertEqual(status, 200)
        self.assertIn(b"#EXTM3U", body)
        self.assertIn("mpegurl", content_type)
        tv3_status, _tv3_type, tv3_body = _fetch_bytes(tv3["stream"]["url"])
        if tv3["stream"]["limited"]:
            self.assertIn(tv3_status, (200, 403))
        else:
            self.assertEqual(tv3_status, 200)
            self.assertIn(b"#EXTM3U", tv3_body)


if __name__ == "__main__":
    unittest.main()
