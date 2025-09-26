#!/bin/bash

## Install kivy with more advanced font handling
## See https://kivy.org/doc/stable/gettingstarted/installation.html#from-source
## This script is tested on Ubuntu-24 (not tested on a fresh installation ):

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPT_DIR

set -e # Exit if any command fails

sudo apt-get update

## Kivy-Dev Dependencies
# Install build tools, and dependencies to perform a full build (including SDL2 dependencies)
sudo apt-get -y install python3-dev build-essential git make autoconf automake libtool \
      pkg-config cmake ninja-build libasound2-dev libpulse-dev libaudio-dev \
      libjack-dev libsndio-dev libsamplerate0-dev libx11-dev libxext-dev \
      libxrandr-dev libxcursor-dev libxfixes-dev libxi-dev libxss-dev libwayland-dev \
      libxkbcommon-dev libdrm-dev libgbm-dev libgl1-mesa-dev libgles2-mesa-dev \
      libegl1-mesa-dev libdbus-1-dev libibus-1.0-dev libudev-dev fcitx-libs-dev

sudo apt install -y libfreetype6-dev libpango1.0-dev libpangoft2-1.0-0

# The following may not be needed
sudo apt install -y ninja-build portaudio19-dev freeglut3-dev

cd "$(mktemp -d)"
curl https://raw.githubusercontent.com/kivy/kivy/master/tools/build_linux_dependencies.sh -o build_kivy_deps.sh
chmod +x build_kivy_deps.sh
./build_kivy_deps.sh
KIVY_DEPS_ROOT=$(pwd)/kivy-dependencies
export KIVY_DEPS_ROOT
export USE_X11=1
python -m pip install "kivy[full]" kivy_examples --no-binary kivy --force-reinstall

## Buildozer Prereqs
## https://buildozer.readthedocs.io/en/latest/installation.html
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo6 cmake libffi-dev libssl-dev
# pip3 install --user --upgrade Cython==0.29.33 virtualenv  # the --user should be removed if you do this in a venv

# add the following line at the end of your ~/.bashrc file
export PATH=$PATH:~/.local/bin/


## Endra's DevOps dependencies:
pip install -r $SCRIPT_DIR/requirements-dev.txt

sudo apt install -y yq


## flatpak deps:
sudo apt install -y qemu-user-static


## icon processing:
sudo apt -y install icnsutils
