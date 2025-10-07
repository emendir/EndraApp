#!/bin/bash
## This script generates a full list of python dependencies for this project
## as required for a specific packaging pipeline.
## This list contains dependencies recursively, each with the currently installed version.
## This list is based on the dependencies declared in /requirements.txt (and their deps recursively)
## filtered by ./requireemnets-exclusions.txt
## and complemented by ./requirements-manual.txt

set -e

REWRITE_VCS_INSTALLS=1 # 0: leave VCS dependencies as-is; 1: install VCS dependencies from PyPa instead


# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECT_DIR=$(realpath $SCRIPT_DIR/../..)
DIST_DIR=$PROJECT_DIR/dist/
BUILDOZER_SPEC=$SCRIPT_DIR/buildozer.spec

PY_PACKAGE_NAME=$(grep -E '^name\s*=' $PROJECT_DIR/pyproject.toml | sed -E 's/name\s*=\s*"(.*)"/\1/')
APP_VERSION=$(grep -E '^version\s*=' $PROJECT_DIR/pyproject.toml | sed -E 's/version\s*=\s*"(.*)"/\1/')

REQS_MAIN=$PROJECT_DIR/requirements.txt
REQS_AUTO=$SCRIPT_DIR/requirements-auto.txt
REQS_MANUAL=$SCRIPT_DIR/requirements-manual.txt
REQS_EXCLUSIONS=$SCRIPT_DIR/requirements-exclusions.txt

if ! [ -e "$BUILDOZER_SPEC" ]; then
  echo "Can't find $BUILDOZER_SPEC"
  exit 1
fi
if ! [ -e "$REQS_MAIN" ]; then
  echo "Can't find $REQS_MAIN"
  exit 1
fi

# pip install $PROJECT_DIR --force-reinstall
# # reinstall python packages that are editable installs (needed for listing dependencies)
# pkgs=$(pipdeptree --packages $PY_PACKAGE_NAME -f --warn silence \
#   | sed 's/^[[:space:]]*//' \
#   | sort -u \
#   | grep -v "$PY_PACKAGE_NAME" \
#   | grep -i "@" || true \
#   | awk '{print $1}')
# if [ -n "$pkgs" ]; then
#     echo "$pkgs" | while read -r pkg_name; do
#         echo "Reinstalling $pkg_name"
#         pip install --force-reinstall "$pkg_name"
#     done
# else
#     echo "No packages to reinstall."
# fi

# # list all python dependencies recursively with versions
# pipdeptree --packages $PY_PACKAGE_NAME -f --warn silence \
#   | sed 's/^[[:space:]]*//' \
#   | sort -u \
#   | grep -v -i "^$PY_PACKAGE_NAME" \
#   | grep -v "/"  \
#   | grep -v "Editable" \
#   | tee $REQS_AUTO


# -------------------------
# Step 1: List all dependencies from requirements.txt
# -------------------------
if ! [ -e "$REQS_MAIN" ]; then
  echo "Can't find $REQS_MAIN"
  exit 1
fi

# read package names from requirements.txt
REQ_PKGS=$(grep -v '^\s*#' "$REQS_MAIN" | grep -v '^\s*$' \
  | sed -E 's/[<>=!].*//' \
  | awk '{print $1}' \
  | sort -u | paste -sd "," -)

# build full dependency tree
pipdeptree --warn silence --packages "$REQ_PKGS" -f \
  | sed 's/^[[:space:]]*//' \
  | sort -u \
  | grep -v "^-e /" \
  | tee $REQS_AUTO


