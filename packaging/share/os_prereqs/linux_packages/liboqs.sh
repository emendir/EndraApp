#!/bin/bash
# Compile and install liboqs

set -euo pipefail # Exit if any command/script fails

# Compile and install liboqs
export LD_LIBRARY_PATH="/usr/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
# export LD_LIBRARY_PATH="/usr/local/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
# export OQS_INSTALL_PATH=/path/to/liboqs
cd $(mktemp -d)
git clone --depth=1 https://github.com/open-quantum-safe/liboqs
# if [ -e liboqs/build ];then
#   rm -rf liboqs/build
# fi
cmake -S liboqs -B liboqs/build -DBUILD_SHARED_LIBS=ON -DOQS_OPT_TARGET=generic
cmake --build liboqs/build --parallel $(nproc)
sudo cmake --build liboqs/build --target install

