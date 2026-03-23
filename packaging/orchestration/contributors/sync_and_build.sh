#!/bin/bash
# See `./_utils/config.sh` for this script's parameters.

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

source "$SCRIPT_DIR/_utils/config.sh"

set -euo pipefail

source "$SCRIPT_DIR/_utils/validate_config.sh"


echo ""
echo "Upstream repo:  $UPSTREAM_REPO"
echo "Fork repo:      $FORK_REPO"
echo "Local repo dir: $REPO_DIR"
echo ""

cd "$REPO_DIR"
source packaging/os_prereqs/os_platform_info.sh



# Checkout branch from upstream repo:
git fetch upstream
git checkout release/dev
git reset --hard upstream/release/dev


#$BUILD_SCRIPT


# Commit
git add .
if git diff --cached --quiet; then
  echo "⚠️ Build produced no file changes. Exiting."
  exit 0
fi
git commit -m "devops(build): produced build for $OS $ARCH"

# Push to fork repo
git push origin release/dev
