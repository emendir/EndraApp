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

APP_VERSION=$(grep -E '^version\s*=' "$REPO_DIR/pyproject.toml" | sed -E 's/version\s*=\s*"(.*)"/\1/')

BRANCH_NAME="build/$OS-$ARCH"


echo ""
if ! ask_yes_no "About to reset branch $BRANCH_NAME to upstream, will override $BRANCH_NAME on origin. If you've made any manual changes, make sure they're commited to another branch. Proceed?" y;then
    exit 0
fi

# Ensure clean working tree
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "Working tree not clean. Commit or stash first."
    exit 1
fi

git fetch origin
git fetch upstream


# create branch if missing,
# reset to upstream if existing
git checkout -B "$BRANCH_NAME" upstream/release/candidate



$BUILD_SCRIPT

# for testing
# date | tee "$REPO_DIR/testing"

# Commit
git add -A
if git diff --cached --quiet; then
  echo "⚠️ Build produced no file changes. Exiting."
  exit 0
fi
git commit -m "devops(build): produced build for v$APP_VERSION on $OS $ARCH"


echo ""
if ask_yes_no "Push to origin and open pull request? Do this when you've ensured that the build works." y; then
    # Push to fork repo
    git push --force-with-lease origin "$BRANCH_NAME"

    # open PR
    github_user="${FORK_REPO%%/*}"
    gh pr create \
        --repo $UPSTREAM_REPO \
        --head "$github_user:$BRANCH_NAME" \
        --base release/candidate \
        --title "Build for v$APP_VERSION on $OS $ARCH" \
        --body "Updated dependencies for build for v$APP_VERSION on $OS $ARCH"
else
    echo "Not creating pull request."
fi
