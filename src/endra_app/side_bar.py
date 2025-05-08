# side_bar.py
from threading import Thread
from time import sleep
from enum import Enum
from .profiles import Profiles
from .settings import ProfileSettingsPopup
from walytis_beta_tools.exceptions import JoinFailureError
import json
from loguru import logger
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from endra import Profile, Correspondence
import os
from kivy.uix.popup import Popup
from kivy.clock import Clock

# Load the KV file
KV_FILE = os.path.join(os.path.dirname(__file__), "side_bar.kv")
Builder.load_file(KV_FILE)


class AddCorrespondencePopupView(Popup):
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.text_input_txbx = self.ids.text_input_txbx
        self.join_conv_btn = self.ids.join_conv_btn
        self.create_conv_btn = self.ids.create_conv_btn
        self.scroll_view = self.ids.scroll_view
        self.scroll_layout = self.ids.scroll_layout


class AddCorrespondencePopup(AddCorrespondencePopupView):
    def __init__(self,  main, profile: Profile, **kwargs):
        super().__init__(**kwargs)
        self.main = main
        self.profile = profile
        self.join_conv_btn.bind(on_press=self.join_correspondence)
        self.create_conv_btn.bind(on_press=self.create_correspondence)

    def create_correspondence(self, instance=None):
        task = CreateCorrespondenceTask(
            self.main, self.profile, self)
        self.scroll_layout.add_widget(task, 0)

    def join_correspondence(self, *args, **kwargs):
        try:
            invitation = json.loads(self.text_input_txbx.text)
        except json.JSONDecodeError:
            self.text_input_txbx.hint_text = "Invalid Invitation code.\nPaste invitation code here."
            return
        task = JoinCorrespondenceTask(
            self.main, self.profile, invitation, self)
        self.scroll_layout.add_widget(task, 0)
        # try:
        #     invitation = json.loads(self.text_input_txbx.text)
        #     correspondence = self.profile.join_correspondence(invitation)
        # except json.JSONDecodeError:
        #     self.text_input_txbx.hint_text = "Invalid Invitation code.\nPaste invitation code here."
        #     return
        # except JoinFailureError:
        #     self.join_conv_btn.hint_text = "Try again\n(join attampt failed)"
        #     return
        #
        # self.main.side_bar.reload_correspondences()
        # self.main.chat_page.load_correspondence(correspondence)
        #
        # self.dismiss()


class TaskStatus(Enum):
    initialising = 0
    in_progress = 1
    succeeded = 2
    error = 3


class TaskItemView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = self.ids.label


class TaskItem(TaskItemView):
    task_description = "Generic Task"
    def __init__(
        self,
        main,
        profile: Profile,
        popup_window: AddCorrespondencePopup | None = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._terminate = False
        self.main = main
        self.profile = profile
        self.popup_window = popup_window
        self.status = TaskStatus.initialising
        self.task_thread = Thread(target=self.run_task)
        self.task_thread.start()

    def update_status(self, status: TaskStatus):
        self.status = status
        self.label.text = f"{self.task_description}: {status.name}"

    def terminate(self):
        self._terminate = True


class CreateCorrespondenceTask(TaskItem):
    task_description = "Create Correspondence"
    def __init__(
        self,
        main,
        profile: Profile,
        popup_window: AddCorrespondencePopup | None = None,
        **kwargs
    ):
        super().__init__(
            main=main,
            profile=profile,
            popup_window=popup_window,
        )
        self.task_thread = Thread(target=self.run_task)
        self.task_thread.start()

    def run_task(self):
        self.update_status(TaskStatus.in_progress)
        try:
            logger.info("Creating correspondence...")
            correspondence = self.profile.create_correspondence()
            logger.info("Created correspondence!")
            self.update_status(TaskStatus.succeeded)
        except Exception as e:
            error_message = (
                f"{e}\n"
                "CreateCorrespondenceTask: error running task"
            )
            logger.error(error_message)
            self.update_status(TaskStatus.error)
            return
        Clock.schedule_once(lambda dt:self.main.side_bar.reload_correspondences())
        
        if self.popup_window and self.popup_window._is_open:
            Clock.schedule_once(lambda dt:self.main.chat_page.load_correspondence(correspondence))
            self.popup_window.dismiss()
class JoinCorrespondenceTask(TaskItem):
    task_description = "Join Correspondence"
    def __init__(
        self,
        main,
        profile: Profile,
        invitation: str,
        
        popup_window: AddCorrespondencePopup | None = None,
        **kwargs
    ):
        super().__init__(
            main=main,
            profile=profile,
            popup_window=popup_window,
        )
        self.invitation: str = invitation
        
        self.task_thread = Thread(target=self.run_task)
        self.task_thread.start()

    def run_task(self):
        self.update_status(TaskStatus.in_progress)
        while not self._terminate:
            try:
                logger.debug("JoinCorrespondenceTask: joining...")
                correspondence = self.profile.join_correspondence(self.invitation)
                self.update_status(TaskStatus.succeeded)
                break
            except JoinFailureError:
                pass
            except Exception as e:
                error_message = (
                    f"{e}\n"
                    "JoinCorrespondenceTask: error running task"
                )
                import traceback
                traceback.print_exc()
                logger.error(error_message)
                self.update_status(TaskStatus.error)
                return
            sleep(1)

        Clock.schedule_once(lambda dt:self.main.side_bar.reload_correspondences())
        
        if self.popup_window and self.popup_window._is_open:
            Clock.schedule_once(lambda dt:self.main.chat_page.load_correspondence(correspondence))
            self.popup_window.dismiss()

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
        self.switch_profile(profile)

    def switch_profile(self, profile: Profile):

        self.profile = profile

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
        popup = AddCorrespondencePopup(
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
