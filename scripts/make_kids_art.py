#!/usr/bin/env python3
"""Deprecated. Infantil artwork is now the approved set in resources/media/kids.

Running this script used to draw those files. It no longer does: a new run
would replace the approved pictures. See docs/specs.md.
"""

from __future__ import annotations

import sys


def main():
    print(
        "make_kids_art.py is deprecated. The Infantil pictures live in "
        "resources/media/kids and are not generated.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
