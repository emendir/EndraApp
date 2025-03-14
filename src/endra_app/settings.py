# side_bar.py
from endra import Device
from .utils import InvitationPopupView
import json
from loguru import logger
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from endra import Profile
import os
from kivy.uix.popup import Popup
# Load the KV file
KV_FILE = os.path.join(os.path.dirname(__file__), "settings.kv")
Builder.load_file(KV_FILE)


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
        popup = InvitationPopupView(
            invitation_code=invitation_str,
            title="New Device Invitation"
        )
        popup.open()

    def reload_devices(self):
        logger.info("Reloading devices...")

        self.remove_scroll_widgets()
        if self.profile:
            device_ids = self.profile.get_devices()
            for device_id in device_ids:
                self.add_device_wdg(
                    self.profile.get_device(device_id))

    def add_device_wdg(self, device: Device):
        print("DEVICE", type(device.id))
        print(device.id)
        widget = DeviceItem(
            main=self.main, device=device
        )
        self.scroll_layout.add_widget(widget)


class DeviceItemView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = self.ids.label


class DeviceItem(DeviceItemView):
    def __init__(self, main, device: Device, **kwargs):
        super().__init__(**kwargs)
        self.main = main
        self.device = device
        self.label.text = device.id
