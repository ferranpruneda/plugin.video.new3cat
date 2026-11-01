# -*- coding: utf-8 -*-
import unittest
from pathlib import Path

from resources.lib.strings import category_title, text

KIDS_MEDIA = Path(__file__).resolve().parents[1] / "resources" / "media" / "kids"
KIDS_FILES = (
    "fanart.png",
    "banner.png",
    "icon-home.png",
    "poster-home.png",
    "icon-live.png",
    "poster-live.png",
    "icon-programmes.png",
    "poster-programmes.png",
    "icon-ages.png",
    "poster-ages.png",
    "icon-petits.png",
    "poster-petits.png",
    "icon-tots.png",
    "poster-tots.png",
    "icon-age7.png",
    "poster-age7.png",
    "icon-age10.png",
    "poster-age10.png",
    "icon-highlights.png",
    "poster-highlights.png",
)


class StringTests(unittest.TestCase):
    def test_default_is_catalan_even_if_kodi_is_spanish(self):
        self.assertEqual(text(30100, follow_kodi=False, kodi_language="es"), "Directes")
        self.assertEqual(text(30105, follow_kodi=False, kodi_language="en"), "Cerca")

    def test_follow_kodi_language(self):
        self.assertEqual(text(30102, follow_kodi=True, kodi_language="es"), "Novedades")
        self.assertEqual(text(30102, follow_kodi=True, kodi_language="en_GB"), "Latest")
        self.assertEqual(text(30102, follow_kodi=True, kodi_language="ca"), "Novetats")
        self.assertEqual(text(30100, follow_kodi=True, kodi_language="fr"), "Directes")
        self.assertEqual(text(30130, follow_kodi=False, kodi_language="es"), "Infantil")
        self.assertEqual(text(30134, follow_kodi=True, kodi_language="es"), "Los más pequeños")

    def test_kids_artwork_is_original_png(self):
        for name in KIDS_FILES:
            path = KIDS_MEDIA / name
            data = path.read_bytes()
            self.assertGreater(len(data), 1000, name)
            self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"), name)

    def test_category_titles_ignore_a_foreign_api_name(self):
        self.assertEqual(category_title("pellicules", "Películas"), "Pel·lícules")
        self.assertEqual(category_title("sx3", None), "SX3")
        self.assertEqual(category_title("desconegut", "Un nom"), "Un nom")


if __name__ == "__main__":
    unittest.main()
