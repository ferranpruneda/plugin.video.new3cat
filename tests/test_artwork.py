# -*- coding: utf-8 -*-
import struct
import subprocess
import sys
import unittest
from pathlib import Path

import hashlib

from resources.lib.artwork import (
    SHIPPED_MEDIA,
    addon_fanart,
    addon_icon,
    addon_path,
    category_art,
    fast_poster,
    kids_filename,
    letter_art,
    live_art,
    menu_art,
    ranking_row_art,
    shelf_slug,
)

# icon.png from tag v1.0.2 (same bytes as v1.0.0).
LOGO_SHA256 = "717b46e5bee052c80e96dcc6855796c9f6faba331c48c4c3542b2c5121d3220f"

ROOT = Path(__file__).resolve().parents[1]


def _png_size(data):
    return struct.unpack(">II", data[16:24])


class ArtworkTests(unittest.TestCase):
    def test_every_shipped_media_file_is_a_real_image(self):
        media = ROOT / "resources" / "media"
        found = sorted(path.relative_to(media).as_posix() for path in media.rglob("*") if path.is_file())
        self.assertEqual(found, sorted(SHIPPED_MEDIA))
        for relative in SHIPPED_MEDIA:
            path = media / relative
            data = path.read_bytes()
            self.assertGreater(len(data), 1000, relative)
            if relative.endswith(".png"):
                self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"), relative)
                if "poster-" in path.name:
                    self.assertEqual(_png_size(data), (480, 720), relative)
                if path.name.startswith("icon-"):
                    self.assertEqual(_png_size(data), (512, 512), relative)
            else:
                self.assertTrue(data.startswith(b"\xff\xd8\xff"), relative)
        self.assertFalse((ROOT / "icon.png").exists())
        self.assertFalse((ROOT / "fanart.jpg").exists())
        self.assertFalse(any(not path.name.endswith("-v2.png") for path in (ROOT / "resources" / "media" / "kids").glob("*.png")))
        icon = pathlib_read(addon_icon())
        fanart = pathlib_read(addon_fanart())
        self.assertEqual(hashlib.sha256(icon).hexdigest(), LOGO_SHA256)
        self.assertEqual(_png_size(icon), (512, 512))
        self.assertTrue(fanart.startswith(b"\xff\xd8\xff"))
        self.assertTrue(addon_icon().endswith("resources/icon-3cat.png"))
        self.assertTrue(addon_fanart().endswith("fanart-v2.jpg"))
        self.assertEqual(kids_filename("poster-home.png"), "poster-home-v2.png")
        self.assertEqual(kids_filename("poster-home-v2.png"), "poster-home-v2.png")

    def test_categories_letters_and_channels_map_to_their_posters(self):
        series = category_art("series")
        self.assertTrue(series["poster"].endswith("categories/poster-series.png"))
        self.assertTrue(series["fanart"].endswith("categories/fanart-series.jpg"))
        sx3 = category_art("sx3")
        self.assertTrue(sx3["poster"].endswith("kids/poster-home-v2.png"))
        self.assertTrue(sx3["icon"].endswith("kids/icon-home-v2.png"))
        self.assertTrue(sx3["fanart"].endswith("kids/fanart-v2.png"))
        unknown = category_art("una-categoria-nova")
        self.assertTrue(unknown["poster"].endswith("categories/poster-generic.png"))
        self.assertTrue(unknown["fanart"].endswith("categories/fanart-generic.jpg"))
        self.assertTrue(letter_art("#")["poster"].endswith("poster-letter-hash.png"))
        self.assertTrue(letter_art("Q")["poster"].endswith("poster-letter-q.png"))
        self.assertTrue(letter_art("")["poster"].endswith("poster-all.png"))
        self.assertTrue(fast_poster("tem2").endswith("poster-fast-tem2.png"))
        self.assertTrue(fast_poster("canal-nou").endswith("poster-fast-generic.png"))
        self.assertTrue(fast_poster("../etc/passwd").endswith("poster-fast-generic.png"))
        self.assertTrue(menu_art("live")["poster"].endswith("menu/poster-live.png"))
        self.assertNotIn("landscape", menu_art("categories"))
        self.assertTrue(os_path_exists(category_art("eva")["poster"]))

    def test_ranking_rows_reuse_one_category_or_the_rankings_poster(self):
        self.assertEqual(shelf_slug("Sèries destacades"), "series")
        self.assertEqual(shelf_slug("Grans pel·lícules"), "pellicules")
        self.assertEqual(shelf_slug("Documentals i reportatges"), "documentals-i-reportatges")
        self.assertEqual(shelf_slug("Món SX3"), "sx3")
        self.assertEqual(shelf_slug("3CatCampus"), "campus")
        self.assertEqual(shelf_slug("EVA"), "eva")
        self.assertIsNone(shelf_slug("El més vist"))
        self.assertIsNone(shelf_slug("Programes i sèries documentals"))
        self.assertTrue(ranking_row_art("Cuines")["poster"].endswith("poster-cuines.png"))
        self.assertTrue(ranking_row_art("El més vist")["poster"].endswith("menu/poster-rankings.png"))
        self.assertTrue(ranking_row_art("EVA")["poster"].endswith("categories/poster-eva.png"))

    def test_live_art_keeps_main_channels_and_logos(self):
        main = live_art(
            {
                "id": "tv3",
                "fast": False,
                "art": {"poster": "https://img.3cat.cat/now.jpg", "clearlogo": "https://img.3cat.cat/tv3.png", "icon": "https://img.3cat.cat/tv3.png"},
            }
        )
        self.assertEqual(main["poster"], "https://img.3cat.cat/now.jpg")
        self.assertEqual(main["clearlogo"], "https://img.3cat.cat/tv3.png")
        fast = live_art(
            {
                "id": "pucfc1",
                "fast": True,
                "art": {"poster": "https://img.3cat.cat/api.jpg", "clearlogo": "https://img.3cat.cat/logo.png"},
            }
        )
        self.assertTrue(fast["poster"].endswith("poster-fast-pucfc1.png"))
        self.assertEqual(fast["icon"], "https://img.3cat.cat/logo.png")
        self.assertEqual(fast["clearlogo"], "https://img.3cat.cat/logo.png")

    def test_kids_generator_is_deprecated(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "make_kids_art.py")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("deprecated", result.stderr.lower())


def os_path_exists(path):
    return Path(path).is_file() and path.startswith(str(addon_path("resources", "media")))


def pathlib_read(path):
    return Path(path).read_bytes()


if __name__ == "__main__":
    unittest.main()
