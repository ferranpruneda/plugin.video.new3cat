# -*- coding: utf-8 -*-
import struct
import subprocess
import sys
import unittest
from pathlib import Path

from resources.lib.artwork import (
    SHIPPED_MEDIA,
    addon_fanart,
    addon_path,
    category_art,
    fast_poster,
    letter_art,
    live_art,
    menu_art,
    ranking_row_art,
    shelf_slug,
)

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
        icon = (ROOT / "icon.png").read_bytes()
        fanart = (ROOT / "fanart.jpg").read_bytes()
        self.assertTrue(icon.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertEqual(_png_size(icon), (512, 512))
        self.assertTrue(fanart.startswith(b"\xff\xd8\xff"))
        self.assertEqual(addon_fanart(), str(ROOT / "fanart.jpg"))

    def test_categories_letters_and_channels_map_to_their_posters(self):
        series = category_art("series")
        self.assertTrue(series["poster"].endswith("categories/poster-series.png"))
        self.assertTrue(series["fanart"].endswith("categories/fanart-series.jpg"))
        sx3 = category_art("sx3")
        self.assertTrue(sx3["poster"].endswith("kids/poster-home.png"))
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


if __name__ == "__main__":
    unittest.main()
