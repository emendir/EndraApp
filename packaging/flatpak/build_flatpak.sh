#!/bin/bash

PACKAGE_NAME=endra_app

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECT_DIR=$(realpath $SCRIPT_DIR/../..)
DIST_DIR=$PROJECT_DIR/dist/

FLATPAK_BUILD_DIR=$SCRIPT_DIR/build-dir
FLATPAK_STATE_DIR=$SCRIPT_DIR/.flatpak-builder

if [ -z $FLATPAK_REPO_DIR ];then
  echo 'Please define `FLATPAK_REPO_DIR`'
exit 1
fi

set -euo pipefail

cd $SCRIPT_DIR

# Get App ID from flatpak manifest file name
shopt -s nullglob  # Makes *.yml expand to an empty array if no match
yml_files=(*.yml) # Get all .yml files in the current directory
# Count the number of .yml files
if [ ${#yml_files[@]} -ne 1 ] ; then
    echo "Error: Expected exactly one .yml file, found ${#yml_files[@]}."
    exit 1
fi
# Get the filename without the extension
APP_ID="${yml_files[0]%.yml}"
echo "APP ID: $APP_ID"

## Prerequisites
flatpak install -y --user flathub org.flatpak.Builder
flatpak remote-add --if-not-exists --user flathub https://dl.flathub.org/repo/flathub.flatpakrepo

pip install $PROJECT_DIR --force-reinstall
# reinstall python packages that are editable installs (needed for listing dependencies)
pkgs=$(pipdeptree --packages . -f --warn silence \
  | sed 's/^[[:space:]]*//' \
  | sort -u \
  | grep -v "$PACKAGE_NAME" \
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

# list all python dependencies recursively with versions
pipdeptree --packages $PACKAGE_NAME -f --warn silence \
  | sed 's/^[[:space:]]*//' \
  | sort -u \
  | grep -v -i "^$PACKAGE_NAME" \
  | grep -v "/"  \
  | grep -v "Editable" \
  | tee $SCRIPT_DIR/requirements-full.txt

## Generate Flatpak modules from requirements files
req2flatpak --requirements-file $SCRIPT_DIR/requirements-full.txt --target-platforms 311-x86_64 311-aarch64 -o python3-modules-full.json
req2flatpak --requirements-file $SCRIPT_DIR/requirements-prereqs.txt --target-platforms 311-x86_64 311-aarch64 -o python3-modules-prereqs.json
# req2flatpak --requirements-file $SCRIPT_DIR/requirements-flatpak-binary.txt --target-platforms 311-x86_64 311-aarch64 -o python3-modules-flatpak-binary.json
req2flatpak --requirements-file $SCRIPT_DIR/requirements-force.txt --target-platforms 311-x86_64 311-aarch64 -o python3-modules-force.json
# Patch python module builds for packages that should ignore system installs
sed -i 's/pip3 install /pip3 install --ignore-installed /' python3-modules-force.json


cd $PROJECT_DIR
# validate Flatpak Manifest
flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest "${SCRIPT_DIR}/${APP_ID}.yml" || true


## Flatpak MetaInfo XML
# generate MetaInfo XML file from pyproject.toml
python $SCRIPT_DIR/generate_metainfo.py $PROJECT_DIR/pyproject.toml $APP_ID  "${SCRIPT_DIR}/${APP_ID}.metainfo.xml"
# validate MetaInfo XML file  
flatpak run --command=flatpak-builder-lint org.flatpak.Builder appstream "${SCRIPT_DIR}/${APP_ID}.metainfo.xml"



# flatpak-builder --user --install  --install-deps-from=flathub --force-clean build-dir $APP_ID.yml
flatpak run org.flatpak.Builder \
  --force-clean --ccache \
  --user --install \
  --install-deps-from=flathub \
  --mirror-screenshots-url=https://dl.flathub.org/media/ \
  --repo=$FLATPAK_REPO_DIR \
  --state-dir $FLATPAK_STATE_DIR \
  $FLATPAK_BUILD_DIR \
  "${SCRIPT_DIR}/${APP_ID}.yml" # \
  # --sandbox 
  
cd $SCRIPT_DIR

flatpak build-export $FLATPAK_REPO_DIR $FLATPAK_BUILD_DIR
flatpak build-bundle $FLATPAK_REPO_DIR $DIST_DIR/${APP_ID}_Testing.flatpak $APP_ID 



echo "
To debug the flatpak build, run this from the project directory:

flatpak-builder --run \
 $FLATPAK_BUILD_DIR \
 $SCRIPT_DIR/$APP_ID.yml \
 sh
"

