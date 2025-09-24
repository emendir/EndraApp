#!/bin/bash

APP_NAME="Endra" # leave empty to read from pyproject.toml
PYTHON_VERSION="3.11"

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECT_DIR=$(realpath $SCRIPT_DIR/../..)
DIST_DIR=$PROJECT_DIR/dist/
MANIFEST_DIR=$SCRIPT_DIR/manifest/
MANIFEST_GEN_DIR=$MANIFEST_DIR/generated_modules

FLATPAK_BUILD_DIR_AARCH=$SCRIPT_DIR/build-dir-aarch
FLATPAK_BUILD_DIR_X86=$SCRIPT_DIR/build-dir-x86
FLATPAK_STATE_DIR=$SCRIPT_DIR/.flatpak-builder

if [ -z $APP_NAME ];then # allow optional overriding variable using declaration above
  APP_NAME=$(grep -E '^name\s*=' $PROJECT_DIR/pyproject.toml | sed -E 's/name\s*=\s*"(.*)"/\1/')
fi
APP_VERSION=$(grep -E '^version\s*=' $PROJECT_DIR/pyproject.toml | sed -E 's/version\s*=\s*"(.*)"/\1/')


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

REQS_AUTO=$SCRIPT_DIR/requirements-auto.txt
REQS_MANUAL=$SCRIPT_DIR/requirements-manual.txt
REQS_EXCLUSIONS=$SCRIPT_DIR/requirements-exclusions.txt
pip install $PROJECT_DIR --force-reinstall
# reinstall python packages that are editable installs (needed for listing dependencies)
pkgs=$(pipdeptree --packages . -f --warn silence \
  | sed 's/^[[:space:]]*//' \
  | sort -u \
  | grep -v "$APP_NAME" \
  | grep -i "@" || true \
  | awk '{print $1}')
if [ -n "$pkgs" ]; then
    echo "$pkgs" | while read -r pkg_name; do
        echo "Reinstalling $pkg_name"
        pip install --force-reinstall "$pkg_name"
    done
else
    echo "No packages to reinstall."
fi

if [ -e $MANIFEST_GEN_DIR ];then
  rm -rf $MANIFEST_GEN_DIR
fi
mkdir -p $MANIFEST_GEN_DIR
# list all python dependencies recursively with versions
pipdeptree --packages $APP_NAME -f --warn silence \
  | sed 's/^[[:space:]]*//' \
  | sort -u \
  | grep -v -i "^$APP_NAME" \
  | grep -v "/"  \
  | grep -v "Editable" \
  | tee $REQS_AUTO

## Filter auto-generated python dependecies using exclusions list
if [ -e $REQS_EXCLUSIONS ];then
  tmp_file="$(mktemp)"
  # Build grep pattern from exclusions (anchored at start of line, before ==)
  pattern=$(sed 's/^/^/; s/$/==/' "$REQS_EXCLUSIONS" | paste -sd'|' -)
  # If pattern is empty (no exclusions), just copy the file
  if [[ -z "$pattern" ]]; then
      cp "$REQS_AUTO" "$tmp_file"
  else
      grep -Ev "$pattern" "$REQS_AUTO" > "$tmp_file"
  fi
  mv "$tmp_file" "$REQS_AUTO"
fi

## Generate Flatpak modules from requirements files
PYVER="${PYTHON_VERSION//./}"
req2flatpak --requirements-file $REQS_AUTO --target-platforms $PYVER-x86_64 $PYVER-aarch64 -o $MANIFEST_GEN_DIR/python3-modules-auto.yml
if [ -e $SCRIPT_DIR/requirements-manual.txt ];then
  req2flatpak --requirements-file $SCRIPT_DIR/requirements-manual.txt --target-platforms $PYVER-x86_64 $PYVER-aarch64 -o $MANIFEST_GEN_DIR/python3-modules-manual.yml

  # Patch python module builds for packages that should ignore system installs
  sed -i 's/pip3 install /pip3 install --ignore-installed /' $MANIFEST_GEN_DIR/python3-modules-manual.yml
fi


cd $PROJECT_DIR
# validate Flatpak Manifest
flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest $MANIFEST_FILE || true


## Flatpak MetaInfo XML
# generate MetaInfo XML file from pyproject.toml
python $SCRIPT_DIR/generate_metainfo.py $PROJECT_DIR/pyproject.toml $APP_ID  "$MANIFEST_DIR/${APP_ID}.metainfo.xml"
# validate MetaInfo XML file  
flatpak run --command=flatpak-builder-lint org.flatpak.Builder appstream "${MANIFEST_DIR}/${APP_ID}.metainfo.xml" || true



cd $SCRIPT_DIR
# x86_64 build
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


# # aarch64 build
# flatpak run org.flatpak.Builder \
#   --arch=aarch64 \
#   --force-clean --ccache \
#   --user --install \
#   --install-deps-from=flathub \
#   --mirror-screenshots-url=https://dl.flathub.org/media/ \
#   --repo=$FLATPAK_REPO_DIR \
#   --state-dir=$FLATPAK_STATE_DIR \
#   $FLATPAK_BUILD_DIR_AARCH \
#   $MANIFEST_FILE  # \
#   # --sandbox 
# flatpak build-export $FLATPAK_REPO_DIR $FLATPAK_BUILD_DIR_AARCH
# # bundle for aarch64
# flatpak build-bundle $FLATPAK_REPO_DIR $DIST_DIR/${APP_NAME}_v${APP_VERSION}_linux_aarch64.flatpak $APP_ID --arch=aarch64



echo "
To debug the flatpak build, run this from the project directory:

flatpak-builder --run \
 $FLATPAK_BUILD_DIR_X86 \
 $SCRIPT_DIR/$APP_ID.yml \
 sh
"

