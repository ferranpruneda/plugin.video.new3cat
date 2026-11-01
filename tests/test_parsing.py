# -*- coding: utf-8 -*-
import unittest

from resources.lib.parsing import (
    allowed_url,
    art_from_images,
    as_list,
    choose_stream,
    classify,
    ensure_params,
    is_film,
    is_generic_episode_title,
    keep_shelf,
    parse_date,
    parse_duration,
    present_item,
    season_number,
    with_page,
)


class ParsingTests(unittest.TestCase):
    def test_duration_and_date(self):
        self.assertEqual(parse_duration("00:44:07:23"), 44 * 60 + 7)
        self.assertEqual(parse_duration("01:30:00"), 5400)
        self.assertEqual(parse_duration({"milisegons": 2926000}), 2926)
        self.assertIsNone(parse_duration(""))
        self.assertEqual(parse_date("11/09/2017 22:38:00"), "2017-09-11")
        self.assertEqual(parse_date("2026-10-31T19:19:37+01:00"), "2026-10-31")

    def test_artwork_prefers_poster_and_landscape(self):
        art = art_from_images(
            [
                {"rel_name": "img_logo", "mida": "MASTER", "text": "https://img.3cat.cat/logo.png"},
                {"rel_name": "imatge_169", "mida": "MASTER", "text": "https://img.3cat.cat/wide.jpg"},
                {"rel_name": "IMAGE", "mida": "288x422", "text": "https://img.3cat.cat/poster.jpg"},
                {"rel_name": "IMG_POSTER", "mida": "MASTER", "text": "https://img.3cat.cat/poster-master.jpg"},
            ]
        )
        self.assertEqual(art["clearlogo"], "https://img.3cat.cat/logo.png")
        self.assertEqual(art["fanart"], "https://img.3cat.cat/wide.jpg")
        self.assertEqual(art["poster"], "https://img.3cat.cat/poster-master.jpg")

    def test_as_list_shapes(self):
        self.assertEqual(as_list(None), [])
        self.assertEqual(as_list({"id": 1})[0]["id"], 1)
        grouped = {"num": 2, "lletra": [{"valor": "A", "item": [{"id": 2}, {"id": 3}]}]}
        self.assertEqual([item["id"] for item in as_list(grouped)], [2, 3])
        container = {"num": 1, "item": {"id": 9, "titol": "Un"}}
        self.assertEqual(as_list(container)[0]["id"], 9)

    def test_classify_and_film(self):
        self.assertEqual(classify({"tipologia": "PTVC_PROGRAMA", "titol": "A", "id": 1}), "program")
        self.assertEqual(classify({"tipologia": "DTY_VIDEO_MM", "durada": "00:10:00", "id": 2}), "video")
        self.assertEqual(classify({"tipologia": "NOT_NOTICIA", "titol": "N", "id": 3}), "skip")
        self.assertTrue(is_film({"formats": [{"id": "PUFF_FILM", "desc": "Película/Telefilm"}]}))
        self.assertTrue(is_generic_episode_title("T10xC1"))
        self.assertFalse(is_generic_episode_title("Assetjament"))
        shown = present_item(
            {
                "tipologia": "DTY_VIDEO_MM",
                "titol": "T1xC4",
                "id": 5,
                "capitol_temporada": 4,
                "durada": "00:40:00",
                "temporades": [{"id": "PUTEMP_1"}],
                "programa": "Com si fos ahir",
                "data_emissio": "11/09/2017 22:38:00",
            }
        )
        self.assertTrue(shown["generic_episode"])
        self.assertEqual(shown["episode"], 4)
        self.assertEqual(shown["season"], 1)
        self.assertEqual(shown["premiered"], "2017-09-11")
        self.assertEqual(season_number("PUTEMP_10"), 10)

    def test_keep_shelf_skips_audio(self):
        self.assertFalse(keep_shelf({"tipus": "PROGRAMES_RADIO", "nom": "Pòdcasts", "url_dades": "https://api.3cat.cat/x"}))
        self.assertFalse(keep_shelf({"tipus": "RANQUING", "nom": "El més escoltat", "format": "QUADRAT", "url_dades": "https://api.3cat.cat/x"}))
        self.assertTrue(keep_shelf({"tipus": "VIDEOS", "nom": "Novetats", "url_dades": "https://api.3cat.cat/videos"}))
        self.assertTrue(keep_shelf({"tipus": "DIRECTES", "nom": "Directes"}))

    def test_url_helpers(self):
        self.assertTrue(allowed_url("https://api.3cat.cat/videos?a=1"))
        self.assertFalse(allowed_url("http://api.3cat.cat/videos"))
        self.assertFalse(allowed_url("https://evil.example/videos"))
        updated = with_page("https://api.3cat.cat/videos?pagina=1&items_pagina=12", 3)
        self.assertIn("pagina=3", updated)
        self.assertIn("items_pagina=12", updated)
        ensured = ensure_params("https://api.3cat.cat/videos?frontal=abc")
        self.assertIn("master=yes", ensured)
        self.assertIn("sdom=img", ensured)

    def test_choose_live_stream_by_geo(self):
        media = [
            {"geo": "CATALUNYA", "format": "HLS", "url": "https://cdn.example/cat.m3u8"},
            {"geo": "ESPANYA", "format": "HLS", "url": "https://cdn.example/es.m3u8"},
        ]
        abroad = choose_stream(media, "TOTS", mode="auto")
        self.assertEqual(abroad["url"], "https://cdn.example/es.m3u8")
        self.assertEqual(abroad["protocol"], "hls")
        self.assertTrue(abroad["limited"])
        home = choose_stream(media, "CATALUNYA", mode="auto")
        self.assertEqual(home["url"], "https://cdn.example/cat.m3u8")
        self.assertFalse(home["limited"])
        worldwide = choose_stream(
            [{"geo": "TOTS", "format": "HLS", "url": "https://cdn.example/int.m3u8"}],
            "CATALUNYA",
        )
        self.assertFalse(worldwide["limited"])

    def test_choose_vod_prefers_clear_dash_and_keeps_mp4(self):
        media = {
            "geo": "TOTS",
            "format": "MP4",
            "url": [
                {"file": "https://cdn.example/stream.mpd", "label": "DASH", "active": True},
                {"file": "https://cdn.example/high.mp4", "label": "720p", "active": False},
                {"file": "https://cdn.example/low.mp4", "label": "480p", "active": False},
                {"file": "https://drm.example/widevine", "label": "DASH", "drm": "widevine"},
            ],
        }
        auto = choose_stream(media, "TOTS", mode="auto")
        self.assertEqual(auto["protocol"], "mpd")
        self.assertEqual(auto["url"], "https://cdn.example/stream.mpd")
        self.assertEqual(auto["fallback_mp4"], "https://cdn.example/high.mp4")
        mp4 = choose_stream(media, "TOTS", mode="mp4")
        self.assertEqual(mp4["url"], "https://cdn.example/high.mp4")
        self.assertIsNone(mp4["fallback_mp4"])

    def test_drm_only_is_not_playable(self):
        media = {
            "geo": "TOTS",
            "format": "MP4",
            "url": [{"file": "https://drm.example/manifest.mpd", "label": "widevine"}],
        }
        self.assertIsNone(choose_stream(media, "TOTS"))


if __name__ == "__main__":
    unittest.main()
