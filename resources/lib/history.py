"""Watch history stored only in the addon profile. Nothing is uploaded."""

from __future__ import annotations

import json
import os
import time

HISTORY_NAME = "history.json"
PENDING_NAME = "now_playing.json"
MAX_ITEMS = 40


def stream_key(url):
    return (url or "").split("|", 1)[0].split("?", 1)[0]


def should_resume(item):
    try:
        position = float(item.get("position") or 0)
        duration = float(item.get("duration") or 0)
    except (TypeError, ValueError):
        return False
    if position < 20:
        return False
    if duration and (position >= duration * 0.92 or duration - position < 30):
        return False
    return True


def format_position(seconds):
    try:
        total = max(0, int(float(seconds)))
    except (TypeError, ValueError):
        return ""
    minutes, _secs = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return "%d h %d min" % (hours, minutes)
    return "%d min" % max(minutes, 1)


class HistoryStore:
    def __init__(self, directory):
        self.directory = directory
        self.path = os.path.join(directory, HISTORY_NAME)
        self.pending_path = os.path.join(directory, PENDING_NAME)

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, ValueError):
            return []
        if not isinstance(data, list):
            return []
        return [item for item in data if isinstance(item, dict) and item.get("video_id")]

    def get(self, video_id):
        for item in self.load():
            if str(item.get("video_id")) == str(video_id):
                return item
        return None

    def remember(self, item):
        video_id = str(item.get("video_id") or "")
        if not video_id:
            return
        stored = {
            "video_id": video_id,
            "program_id": str(item.get("program_id") or ""),
            "title": item.get("title") or "",
            "show": item.get("show") or "",
            "plot": item.get("plot") or "",
            "thumb": item.get("thumb") or "",
            "fanart": item.get("fanart") or "",
            "tematica": str(item.get("tematica") or ""),
            "position": _number(item.get("position")),
            "duration": _number(item.get("duration")),
            "updated": item.get("updated") or time.time(),
        }
        others = [entry for entry in self.load() if str(entry.get("video_id")) != video_id]
        self._write(self.path, [stored] + others[: MAX_ITEMS - 1])

    def recent(self, limit=24):
        items = self.load()
        items.sort(key=lambda entry: entry.get("updated") or 0, reverse=True)
        return items[:limit]

    def program_ids(self, limit=5):
        found = []
        for item in self.recent(MAX_ITEMS):
            program_id = str(item.get("program_id") or "")
            if program_id and program_id not in found:
                found.append(program_id)
            if len(found) >= limit:
                break
        return found

    def clear(self):
        for path in (self.path, self.pending_path):
            try:
                os.remove(path)
            except OSError:
                pass

    def write_pending(self, item):
        payload = dict(item)
        payload["stream_url"] = stream_key(item.get("stream_url") or "")
        self._write(self.pending_path, payload)

    def _write(self, path, payload):
        os.makedirs(self.directory, exist_ok=True)
        temporary = path + ".tmp"
        with open(temporary, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False)
        os.replace(temporary, path)


def _number(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0
