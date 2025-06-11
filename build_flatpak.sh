#!/bin/bash
""":"
  
flatpak remote-add --if-not-exists --user flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install --user flathub runtime/org.freedesktop.Platform/x86_64/24.08
flatpak-builder --user --install  --install-deps-from=flathub --force-clean build-dir flatpak.yaml

flatpak build-export $FLATPAK_REPO_DIR build-dir
flatpak build-bundle $FLATPAK_REPO_DIR dist/endra-current.flatpak tech.emendir.endra 








exit 0
"""
import os
import sys

# Python: re-execute the script in Bash
os.execvp("bash", ["bash", __file__] + sys.argv[1:])
