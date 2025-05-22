
import shutil
import _testing_utils
import walytis_beta_api as walytis_api
from endra_app import config
from endra_app.config import APPDATA_DIR
import os
import endra_app
from endra_app import run
walytis_api.log.PRINT_DEBUG = False


_testing_utils.assert_is_loaded_from_source(
    source_dir=os.path.join(os.path.dirname(__file__), "..", ".."), module=config
)
_testing_utils.assert_is_loaded_from_source(
    source_dir=os.path.join(os.path.dirname(__file__), "..", ".."), module=endra_app
)
WORKING_DIR = os.path.join(os.path.dirname(__file__))
APPDATA_BACKUP_DIR = os.path.join(
    WORKING_DIR, "appdata"
)


# replace appdata with appdata backup
if not os.path.exists(APPDATA_BACKUP_DIR):
    os.makedirs(APPDATA_BACKUP_DIR)
if os.path.exists(APPDATA_DIR):
    shutil.rmtree(APPDATA_DIR)
shutil.copytree(APPDATA_BACKUP_DIR, APPDATA_DIR)

# run Endra App
run()

# copy appdata back into appdata backup
if os.path.exists(APPDATA_BACKUP_DIR):
    shutil.rmtree(APPDATA_BACKUP_DIR)
shutil.copytree(APPDATA_DIR, APPDATA_BACKUP_DIR)
