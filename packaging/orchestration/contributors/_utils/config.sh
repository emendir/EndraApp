#!/bin/bash

REPO_DIR=$1
FORK_REPO=$2

UPSTREAM_REPO=emendir/EndraApp

BUILD_SCRIPT=packaging/build_all.sh







# Detect if the script is being executed instead of sourced
(return 0 2>/dev/null) && sourced=1 || sourced=0
if [ "$sourced" -eq 0 ]; then
    echo "Error: This script must be sourced, not executed." >&2
    exit 1
fi

