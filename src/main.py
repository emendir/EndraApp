
import portalocker
from loguru import logger
import shutil
import os
from kivy import platform
import traceback


def main():
    try:
        # # IMPORT ORDER IS IMPORTANT
        # if platform == "android":
        #     print("DELETING ENDRA APPDATA")
        #     shutil.rmtree(os.path.join(".", "EndraAppdata"))

        # config should be loaded early to configure ipfs & walytis
        from endra_app.config import APPDATA_DIR

        # app_lock = AppLock(os.path.join(APPDATA_DIR, "endra.lock"))
        # app_lock.acquire()
        logger.debug("Getting AppLock...")
        with portalocker.Lock(os.path.join(APPDATA_DIR, "endra.lock"), timeout=1):
            import endra_app.logging  # initialise IPFS logging
            logger.debug("Got AppLock!")

            from endra_app.mainwindow import run
            print('Running Endra with appdata at', APPDATA_DIR)
            run()
        logger.debug("Released AppLock...")
        # app_lock.release()
    except Exception as e:
        from crash_window import CrashWindow
        
        logger.error(traceback.format_exc()+ "\n" + str(e))

        error_message = (
            str(e)
             + "\n\n" + 
            '\n'.join(traceback.format_exc().split('\n')[-15:])
        )
        CrashWindow(error_message).run()


if __name__ == "__main__":
    main()
