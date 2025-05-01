

if True: # IMPORT ORDER IS IMPORTANT
    from kivy import platform
    import shutil
    import os
    if platform == "android" :
        print("DELETING ENDRA APPDATA")
        shutil.rmtree(os.path.join(".", "EndraAppdata"))
    # config should be loaded first to configure ipfs & walytis
    from endra_app.config import APPDATA_DIR
    from endra_app.mainwindow import run
    import endra_app.logging # initialise IPFS logging
def main():
    print('Running Endra with appdata at', APPDATA_DIR)
    run()


if __name__ == "__main__":
    main()