# convert editable and VCS dependencies in tree to pinned versions
tmpfile=$(mktemp)
while IFS= read -r line; do
  # skip empty lines
  [[ -z "$line" ]] && continue

  if [[ "$line" =~ ^-e[[:space:]] ]]; then
    # Editable/VCS install
    if [ $REWRITE_VCS_INSTALLS -eq 1 ];then
      pkg_name=$(echo "$line" | sed -n 's/.*#egg=\([^ ]*\)/\1/p')
      if [[ -n "$pkg_name" ]]; then
        echo "Reinstalling $pkg_name from PyPI..."
        pip install --upgrade --no-deps "$pkg_name"
        version=$(pip show "$pkg_name" | awk '/^Version:/{print $2}')
        echo "${pkg_name}==${version}" >> "$tmpfile"
      else
        echo "Warning: could not extract package name from: $line" >&2
      fi
    else
      echo $line >> "$tmpfile"
    fi

  elif [[ "$line" =~ ^#\ Editable ]]; then
    # Commented editable with pinned version inside parentheses
    pkg_spec=$(echo "$line" | sed -n 's/.*(\(.*\)).*/\1/p')
    pkg_name=$(echo "$pkg_spec" | cut -d= -f1)
    echo "Reinstalling $pkg_name from PyPI (pinned: $pkg_spec)..."
    pip install --upgrade --no-deps "$pkg_spec"
    version=$(pip show "$pkg_name" | awk '/^Version:/{print $2}')
    echo "${pkg_name}==${version}" >> "$tmpfile"
  elif [[ "$line" =~ ^# ]]; then
    # skip all other comments
    continue
  else
    # Normal pinned requirement
    pkg_name=$(echo "$line" | cut -d= -f1)
    # if pip show "$pkg_name" >/dev/null 2>&1; then
    #   echo "$pkg_name already installed, skipping."
    # else
    #   echo "Installing $line..."
    #   pip install "$line"
    # fi
    echo "$line" >> "$tmpfile"
  fi
done < "$REQS_AUTO"
mv "$tmpfile" "$REQS_AUTO"




## Filter auto-generated python dependencies using exclusions list
echo "Filtering from exclusions..."
if [ -e "$REQS_EXCLUSIONS" ]; then
  tmp_file="$(mktemp)"
  # Normalize exclusions: strip version part if present (keep only package name)
  exclusions=$(sed -E 's/[[:space:]]*#.*//; s/[[:space:]]*$//; /^$/d; s/==.*$//' "$REQS_EXCLUSIONS")
  # Build grep pattern from exclusions (anchor to start of line, match until ==)
  if [[ -n "$exclusions" ]]; then
    pattern=$(printf '%s\n' $exclusions | sed 's/^/^/; s/$/==/' | paste -sd'|' -)
    grep -Ev "$pattern" "$REQS_AUTO" | tee "$tmp_file"
  else
    # No exclusions, just copy
    cp "$REQS_AUTO" "$tmp_file"
  fi
  mv "$tmp_file" "$REQS_AUTO"
fi

## Filter auto-generated python dependencies using exclusions list
echo "Filtering from manual specifications..."
if [ -e "$REQS_MANUAL" ]; then
  tmp_file="$(mktemp)"
  # Normalize exclusions: strip version part if present (keep only package name)
  exclusions=$(sed -E 's/[[:space:]]*#.*//; s/[[:space:]]*$//; /^$/d; s/==.*$//' "$REQS_MANUAL")
  # Build grep pattern from exclusions (anchor to start of line, match until ==)
  if [[ -n "$exclusions" ]]; then
    pattern=$(printf '%s\n' $exclusions | sed 's/^/^/; s/$/==/' | paste -sd'|' -)
    echo "grep -Ev '$pattern' $REQS_AUTO > $tmp_file"
    grep -Ev "$pattern" "$REQS_AUTO" | tee "$tmp_file"
  else
    # No exclusions, just copy
    cp "$REQS_AUTO" "$tmp_file"
  fi
  mv "$tmp_file" "$REQS_AUTO"
fi

echo "Prepending manual specifications..."
## Prepend manual requirements to auto-generated ones
if [ -e "$REQS_MANUAL" ]; then
  tmp_file="$(mktemp)"
  cat "$REQS_MANUAL" "$REQS_AUTO" > "$tmp_file"
  mv "$tmp_file" "$REQS_AUTO"
fi

sort $REQS_AUTO -o $REQS_AUTO

# exit 1

echo "Updating buildozer.spec"
## Update buildozer.spec requires=
# Convert requirements.txt to comma-separated list
reqs=$(paste -sd',' "$REQS_AUTO")

# Replace (or add if missing) requires= line in buildozer.spec
if grep -q '^requirements = ' "$BUILDOZER_SPEC"; then
  sed -i "s|^requirements = .*|requirements = $reqs|" "$BUILDOZER_SPEC"
else
  echo "requirements = $reqs" >> "$BUILDOZER_SPEC"
fi
