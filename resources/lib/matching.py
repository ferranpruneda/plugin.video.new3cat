"""Tolerant matching for spoken programme titles.

Accents, extra spaces and small mishearings ("ahir" / "air") still rank the
right title first. This does not record audio.
"""

from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher

_PUNCT = re.compile(r"[^a-z0-9 ]+")
_SPACE = re.compile(r"\s+")


def fold(value):
    text = unicodedata.normalize("NFD", value or "")
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    text = text.lower().replace("·", " ")
    text = _PUNCT.sub(" ", text)
    return _SPACE.sub(" ", text).strip()


def similarity(query, title):
    left = fold(query)
    right = fold(title)
    if not left or not right:
        return 0.0
    if left == right:
        return 1.0
    compact_left = left.replace(" ", "")
    compact_right = right.replace(" ", "")
    if compact_left == compact_right:
        return 0.98
    contained = 0.0
    if left in right or right in left or compact_left in compact_right:
        contained = 0.9
    left_words = set(left.split())
    right_words = set(right.split())
    overlap = len(left_words & right_words) / float(len(left_words) or 1)
    ratio = SequenceMatcher(None, compact_left, compact_right).ratio()
    return max(contained, overlap, ratio)


def search_variants(spoken):
    """Queries to send to the API: the words as heard, then without accents."""
    raw = (spoken or "").strip()
    folded = fold(raw)
    variants = []
    for value in (raw, folded):
        if value and value not in variants:
            variants.append(value)
    return variants


def rank_matches(query, items, minimum=0.42):
    """Put close titles first. Weaker API hits stay at the end, not dropped."""
    close = []
    rest = []
    for item in items:
        if not isinstance(item, dict):
            continue
        title = item.get("titol") or ""
        extra = item.get("programa") or item.get("nombonic") or ""
        score = max(similarity(query, title), similarity(query, extra) * 0.95)
        if score >= minimum:
            close.append((score, item))
        else:
            rest.append(item)
    close.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _score, item in close] + rest
