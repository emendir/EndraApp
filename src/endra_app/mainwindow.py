from . import config
import walytis_beta_embedded
from loguru import logger
import tempfile
from datetime import datetime
from walidentity.did_objects import Key
from endra import Profile
import shutil
from walidentity.did_manager import blockchain_id_from_did
from .chat_page import MessagePage
from .side_bar import SideBar
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from . import _load_kivy  # IMPORTANT: import this before importing kivy
from .config import APPDATA_DIR
import os
print("mainwindow.py")

print("Imported components.")

CRYPTO_FAMILY = "EC-secp256k1"
TEMP_HARDCODED_KEY = Key(
    family=CRYPTO_FAMILY,
    public_key=b'\x04\xa6#\x1a\xcf\xa7\xbe\xa8\xbf\xd9\x7fd\xa7\xab\xba\xeb{Wj\xe2\x8fH\x08*J\xda\xebS\x94\x06\xc9\x02\x8c9>\xf45\xd3=Zg\x92M\x84\xb3\xc2\xf2\xf4\xe6\xa8\xf9i\x82\xdb\xd8\x82_\xcaIT\x14\x9cA\xd3\xe1',
    private_key=b'\xd9\xd1\\D\x80\xd7\x1a\xe6E\x0bt\xdf\xd0z\x88\xeaQ\xe8\x04\x91\x11\xaf\\%wC\x83~\x0eGP\xd8',
    creation_time=datetime(2024, 11, 6, 19, 17, 45, 713000)
)


class MainApp(App):
    def build(self):
        print("MainApp.build()")
        if not config.USE_BRENTHY:
            walytis_beta_embedded.run_blockchains()

        self.profiles_dir = os.path.join(APPDATA_DIR, "Profiles")
        # Root layout
        root = BoxLayout(orientation='horizontal')
        self.profiles = self.load_profiles()
        self.profile: Profile | None = None

        if not len(self.profiles):
            self.create_profile()
        if len(self.profiles):
            print(len(self.profiles))
            self.profile = list(self.profiles.values())[0]
        # Add side-bar and central page
        self.side_bar = SideBar(self, self.profile)
        self.chat_page = MessagePage(self, None)
        if self.profile:
            correspondences = self.profile.get_active_correspondences()
            if len(correspondences) > 0:
                self.chat_page.load_correspondence(
                    self.profile.get_correspondence(list(correspondences)[0]))

        root.add_widget(self.side_bar)
        root.add_widget(self.chat_page)

        print("MianApp.build")
        return root

    def load_profiles(self) -> dict[Profile]:
        logger.debug("Loading profiles...")

        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)
        profiles: dict[Profile] = dict()
        for dirname in os.listdir(self.profiles_dir):
            profile = Profile.load(
                os.path.join(self.profiles_dir, dirname), TEMP_HARDCODED_KEY
            )
            profiles.update({profile.did: profile})
        return profiles

    def get_profile_ids(self) -> set[str]:
        return set(self.profiles.keys())

    def create_profile(self) -> Profile:
        logger.debug("Creating profile...")
        tempdir = tempfile.mkdtemp()
        profile = Profile.create(tempdir, TEMP_HARDCODED_KEY, auto_run=False)

        profile.terminate()
        target_dir = os.path.join(
            self.profiles_dir, blockchain_id_from_did(profile.did))
        shutil.move(tempdir, target_dir)

        profile = Profile.load(target_dir, TEMP_HARDCODED_KEY)
        self.profiles.update({profile.did: profile})
        return profile

    def join_profile(self, invitation: str) -> Profile:
        """
        Args:
            invitation: 
        Returns:
            Profile:
        Raises:
            JoinFailureError: 
        """
        logger.debug("Joining profile...")

        tempdir = tempfile.mkdtemp()
        profile = Profile.join(
            invitation, tempdir, TEMP_HARDCODED_KEY, auto_run=False
        )
        logger.debug("Joined profile.")

        profile.terminate()
        logger.debug("Terminated profile.")
        target_dir = os.path.join(
            self.profiles_dir, blockchain_id_from_did(profile.did))
        shutil.move(tempdir, target_dir)
        logger.debug("Joining profile: migrated tempfile.")

        profile = Profile.load(target_dir, TEMP_HARDCODED_KEY)
        self.profiles.update({profile.did: profile})
        return profile

    def switch_profile(self, profile_id: Profile | str):
        if isinstance(profile_id, Profile):
            profile_id = profile_id.did

        if profile_id == self.profile.did:
            return
        print(f"Switching profile to: {profile_id}")
        self.profile = self.profiles[profile_id]
        self.side_bar.switch_profile(self.profile)
        self.chat_page.reset()
        correspondences = self.profile.get_active_correspondences()
        if len(correspondences) > 0:
            self.chat_page.load_correspondence(
                self.profile.get_correspondence(list(correspondences)[0]))

    def on_stop(self, *args):
        logger.debug("Mainwindow: Shutting down...")
        for profile in self.profiles.values():
            profile.terminate()
        
        if not config.USE_BRENTHY:
            logger.debug("Mainwindow: Terminating Wwalytis_beta_embedded!")
            walytis_beta_embedded.terminate()
        logger.debug("Mainwindow: Closed!")


def run():
    print("mainwindow.run()")
    MainApp().run()


if __name__ == '__main__':
    print(f"USING_PANGO: {_load_kivy.USING_PANGO}")
    run()
