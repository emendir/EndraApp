# side_bar.py
from endra import Device
from .utils import InvitationPopupView
from .utils import InvitationView
import walytis_beta_api
import json
from loguru import logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from endra import Profile, Correspondence
import os
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
from kivy_garden.qrcode import QRCodeWidget
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
        except json.JSONDecodeError as e:
            self.text_input_txbx.hint_text = "Invalid Invitation code.\nPaste invitation code here."
            return
        except walytis_beta_api.JoinFailureError as e:
            self.join_conv_btn.hint_text = "Try again\n(join attampt failed)"
            return

        self.main.side_bar.reload_correspondences()
        self.main.chat_page.load_correspondence(correspondence)

        self.dismiss()


class ProfileSettingsPopupView(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = self.ids.layout
        self.scroll_view = self.ids.scroll_view
        self.scroll_layout = self.ids.scroll_layout
        self.add_device_btn = self.ids.add_device_btn

    def remove_widget_from_scroll(self, index):
        if 0 <= index < len(self.scroll_layout.children):
            self.scroll_layout.remove_widget(
                self.scroll_layout.children[index])

    def remove_scroll_widgets(self):
        while (len(self.scroll_layout.children)):
            self.scroll_layout.remove_widget(self.scroll_layout.children[0])


class ProfileSettingsPopup(ProfileSettingsPopupView):
    def __init__(self, main, profile: Profile, **kwargs):
        super().__init__(**kwargs)
        self.main = main
        self.profile = profile

        self.add_device_btn.bind(on_press=self.invite_device)
        self.reload_devices()
    def invite_device(self, *args, **kwargs):
        invitation = self.profile.invite()
        invitation_str = json.dumps(invitation)
        popup = InvitationPopupView(invitation_str)
        popup.open()

    def reload_devices(self):
        logger.info("Reloading devices...")

        self.remove_scroll_widgets()
        if self.profile:
            device_ids = self.profile.get_devices()
            for device_id in device_ids:
                self.add_device_wdg(
                    self.profile.get_device(device_id))

    def add_device_wdg(self, device:Device):
        print("DEVICE", type(device.id))
        print(device.id)
        widget = DeviceHeader(
            main=self.main, device=device
        )
        self.scroll_layout.add_widget(widget)


class DeviceHeaderView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = self.ids.label


class DeviceHeader(DeviceHeaderView):
    def __init__(self, main, device: Device, **kwargs):
        super().__init__(**kwargs)
        self.main = main
        self.device = device
        self.label.text = device.id



class CorrespondenceHeaderView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = self.ids.label


class CorrespondenceHeader(CorrespondenceHeaderView):
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


class SideBarView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scroll_view = self.ids.scroll_view

        self.scroll_layout = self.ids.scroll_layout
        self.my_profile_btn = self.ids.my_profile_btn
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

    def add_correspondence_header(self, correspondence):
        widget = CorrespondenceHeader(
            main=self.main, correspondence=correspondence
        )
        self.scroll_layout.add_widget(widget)
