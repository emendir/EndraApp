
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import os
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
# Load the KV file
KV_FILE = os.path.join(os.path.dirname(__file__), "utils.kv")
Builder.load_file(KV_FILE)



class InvitationView(BoxLayout):
    """Box layout containing QR code & label with clipboard interactivity."""
    def __init__(self, invitation_code:str, **kwargs):
        super().__init__(**kwargs)
        self.qr_code = self.ids.qr_code
        self.text_lbl = self.ids.text_lbl
        self.invitation_code = invitation_code

        self.qr_code.data = self.invitation_code
        self.copy_to_clipboard()
        # Add click event listener to text_lbl
        self.text_lbl.bind(on_touch_down=self.copy_to_clipboard)
        self.qr_code.bind(on_touch_down=self.copy_to_clipboard)
        

    def copy_to_clipboard(self, *args, **kwargs):
        Clipboard.copy(self.qr_code.data)  # Copy text to clipboard
        return True  # Indicate that the event was handled

class InvitationPopupView(Popup):
    """Popup window containing InvitationView"""
    def __init__(self, invitation_code: str, title:str, **kwargs):
        super().__init__(**kwargs)
        self.layout = self.ids.layout
        self.title=title
        # self.invitation_view = self.ids.invitation_view
        self.invitation_view = InvitationView(invitation_code)
        self.layout.add_widget(self.invitation_view, 1)
        