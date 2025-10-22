#!/bin/bash
## This script generates a full list of python dependencies for this project
## as required for a specific packaging pipeline.
## The dependencies are listed with specific versions
## This list is consists of:
## - the dependencies declared in $REQS_MAIN
## - complemented by $REQS_MANUAL
## - and their dependencies recursively
## - filtered by $REQS_EXCLUSIONS

set -e



# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"



if ! [ -e "$REQS_MANUAL" ]; then
  "REQS_MANUAL not found: $REQS_MANUAL"
  exit 1
fi
if ! [ -e "$REQS_MAIN" ]; then
  "REQS_MANUAL not found: $REQS_MAIN"
  exit 1
fi
if ! [ -e "$REQS_EXCLUSIONS" ]; then
  "REQS_MANUAL not found: $REQS_EXCLUSIONS"
  exit 1
fi

function filter_reqs(){
  REQS_BASE=$1
  REQS_FILTER=$2
  REQS_OUTPUT=$3
  # Normalize exclusions: strip version part if present (keep only package name)
  exclusions=$(sed -E 's/[[:space:]]*#.*//; s/[[:space:]]*$//; /^$/d; s/==.*$//; /^$/d; s/>=.*$//; /^$/d; s/<=.*$//' "$REQS_FILTER")
  # Build grep pattern from exclusions (anchor to start of line, match until ==)
  if [[ -n "$exclusions" ]]; then
    local tmp_file="$(mktemp)"
    pattern=$(printf '%s\n' $exclusions | sed 's/^/^/; s/$//' | paste -sd'|' -)
    grep -Ev "$pattern" "$REQS_BASE" | tee "$tmp_file"
    # echo $(cat $tmp_file)
    mv $tmp_file $REQS_OUTPUT
    # echo $(cat $REQS_OUTPUT)
  else
    # No exclusions, just copy
    if ! [ $REQS_BASE = $REQS_OUTPUT ];then
      cp "$REQS_BASE" "$REQS_OUTPUT"
    fi
  fi
    # echo $(cat $REQS_OUTPUT)
}




echo "Prepending manual specifications..."
## Prepend manual requirements to auto-generated ones
tmp_file_merge="$(mktemp)"
tmp_file_main="$(mktemp)"
# reqs in manual override reqs in main
filter_reqs $REQS_MAIN $REQS_MANUAL $tmp_file_main
cat "$REQS_MANUAL" "$tmp_file_main" | grep -v "^#" | grep -v "^$" > "$tmp_file_merge"
mv "$tmp_file_merge" "$REQS_AUTO"


echo "Filtering from exclusions..."
## Filter auto-generated python dependencies using exclusions list
if [ -e "$REQS_EXCLUSIONS" ]; then
  filter_reqs $REQS_AUTO $REQS_EXCLUSIONS $REQS_AUTO
fi

# sort $REQS_AUTO -o $REQS_AUTO

tempdir=$(mktemp -d)
cd $tempdir
virtualenv $tempdir
source $tempdir/bin/activate
pip install pipdeptree

# get packages needed in this venv that are not part of this project's requirements
reqs_venv=$(mktemp)
python -m pipdeptree -f --warn silence \
  | sed 's/^[[:space:]]*//' \
  | sort -u \
  | grep -v "/"  \
  | grep -v "Editable" \
  | tee $reqs_venv

# remove packages in $reqs_venv that are part of this project's requiremnts
filter_reqs $reqs_venv $REQS_AUTO $reqs_venv


pip install -r $REQS_AUTO
# list all python dependencies recursively with versions
reqs_installed=$(mktemp)
python -m pipdeptree -f --warn silence \
  | sed 's/^[[:space:]]*//' \
  | sort -u \
  | grep -v "/"  \
  | grep -v "Editable" \
  | tee $reqs_installed

# remove packages in $reqs_installed that are included in $reqs_venv
filter_reqs $reqs_installed $reqs_venv $reqs_installed


# remove packages in $reqs_installed that are included in $REQS_EXCLUSIONS
filter_reqs $reqs_installed $REQS_EXCLUSIONS $REQS_AUTO
