#!/bin/bash

APP_NAME="Endra" # leave empty to read from pyproject.toml
PYTHON_VERSION="3.11"

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJ_DIR=$(realpath $SCRIPT_DIR/../..)
DIST_DIR=$PROJ_DIR/dist/
MANIFEST_DIR=$SCRIPT_DIR/manifest/
MANIFEST_GEN_DIR=$MANIFEST_DIR/generated_modules

FLATPAK_BUILD_DIR_AARCH=$SCRIPT_DIR/build-dir-aarch
FLATPAK_BUILD_DIR_X86=$SCRIPT_DIR/build-dir-x86
FLATPAK_STATE_DIR=$SCRIPT_DIR/.flatpak-builder

PY_PACKAGE_NAME=$(grep -E '^name\s*=' $PROJ_DIR/pyproject.toml | sed -E 's/name\s*=\s*"(.*)"/\1/')
if [ -z $APP_NAME ];then # allow optional overriding variable using declaration above
  APP_NAME=$PY_PACKAGE_NAME
fi
APP_VERSION=$(grep -E '^version\s*=' $PROJ_DIR/pyproject.toml | sed -E 's/version\s*=\s*"(.*)"/\1/')


## export variables used by the $GET_PYTHON_DEPS script
# general project requirements
export REQS_MAIN=$PROJ_DIR/requirements.txt
# requirements specific to this build pipeline
export REQS_MANUAL=$SCRIPT_DIR/requirements-manual.txt
# requirements to be excluded in this build pipeline
export REQS_EXCLUSIONS=$SCRIPT_DIR/requirements-exclusions.txt
# final generated requirements list
export REQS_AUTO=$SCRIPT_DIR/requirements-auto.txt
# script for generating python requirements
GET_PYTHON_DEPS=$PROJ_DIR/packaging/share/get_python_deps.sh

echo "Project: $APP_NAME"
echo "Version: $APP_VERSION"
set -euo pipefail

if [ -z $FLATPAK_REPO_DIR ];then
  echo 'Please define `FLATPAK_REPO_DIR`'
exit 1
fi

if ! [ -e $DIST_DIR ]; then
  mkdir -p $DIST_DIR
fi

cd $SCRIPT_DIR

# Get App ID from flatpak manifest file name
shopt -s nullglob
files=($MANIFEST_DIR/*"$APP_NAME"*.yml)
(( ${#files[@]} == 1 )) || { echo "❌ Expected exactly one match for *$APP_NAME*.yml, found ${#files[@]}" >&2; exit 1; }
file=${files[0]}
filename=$(basename $file)
APP_ID="${filename%.yml}" # Get the filename without the extension
MANIFEST_FILE=$file
echo "APP ID: $APP_ID"
echo "MANIFEST: $MANIFEST_FILE"

## Prerequisites
flatpak remote-add --if-not-exists --user flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install -y --user flathub org.flatpak.Builder


if [ -e $MANIFEST_GEN_DIR ];then
  rm -rf $MANIFEST_GEN_DIR
fi
mkdir -p $MANIFEST_GEN_DIR

export PY_VENV_DIR=$(mktemp -d)
virtualenv $PY_VENV_DIR
source $PY_VENV_DIR/bin/activate
pip install req2flatpak
pip install flatpak_pip_generator
pip install pyyaml

# generate $REQS_AUTO file with python dependencies
$GET_PYTHON_DEPS

# Generate Flatpak modules from requirements files
PYVER="${PYTHON_VERSION//./}"
PY_REQS_MANIFEST=$MANIFEST_GEN_DIR/python3-modules-auto.yml
python3 -m req2flatpak --requirements-file $REQS_AUTO --target-platforms $PYVER-x86_64 $PYVER-aarch64 -o $PY_REQS_MANIFEST

# patch PY_REQS_MANIFEST
sed -i 's/pip3 install/pip3 install --ignore-installed/g' $PY_REQS_MANIFEST

cd $PROJ_DIR
# validate Flatpak Manifest
flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest $MANIFEST_FILE || true


## Flatpak MetaInfo XML
# generate MetaInfo XML file from pyproject.toml
python $SCRIPT_DIR/generate_metainfo.py $PROJ_DIR/pyproject.toml $APP_ID  "$MANIFEST_DIR/${APP_ID}.metainfo.xml"
# validate MetaInfo XML file  
flatpak run --command=flatpak-builder-lint org.flatpak.Builder appstream "${MANIFEST_DIR}/${APP_ID}.metainfo.xml" || true



cd $SCRIPT_DIR

# Get the CPU architecture
ARCH=$(uname -m)

# x86_64 build
if [ "$ARCH" == "x86_64" ]; then
    flatpak run org.flatpak.Builder \
      --arch=x86_64 \
      --force-clean --ccache \
      --user --install \
      --install-deps-from=flathub \
      --mirror-screenshots-url=https://dl.flathub.org/media/ \
      --repo=$FLATPAK_REPO_DIR \
      --state-dir=$FLATPAK_STATE_DIR \
      $FLATPAK_BUILD_DIR_X86 \
      $MANIFEST_FILE #  \
      # --sandbox 
    flatpak build-export $FLATPAK_REPO_DIR $FLATPAK_BUILD_DIR_X86
    # bundle for x86_64
    flatpak build-bundle $FLATPAK_REPO_DIR $DIST_DIR/${APP_NAME}_v${APP_VERSION}_linux_x86_64.flatpak $APP_ID --arch=x86_64
fi

# aarch64 build
if [ "$ARCH" == "aarch64" ]; then
    flatpak run org.flatpak.Builder \
      --arch=aarch64 \
      --force-clean --ccache \
      --user --install \
      --install-deps-from=flathub \
      --mirror-screenshots-url=https://dl.flathub.org/media/ \
      --repo=$FLATPAK_REPO_DIR \
      --state-dir=$FLATPAK_STATE_DIR \
      $FLATPAK_BUILD_DIR_AARCH \
      $MANIFEST_FILE  # \
      # --sandbox 
    flatpak build-export $FLATPAK_REPO_DIR $FLATPAK_BUILD_DIR_AARCH
    # bundle for aarch64
    flatpak build-bundle $FLATPAK_REPO_DIR $DIST_DIR/${APP_NAME}_v${APP_VERSION}_linux_aarch64.flatpak $APP_ID --arch=aarch64
fi


echo "
To debug the flatpak build, run this from the project directory:

flatpak-builder --run \
 $FLATPAK_BUILD_DIR_X86 \
 $SCRIPT_DIR/$APP_ID.yml \
 sh
"

