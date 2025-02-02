# central_page.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class CentralPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='Central Page', font_size=24, size_hint=(1, None), height=50))
