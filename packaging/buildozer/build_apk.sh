#!/bin/bash

set -e

APP_NAME="Endra" # leave empty to read from pyproject.toml

# DOCKER_IMAGE=ghcr.io/kivy/buildozer
DOCKER_IMAGE=ghcr.io/kivy/buildozer@sha256:75a1ed9d378489eb281733ae61b1e144ce45443c12c6f424f5d847623e28fc68
# DOCKER_IMAGE=local/buildozer

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPT_DIR

PROJ_DIR=$(realpath $SCRIPT_DIR/../..)
WORK_DIR=$SCRIPT_DIR

PY_PACKAGE_NAME=$(grep -E '^name\s*=' $PROJ_DIR/pyproject.toml | sed -E 's/name\s*=\s*"(.*)"/\1/')
if [ -z $APP_NAME ];then # allow optional overriding variable using declaration above
  APP_NAME=$PY_PACKAGE_NAME
fi
APP_VERSION=$(grep -E '^version\s*=' $PROJ_DIR/pyproject.toml | sed -E 's/version\s*=\s*"(.*)"/\1/')
APK_PATH=$PROJ_DIR/dist/${APP_NAME}_v${APP_VERSION}_android_28_arm64_v8a.apk

# script for generating python requirements
GET_PYTHON_DEPS=$PROJ_DIR/packaging/share/get_python_deps.sh

BUILDOZER_SPEC=$SCRIPT_DIR/buildozer.spec

if ! [ -e "$BUILDOZER_SPEC" ]; then
  echo "Can't find $BUILDOZER_SPEC"
  exit 1
fi

BLACK='\033[0;30m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'
NC='\033[0m' # no colour

set -e
echo -e "$YELLOW
REMEMBER: If you've updated dependecies, run:"
echo -e "$MAGENTA
buildozer android clean
$NC"



if ! [ -e ~/.buildozer ];then
  mkdir ~/.buildozer
fi
if ! [ -e $WORK_DIR/bin ];then
  mkdir $WORK_DIR/bin
  chmod -R 777 $WORK_DIR/bin
fi
if ! [ -e $WORK_DIR/.buildozer ];then
  mkdir $WORK_DIR/.buildozer
  chmod -R 777 $WORK_DIR/.buildozer
fi
if ! [ -e $HOME/.buildozer ];then
  mkdir $HOME/.buildozer
  chmod -R 777 $HOME/.buildozer
fi

## export variables used by the $GET_PYTHON_DEPS script
export PY_VENV_DIR=$(mktemp -d)
virtualenv $PY_VENV_DIR
source $PY_VENV_DIR/bin/activate
# general project requirements
export REQS_MAIN=$PROJ_DIR/requirements.txt
# requirements specific to this build pipeline
export REQS_MANUAL=$SCRIPT_DIR/requirements-manual.txt
# final generated requirements list
export REQS_AUTO=$SCRIPT_DIR/requirements-auto.txt
# requirements to be excluded in this build pipeline
REQS_EXCLUSIONS=$SCRIPT_DIR/requirements-exclusions.txt
REQS_BUILDOZER=$SCRIPT_DIR/requirements-buildozer.txt

# make $GET_PYTHON_DEPS exclude from both $REQS_EXCLUSIONS and $REQS_BUILDOZER
tmp_file="$(mktemp)"
cat "$REQS_EXCLUSIONS" "$REQS_BUILDOZER" | grep -v "^#" | grep -v "^$" > "$tmp_file"
export REQS_EXCLUSIONS=$tmp_file
$GET_PYTHON_DEPS
# update buildozer.spec `requirements` field
echo "Updating buildozer.spec"
## Update buildozer.spec requires=
# Convert requirements.txt to comma-separated list
reqs=$(paste -sd',' "$REQS_AUTO")
reqs_buildozer=$(paste -sd',' "$REQS_BUILDOZER")

# Replace (or add if missing) requires= line in buildozer.spec
if grep -q '^requirements = ' "$BUILDOZER_SPEC"; then
  sed -i "s|^requirements = .*|requirements = $reqs_buildozer,$reqs|" "$BUILDOZER_SPEC"
else
  echo "requirements = $reqs_buildozer,$reqs" >> "$BUILDOZER_SPEC"
fi

docker pull $DOCKER_IMAGE

docker run  \
  -v $HOME/.buildozer:/home/user/.buildozer \
  -v $WORK_DIR/buildozer.spec:/home/user/hostcwd/buildozer.spec \
  -v $WORK_DIR/.buildozer:/home/user/hostcwd/.buildozer \
  -v $WORK_DIR/bin:/home/user/hostcwd/bin \
  -v $PROJ_DIR/src:/home/user/hostcwd/src \
  $DOCKER_IMAGE android debug

# tempdir=$(mktemp -d)
# cp -r $WORK_DIR/buildozer.spec $tempdir/
# # cp -r $WORK_DIR/.buildozer $tempdir/
# # cp -r $WORK_DIR/bin $tempdir/
# cp -r $PROJ_DIR/src $tempdir/
# docker run  \
#   -v $HOME/.buildozer:/home/user/.buildozer \
#   -v $tempdir:/home/user/hostcwd \
#   $DOCKER_IMAGE android debug
#

cp $WORK_DIR/bin/EndraApp-0.1-arm64-v8a-debug.apk $APK_PATH

cd $WORK_DIR
buildozer android deploy run logcat

