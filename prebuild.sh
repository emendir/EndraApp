#!/bin/bash
""":"

# the absolute path of this script's directory
script_dir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $script_dir
# Exit if any command fails
set -e

rsync -XAva --delete ../EndraProtocol/src/endra ./src/
rsync -XAva --delete ../../BlockchainOverlays/WalIdentity/src/walidentity ./src/
rsync -XAva --delete ../../BlockchainOverlays/Mutablock/src/mutablockchain ./src/
rsync -XAva --delete ../../BlockchainOverlays/PrivateBlocks/src/private_blocks ./src/
rsync -XALva --delete ../../Brenthy/Deployment/walytis_beta_embedded/walytis_beta_embedded ./src/
rsync -XALva --delete ../../Brenthy/Brenthy/brenthy_tools_beta ./src/





exit 0
"""
import os
import sys
# Python: re-execute the script in Bash
os.execvp('bash', ['bash', __file__] + sys.argv[1:])
#"