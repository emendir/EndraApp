# side_bar.py
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from plyer import filechooser
from enum import Enum
from kivy.clock import Clock
import json
from .log import logger_endra as logger
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from endra import (
    Message,
    Correspondence,
)
from endra.message import (
    MessageContent,
    EmbeddedContentPart,
    MessageAttachment,
    AttachedContentPart,
    ReferencedContentPart,
)
import os
from .utils import InvitationPopupView

# Load the KV file
KV_FILE = os.path.join(os.path.dirname(__file__), "chat_page.kv")
Builder.load_file(KV_FILE)


class MediaType(Enum):
    TEXT_MARKDOWN = "text/markdown"
    IMAGE_PNG = "image/png"
    IMAGE_JPG = "image/jpg"


class MessageEditorView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.text_input_txbx = self.ids.text_input_txbx


@dataclass_json
@dataclass
class PendingMessageAttachment:
    file_path: str

    # media type is MIME-compatible
    media_type: str

    # metadata extracted from payload depending on media type,
    # e.g. image width & height, audio or video length, embedded title
    derived_properties: dict
    # metadata defined by user, e.g. filename, title-override
    user_attributes: dict
    rendering_metadata: dict


class MessageEditor(MessageEditorView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pending_attachments: list[PendingMessageAttachment] = []

    def add_attachment_from_paths(self, attachment_paths: list[str]) -> None:
        for attachment_path in attachment_paths:
            filename = os.path.basename(attachment_path)
            media_type = "unknown/unknown"
            if attachment_path.endswith(".jpg"):
                media_type = "image/jpg"
            elif attachment_path.endswith(".png"):
                media_type = "image/png"
            attachment = PendingMessageAttachment(
                file_path=attachment_path,
                media_type=media_type,
                derived_properties={},
                user_attributes={"filename": filename},
                rendering_metadata={},
            )
            self.pending_attachments.append(attachment)

    def get_pending_attachments(self) -> list[PendingMessageAttachment]:
        return self.pending_attachments

    def get_message_content(self):
        return EmbeddedContentPart(
            part_id=0,  # part_id will be automatically adjusted
            media_type=MediaType.TEXT_MARKDOWN.value,
            rendering_metadata={},
            payload=self.text_input_txbx.text.encode(),
        )

    def clear(self) -> None:
        self.text_input_txbx.text = ""
        self.pending_attachments = []


class MessageView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = self.ids.label


class MessageWidget(MessageView):
    def __init__(
        self, message_metadata: dict, content_parts: list[EmbeddedContentPart], **kwargs
    ):
        super().__init__(**kwargs)
        self.message_metadata = message_metadata
        self.content_parts = content_parts
        self.label.text = ""
        for content_part in self.content_parts:
            if content_part.media_type == MediaType.TEXT_MARKDOWN.value:
                self.label.text += content_part.payload.decode()
            else:
                self.label.text += f"\n<{content_part.media_type}>"
                logger.debug(
                    f"Unhandled message part MediaType: {content_part.media_type}"
                )

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
        self.add_attachment_btn = self.ids.add_attachment_btn
        self.invite_btn = self.ids.invite_btn
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter("height"))

        self.message_editor = MessageEditor()
        self.ids.add_message_btn_lyt.add_widget(self.message_editor)

    def deactivate(self):
        self.disabled = True

    def activate(self):
        self.disabled = False

    def remove_widget_from_scroll(self, index):
        if 0 <= index < len(self.scroll_layout.children):
            self.scroll_layout.remove_widget(self.scroll_layout.children[index])

    def remove_all_widgets(self):
        while len(self.scroll_layout.children):
            self.scroll_layout.remove_widget(self.scroll_layout.children[0])


class MessagePage(MessagePageView):
    def __init__(self, main, correspondence: Correspondence | None, **kwargs):
        super().__init__(**kwargs)
        self.deactivate()

        self.main = main
        self.correspondence = correspondence

        self.add_message_btn.bind(on_press=self.create_message)
        self.add_attachment_btn.bind(on_press=self.add_attchment)
        self.invite_btn.bind(on_press=self.create_invitation)
        self.reload_messages()

    def on_message_received(self, message):
        # run self.reload_messages on main kivy thread
        Clock.schedule_once(lambda dt: self.reload_messages())

    def load_correspondence(self, correspondence):
        self.correspondence = correspondence
        # TODO we should define a block received handler outside of the MessagePage
        # self.correspondence.clear_block_received_handler()
        self.correspondence.block_received_handler = self.on_message_received

        self.reload_messages()
        self.activate()

    def reload_messages(self):
        logger.info("Reloading chat messages...")

        self.remove_all_widgets()
        if self.correspondence:
            print("Number of messages:", len(self.correspondence.get_messages()))
            for message in self.correspondence.get_messages():
                # print(message.content.text)
                self.add_widget_to_scroll(message)

    def create_message(self, instance=None):
        logger.info("Creating message...")
        pending_attachments = self.message_editor.get_pending_attachments()
        attachment_parts = []
        for pending_attachment in pending_attachments:
            with open(pending_attachment.file_path, "rb") as file:
                file_data = file.read()
            attachment = MessageAttachment.create(
                media_type=pending_attachment.media_type,
                derived_properties=pending_attachment.derived_properties,
                user_attributes=pending_attachment.user_attributes,
                payload=file_data,
            )
            attachment_block_id = self.correspondence.add_attachment(attachment)
            attachment_parts.append(
                AttachedContentPart(
                    part_id=None,
                    rendering_metadata=pending_attachment.rendering_metadata,
                    attachment_id=attachment_block_id,
                )
            )
        message_text = self.message_editor.get_message_content()
        message_parts = [message_text] + attachment_parts
        message_content = MessageContent(
            message_metadata={},
            message_parts=message_parts,
        )
        self.correspondence.add_message(message_content)
        self.message_editor.clear()
        self.reload_messages()

    def add_attchment(self, instance=None):
        logger.info("Adding attachment...")

        attachment_path = filechooser.open_file()
        self.message_editor.add_attachment_from_paths(attachment_path)
        logger.info(attachment_path)

    def create_invitation(self, instance=None):
        logger.info("Creating invitation...")
        invitation = self.correspondence.create_invitation()
        invitation_str = json.dumps(invitation)
        popup = InvitationPopupView(
            invitation_code=invitation_str, title="Chat Invitation"
        )
        popup.open()

    def add_widget_to_scroll(self, message):
        message_content_parts = self.correspondence.get_message_content_parts(message)
        widget = MessageWidget(
            message_metadata=message.content.message_metadata,
            content_parts=message_content_parts,
        )
        self.scroll_layout.add_widget(widget)

    def reset(self):
        self.remove_all_widgets()
        self.deactivate()
