#!/usr/bin/env bash
# Compile and install liboqs

set -euo pipefail # Exit if any command/script fails

# Compilation configuration
LIBOQS_REPO="https://github.com/open-quantum-safe/liboqs.git"
LIBOQS_TAG="0.14.0"            # adjust if needed
# LIBOQS_INSTALL_PREFIX="/mingw64/liboqs"   # or another prefix visible to your MSYS2 / MinGW
LIBOQS_INSTALL_PREFIX="C:/Program Files/liboqs"   # or another prefix visible to your MSYS2 / MinGW
# Number of parallel build jobs
NPROC=$(( $(nproc) - 1 ))


# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPT_DIR
source $SCRIPT_DIR/../os_package_utils.sh
source $SCRIPT_DIR/../os_platform_info.sh



WORK_DIR=/tmp/EndraAppBuildLiboqs
LIBOQS_BUILD_DIR="$WORK_DIR/liboqs-build"


if [ -e "$LIBOQS_INSTALL_PREFIX/bin/liboqs.dll" ]; then 
    echo "Liboqs is already installed, skipping."
    add_to_windows_system_path "$LIBOQS_INSTALL_PREFIX/bin"
    exit 0
fi


echo "=== Clone liboqs ==="
if [ ! -d "$WORK_DIR" ]; then
  git clone --depth 1 --branch "${LIBOQS_TAG}" "${LIBOQS_REPO}" $WORK_DIR
else
  echo "liboqs directory exists, skipping clone"
fi

cd $WORK_DIR
git checkout ${LIBOQS_TAG} # ensure we're on the desired branch

echo "=== Configure and build liboqs ==="
rm -rf "${LIBOQS_BUILD_DIR}"
mkdir -p "${LIBOQS_BUILD_DIR}"

echo "$(which cmake)"
cmake -S $WORK_DIR -B $LIBOQS_BUILD_DIR \
    -DCMAKE_INSTALL_PREFIX="$LIBOQS_INSTALL_PREFIX" \
    -DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=TRUE \
    -DOQS_DIST_BUILD=OFF \
    -DBUILD_SHARED_LIBS=ON \
    -DOQS_BUILD_ONLY_LIB=ON \
    -DOQS_OPT_TARGET=generic

cmake --build $LIBOQS_BUILD_DIR --parallel $NPROC

cmake --build $LIBOQS_BUILD_DIR  --target install

add_to_windows_system_path "$LIBOQS_INSTALL_PREFIX/bin"
