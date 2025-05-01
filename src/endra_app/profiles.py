# side_bar.py
from kivy.uix.popup import Popup
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
        self.scroll_layout.height = 0

    def add_widget_to_scroll(self, widget):
        self.scroll_layout.add_widget(widget)
        self.scroll_layout.height = self.scroll_layout.height + widget.height


class Profiles(ProfilesView):
    def __init__(self, main, profile: Profile, **kwargs):
        super().__init__(**kwargs)
        self.main = main
        self.profile = profile

        self.add_profile_btn.bind(on_press=self.offer_add_profile)
        self.reload_profiles()
        print("Loading Dropdown!")

    def offer_add_profile(self, *args, **kwargs):
        AddProfilePopup(self.main, self.profile, self).open()
        self.reload_profiles()

    def reload_profiles(self):
        logger.info("Reloading profiles...")
        self.remove_scroll_widgets()
        for profile in self.main.profiles.values():
            print("PROFILE", profile.did)
            self.add_profile_wdg(profile)
        print(self.scroll_layout.height)

    def add_profile_wdg(self, profile: Profile):
        widget = ProfileItem(
            main=self.main, profile=profile, profiles_popup=self
        )
        self.add_widget_to_scroll(widget)


class ProfileItemView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = self.ids.label


class ProfileItem(ProfileItemView):
    def __init__(self, main, profile: Profile, profiles_popup: Profiles, **kwargs):
        super().__init__(**kwargs)
        self.main = main
        self.profile = profile
        self.profiles_popup = profiles_popup
        self.label.text = profile.did
        self.label.bind(on_press=self.switch_profile)

    def switch_profile(self, *args, **kwargs):
        self.main.switch_profile(self.profile.did)
        self.profiles_popup.dismiss()


class AddProfilePopupView(Popup):
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.text_input_txbx = self.ids.text_input_txbx
        self.join_profile_btn = self.ids.join_profile_btn
        self.create_profile_btn = self.ids.create_profile_btn
from kivy.app import App; 
from kivy.uix.button import Button; 
from kivy.uix.popup import Popup; 
from kivy.uix.label import Label; 

from endra import JoinFailureError
class AddProfilePopup(AddProfilePopupView):
    def __init__(self,  main, profile: Profile, profiles_popup: Profiles, **kwargs):
        super().__init__(**kwargs)
        self.main = main
        self.profile = profile
        self.profiles_popup = profiles_popup
        self.join_profile_btn.bind(on_press=self.join_profile)
        self.create_profile_btn.bind(on_press=self.create_profile)

    def create_profile(self, instance=None):
        logger.info("Creating profile...")
        profile = self.main.create_profile()
        self.profiles_popup.reload_profiles()
        self.main.switch_profile(profile)
        self.dismiss()

    def join_profile(self, *args, **kwargs):
        try:
            invitation = json.loads(self.text_input_txbx.text)
            profile = self.main.join_profile(invitation)
        except json.JSONDecodeError:
            self.text_input_txbx.hint_text = "Invalid Invitation code.\nPaste invitation code here."
            return
        except JoinFailureError:
            Popup(
                title='Profile Join Failure', 
                content=Label(text='Failed to join profile. Trying again later might work.'), 
                size_hint=(None,None), size=(300,200)
            ).open()
            return
        self.profiles_popup.reload_profiles()

        self.main.switch_profile(profile)

        self.dismiss()
