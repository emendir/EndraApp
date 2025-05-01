# patch for pycryptodome, from https://github.com/kivy/python-for-android/issues/1866#issuecomment-927157780
import ctypes, sys
ctypes.pythonapi = ctypes.PyDLL("libpython%d.%d.so" % sys.version_info[:2])   # replaces ctypes.PyDLL(None)

import os
USE_BRENTHY=False
if USE_BRENTHY:
    os.environ["USE_IPFS_NODE"] = "false"
    os.environ["WALYTIS_BETA_API_TYPE"] = "WALYTIS_BETA_BRENTHY_API"
    
else:
    os.environ["USE_IPFS_NODE"] = "true"
    os.environ["AUTO_LOAD_BAP_MODULES"] = "false"
    os.environ["WALYTIS_BETA_API_TYPE"] = "WALYTIS_BETA_DIRECT_API"
print("Set environ:", os.environ["WALYTIS_BETA_API_TYPE"])

print('main.py')
from endra_app.mainwindow import run
def main():
    print('main.main()')
    run()
if __name__ == "__main__":
    main()
