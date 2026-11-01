# -*- coding: utf-8 -*-
import time
import unittest

from resources.lib.api import Client
from resources.lib.cache import MemoryCache


class CacheTests(unittest.TestCase):
    def test_memory_cache_expires(self):
        cache = MemoryCache()
        cache.set("k", {"ok": 1}, ttl=30)
        self.assertEqual(cache.get("k"), {"ok": 1})
        cache._data["k"] = (time.time() - 5, {"ok": 1})
        self.assertIsNone(cache.get("k"))


def _payload(url):
    if "geo.json" in url:
        return {"geo": "TOTS"}
    if "/arafem" in url:
        return {
            "canal": [
                {
                    "name": "tv3",
                    "ara_fem": {
                        "codi_canal": "tv3",
                        "titol_programa": "Tàndem",
                        "titol_capitol": "Capítol",
                        "sinopsi": "Una sèrie.",
                        "durada": "00:48:00",
                        "imatges": [
                            {"rel_name": "IMATGE_169", "mida": "MASTER", "text": "https://img.3cat.cat/now.jpg"}
                        ],
                    },
                }
            ]
        }
    if "/destacats" in url:
        return {
            "resposta": {
                "items": {
                    "num": 1,
                    "item": [
                        {
                            "titol": "3Cat Anime",
                            "avantitol": "Anime",
                            "canals": [{"id": "TEM2"}],
                            "imatges": [
                                {"rel_name": "IMAGE", "mida": "1014x570", "text": "https://img.3cat.cat/anime.jpg"}
                            ],
                        }
                    ],
                },
                "paginacio": {"total_items": 1, "total_pagines": 1, "pagina_actual": 1},
            }
        }
    if "programestv/77" in url:
        return {
            "resposta": {
                "status": "OK",
                "item": {
                    "id": 77,
                    "titol": "Sèrie curta",
                    "tipologia": "PTVC_PROGRAMA",
                    "entradeta": "Dues temporades.",
                    "temporades": [{"id": "PUTEMP_2", "desc": "2a Temporada"}],
                    "imatges": [],
                },
            }
        }
    if "/videos" in url and "temporada=PUTEMP_" in url:
        number = int(url.split("temporada=PUTEMP_")[1].split("&")[0])
        total = {1: 3, 2: 4}.get(number, 0)
        item = [] if total == 0 else [{"id": 1000 + number, "titol": "T%sxC1" % number, "tipologia": "DTY_VIDEO_MM"}]
        return {
            "resposta": {
                "items": {"num": len(item), "item": item},
                "paginacio": {"total_items": total, "items_pagina": 1, "pagina_actual": 1, "total_pagines": total or 0},
            }
        }
    if "media.jsp" in url and "idint=324" in url:
        return {
            "informacio": {"id": "324", "nom": "324"},
            "media": [{"geo": "TOTS", "format": "HLS", "url": "https://cdn.example/324.m3u8"}],
        }
    if "media.jsp" in url and "idint=99" in url:
        return {
            "informacio": {"id": 99},
            "media": {"geo": "TOTS", "format": "MP4", "url": [{"file": "https://drm.example/w.mpd", "label": "widevine"}]},
        }
    if "tematiques" in url or url.endswith("3play_home_tematiques_web_v1.json"):
        return {
            "resposta": {
                "items": {
                    "item": [
                        {
                            "slug": "series",
                            "titol_pastilla": "Sèries",
                            "entradeta": "Sèries",
                            "img_pastilla": "https://statics.3cat.cat/series.png",
                            "imatges": [
                                {"rel_name": "SUPERDESTACAT", "mida": "1014x570", "text": "https://statics.3cat.cat/series.jpg"}
                            ],
                        },
                        {"slug": "podcasts", "titol_pastilla": "Pòdcasts"},
                        {"slug": "entreteniment", "titol_pastilla": "Entreteniment", "entradeta": "Humor"},
                    ]
                }
            }
        }
    raise AssertionError("unexpected url %s" % url)


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.client = Client(fetch=_payload, cache=MemoryCache(), ttl=60)

    def test_live_channels_merge_now_and_fast(self):
        channels = self.client.live_channels(include_fast=True)
        by_id = {channel["id"]: channel for channel in channels}
        self.assertIn("tv3", by_id)
        self.assertIn("Tàndem", by_id["tv3"]["plot"])
        self.assertEqual(by_id["tv3"]["art"]["thumb"], "https://img.3cat.cat/now.jpg")
        self.assertEqual(by_id["tv3"]["art"]["clearlogo"], "https://statics.3cat.cat/img/logos/tv3.png")
        self.assertIn("tem2", by_id)
        self.assertEqual(by_id["tem2"]["title"], "3Cat Anime")

    def test_categories_skip_podcasts_and_mark_fallback(self):
        categories = {item["slug"]: item for item in self.client.categories()}
        self.assertIn("series", categories)
        self.assertNotIn("podcasts", categories)
        self.assertEqual(categories["entreteniment"]["fallback_tematica"], "PUENTRETENIM")
        self.assertFalse(categories["entreteniment"]["has_frontal"])
        self.assertTrue(categories["series"]["has_frontal"])

    def test_season_probe_finds_older_seasons(self):
        _detail, seasons = self.client.seasons(77)
        numbers = [season["number"] for season in seasons]
        self.assertEqual(numbers, [1, 2])
        self.assertEqual(seasons[0]["episodes"], 3)
        self.assertEqual(seasons[1]["title"], "2a Temporada")

    def test_resolve_hls_and_drm(self):
        live = self.client.resolve(channel_id="324", mode="auto")
        self.assertTrue(live["ok"])
        self.assertEqual(live["stream"]["protocol"], "hls")
        self.assertFalse(live["stream"]["limited"])
        blocked = self.client.resolve(video_id="99", mode="auto")
        self.assertFalse(blocked["ok"])
        self.assertEqual(blocked["reason"], "drm")

    def test_refuses_foreign_listing_url(self):
        with self.assertRaises(Exception):
            self.client.listing("https://evil.example/videos", page=1)


if __name__ == "__main__":
    unittest.main()
