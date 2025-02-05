# side_bar.py
from loguru import logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from endra import Message, Correspondence
import os
# Load the KV file
KV_FILE = os.path.join(os.path.dirname(__file__), "chat_page.kv")
Builder.load_file(KV_FILE)


class MessageView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = self.ids.label
        self.button1 = self.ids.button1
        self.button2 = self.ids.button2


class MessageWidget(MessageView):
    def __init__(self, correspondence:Correspondence, **kwargs):
        super().__init__(**kwargs)
        self.label.text = correspondence.id
        # Bind events
        self.label.bind(on_touch_down=self.on_label_click)
        self.button1.bind(on_press=self.on_button1_click)
        self.button2.bind(on_press=self.on_button2_click)

    def on_label_click(self, instance, touch):
        if self.collide_point(*touch.pos):
            print(f"Label '{self.label.text}' clicked!")

    def on_button1_click(self, instance):
        print(f"Button 1 in '{self.label.text}' clicked!")

    def on_button2_click(self, instance):
        print(f"Button 2 in '{self.label.text}' clicked!")


class MessagePageView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.scroll_view = self.ids.scroll_view
        
        self.scroll_layout = self.ids.scroll_layout
        self.add_message_btn = self.ids.add_message_btn

        self.scroll_layout.bind(
            minimum_height=self.scroll_layout.setter('height')
        )

class MessagePage(MessagePageView):
    def __init__(self, correspondence: Correspondence | None, **kwargs):
        super().__init__(**kwargs)

        self.correspondence = correspondence

        self.add_message_btn.bind(on_press=self.create_message)
        self.reload_messages()

    def reload_messages(self):
        logger.info("Reloading correspondences...")

        self.remove_all_widgets()
        if self.correspondence:
            for message in self.correspondence.get_messages():
                self.add_widget_to_scroll(message)

    def create_message(self, instance=None):
        logger.info("Creating correspondence...")
        self.correspondence.add_message()
        self.reload_messages()

    def add_widget_to_scroll(self, message):
        widget = MessageWidget(message=message)
        self.scroll_layout.add_widget(widget)

    def remove_widget_from_scroll(self, index):
        if 0 <= index < len(self.scroll_layout.children):
            self.scroll_layout.remove_widget(
                self.scroll_layout.children[index])

    def remove_all_widgets(self):
        while (len(self.scroll_layout.children)):
            self.scroll_layout.remove_widget(self.scroll_layout.children[0])
