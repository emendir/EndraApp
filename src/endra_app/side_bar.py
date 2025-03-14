# side_bar.py
from .settings import ProfileSettingsPopup
import walytis_beta_api
import json
from loguru import logger
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from endra import Profile, Correspondence
import os
from kivy.uix.popup import Popup
# Load the KV file
KV_FILE = os.path.join(os.path.dirname(__file__), "side_bar.kv")
Builder.load_file(KV_FILE)


class AddCorrespondencePopupView(Popup):
    def __init__(self, main, profile: Profile, **kwargs):
        super().__init__(**kwargs)
        self.main = main
        self.profile = profile
        self.text_input_txbx = self.ids.text_input_txbx
        self.join_conv_btn = self.ids.join_conv_btn
        self.create_conv_btn = self.ids.create_conv_btn

        self.join_conv_btn.bind(on_press=self.join_correspondence)
        self.create_conv_btn.bind(on_press=self.create_correspondence)

    def create_correspondence(self, instance=None):
        logger.info("Creating correspondence...")
        correspondence = self.profile.create_correspondence()
        self.main.side_bar.reload_correspondences()
        self.main.chat_page.load_correspondence(correspondence)
        self.dismiss()

    def join_correspondence(self, *args, **kwargs):
        try:
            invitation = json.loads(self.text_input_txbx.text)
            correspondence = self.profile.join_correspondence(invitation)
        except json.JSONDecodeError:
            self.text_input_txbx.hint_text = "Invalid Invitation code.\nPaste invitation code here."
            return
        except walytis_beta_api.JoinFailureError:
            self.join_conv_btn.hint_text = "Try again\n(join attampt failed)"
            return

        self.main.side_bar.reload_correspondences()
        self.main.chat_page.load_correspondence(correspondence)

        self.dismiss()


class CorrespondenceItemView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = self.ids.label


class CorrespondenceItem(CorrespondenceItemView):
    def __init__(self, main, correspondence: Correspondence, **kwargs):
        super().__init__(**kwargs)
        self.main = main
        self.correspondence = correspondence
        self.label.text = correspondence.id
        # Bind events
        self.label.bind(on_touch_down=self.on_label_click)

    def on_label_click(self, instance, touch):
        if self.collide_point(*touch.pos):
            print(f"Label '{self.label.text}' clicked!")
            self.main.chat_page.load_correspondence(self.correspondence)

from .profiles import Profiles
class SideBarView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scroll_view = self.ids.scroll_view
        self.profile_controls_lyt = self.ids.profile_controls_lyt
        self.scroll_layout = self.ids.scroll_layout
        self.my_profile_btn = self.ids.my_profile_btn
        self.open_profiles_btn = self.ids.open_profiles_btn
        self.add_corresp_btn = self.ids.add_corresp_btn

        self.scroll_layout.bind(
            minimum_height=self.scroll_layout.setter('height')
        )

    def remove_widget_from_scroll(self, index):
        if 0 <= index < len(self.scroll_layout.children):
            self.scroll_layout.remove_widget(
                self.scroll_layout.children[index])

    def remove_scroll_widgets(self):
        while (len(self.scroll_layout.children)):
            self.scroll_layout.remove_widget(self.scroll_layout.children[0])


class SideBar(SideBarView):
    def __init__(self, main, profile: Profile | None, **kwargs):
        super().__init__(**kwargs)
        self.main = main

        self.profile = profile

        self.add_corresp_btn.bind(on_press=self.offer_add_correspondence)
        self.my_profile_btn.bind(on_press=self.open_profile_settings)
        self.open_profiles_btn.bind(on_press=self.open_profiles)
        self.reload_correspondences()

    def reload_correspondences(self):
        logger.info("Reloading correspondences...")

        self.remove_scroll_widgets()
        if self.profile:
            active_correspondences = self.profile.get_active_correspondences()
            for correspondence_id in active_correspondences:
                self.add_correspondence_header(
                    self.profile.get_correspondence(correspondence_id))

    def offer_add_correspondence(self, *args, **kwargs):
        popup = AddCorrespondencePopupView(
            main=self.main,
            profile=self.profile,
        )
        popup.open()

    def open_profile_settings(self, *args, **kwargs):
        popup = ProfileSettingsPopup(
            main=self.main,
            profile=self.profile,
        )
        popup.open()
    def open_profiles(self, *args, **kwargs):
        dropdown = Profiles(self.main, self.profile)
        dropdown.open(self.profile_controls_lyt)

    def add_correspondence_header(self, correspondence):
        widget = CorrespondenceItem(
            main=self.main, correspondence=correspondence
        )
        self.scroll_layout.add_widget(widget)
