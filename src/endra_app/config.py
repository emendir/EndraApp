from emtest import env_vars, set_env_var
import sys
import ctypes
import os
from .utils import ensure_dir_exists
from kivy.utils import platform

if platform == "android":
    # patch for pycryptodome, from https://github.com/kivy/python-for-android/issues/1866#issuecomment-927157780
    # replaces ctypes.PyDLL(None)
    ctypes.pythonapi = ctypes.PyDLL("libpython%d.%d.so" % sys.version_info[:2])

if platform == "android":
    from android.storage import app_storage_path

    APPDATA_DIR = app_storage_path()
elif platform in ("linux", "win", "macosx"):
    from appdirs import user_data_dir

    APPDATA_DIR = os.path.join(user_data_dir(), "Endra")
else:
    raise NotImplementedError(f"Unsupported platform: {platform}")

# override if environment variable is set
APPDATA_DIR = env_vars.str("ENDRA_APPDATA_DIR", default=APPDATA_DIR)
print(f"Appdata Dir: {APPDATA_DIR}")

set_env_var("WALY_LOG_DIR", "DISABLED", override=False)
if os.environ["WALY_LOG_DIR"] == "ENDRA_APPDATA":
    os.environ["WALY_LOG_DIR"] = os.path.join(APPDATA_DIR, "logs")

ENABLE_PUBSUB_LOGGING = env_vars.bool("ENDRA_PUBSUB_LOGGING", default=False)
BOOTSTRAP_PEERS_PATH = os.path.join(APPDATA_DIR, "BOOTSTRAP_PEERS.txt")
PEER_MONITOR_PATH = os.path.join(APPDATA_DIR, "ipfs_bootstrap_peer_monitor.json")

# only relevant if USE_BRENTHY==False
IPFS_REPO_DIR = ensure_dir_exists(os.path.join(APPDATA_DIR, "ipfs"))
WALYTIS_BETA_DATA_DIR = ensure_dir_exists(
    os.path.join(APPDATA_DIR, "walytis")
)  # only relevant if USE_BRENTHY==False
PRIVATE_BLOCKS_DATA_DIR = ensure_dir_exists(
    os.path.join(APPDATA_DIR, "private_blocks")
)  # only relevant if USE_BRENTHY==False
os.environ["PRIVATE_BLOCKS_DATA_DIR"] = PRIVATE_BLOCKS_DATA_DIR

# defaults to False
USE_BRENTHY = os.environ.get("USE_BRENTHY", "").lower() in ["true", "1"]
print("USE_BRENTHY", USE_BRENTHY)
