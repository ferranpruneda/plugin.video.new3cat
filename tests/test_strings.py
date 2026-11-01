# -*- coding: utf-8 -*-
import unittest

from resources.lib.strings import category_title, text


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

    def test_category_titles_ignore_a_foreign_api_name(self):
        self.assertEqual(category_title("pellicules", "Películas"), "Pel·lícules")
        self.assertEqual(category_title("sx3", None), "SX3")
        self.assertEqual(category_title("desconegut", "Un nom"), "Un nom")


if __name__ == "__main__":
    unittest.main()
