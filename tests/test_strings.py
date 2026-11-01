# -*- coding: utf-8 -*-
import unittest
from pathlib import Path

from resources.lib.strings import (
    CATEGORY_PLOT_IDS,
    ROOT_MENU_PLOTS,
    STRINGS,
    category_plot,
    category_title,
    folder_plot,
    letter_plot,
    search_plot,
    text,
)

ROOT = Path(__file__).resolve().parents[1]
KIDS_MEDIA = ROOT / "resources" / "media" / "kids"
KIDS_FILES = (
    "fanart-v2.png",
    "banner-v2.png",
    "icon-home-v2.png",
    "poster-home-v2.png",
    "icon-live-v2.png",
    "poster-live-v2.png",
    "icon-programmes-v2.png",
    "poster-programmes-v2.png",
    "icon-ages-v2.png",
    "poster-ages-v2.png",
    "icon-petits-v2.png",
    "poster-petits-v2.png",
    "icon-tots-v2.png",
    "poster-tots-v2.png",
    "icon-age7-v2.png",
    "poster-age7-v2.png",
    "icon-age10-v2.png",
    "poster-age10-v2.png",
    "icon-highlights-v2.png",
    "poster-highlights-v2.png",
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

    def test_menu_descriptions_exist_in_catalan_spanish_and_english(self):
        ids = set(range(30160, 30195))
        ids.update(ROOT_MENU_PLOTS.values())
        ids.update(CATEGORY_PLOT_IDS.values())
        for lang in ("ca", "es", "en"):
            for string_id in ids:
                value = STRINGS[lang][string_id]
                self.assertTrue(value.strip(), "%s %s" % (lang, string_id))
                self.assertNotEqual(STRINGS["ca"][string_id], STRINGS["es"][string_id])
                self.assertNotEqual(STRINGS["ca"][string_id], STRINGS["en"][string_id])
        for action, plot_id in ROOT_MENU_PLOTS.items():
            title_id = {
                "live": 30100,
                "rankings": 30101,
                "latest": 30102,
                "categories": 30103,
                "letters": 30104,
                "search": 30105,
                "voice": 30150,
                "continue": 30152,
            }[action]
            self.assertNotEqual(text(plot_id).casefold(), text(title_id).casefold())

    def test_category_plot_keeps_a_real_api_text_and_fills_the_gap(self):
        api = "Qualitat i rigor: tot el que està passant quan està passant"
        self.assertEqual(category_plot("actualitat", api, "Actualitat"), api)
        self.assertEqual(
            category_plot("series", "", "Sèries"),
            text(30189),
        )
        self.assertEqual(
            category_plot("series", "Sèries", "Sèries", follow_kodi=True, kodi_language="es"),
            text(30189, follow_kodi=True, kodi_language="es"),
        )
        self.assertIn("secció", category_plot("nova", "", "Nova").casefold())
        self.assertNotEqual(category_plot("cuines", "", "Cuines").casefold(), "cuines")

    def test_folder_letter_and_search_plots_are_never_just_the_title(self):
        def translate(string_id):
            return text(string_id)

        shelf = folder_plot("", "Sèries destacades", "PROGRAMES", translate)
        self.assertNotEqual(shelf.casefold(), "sèries destacades")
        self.assertIn("Sèries destacades", shelf)
        self.assertEqual(folder_plot("Una fila amb sinopsi", "Sèries destacades", "PROGRAMES", translate), "Una fila amb sinopsi")
        self.assertTrue(folder_plot("", "Directes", "DIRECTES", translate))
        self.assertNotEqual(folder_plot("", "Directes", "DIRECTES", translate).casefold(), "directes")
        self.assertTrue(folder_plot("", "", "", translate))
        for label in ["#"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            plot = letter_plot(label, translate)
            self.assertTrue(plot.strip())
            self.assertNotEqual(plot.casefold(), label.casefold())
        self.assertIn("Polònia", search_plot("program", "Polònia", translate))
        self.assertIn("100%", search_plot("video", "100%", translate))

    def test_po_files_carry_the_descriptions_and_keep_settings_in_catalan(self):
        languages = {
            "ca_es": "ca",
            "es_es": "es",
            "en_gb": "en",
        }
        for folder, lang in languages.items():
            path = ROOT / "resources" / "language" / ("resource.language.%s" % folder) / "strings.po"
            entries = _parse_po(path)
            for string_id in range(30160, 30195):
                key = "#%s" % string_id
                self.assertIn(key, entries)
                self.assertEqual(entries[key], STRINGS[lang][string_id])
            self.assertEqual(entries["#32027"], "Llista ampla")
            self.assertEqual(entries["#32028"], "Menús i categories")
            self.assertEqual(entries["#32029"], "Vídeos i directes")
            self.assertEqual(entries["#32030"], "Programes")
            self.assertEqual(entries["#32022"], "Força la vista d'Estuary")


def _parse_po(path):
    entries = {}
    current = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("msgctxt "):
            current = line.split('"', 2)[1]
        elif line.startswith("msgstr ") and current:
            entries[current] = line.split('"', 2)[1]
            current = None
    return entries


if __name__ == "__main__":
    unittest.main()
