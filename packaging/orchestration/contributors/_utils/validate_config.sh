# Checks that parameters are valid
# Ensures git remotes match parameters.

# Detect if the script is being executed instead of sourced
(return 0 2>/dev/null) && sourced=1 || sourced=0
if [ "$sourced" -eq 0 ]; then
    echo "Error: This script must be sourced, not executed." >&2
    exit 1
fi


if [ -z  "$REPO_DIR" ]; then
    echo "Specify a path for the repository on this computer."
    exit 1
fi
if ! [ -d "$REPO_DIR" ]; then
    echo "Specified repo path is not a directory: $REPO_DIR"
    exit 1
fi

if [ -z  "$FORK_REPO" ]; then
    echo "Specify your git fork repository on the web."
    exit 1
fi
if ! env GIT_PROXY_COMMAND=myproxy.sh GIT_TRACE=1 git ls-remote "https://github.com/$FORK_REPO.git" 2>/dev/null 1>&2; then
    echo "Failed to access fork repository: 'https://github.com/$FORK_REPO.git'"
    exit 1
fi


cd "$REPO_DIR" || exit 1

if ! git rev-parse --git-dir 1>/dev/null 2>&1; then
    echo "Not a git repository: $REPO_DIR"
    exit 1
fi

if git remote | grep upstream 1>/dev/null;then
    git remote set-url upstream "https://github.com/$UPSTREAM_REPO.git"
else
    git remote add upstream "https://$UPSTREAM_REPO.git"
fi

if git remote | grep origin 1>/dev/null;then
    git remote set-url origin "ssh://git@github.com/$FORK_REPO.git"
else
    git remote add upstream "ssh://git@github.com/$FORK_REPO.git"
fi
