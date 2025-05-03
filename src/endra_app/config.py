import sys
import ctypes
from appdirs import user_data_dir
import os
from .utils import ensure_dir_exists
import os
from kivy.utils import platform
# patch for pycryptodome, from https://github.com/kivy/python-for-android/issues/1866#issuecomment-927157780
# replaces ctypes.PyDLL(None)
ctypes.pythonapi = ctypes.PyDLL("libpython%d.%d.so" % sys.version_info[:2])

if platform == 'android':
    from android.storage import app_storage_path
    APPDATA_DIR = app_storage_path()
elif platform in ('linux', 'win', 'macosx'):
    from appdirs import user_data_dir
    APPDATA_DIR = os.path.join(user_data_dir(), "Endra")
else:
    raise NotImplementedError(f"Unsupported platform: {platform}")

# APPDATA_DIR = os.path.join(user_data_dir(), "Endra")
# APPDATA_DIR = os.path.join(".", "EndraAppdata")

USE_BRENTHY = False

IPFS_REPO_DIR = ensure_dir_exists(os.path.join(APPDATA_DIR, "ipfs")) # only relevant if USE_BRENTHY==False
WALYTIS_BETA_DATA_DIR = ensure_dir_exists(os.path.join(APPDATA_DIR, "walytis")) # only relevant if USE_BRENTHY==False
PRIVATE_BLOCKS_DATA_DIR = ensure_dir_exists(os.path.join(APPDATA_DIR, "private_blocks")) # only relevant if USE_BRENTHY==False


if USE_BRENTHY:
    os.environ["USE_IPFS_NODE"] = "false"
    os.environ["WALYTIS_BETA_API_TYPE"] = "WALYTIS_BETA_BRENTHY_API"

else:
    os.environ["USE_IPFS_NODE"] = "true"
    os.environ["IPFS_REPO_DIR"] = IPFS_REPO_DIR
    os.environ["AUTO_LOAD_BAP_MODULES"] = "false"
    os.environ["WALYTIS_BETA_API_TYPE"] = "WALYTIS_BETA_DIRECT_API"
    os.environ["WALYTIS_BETA_DATA_DIR"] = WALYTIS_BETA_DATA_DIR
os.environ["PRIVATE_BLOCKS_DATA_DIR"] = PRIVATE_BLOCKS_DATA_DIR
print("Set environ:", os.environ["WALYTIS_BETA_API_TYPE"])

