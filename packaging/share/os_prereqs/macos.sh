#!/bin/bash


# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPT_DIR
source $SCRIPT_DIR/os_package_utils.sh

set -euo pipefail # Exit if any command/script fails

REQUIRED_COMMANDS=(
    git
    cmake
    make
)
# install prerequisites with brew, if available
if command -v "brew" >/dev/null 2>&1; then
    brew install "${REQUIRED_COMMANDS[@]}"
else # brew is not available
    REQUIRED_COMMANDS=(
        git
        cmake
        make
        )
    if check_commands "${REQUIRED_COMMANDS[@]}";then
        echo "Found all necessary prerequisite tools!"
    else
        echo "Could not find all prerequisite tools. Install them manually, or install brew so that I can install them."
        exit 1
    fi
fi

