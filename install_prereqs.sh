#!/bin/bash

## Install kivy with more advanced font handling
## See https://kivy.org/doc/stable/gettingstarted/installation.html#from-source

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPT_DIR

set -e # Exit if any command fails

sudo apt install libfreetype6-dev libpango1.0-dev libpangoft2-1.0-0

cd "$(mktemp -d)"
curl https://raw.githubusercontent.com/kivy/kivy/master/tools/build_linux_dependencies.sh -o build_kivy_deps.sh
chmod +x build_kivy_deps.sh
./build_kivy_deps.sh
KIVY_DEPS_ROOT=$(pwd)/kivy-dependencies
export KIVY_DEPS_ROOT
python -m pip install "kivy[full]" kivy_examples --no-binary kivy
