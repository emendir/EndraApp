#!/bin/bash
""":"

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECT_DIR=$(realpath $SCRIPT_DIR/../..)

FLATPAK_BUILD_DIR=$SCRIPT_DIR/build-dir
FLATPAK_STATE_DIR=$SCRIPT_DIR/.flatpak-builder

if [ -z $FLATPAK_REPO_DIR ];then
  echo 'Please define `FLATPAK_REPO_DIR`'
exit 1
fi

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


## Flatpak Manifest
## Collect Python Packages
python_packages=$(while IFS= read -r line; do
  [[ $line == PyQt* ]] && continue # skip PyQt cause we're using a PyQt base
  printf '%s ' "$line"
done < $PROJECT_DIR/requirements.txt)
# flatpak_pip_generator $python_packages
cd $PROJECT_DIR
# validate Flatpak Manifest
flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest "${SCRIPT_DIR}/${APP_ID}.yml"


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
  "${SCRIPT_DIR}/${APP_ID}.yml" \
  # --sandbox \
  
cd $SCRIPT_DIR

flatpak build-export $FLATPAK_REPO_DIR $FLATPAK_BUILD_DIR
flatpak build-bundle $FLATPAK_REPO_DIR $PROJECT_DIR/dist/dist/${APP_ID}_Testing.flatpak $APP_ID 



echo "
To debug the flatpak build, run this from the project directory:

flatpak run org.flatpak.Builder --run \
 --repo=$FLATPAK_REPO_DIR \
 --state-dir $FLATPAK_STATE_DIR \
 $FLATPAK_BUILD_DIR \
 $SCRIPT_DIR/$APP_ID.yml
"




exit 0
"""
import os
import sys

# Python: re-execute the script in Bash
os.execvp("bash", ["bash", __file__] + sys.argv[1:])
