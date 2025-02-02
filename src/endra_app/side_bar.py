# side_bar.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from endra import Profile
import os
# Load the KV file
KV_FILE= os.path.join(os.path.dirname(__file__), "style.kv")
Builder.load_file(KV_FILE)

class CorrespondenceHeader(BoxLayout):
    def __init__(self, label_text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 50

        # Create widgets
        self.label = self.ids.label
        self.button1 = self.ids.button1
        self.button2 = self.ids.button2

class CorrespondenceHeaderController(CorrespondenceHeader):
    def __init__(self, label_text, **kwargs):
        super().__init__(label_text, **kwargs)
        self.label.text = label_text
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
        
        
from loguru import logger
class SideBar(BoxLayout):
    def __init__(self, profile:Profile|None,**kwargs):
        super().__init__(**kwargs)
        
        self.profile = profile
        
        self.orientation = 'vertical'
        self.size_hint = (0.3, 1)
        

        # Add scroll view
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scroll_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))
        self.scroll_view.add_widget(self.scroll_layout)

        self.add_widget(self.scroll_view)

        # Add button for testing
        self.add_widget(Button(text='Add Widget', size_hint=(1, None), height=50, on_press=self.create_correspondence))
        self.reload_correspondences()
        

    def reload_correspondences(self):
        logger.info("Reloading correspondences...")
        
        self.remove_all_widgets()
        if self.profile:
            for correspondence_id in self.profile.get_active_correspondences():
                self.add_widget_to_scroll(correspondence_id)
    
    def create_correspondence(self, instance=None):
        logger.info("Creating correspondence...")
        self.profile.create_correspondence()
        self.reload_correspondences()
    def add_widget_to_scroll(self, correspondence_name:str):
        widget = CorrespondenceHeaderController(label_text=correspondence_name)
        self.scroll_layout.add_widget(widget)

    def remove_widget_from_scroll(self, index):
        if 0 <= index < len(self.scroll_layout.children):
            self.scroll_layout.remove_widget(self.scroll_layout.children[index])
    def remove_all_widgets(self):
        while(len(self.scroll_layout.children)):
            self.scroll_layout.remove_widget(self.scroll_layout.children[0])
            
