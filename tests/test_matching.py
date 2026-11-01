# -*- coding: utf-8 -*-
import unittest

from resources.lib.matching import fold, rank_matches, search_variants, similarity


class MatchingTests(unittest.TestCase):
    def test_fold_strips_accents_and_punctuation(self):
        self.assertEqual(fold("Àngel Casas!"), "angel casas")
        self.assertEqual(fold("Com si fos ahir"), "com si fos ahir")

    def test_spoken_mishearing_still_matches(self):
        score = similarity("com si fos air", "Com si fos ahir")
        self.assertGreater(score, 0.8)
        self.assertLess(similarity("telenoticies", "Bola de Drac"), 0.5)

    def test_rank_puts_the_closest_title_first(self):
        items = [
            {"id": 1, "titol": "Telenotícies"},
            {"id": 2, "titol": "Com si fos ahir"},
            {"id": 3, "titol": "Crims"},
        ]
        ranked = rank_matches("comsi fos ahir", items)
        self.assertEqual(ranked[0]["id"], 2)

    def test_search_variants_include_folded_form(self):
        self.assertEqual(search_variants("Àngel"), ["Àngel", "angel"])


if __name__ == "__main__":
    unittest.main()
