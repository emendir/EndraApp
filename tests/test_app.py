
import shutil
import _testing_utils
import walytis_beta_api as walytis_api
from endra_app import config
from endra_app.config import APPDATA_DIR
import os
from endra_app import main
from endra_app.main import run_app
walytis_api.log.PRINT_DEBUG = False


_testing_utils.assert_is_loaded_from_source(
    source_dir=os.path.join(os.path.dirname(__file__), "..", ".."), module=config
)
_testing_utils.assert_is_loaded_from_source(
    source_dir=os.path.join(os.path.dirname(__file__), "..", ".."), module=main
)
print(APPDATA_DIR)
if os.path.exists(APPDATA_DIR):
    shutil.rmtree(APPDATA_DIR)
WORKING_DIR = os.path.join(os.path.dirname(__file__))
APPDATA_BACKUP_DIR = os.path.join(
    WORKING_DIR, "appdata"
)
print(APPDATA_BACKUP_DIR)
shutil.copytree(APPDATA_BACKUP_DIR, APPDATA_DIR)
run_app()
