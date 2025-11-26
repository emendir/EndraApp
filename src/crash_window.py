from kivy.app import App
from kivy.uix.label import Label
import sys


class CrashWindow(App):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text

    def build(self):
        label = Label(
            text=f"{sys.version}\n{self.text}",
            size_hint=(1, 1),
            halign="left",
            valign="top",
        )
        # Make text wrap by setting text_size to label size
        label.bind(size=lambda *args: setattr(label, "text_size", label.size))
        return label


if __name__ == "__main__":
    CrashWindow("Hello there!\nTesting").run()
