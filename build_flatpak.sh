#!/bin/bash
""":"

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECT_DIR=$SCRIPT_DIR


if [ -z $FLATPAK_REPO_DIR ];then
  echo 'Please define `FLATPAK_REPO_DIR`'
exit 1
fi
# pip install $PROJECT_DIR


flatpak remote-add --if-not-exists --user flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install --user flathub runtime/org.freedesktop.Platform/x86_64/24.08
flatpak-builder --user --install  --install-deps-from=flathub --force-clean build-dir flatpak.yaml

flatpak build-export $FLATPAK_REPO_DIR build-dir
flatpak build-bundle $FLATPAK_REPO_DIR dist/endra-current.flatpak tech.emendir.Endra 








exit 0
"""
import os
import sys

# Python: re-execute the script in Bash
os.execvp("bash", ["bash", __file__] + sys.argv[1:])
