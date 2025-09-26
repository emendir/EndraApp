"""This module loads the kivy library.

If possible, it tries to load kivy with more advanced font handling.
"""

import sys
import platform
import traceback
import os

using_pango = False
FONTS_DIR = os.path.join(os.path.dirname(__file__), "fonts")

# fix for bug in pyinstaller on Windows:
# https://github.com/pyinstaller/pyinstaller/issues/8878
if getattr(sys, "frozen", False):
    import site

    site.USER_BASE = ""
    site.USER_SITE = ""
# The following is only necessary when Windows doesn't support OpenGL >=2.0
# if platform.system() == "Windows":
#     os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"

# decide whether or not we're gonna try to load the pango text provider,
# cause trying under the wrong circumstances can crash the app
try:
    DEF_USE_PANGO = False

    print("Platform", platform.platform().lower())
    if (
        "linux" in platform.platform().lower()
        and "x86_64" in platform.platform().lower()
    ):
        # result = subprocess.run("pkg-config --modversion pango", shell=True, capture_output=True)
        # print(result.stdout)
        # if len(result.stdout.strip().decode().split(".")) == 3:
        DEF_USE_PANGO = True
        pass
except Exception as e:
    traceback.print_exc()
    print(e)
    DEF_USE_PANGO = False
ENV_USE_PANGO = os.environ.get("USE_PANGO")
if ENV_USE_PANGO:
    match ENV_USE_PANGO.lower():
        case "0":
            USE_PANGO = False
        case "false":
            USE_PANGO = False
        case "1":
            USE_PANGO = True
        case "true":
            USE_PANGO = True
        case _:
            raise ValueError(
                "The environment variable USE_PANGO should have a value from [0,1,True,False], "
                f" not {ENV_USE_PANGO}"
            )
else:
    USE_PANGO = DEF_USE_PANGO
# try to load the pango text provider
if USE_PANGO:
    print("Trying to load Kivy with pango...")
    print("If this crashes, set the environment variable USE_PANGO to 0")
    # sometimes when kivy can't load pango
    # it crashes the app despite this try block
    try:
        os.environ["KIVY_TEXT"] = "pango"
        import kivy
        from kivy.core.text import FontContextManager as FCM

        FCM.create("system://myapp")
        # family = FCM.add_font('system://myapp', os.path.join(FONTS_DIR,'LibertinusSerif-Regular.otf'))
        # family = FCM.add_font('system://myapp', 'FreeSerif.ttf')
        # family = FCM.add_font('system://myapp', 'NotoColorEmoji.ttf')
        using_pango = True
        print("Successfully loaded font context!")
    except Exception as e:
        os.environ.pop("KIVY_TEXT")  # = ORG_KIVY_TEXT
        print("Failed to load font context, pity. Reloading kivy.")
        print(e)
        import traceback

        traceback.print_exc()
        # import importlib
        # importlib.reload(kivy)
        import kivy
else:
    print("Loading kivy without pango.")
    import kivy

print(f"Loaded kivy {kivy.sys.version}")
if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.label import Label

    class MyApp(App):
        def build(self):
            return Label(
                text="""Hello there!
⏷▼⮟⯆🞃🚀😊
Русский
Tiếng Việt
العربية
中文
日本語
বাংলা
                """,
                font_context="system://myapp",
                font_name="./fonts/LibertinusSerif-Regular.otf",
            )

    MyApp().run()
