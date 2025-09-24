#!/bin/bash
""":"
script_dir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $script_dir

rm -rf appdata
cp -r /home/$USER/.local/share/Endra ./appdata

exit 0
"""


# reexecute this file in shell if it's run in python
import os
os.system(__file__)
