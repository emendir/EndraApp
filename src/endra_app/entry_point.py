
import portalocker
from loguru import logger
import shutil
import os
from kivy import platform
import traceback


def run():
    # # IMPORT ORDER IS IMPORTANT
    # if platform == "android":
    #     print("DELETING ENDRA APPDATA")
    #     shutil.rmtree(os.path.join(".", "EndraAppdata"))

    # config should be loaded early to configure ipfs & walytis
    from .config import APPDATA_DIR

    # app_lock = AppLock(os.path.join(APPDATA_DIR, "endra.lock"))
    # app_lock.acquire()
    logger.debug("Getting AppLock...")
    with portalocker.Lock(os.path.join(APPDATA_DIR, "endra.lock"), timeout=1):
        from . import logging  # initialise IPFS logging
        logger.debug("Got AppLock!")

        from .mainwindow import run
        print('Running Endra with appdata at', APPDATA_DIR)
        run()
    logger.debug("Released AppLock...")



if __name__ == "__main__":
    run()
