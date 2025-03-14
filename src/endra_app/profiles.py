# side_bar.py
from endra import Profile
from .utils import InvitationPopupView
import json
from loguru import logger
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import os
from kivy.uix.dropdown import DropDown
# Load the KV file
KV_FILE = os.path.join(os.path.dirname(__file__), "profiles.kv")
Builder.load_file(KV_FILE)


class ProfilesView(DropDown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.layout = self.ids.layout
        self.scroll_view = self.ids.scroll_view
        self.scroll_layout = self.ids.scroll_layout
        self.add_profile_btn = self.ids.add_profile_btn

    def remove_widget_from_scroll(self, index):
        if 0 <= index < len(self.scroll_layout.children):
            self.scroll_layout.remove_widget(
                self.scroll_layout.children[index])

    def remove_scroll_widgets(self):
        while (len(self.scroll_layout.children)):
            self.scroll_layout.remove_widget(self.scroll_layout.children[0])


class Profiles(ProfilesView):
    def __init__(self, main, profile: Profile, **kwargs):
        super().__init__(**kwargs)
        self.main = main
        self.profile = profile

        self.add_profile_btn.bind(on_press=self.offer_add_profile)
        self.reload_profiles()
        print("Loading Dropdown!")

    def offer_add_profile(self, *args, **kwargs):
        pass

    def reload_profiles(self):
        logger.info("Reloading profiles...")

        for profile in self.main.profiles.values():
            print("PROFILE", profile.did)
            self.add_profile_wdg(profile)

    def add_profile_wdg(self, profile: Profile):
        widget = ProfileItem(
            main=self.main, profile=profile
        )
        self.scroll_layout.add_widget(widget)


class ProfileItemView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = self.ids.label


class ProfileItem(ProfileItemView):
    def __init__(self, main, profile: Profile, **kwargs):
        super().__init__(**kwargs)
        self.main = main
        self.profile = profile
        self.label.text = profile.did
