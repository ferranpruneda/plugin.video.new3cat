"""Small TTL caches for 3Cat API responses."""

from __future__ import annotations

import hashlib
import json
import os
import time


class MemoryCache:
    """Process-local cache. Used by tests and as a fallback."""

    def __init__(self):
        self._data = {}

    def get(self, key):
        item = self._data.get(key)
        if not item:
            return None
        expires, value = item
        if expires < time.time():
            self._data.pop(key, None)
            return None
        return value

    def set(self, key, value, ttl):
        if ttl and ttl > 0:
            self._data[key] = (time.time() + ttl, value)


class FileCache:
    """JSON files with an expiry timestamp. Safe to use from Kodi's profile folder."""

    def __init__(self, directory):
        self.directory = directory
        os.makedirs(directory, exist_ok=True)

    def _path(self, key):
        digest = hashlib.sha1(key.encode("utf-8")).hexdigest()
        return os.path.join(self.directory, digest + ".json")

    def get(self, key):
        path = self._path(key)
        try:
            with open(path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, ValueError):
            return None
        if payload.get("exp", 0) < time.time():
            try:
                os.remove(path)
            except OSError:
                pass
            return None
        return payload.get("data")

    def set(self, key, value, ttl):
        if not ttl or ttl <= 0:
            return
        path = self._path(key)
        temporary = path + ".tmp"
        with open(temporary, "w", encoding="utf-8") as handle:
            json.dump({"exp": time.time() + ttl, "data": value}, handle, ensure_ascii=False)
        os.replace(temporary, path)
