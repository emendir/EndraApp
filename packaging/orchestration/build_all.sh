#!/bin/bash


# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJ_DIR=$(realpath "$SCRIPT_DIR/../..")
BUILD_RUNNERS_DIR="$PROJ_DIR/packaging/build_runners"

ENDRA_BUILD_SKIP_APK=${ENDRA_BUILD_SKIP_APK-0}

source "$PROJ_DIR/packaging/os_prereqs/os_platform_info.sh"

set -euo pipefail # Exit if any command fails



cd "$SCRIPT_DIR"


case "$OS" in
    Linux)
        "$BUILD_RUNNERS_DIR/flatpak/build_flatpak.sh"
        "$BUILD_RUNNERS_DIR/pyinstaller/build_pyinstaller.sh"
        if [ "$ENDRA_BUILD_SKIP_APK" -eq 0 ];then
            "$BUILD_RUNNERS_DIR/buildozer/build_apk.sh"
        fi
        ;;
    Darwin)
        "$BUILD_RUNNERS_DIR/pyinstaller/build_pyinstaller.sh"
        ;;
    Windows)
        "$BUILD_RUNNERS_DIR/pyinstaller/build_pyinstaller.sh"
        ;;
    *)
        echo "Error: Unsupported platform: $OS"
        exit 1
        ;;
esac
