#!/bin/bash
# Git clone a repo or ensure the given local repo is correctly configured.
# See `./_utils/config.sh` for this script's parameters.

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

source "$SCRIPT_DIR/_utils/config.sh"

set -euo pipefail

if [ -z  "$REPO_DIR" ]; then
    echo "Specify a path for the repository on this computer."
    exit 1
fi
if ! [ -d "$REPO_DIR" ]; then
    echo "Specified repo path is not a directory: $REPO_DIR"
    exit 1
fi


cd "$REPO_DIR"
echo "Local repo dir: $REPO_DIR"

if ! git rev-parse --git-dir 1>/dev/null 2>&1; then
    echo "Cloning https://github.com/$FORK_REPO"
    git clone "https://github.com/$FORK_REPO" "$REPO_DIR"
fi




source "$SCRIPT_DIR/_utils/validate_config.sh"

git fetch upstream

