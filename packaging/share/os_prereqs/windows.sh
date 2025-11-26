#!/usr/bin/env bash
set -euo pipefail # Exit if any command/script fails

SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPT_DIR
source $SCRIPT_DIR/os_package_utils.sh

export PATH="/mingw64/bin:$PATH"

PYTHON="${PYTHON:-python}"

REQUIRED_COMMANDS=(
        git
        cmake
        make
        $PYTHON
        )


if net session > /dev/null 2>&1; then
    echo "Running with Administrator privileges"
else
    echo "NOT running as Administrator"
    echo "Run your shell with administrator privileges."
    exit 1
fi
if check_commands pacman;then

    echo "=== Installing prerequisites via pacman ==="
    # You may need to install cmake, ninja, git, python3, etc.
    pacman --needed -Sy \
      mingw-w64-x86_64-gcc \
      mingw-w64-x86_64-cmake \
      mingw-w64-x86_64-make \
      mingw-w64-x86_64-ninja \
      git \
      mingw-w64-x86_64-python \
      mingw-w64-x86_64-python-pip \
      mingw-w64-x86_64-python-virtualenv


    if ! [ -e /mingw64/bin/make ]; then
        ln -s /mingw64/bin/mingw32-make.exe /mingw64/bin/make
    fi
    if ! [ -e /mingw64/bin/python ]; then
        ln -s /mingw64/bin/mingw32-python.exe /mingw64/bin/python
    fi
    if ! [ -e /mingw64/bin/gcc ]; then
        ln -s /mingw64/bin/mingw32-gcc.exe /mingw64/bin/gcc
    fi
    if ! [ -e /mingw64/bin/cmake ]; then
        ln -s /mingw64/bin/mingw32-cmake.exe /mingw64/bin/cmake
    fi
    if check_commands "${REQUIRED_COMMANDS[@]}";then
        echo "Found all necessary prerequisite tools!"
    else
        echo "Either you forgot to install some of these packages with pacman, or you need to restart your shell or Windows to complete the installation."
        exit 1
    fi
else 
    if check_commands "${REQUIRED_COMMANDS[@]}";then
        echo "Found all necessary prerequisite tools!"
    else
        echo "Didn't find all prerequisites and could not install them because pacman is not available."
        echo "I recommend you install MSYS2 from https://www.msys2.org/ so that I can install them for you."
        echo "Otherwise, install the prerequisites listed above manually."
        exit 1
    fi
fi

# Verify that $PYTHON refers to a Windows-native Python.
# (MSYS2 / MSYS python will fail this check.)

if ! "$PYTHON" - <<'EOF'
import sys
from pip._internal.utils.compatibility_tags import get_supported

# Extract the set of supported platform tags (e.g., win_amd64, win32)
platforms = {tag.platform for tag in get_supported()}

# Acceptable Windows platform tags
WIN_PLATFORMS = {"win_amd64", "win32", "win_arm64"}

if not any(p in platforms for p in WIN_PLATFORMS):
    sys.exit(1)
print("Python version looks good.")
print(platforms)
EOF
then
    echo "ERROR: The PYTHON command ('$PYTHON') is not a Windows-native Python."
    echo "       Pip will NOT be able to download prebuilt Windows wheels."
    echo ""
    echo "Detected environment: $("$PYTHON" -c 'import sys; print(sys.platform)')"
    echo ""
    echo "Fix:"
    echo "  • Use a real Windows Python interpreter (e.g. C:/Users/.../python.exe)"
    echo "  • Or export PYTHON=/c/Path/To/Windows/python.exe"
    exit 1
fi
