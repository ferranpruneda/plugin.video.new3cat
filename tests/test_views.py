# -*- coding: utf-8 -*-
import unittest

import xml.etree.ElementTree as ET
from pathlib import Path

from resources.lib.views import (
    ESTUARY_INFOWALL,
    ESTUARY_POSTER,
    ESTUARY_WALL,
    ESTUARY_WIDELIST,
    SECTION_DEFAULT_INDEX,
    SECTION_DEFAULTS,
    directory_content,
    estuary_view_id,
    fill_art,
    listing_section,
    manual_view_update,
    migrate_picked_menu,
    parse_viewmode,
    resolve_directory_view,
    section_view,
)

ROOT = Path(__file__).resolve().parents[1]


class ViewTests(unittest.TestCase):
    def test_estuary_defaults_to_the_wall_for_every_list(self):
        for content in ("videos", "tvshows", "episodes", "movies", "seasons"):
            self.assertEqual(estuary_view_id("skin.estuary", True, "wall", content), ESTUARY_WALL)

    def test_poster_is_only_forced_where_estuary_allows_it(self):
        self.assertEqual(estuary_view_id("skin.estuary", True, "poster", "tvshows"), ESTUARY_POSTER)
        self.assertEqual(estuary_view_id("skin.estuary", True, "poster", "movies"), ESTUARY_POSTER)
        self.assertEqual(estuary_view_id("skin.estuary", True, "poster", "videos"), ESTUARY_WALL)
        self.assertEqual(estuary_view_id("skin.estuary", True, "poster", "episodes"), ESTUARY_WALL)

    def test_infowall_widelist_and_unknown_choice(self):
        self.assertEqual(ESTUARY_INFOWALL, 54)
        self.assertEqual(ESTUARY_WIDELIST, 55)
        for content in ("videos", "tvshows", "episodes", "movies", "seasons"):
            self.assertEqual(estuary_view_id("skin.estuary", True, "infowall", content), ESTUARY_INFOWALL)
            self.assertEqual(estuary_view_id("skin.estuary", True, "widelist", content), ESTUARY_WIDELIST)
        self.assertEqual(estuary_view_id("skin.estuary", True, "no-such", "tvshows"), ESTUARY_WALL)

    def test_section_defaults_match_the_estuary_ids(self):
        self.assertEqual(section_view("menu", ""), "poster")
        self.assertEqual(section_view("video", ""), "widelist")
        self.assertEqual(section_view("programme", ""), "wall")
        for section, index in SECTION_DEFAULT_INDEX.items():
            self.assertEqual(section_view(section, index), SECTION_DEFAULTS[section])
            self.assertEqual(section_view(section, "   "), SECTION_DEFAULTS[section])
        self.assertEqual(section_view("menu", "0"), "wall")
        self.assertEqual(section_view("video", "2"), "infowall")
        self.assertEqual(section_view("programme", "1"), "poster")
        self.assertEqual(section_view("programme", "9"), "wall")
        menu_content = directory_content("menu", "videos")
        self.assertEqual(
            estuary_view_id("skin.estuary", True, section_view("menu", ""), menu_content),
            ESTUARY_POSTER,
        )
        self.assertEqual(
            estuary_view_id("skin.estuary", True, section_view("video", ""), "episodes"),
            ESTUARY_WIDELIST,
        )
        self.assertEqual(
            estuary_view_id("skin.estuary", True, section_view("programme", ""), "tvshows"),
            ESTUARY_WALL,
        )
        self.assertEqual(
            estuary_view_id("skin.estuary", True, section_view("programme", ""), "seasons"),
            ESTUARY_WALL,
        )
        self.assertEqual(
            estuary_view_id("skin.estuary", True, section_view("programme", "1"), "seasons"),
            ESTUARY_POSTER,
        )
        self.assertEqual(
            estuary_view_id("skin.estuary", True, section_view("video", "1"), "episodes"),
            ESTUARY_WALL,
        )

    def test_menu_directories_use_tvshows_so_infowall_keeps_the_poster(self):
        self.assertEqual(directory_content("menu", "videos"), "tvshows")
        self.assertEqual(directory_content("menu", "tvshows"), "tvshows")
        self.assertEqual(directory_content("menu", ""), "tvshows")
        self.assertEqual(directory_content("video", "videos"), "videos")
        self.assertEqual(directory_content("video", "episodes"), "episodes")
        self.assertEqual(directory_content("video", "movies"), "movies")
        self.assertEqual(directory_content("programme", "tvshows"), "tvshows")
        self.assertEqual(directory_content("programme", "seasons"), "seasons")
        shown = directory_content("menu", "videos")
        self.assertEqual(estuary_view_id("skin.estuary", True, "infowall", shown), ESTUARY_INFOWALL)
        self.assertEqual(estuary_view_id("skin.estuary", True, "poster", shown), ESTUARY_POSTER)
        self.assertEqual(estuary_view_id("skin.estuary", True, "widelist", "episodes"), ESTUARY_WIDELIST)

    def test_back_navigation_reapplies_the_section_view(self):
        # Force on: the configured default wins over a view the user tried.
        self.assertEqual(resolve_directory_view("skin.estuary", True, 54, "50"), 54)
        self.assertEqual(resolve_directory_view("skin.estuary", True, 55, ""), 55)
        self.assertIsNone(resolve_directory_view("skin.estuary", True, None, "55"))
        # Force off: only the remembered manual choice is put back.
        self.assertEqual(resolve_directory_view("skin.estuary", False, 54, "51"), 51)
        self.assertIsNone(resolve_directory_view("skin.estuary", False, 54, ""))
        self.assertIsNone(resolve_directory_view("skin.aeon.nox", True, 54, "51"))
        self.assertIsNone(resolve_directory_view("skin.estuary", False, 54, "WideList"))

    def test_manual_view_change_is_stored_per_section(self):
        self.assertEqual(parse_viewmode("54"), 54)
        self.assertIsNone(parse_viewmode(""))
        self.assertIsNone(parse_viewmode("InfoWall"))
        self.assertIsNone(manual_view_update("menu", "54", "54"))
        self.assertEqual(manual_view_update("menu", "54", "51"), ("menu", 51))
        self.assertEqual(manual_view_update("video", "", "55"), ("video", 55))
        self.assertIsNone(manual_view_update("", "54", "50"))
        self.assertIsNone(manual_view_update("menu", "54", ""))
        self.assertIsNone(manual_view_update("other", "54", "50"))
        self.assertIsNone(manual_view_update("menu", "", "54", "54"))
        self.assertEqual(manual_view_update("menu", "", "50", "54"), ("menu", 50))

    def test_upgrade_drops_the_old_infowall_menu_pick_once(self):
        self.assertEqual(migrate_picked_menu("54", ""), ("", "1.0.4", 54))
        self.assertEqual(migrate_picked_menu("54", "1.0.4"), ("54", "1.0.4", None))
        self.assertEqual(migrate_picked_menu("51", ""), ("51", "1.0.4", None))
        self.assertEqual(migrate_picked_menu("", ""), ("", "1.0.4", None))
        self.assertEqual(migrate_picked_menu("500", ""), ("500", "1.0.4", None))

    def test_listing_section_keeps_programmes_and_sends_videos_to_the_wide_list(self):
        self.assertEqual(listing_section("tvshows"), "programme")
        self.assertEqual(listing_section("episodes"), "video")
        self.assertEqual(listing_section("movies"), "video")
        self.assertEqual(listing_section("videos"), "video")

    def test_settings_replace_the_single_view_with_three_defaults(self):
        root = ET.parse(ROOT / "resources" / "settings.xml").getroot()
        found = {node.get("id"): node for node in root.iter("setting")}
        self.assertNotIn("view_type", found)
        self.assertEqual(found["force_view"].get("default"), "true")
        self.assertEqual(found["view_menus"].get("default"), SECTION_DEFAULT_INDEX["menu"])
        self.assertEqual(found["view_videos"].get("default"), SECTION_DEFAULT_INDEX["video"])
        self.assertEqual(found["view_programmes"].get("default"), SECTION_DEFAULT_INDEX["programme"])
        labels = "32024|32025|32026|32027"
        for key in ("view_menus", "view_videos", "view_programmes"):
            self.assertEqual(found[key].get("lvalues"), labels)

    def test_other_skins_and_disabled_force_are_left_alone(self):
        self.assertIsNone(estuary_view_id("skin.estuary", False, "wall", "tvshows"))
        self.assertIsNone(estuary_view_id("skin.aeon.nox.silvo", True, "wall", "tvshows"))
        self.assertIsNone(estuary_view_id("", True, "poster", "videos"))

    def test_fill_art_copies_the_only_picture_into_poster_and_thumb(self):
        art = fill_art({"fanart": "https://img.example/wide.jpg"})
        self.assertEqual(art["poster"], "https://img.example/wide.jpg")
        self.assertEqual(art["thumb"], "https://img.example/wide.jpg")
        self.assertEqual(art["icon"], "https://img.example/wide.jpg")
        kept = fill_art({"poster": "https://img.example/poster.jpg", "thumb": "https://img.example/thumb.jpg"})
        self.assertEqual(kept["poster"], "https://img.example/poster.jpg")
        self.assertEqual(kept["thumb"], "https://img.example/thumb.jpg")
        self.assertEqual(kept["fanart"], "https://img.example/poster.jpg")
        empty = fill_art({}, "https://img.example/fallback-poster.png", "https://img.example/fanart.jpg")
        self.assertEqual(empty["poster"], "https://img.example/fallback-poster.png")
        self.assertEqual(empty["thumb"], "https://img.example/fallback-poster.png")
        self.assertEqual(empty["fanart"], "https://img.example/fanart.jpg")


if __name__ == "__main__":
    unittest.main()
