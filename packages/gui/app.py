import customtkinter as ctk

from packages.gui.main_frame import MainFrame
from packages.gui.side_panel import SidebarFrame
from packages.utilities.logger import Logger
from packages.utilities.file_handler import FileHandler
from packages.gui.player import Player, PlayerState
from packages.utilities.player_engine import EngineState, PlayerEngine
from packages.utilities.temp import TempDir
from setup import Setup


logger = Logger("app")
config = Setup()

file_handler = FileHandler()
settings = file_handler.open_settings()

appearance_mode = settings["gui"]["appearance_mode"]
custom_theme = settings["gui"]["theme"]

ctk.set_appearance_mode(appearance_mode)  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme(custom_theme)  # Themes: "blue", "green", "dark-blue"


# noinspection PyTypeChecker
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # window setup
        self.title(f"{config.NAME} v{config.VERSION}")
        self.geometry(f"{900}x{600}")
        self.resizable(False, False)
        self.iconbitmap(config.ICON)  # set icon image

        # configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create widgets
        self.main_frame = MainFrame(master=self)
        self.sidebar_frame = SidebarFrame(self, self.main_frame)

        logger.log("info", "Main window loaded")

        # create temporary dir
        self.temporary_directory = TempDir()
        self.temp_dir = self.temporary_directory.create_dir()

        # on application close
        self.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def on_window_close(self) -> None:
        # stop playback before exiting
        if EngineState.PLAYING:
            PlayerEngine.stop_playback()

        # close temp dir
        self.temporary_directory.close_dir()

        logger.log("info", "Application closed")

        return self.quit()

    def open_player(self, name: str, image_url: str, preview_url: str) -> None:
        if not PlayerState.PLAYER_OPEN:
            player = Player(self.sidebar_frame, name, image_url, preview_url, self.temp_dir)
            player.animate_open()
            player.start_playback()
