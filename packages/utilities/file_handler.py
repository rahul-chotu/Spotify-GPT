import json

from packages.utilities.logger import Logger
from setup import Setup

logger = Logger("files")
config = Setup()


class FileHandler:
    def __init__(self):
        self.settings_path = config.SETTINGS_PATH
        self.settings = None

    def open_settings(self) -> dict:
        """Returns settings file"""

        with open(self.settings_path, "r") as settings_file:
            self.settings = json.load(settings_file)

        return self.settings

    def update_settings(self, new_settings: dict) -> None:
        """Update settings file"""

        with open(self.settings_path, "w") as settings_file:
            json.dump(new_settings, settings_file, indent=4)

        return logger.log("debug", "Settings file updated")
