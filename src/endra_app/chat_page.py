# side_bar.py
from loguru import logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from endra import Message, Correspondence, MessageContent
import os
# Load the KV file
KV_FILE = os.path.join(os.path.dirname(__file__), "chat_page.kv")
Builder.load_file(KV_FILE)

class MessageEditorView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
        self.text_input_txbx = self.ids.text_input_txbx
class MessageEditor(MessageEditorView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def get_message_content(self):
        return MessageContent(
            text = self.text_input_txbx.text,
            file_data=None
        )
class MessageView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = self.ids.label


class MessageWidget(MessageView):
    def __init__(self, message:Message, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.label.text = self.message.content.text
        # Bind events
        self.label.bind(on_touch_down=self.on_label_click)

    def on_label_click(self, instance, touch):
        if self.collide_point(*touch.pos):
            print(f"Label '{self.label.text}' clicked!")



class MessagePageView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.scroll_view = self.ids.scroll_view
        
        self.scroll_layout = self.ids.scroll_layout
        self.add_message_btn = self.ids.add_message_btn
        self.scroll_layout.bind(
            minimum_height=self.scroll_layout.setter('height')
        )
        self.message_editor = MessageEditor()
        self.ids.add_message_btn_lyt.add_widget(self.message_editor)
        
    def deactivate(self):
        self.disabled=True
    def activate(self):
        self.disabled=False

class MessagePage(MessagePageView):
    def __init__(self, main, correspondence: Correspondence | None, **kwargs):
        super().__init__(**kwargs)
        self.deactivate()
        
        self.main = main
        self.correspondence = correspondence

        self.add_message_btn.bind(on_press=self.create_message)
        self.reload_messages()
    def load_correspondence(self, correspondence):
        self.correspondence = correspondence
        self.reload_messages()
        self.activate()
        
    def reload_messages(self):
        logger.info("Reloading chat messages...")

        self.remove_all_widgets()
        if self.correspondence:
            print("Number of messages:", len(self.correspondence.get_messages()))
            for message in self.correspondence.get_messages():
                print(message.content.text)
                self.add_widget_to_scroll(message)

    def create_message(self, instance=None):
        logger.info("Creating message...")
        self.correspondence.add_message(
            self.message_editor.get_message_content()
        )
        self.message_editor.text_input_txbx.text = ""
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
