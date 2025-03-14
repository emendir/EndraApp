"""This script tries to load kivy with more advanced font handling if possible.
"""
import os
USING_PANGO = False
try:
    os.environ['KIVY_TEXT'] = 'pango'
    import kivy
    from kivy.core.text import FontContextManager as FCM
    FCM.create('system://myapp')
    # family = FCM.add_font('system://myapp', 'LibertinusSerif-Regular.otf')
    # family = FCM.add_font('system://myapp', 'FreeSerif.ttf')
    # family = FCM.add_font('system://myapp', 'NotoColorEmoji.ttf')
    USING_PANGO = True
    print("Successfully loaded font context!")
except:
    os.environ.pop('KIVY_TEXT')  # = ORG_KIVY_TEXT
    print("Failed to load font context, pity. Reloading kivy.")
    import importlib
    importlib.reload(kivy)


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
            )
    MyApp().run()
