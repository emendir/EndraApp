## Performs the PyInstaller build in a temporary directory

## On Windows, run this script using MINGW-Bash
set -e

tempdir=$(mktemp -d)

# get the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

PROJ_DIR=$(realpath $SCRIPT_DIR/../..)
DIST_DIR=$PROJ_DIR/dist
if ! [ -e $DIST_DIR ];then
    mkdir -p $DIST_DIR
fi

echo "$PROJ_DIR"


PYINST_SPEC=$SCRIPT_DIR/$PYINST_SPEC_NAME
PYTHON="${PYTHON:-python3}"

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


cd $tempdir
ls -la

IPFS_TK_MODE=EMBEDDED WALYTIS_BETA_API_TYPE=WALYTIS_BETA_DIRECT_API $PYTHON packaging/pyinstaller/build_pyinstaller.py

echo $tempdir/dist
cp -r $tempdir/dist/* $PROJ_DIR/dist/
