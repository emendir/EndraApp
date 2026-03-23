#!/bin/bash

set -euo pipefail # Exit if any command fails

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJ_DIR=$(realpath $SCRIPT_DIR/../..)

echo $PROJ_DIR

cd "$SCRIPT_DIR"
#TODO
echo "THIS SCRIPT IS NOT YET FUNCTIONAL"
