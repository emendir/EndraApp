## Performs the PyInstaller build in a temporary directory

## On Windows, run this script using MINGW-Bash

set -euo pipefail

tempdir=$(mktemp -d)

# get the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

PROJ_DIR=$(realpath $SCRIPT_DIR/../..)
DIST_DIR=$PROJ_DIR/dist
if ! [ -e $DIST_DIR ];then
    mkdir -p $DIST_DIR
fi

echo "$PROJ_DIR"


PYTHON="${PYTHON:-python}"
OS=$($PYTHON -c "import platform;print(platform.system())")
echo "Platform: $OS"
echo "Python: $PYTHON"

# Determine platform-specific requirements directory
case "$OS" in
    Linux)
        PLATFORM_DIR="linux"
        ;;
    Darwin)
        PLATFORM_DIR="macos"
        ;;
    Windows)
        PLATFORM_DIR="windows"
        ;;
    *)
        echo "Error: Unsupported platform: $OS"
        exit 1
        ;;
esac

echo "Using platform-specific requirements from: $PLATFORM_DIR"

USE_VENV=1
# if [ $OS = "Windows" ];then
#     echo "DEACTIVATING VENV"
#     # pyinstaller fails to load libkubo DLL when in venv
#     USE_VENV=0
# fi


if ! command -v "$PYTHON" >/dev/null 2>&1; then
    echo "Error: '$PYTHON' command not found. Set the environment variable `PYTHON` to you python command."
    exit 1
fi

cp -r $PROJ_DIR/src $tempdir
cp -r $PROJ_DIR/*.toml $tempdir
cp -r $PROJ_DIR/*.txt $tempdir
mkdir $tempdir/packaging
cp -r $PROJ_DIR/packaging/pyinstaller $tempdir/packaging
cp -r $PROJ_DIR/packaging/share $tempdir/packaging

# Set up platform-specific requirements paths for get_python_deps.sh
export REQS_MAIN=$PROJ_DIR/requirements.txt
export REQS_MANUAL=$PROJ_DIR/packaging/pyinstaller/$PLATFORM_DIR/requirements-manual.txt
export REQS_EXCLUSIONS=$PROJ_DIR/packaging/pyinstaller/$PLATFORM_DIR/requirements-exclusions.txt
export REQS_AUTO=$PROJ_DIR/packaging/pyinstaller/$PLATFORM_DIR/requirements-auto.txt
GET_PYTHON_DEPS=$PROJ_DIR/packaging/share/get_python_deps.sh


cd $tempdir
ls -la
export PY_VENV_DIR=$tempdir/.venv
if [ $USE_VENV -eq 1 ];then
    $PYTHON -m pip install -qq virtualenv
    $PYTHON -m virtualenv $PY_VENV_DIR
    if [ $OS = "Windows" ];then
        source $PY_VENV_DIR/Scripts/activate
    else
        source $PY_VENV_DIR/bin/activate
    fi
    PYTHON=python
fi
$PYTHON -m pip install -r $PROJ_DIR/requirements-dev.txt

# Generate requirements using get_python_deps.sh
# and install them in venv
echo "Generating requirements for $PLATFORM_DIR..."

# installs requirements in virtualenv, and documents the recursive list of dependencies
$GET_PYTHON_DEPS

# Build with PyInstaller
IPFS_TK_MODE=EMBEDDED WALYTIS_BETA_API_TYPE=WALYTIS_BETA_DIRECT_API $PYTHON packaging/pyinstaller/build_pyinstaller.py

echo $tempdir/dist
cp -r $tempdir/dist/* $PROJ_DIR/dist/
