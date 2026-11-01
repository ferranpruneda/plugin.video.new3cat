# -*- coding: utf-8 -*-
import os
import tempfile
import unittest

from resources.lib.history import HistoryStore, should_resume, stream_key


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.store = HistoryStore(self.directory)

    def test_remember_is_local_and_newest_first(self):
        self.store.remember({"video_id": "1", "title": "Primer", "program_id": 10, "updated": 1})
        self.store.remember({"video_id": "2", "title": "Segon", "program_id": 20, "updated": 2})
        self.store.remember({"video_id": "1", "title": "Primer", "position": 90, "duration": 1000, "updated": 3})
        recent = self.store.recent()
        self.assertEqual([item["video_id"] for item in recent], ["1", "2"])
        self.assertEqual(recent[0]["position"], 90)
        self.assertTrue(os.path.isfile(os.path.join(self.directory, "history.json")))
        with open(self.store.path, encoding="utf-8") as handle:
            self.assertNotIn("stream_url", handle.read())

    def test_resume_rules_and_clear(self):
        self.assertFalse(should_resume({"position": 5, "duration": 1000}))
        self.assertTrue(should_resume({"position": 120, "duration": 1000}))
        self.assertFalse(should_resume({"position": 980, "duration": 1000}))
        self.store.remember({"video_id": "9", "title": "Un", "stream_url": "https://cdn.example/a.mp4|User-Agent=x"})
        self.store.write_pending({"video_id": "9", "stream_url": "https://cdn.example/a.mp4|User-Agent=x"})
        self.assertEqual(stream_key("https://cdn.example/a.mp4|User-Agent=x"), "https://cdn.example/a.mp4")
        self.store.clear()
        self.assertEqual(self.store.recent(), [])
        self.assertFalse(os.path.exists(self.store.pending_path))


if __name__ == "__main__":
    unittest.main()
