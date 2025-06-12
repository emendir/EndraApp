#!/bin/bash
""":"

# the absolute path of this script's directory
script_dir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $script_dir
# Exit if any command fails
set -e

# rsync -XAva --delete ../EndraProtocol/src/endra ./src/
# rsync -XAva --delete ../../BlockchainOverlays/walytis_identities/src/walytis_identities ./src/
# rsync -XAva --delete ../../BlockchainOverlays/walytis_mutability/src/walytis_mutability ./src/
# rsync -XAva --delete ../../BlockchainOverlays/walytis_offchain/src/walytis_offchain ./src/
# rsync -XALva --delete ../../Brenthy/Deployment/walytis_beta_embedded/walytis_beta_embedded ./src/
# rsync -XALva --delete ../../Brenthy/Brenthy/brenthy_tools_beta ./src/





exit 0
"""
import os
import sys
# Python: re-execute the script in Bash
os.execvp('bash', ['bash', __file__] + sys.argv[1:])
#"