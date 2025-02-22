# side_bar.py
from loguru import logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from endra import Profile, Correspondence
import os
# Load the KV file
KV_FILE = os.path.join(os.path.dirname(__file__), "side_bar.kv")
Builder.load_file(KV_FILE)


class CorrespondenceHeaderView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = self.ids.label
        self.button1 = self.ids.button1
        self.button2 = self.ids.button2


class CorrespondenceHeader(CorrespondenceHeaderView):
    def __init__(self, main, correspondence:Correspondence, **kwargs):
        super().__init__(**kwargs)
        self.main = main
        self.correspondence = correspondence
        self.label.text = correspondence.id
        # Bind events
        self.label.bind(on_touch_down=self.on_label_click)
        self.button1.bind(on_press=self.on_button1_click)
        self.button2.bind(on_press=self.on_button2_click)

    def on_label_click(self, instance, touch):
        if self.collide_point(*touch.pos):
            print(f"Label '{self.label.text}' clicked!")
            self.main.chat_page.load_correspondence(self.correspondence)

    def on_button1_click(self, instance):
        print(f"Button 1 in '{self.label.text}' clicked!")

    def on_button2_click(self, instance):
        print(f"Button 2 in '{self.label.text}' clicked!")


class SideBarView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.scroll_view = self.ids.scroll_view
        
        self.scroll_layout = self.ids.scroll_layout
        self.add_corresp_btn = self.ids.add_corresp_btn

        self.scroll_layout.bind(
            minimum_height=self.scroll_layout.setter('height')
        )

class SideBar(SideBarView):
    def __init__(self, main, profile: Profile | None, **kwargs):
        super().__init__(**kwargs)
        self.main = main

        self.profile = profile

        self.add_corresp_btn.bind(on_press=self.create_correspondence)
        self.reload_correspondences()

    def reload_correspondences(self):
        logger.info("Reloading correspondences...")

        self.remove_all_widgets()
        if self.profile:
            active_correspondences=self.profile.get_active_correspondences()
            for correspondence_id in active_correspondences:
                self.add_widget_to_scroll(self.profile.get_correspondence(correspondence_id))
            
                
    def create_correspondence(self, instance=None):
        logger.info("Creating correspondence...")
        correspondence = self.profile.create_correspondence()
        self.reload_correspondences()
        self.main.chat_page.load_correspondence(correspondence)

    def add_widget_to_scroll(self, correspondence):
        widget = CorrespondenceHeader(
            main = self.main, correspondence=correspondence
        )
        self.scroll_layout.add_widget(widget)

    def remove_widget_from_scroll(self, index):
        if 0 <= index < len(self.scroll_layout.children):
            self.scroll_layout.remove_widget(
                self.scroll_layout.children[index])

    def remove_all_widgets(self):
        while (len(self.scroll_layout.children)):
            self.scroll_layout.remove_widget(self.scroll_layout.children[0])
