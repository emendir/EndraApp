#!/bin/bash
PYVER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
python3 -c "import sys; print(sys.version); print(sys.path)"
export PYTHONPATH=/app/lib/python3.11/site-packages:$PYTHONPATH
exec python3 -m endra_app "$@"
