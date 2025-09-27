#!/bin/bash

set -e

APP_NAME="Endra" # leave empty to read from pyproject.toml

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECT_DIR=$(realpath $SCRIPT_DIR/../..)
DIST_DIR=$PROJECT_DIR/dist/
BUILDOZER_SPEC=$SCRIPT_DIR/buildozer.spec

PY_PACKAGE_NAME=$(grep -E '^name\s*=' $PROJECT_DIR/pyproject.toml | sed -E 's/name\s*=\s*"(.*)"/\1/')
if [ -z $APP_NAME ];then # allow optional overriding variable using declaration above
  APP_NAME=$PY_PACKAGE_NAME
fi
APP_VERSION=$(grep -E '^version\s*=' $PROJECT_DIR/pyproject.toml | sed -E 's/version\s*=\s*"(.*)"/\1/')


REQS_AUTO=$SCRIPT_DIR/requirements-auto.txt
REQS_MANUAL=$SCRIPT_DIR/requirements-manual.txt
REQS_EXCLUSIONS=$SCRIPT_DIR/requirements-exclusions.txt

if ! [ -e "$BUILDOZER_SPEC" ]; then
  echo "Can't find $BUILDOZER_SPEC"
  exit 1
fi

pip install $PROJECT_DIR --force-reinstall
# reinstall python packages that are editable installs (needed for listing dependencies)
pkgs=$(pipdeptree --packages $PY_PACKAGE_NAME -f --warn silence \
  | sed 's/^[[:space:]]*//' \
  | sort -u \
  | grep -v "$PY_PACKAGE_NAME" \
  | grep -i "@" || true \
  | awk '{print $1}')
if [ -n "$pkgs" ]; then
    echo "$pkgs" | while read -r pkg_name; do
        echo "Reinstalling $pkg_name"
        pip install --force-reinstall "$pkg_name"
    done
else
    echo "No packages to reinstall."
fi

# list all python dependencies recursively with versions
pipdeptree --packages $PY_PACKAGE_NAME -f --warn silence \
  | sed 's/^[[:space:]]*//' \
  | sort -u \
  | grep -v -i "^$PY_PACKAGE_NAME" \
  | grep -v "/"  \
  | grep -v "Editable" \
  | tee $REQS_AUTO

## Filter auto-generated python dependencies using exclusions list
if [ -e "$REQS_EXCLUSIONS" ]; then
  tmp_file="$(mktemp)"
  # Normalize exclusions: strip version part if present (keep only package name)
  exclusions=$(sed -E 's/[[:space:]]*#.*//; s/[[:space:]]*$//; /^$/d; s/==.*$//' "$REQS_EXCLUSIONS")
  # Build grep pattern from exclusions (anchor to start of line, match until ==)
  if [[ -n "$exclusions" ]]; then
    pattern=$(printf '%s\n' $exclusions | sed 's/^/^/; s/$/==/' | paste -sd'|' -)
    grep -Ev "$pattern" "$REQS_AUTO" > "$tmp_file"
  else
    # No exclusions, just copy
    cp "$REQS_AUTO" "$tmp_file"
  fi
  mv "$tmp_file" "$REQS_AUTO"
fi

## Filter auto-generated python dependencies using exclusions list
if [ -e "$REQS_MANUAL" ]; then
  tmp_file="$(mktemp)"
  # Normalize exclusions: strip version part if present (keep only package name)
  exclusions=$(sed -E 's/[[:space:]]*#.*//; s/[[:space:]]*$//; /^$/d; s/==.*$//' "$REQS_MANUAL")
  # Build grep pattern from exclusions (anchor to start of line, match until ==)
  if [[ -n "$exclusions" ]]; then
    pattern=$(printf '%s\n' $exclusions | sed 's/^/^/; s/$/==/' | paste -sd'|' -)
    grep -Ev "$pattern" "$REQS_AUTO" > "$tmp_file"
  else
    # No exclusions, just copy
    cp "$REQS_AUTO" "$tmp_file"
  fi
  mv "$tmp_file" "$REQS_AUTO"
fi

## Prepend manual requirements to auto-generated ones
if [ -e "$REQS_MANUAL" ]; then
  tmp_file="$(mktemp)"
  cat "$REQS_MANUAL" "$REQS_AUTO" > "$tmp_file"
  mv "$tmp_file" "$REQS_AUTO"
fi

## Update buildozer.spec requires=
# Convert requirements.txt to comma-separated list
reqs=$(paste -sd',' "$REQS_AUTO")

# Replace (or add if missing) requires= line in buildozer.spec
if grep -q '^requirements = ' "$BUILDOZER_SPEC"; then
  sed -i "s/^requirements = .*/requirements = $reqs/" "$BUILDOZER_SPEC"
else
  echo "requirements = $reqs" >> "$BUILDOZER_SPEC"
fi
