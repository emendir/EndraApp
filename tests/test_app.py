import _testing_utils
from endra_app import run

from endra_app import _load_kivy  # load kivy with better font handling
import shutil
from endra_app.config import (
    APPDATA_DIR,
    WALYTIS_BETA_DATA_DIR,
    PRIVATE_BLOCKS_DATA_DIR,
    IPFS_REPO_DIR,
)
from endra_app.utils import ensure_dir_exists
import os


# _testing_utils.assert_is_loaded_from_source(
#     source_dir=os.path.join(os.path.dirname(__file__), "..", ".."), module=config
# )
# _testing_utils.assert_is_loaded_from_source(
#     source_dir=os.path.join(os.path.dirname(__file__), "..", ".."), module=endra_app
# )
WORKING_DIR = os.path.join(os.path.dirname(__file__))
APPDATA_BACKUP_DIR = os.path.join(WORKING_DIR, "appdata")

# do something with _load_kivy to stop IDEs from removing the import
print("Using Pango Font Context:", _load_kivy.using_pango)


# replace appdata with appdata backup
if not os.path.exists(APPDATA_BACKUP_DIR):
    os.makedirs(APPDATA_BACKUP_DIR)
if os.path.exists(APPDATA_DIR):
    shutil.rmtree(APPDATA_DIR)
# os.system(f"rsync -XAva {APPDATA_BACKUP_DIR}/ {APPDATA_DIR}/")
shutil.copytree(APPDATA_BACKUP_DIR, APPDATA_DIR)
ensure_dir_exists(APPDATA_DIR)
ensure_dir_exists(WALYTIS_BETA_DATA_DIR)
ensure_dir_exists(IPFS_REPO_DIR)
ensure_dir_exists(PRIVATE_BLOCKS_DATA_DIR)

# run Endra App
run()

# copy appdata back into appdata backup
if os.path.exists(APPDATA_BACKUP_DIR):
    shutil.rmtree(APPDATA_BACKUP_DIR)
shutil.copytree(APPDATA_DIR, APPDATA_BACKUP_DIR)

# os.system(f"rsync -XAva {APPDATA_DIR}/ {APPDATA_BACKUP_DIR}/")
