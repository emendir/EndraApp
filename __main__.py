import sys
import os
os.chdir(os.path.join(os.path.dirname(__file__), "src"))
os.system(f"{sys.executable} -m endra_app")