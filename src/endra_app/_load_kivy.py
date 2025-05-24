"""This script tries to load kivy with more advanced font handling if possible.
"""
import os
using_pango = False
FONTS_DIR=os.path.join(os.path.dirname(__file__), "fonts")
import subprocess
import traceback
# decide whether or not we're gonna try to load the pango text provider,
# cause trying under the wrong circumstances can crash the app
try:
    TRY_USE_PANGO=False
    import platform

    print("Platform",platform.platform().lower())
    if "linux" in platform.platform().lower() and "x86_64" in platform.platform().lower():
        # result = subprocess.run("pkg-config --modversion pango", shell=True, capture_output=True)
        # print(result.stdout)
        # if len(result.stdout.strip().decode().split(".")) == 3:
        TRY_USE_PANGO=True
except Exception as e:
    traceback.print_exc()
    print(e)
    TRY_USE_PANGO=False

# try to load the pango text provider
if TRY_USE_PANGO:
    print("Trying to load Kivy with pango...")
    # sometimes when kivy can't load pango
    # it crashes the app despite this try block
    try:
        os.environ['KIVY_TEXT'] = 'pango'
        import kivy
        from kivy.core.text import FontContextManager as FCM
        FCM.create('system://myapp')
        # family = FCM.add_font('system://myapp', os.path.join(FONTS_DIR,'LibertinusSerif-Regular.otf'))
        # family = FCM.add_font('system://myapp', 'FreeSerif.ttf')
        # family = FCM.add_font('system://myapp', 'NotoColorEmoji.ttf')
        using_pango = True
        print("Successfully loaded font context!")
    except Exception as e:
        
        os.environ.pop('KIVY_TEXT')  # = ORG_KIVY_TEXT
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

if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.label import Label

    class MyApp(App):
        def build(self):
            return Label(
                text='''Hello there!
⏷▼⮟⯆🞃🚀😊
Русский
Tiếng Việt
العربية
中文
日本語
বাংলা
                ''',
                font_context='system://myapp',
                font_name="./fonts/LibertinusSerif-Regular.otf"
            )
    MyApp().run()
