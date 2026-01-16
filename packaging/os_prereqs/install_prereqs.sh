#!/bin/bash

set -euo pipefail # Exit if any command/script fails

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPT_DIR
source $SCRIPT_DIR/os_package_utils.sh
source $SCRIPT_DIR/os_platform_info.sh


case "$OS" in
    Linux)
        $SCRIPT_DIR/linux.sh
        scripts_dir=$SCRIPT_DIR/linux_packages
        ;;
    Darwin)
        $SCRIPT_DIR/macos.sh
        scripts_dir=$SCRIPT_DIR/macos_packages
        ;;
    Windows)
        export PATH="/mingw64/bin:$PATH"
        $SCRIPT_DIR/windows.sh
        scripts_dir=$SCRIPT_DIR/windows_packages
        ;;
    *)
        echo "Error: Unsupported platform: $OS"
        exit 1
        ;;
esac

for script in $scripts_dir/*.sh; do
    [ -e "$script" ] || continue   # skip if no files match
    echo "Running $script"
    echo "$(which cmake)"
    "$script"
done

## Endra's DevOps dependencies:
$PYTHON -m pip install -r $PROJ_DIR/requirements.txt
$PYTHON -m pip install -r $PROJ_DIR/requirements-dev.txt
