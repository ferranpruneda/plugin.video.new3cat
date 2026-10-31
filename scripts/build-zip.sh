#!/usr/bin/env bash
# Build a Kodi-installable zip. The archive root must be plugin.video.new3cat/.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="$(sed -n 's/.*<addon[^>]*version="\([^"]*\)".*/\1/p' "$ROOT/addon.xml" | head -n 1)"
if [[ -z "$VERSION" ]]; then
  echo "Could not read the addon version from addon.xml" >&2
  exit 1
fi

DIST="$ROOT/dist"
STAGE="$(mktemp -d)"
TARGET="$STAGE/plugin.video.new3cat"
mkdir -p "$TARGET" "$DIST"

tar -C "$ROOT" -cf - \
  --exclude='./.git' \
  --exclude='./.github' \
  --exclude='./dist' \
  --exclude='./tests' \
  --exclude='./scripts' \
  --exclude='./.gitignore' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  . | tar -C "$TARGET" -xf -

OUT="$DIST/plugin.video.new3cat-${VERSION}.zip"
rm -f "$OUT"
(
  cd "$STAGE"
  zip -r "$OUT" plugin.video.new3cat
)
rm -rf "$STAGE"
echo "Wrote $OUT"
