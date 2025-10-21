## Run this script on a Windows machine using MINGW-Bash
set -e

tempdir=$(mktemp -d)

# get the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

PROJ_DIR=$(realpath $SCRIPT_DIR/../..)

echo "$PROJ_DIR"

# PYINST_SPEC_NAME=EndraApp.spec
PYINST_SPEC=$SCRIPT_DIR/$PYINST_SPEC_NAME
PY_CMD=python3.13

cp -r $PROJ_DIR/src $tempdir
cp -r $PROJ_DIR/*.toml $tempdir
cp -r $PROJ_DIR/*.txt $tempdir
mkdir $tempdir/packaging
cp -r $PROJ_DIR/packaging/pyinstaller $tempdir/packaging
cp -r $PROJ_DIR/packaging/share $tempdir/packaging
# cp $PYINST_SPEC $tempdir

# # download UPX
# tempdir2=$(mktemp -d)
# cd $tempdir2
# curl -L https://github.com/upx/upx/releases/download/v5.0.2/upx-5.0.2-win64.zip -o upx.zip
# unzip upx.zip
# cp ./upx-*/upx.exe $tempdir
# cp ./upx-*/upx.exe $tempdir/packaging/pyinstaller

cd $tempdir
ls -la
# IPFS_TK_MODE=EMBEDDED WALYTIS_BETA_API_TYPE=WALYTIS_BETA_DIRECT_API python -m PyInstaller $tempdir/$PYINST_SPEC_NAME
IPFS_TK_MODE=EMBEDDED WALYTIS_BETA_API_TYPE=WALYTIS_BETA_DIRECT_API $PY_CMD packaging/pyinstaller/build_pyinstaller.py

echo $tempdir/dist
cp $tempdir/dist/*.dmg $PROJ_DIR/dist/
