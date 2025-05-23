#!/bin/bash
""":"

flatpak install flathub runtime/org.freedesktop.Platform/x86_64/24.08
flatpak-builder --user --install --force-clean build-dir flatpak.yaml

flatpak build-export $FLATPAK_REPO_DIR build-dir
flatpak build-bundle $FLATPAK_REPO_DIR dist/endra-current.flatpak tech.emendir.endra 








exit 0
"""
import os
import sys

# Python: re-execute the script in Bash
os.execvp("bash", ["bash", __file__] + sys.argv[1:])
