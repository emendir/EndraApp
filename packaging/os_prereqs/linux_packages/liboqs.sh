#!/bin/bash
# Compile and install liboqs

set -euo pipefail # Exit if any command/script fails

# Compilation configuration
LIBOQS_REPO="https://github.com/open-quantum-safe/liboqs.git"
LIBOQS_TAG="0.14.0"            # adjust if needed
LIBOQS_INSTALL_PREFIX="/usr/local/lib/"   
export LD_LIBRARY_PATH="/usr/local/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
# Number of parallel build jobs
NPROC=$(( $(nproc) - 1 ))



SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPT_DIR
source $SCRIPT_DIR/../os_package_utils.sh



WORK_DIR=/tmp/EndraAppBuildLiboqs
LIBOQS_BUILD_DIR="$WORK_DIR/liboqs-build"


if [ -e "$LIBOQS_INSTALL_PREFIX/bin/liboqs.so" ]; then 
    echo "Liboqs is already installed, skipping."
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
    -DOQS_DIST_BUILD=OFF \
    -DBUILD_SHARED_LIBS=ON \
    -DOQS_BUILD_ONLY_LIB=ON \
    -DOQS_OPT_TARGET=generic

cmake --build $LIBOQS_BUILD_DIR --parallel $NPROC
sudo cmake --build $LIBOQS_BUILD_DIR --target install

