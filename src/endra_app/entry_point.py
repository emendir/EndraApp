
import portalocker
import os


def run():
    # # IMPORT ORDER IS IMPORTANT
    from .log import logger
    from . import _load_kivy
    from kivy import platform
    # if platform == "android":
    #     print("DELETING ENDRA APPDATA")
    #     shutil.rmtree(os.path.join(".", "EndraAppdata"))

    # config should be loaded early to configure ipfs & walytis
    from .config import APPDATA_DIR

    # app_lock = AppLock(os.path.join(APPDATA_DIR, "endra.lock"))
    # app_lock.acquire()
    logger.debug("Getting AppLock...")
    with portalocker.Lock(os.path.join(APPDATA_DIR, "endra.lock"), timeout=1):
        from . import endra_logging  # initialise IPFS endra_logging
        logger.debug("Got AppLock!")

        from .mainwindow import run
        print('Running Endra with appdata at', APPDATA_DIR)
        run()
    logger.debug("Released AppLock...")



if __name__ == "__main__":
    run()
