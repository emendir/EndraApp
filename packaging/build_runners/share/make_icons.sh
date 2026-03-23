#!/usr/bin/env bash
set -euo pipefail

# get the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJ_DIR=$(realpath $SCRIPT_DIR/../..)

# Input SVG file path
ICON_PATH=$PROJ_DIR/src/images/endra-icon.svg

# Output file names
ICO_OUT="$SCRIPT_DIR/endra-icon.ico"
ICNS_OUT="$SCRIPT_DIR/endra-icon.icns"

# Sizes we want
SIZES=(16 32 48 64 128 256 512 1024)

# Create temporary dir
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

echo "Generating icons from: $ICON_PATH"
echo "Working in: $TMPDIR"

# 1. Export PNGs from SVG
for size in "${SIZES[@]}"; do
    echo " - Rendering ${size}x${size}"
    inkscape -w "$size" -h "$size" "$ICON_PATH" -o "$TMPDIR/icon-${size}.png"
done

# 2. Build ICO (Windows)
echo "Building $ICO_OUT"
convert "$TMPDIR"/icon-{16,32,48,64,128,256}.png "$ICO_OUT"

# 3. Build ICNS (macOS)
echo "Building $ICNS_OUT"
png2icns "$ICNS_OUT" "$TMPDIR"/icon-*.png

echo "Done! Files generated:"
ls -lh "$ICO_OUT" "$ICNS_OUT"
