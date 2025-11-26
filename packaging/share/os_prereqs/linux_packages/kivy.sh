#!/bin/bash

## Install kivy (with more advanced font handling if prerequisites are installed)
## See https://kivy.org/doc/stable/gettingstarted/installation.html#from-source
## This script is tested on Ubuntu-24 (not tested on a fresh installation ):

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPT_DIR
source $SCRIPT_DIR/os_package_utils.sh

cd "$(mktemp -d)"
curl https://raw.githubusercontent.com/kivy/kivy/master/tools/build_linux_dependencies.sh -o build_kivy_deps.sh
chmod +x build_kivy_deps.sh
./build_kivy_deps.sh
KIVY_DEPS_ROOT=$(pwd)/kivy-dependencies
export KIVY_DEPS_ROOT
export USE_X11=1
python -m pip install "kivy[full]" kivy_examples --no-binary kivy --force-reinstall
