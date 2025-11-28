#!/bin/bash

## Install kivy with more advanced font handling
## See https://kivy.org/doc/stable/gettingstarted/installation.html#from-source
## This script is tested on Ubuntu-24 (not tested on a fresh installation ):

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPT_DIR
source $SCRIPT_DIR/os_package_utils.sh

set -euo pipefail # Exit if any command/script fails

# install prerequisites with apt, if available
if command -v "apt" >/dev/null 2>&1; then
    sudo apt-get update

    ## Kivy-Dev Dependencies
    sudo apt-get -y install python3-dev build-essential git make autoconf automake libtool \
          pkg-config cmake ninja-build libasound2-dev libpulse-dev libaudio-dev \
          libjack-dev libsndio-dev libsamplerate0-dev libx11-dev libxext-dev \
          libxrandr-dev libxcursor-dev libxfixes-dev libxi-dev libxss-dev libwayland-dev \
          libxkbcommon-dev libdrm-dev libgbm-dev libgl1-mesa-dev libgles2-mesa-dev \
          libegl1-mesa-dev libdbus-1-dev libibus-1.0-dev libudev-dev fcitx-libs-dev
    # The following may not be needed
    sudo apt install -y ninja-build portaudio19-dev freeglut3-dev

    sudo apt install -y libfreetype6-dev libpango1.0-dev libpangoft2-1.0-0

    sudo apt install -y yq


    ## flatpak deps:
    sudo apt install -y qemu-user-static


    ## icon processing:
    sudo apt -y install icnsutils

    ## liboqs
    sudo apt install -y build-essential python3-dev cmake libssl-dev

    ## Buildozer-Prerequisites
    sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo6 cmake libffi-dev libssl-dev
else # apt is not available
    REQUIRED_COMMANDS=(
        git
        cmake
        make
        )
    if check_commands "${REQUIRED_COMMANDS[@]}";then
        echo "Found all necessary prerequisite tools!"
    else
        echo "Could not find all prerequisite tools. Install them manually, or install apt so that I can install them."
        exit 1
    fi
fi

