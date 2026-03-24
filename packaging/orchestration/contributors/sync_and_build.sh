#!/bin/bash
# See `./_utils/config.sh` for this script's parameters.

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

source "$SCRIPT_DIR/_utils/config.sh"

set -euo pipefail

source "$SCRIPT_DIR/_utils/validate_config.sh"
source "$SCRIPT_DIR/_utils/utils.sh"


echo ""
echo "Upstream repo:  $UPSTREAM_REPO"
echo "Fork repo:      $FORK_REPO"
echo "Local repo dir: $REPO_DIR"
echo ""

cd "$REPO_DIR"
source packaging/os_prereqs/os_platform_info.sh

APP_VERSION=$(grep -E '^version\s*=' $REPO_DIR/pyproject.toml | sed -E 's/version\s*=\s*"(.*)"/\1/')


# Checkout branch from fork repo, discarding any current changes
git fetch origin
git checkout release/dev
git reset --hard origin/release/dev

# Pull changes from upstream repo
git fetch upstream
git checkout release/dev
git rebase upstream/release/dev

#$BUILD_SCRIPT

date | tee "$REPO_DIR/testing"

# Commit
git add .
if git diff --cached --quiet; then
  echo "⚠️ Build produced no file changes. Exiting."
  exit 0
fi
git commit -m "devops(build): produced build for v$APP_VERSION on $OS $ARCH"

# Push to fork repo
git push origin release/dev

echo ""
if ask_yes_no "Open Pull Request? Do this when you've finished all builds for today." n; then
    # open PR
    github_user="${FORK_REPO%%/*}"
    gh pr create --repo $UPSTREAM_REPO --head $github_user:release/dev --base release/dev --title "Build for v$APP_VERSION on $OS $ARCH" --body "Updated dependencies for build for v$APP_VERSION on $OS $ARCH"
else
    echo "Not creating pull request."
fi
