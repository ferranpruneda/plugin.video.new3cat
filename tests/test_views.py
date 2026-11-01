# -*- coding: utf-8 -*-
import unittest

from resources.lib.views import (
    ESTUARY_INFOWALL,
    ESTUARY_POSTER,
    ESTUARY_WALL,
    estuary_view_id,
    fill_art,
)


class ViewTests(unittest.TestCase):
    def test_estuary_defaults_to_the_wall_for_every_list(self):
        for content in ("videos", "tvshows", "episodes", "movies", "seasons"):
            self.assertEqual(estuary_view_id("skin.estuary", True, "wall", content), ESTUARY_WALL)

    def test_poster_is_only_forced_where_estuary_allows_it(self):
        self.assertEqual(estuary_view_id("skin.estuary", True, "poster", "tvshows"), ESTUARY_POSTER)
        self.assertEqual(estuary_view_id("skin.estuary", True, "poster", "movies"), ESTUARY_POSTER)
        self.assertEqual(estuary_view_id("skin.estuary", True, "poster", "videos"), ESTUARY_WALL)
        self.assertEqual(estuary_view_id("skin.estuary", True, "poster", "episodes"), ESTUARY_WALL)

    def test_infowall_and_unknown_choice(self):
        self.assertEqual(estuary_view_id("skin.estuary", True, "infowall", "episodes"), ESTUARY_INFOWALL)
        self.assertEqual(estuary_view_id("skin.estuary", True, "no-such", "tvshows"), ESTUARY_WALL)

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


if __name__ == "__main__":
    unittest.main()
