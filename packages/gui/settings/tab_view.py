import customtkinter as ctk

from PIL import Image
from os import path

from packages.utilities.file_handler import FileHandler
from setup import Setup

config = Setup()
file_handler = FileHandler()
settings = file_handler.open_settings()


class TabView(ctk.CTkTabview):
    def __init__(self, master):
        super().__init__(master)

        # create tabs
        self.add("Theme")
        self.add("Spotify")

        self.purple_theme = path.join(config.THEME_PATH, "purple.json")

        self.image = ctk.CTkImage(dark_image=Image.open(config.EXPLORER_IMAGE),
                                  light_image=Image.open(config.EXPLORER_IMAGE),
                                  size=(20, 20))

        # -----Spotify Tab Widgets-----
        time_range = settings["default_values"]["spotipy"]["top_songs"]["time_range"]

        time_range_location_label = ctk.CTkLabel(self.tab("Spotify"), text="Time Range:")
        time_range_location_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.time_range = ctk.CTkOptionMenu(self.tab("Spotify"),
                                            values=["Short Term", "Medium Term", "Long Term"],
                                            command=self.choose_time_range)
        self.time_range.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        if time_range == "short_term":
            self.time_range.set("Short Term")
        elif time_range == "medium_term":
            self.time_range.set("Medium Term")
        elif time_range == "long_term":
            self.time_range.set("Long Term")

        # -----Theme Tab Widgets-----

        appearance_mode = settings["gui"]["appearance_mode"]

        appearance_label = ctk.CTkLabel(self.tab("Theme"), text="Appearance Mode:")
        appearance_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.dark_button = ctk.CTkRadioButton(self.tab("Theme"), text="Dark", command=self.set_dark_mode)
        self.dark_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.light_button = ctk.CTkRadioButton(self.tab("Theme"), text="Light", command=self.set_light_mode)
        self.light_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        if appearance_mode == "Dark":
            self.dark_button.select()
            if self.light_button:
                self.light_button.deselect()

        elif appearance_mode == "Light":
            self.light_button.select()
            if self.dark_button:
                self.dark_button.deselect()

        theme = settings["gui"]["theme"]

        theme_label = ctk.CTkLabel(self.tab("Theme"), text="Theme:")
        theme_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.theme_option_menu = ctk.CTkOptionMenu(self.tab("Theme"),
                                                   values=["Dark Blue", "Blue", "Green", "Purple"],
                                                   command=self.choose_theme)
        self.theme_option_menu.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="w")

        match theme:
            case "dark-blue":
                self.theme_option_menu.set("Dark Blue")
            case "blue":
                self.theme_option_menu.set("Blue")
            case "green":
                self.theme_option_menu.set("Green")
            case self.purple_theme:
                self.theme_option_menu.set("Purple")

    def choose_time_range(self, _) -> None:
        time_range = self.time_range.get()
        settings["default_values"]["spotipy"]["top_songs"]["time_range"] = time_range

        return file_handler.update_settings(settings)

    def choose_theme(self, _) -> None:
        theme = self.theme_option_menu.get()

        match theme:
            case "Dark Blue":
                settings["gui"]["theme"] = "dark-blue"
            case "Blue":
                settings["gui"]["theme"] = "blue"
            case "Green":
                settings["gui"]["theme"] = "green"
            case "Purple":
                settings["gui"]["theme"] = self.purple_theme

        return file_handler.update_settings(settings)

    def set_dark_mode(self) -> None:
        ctk.set_appearance_mode("Dark")
        settings["gui"]["appearance_mode"] = "Dark"

        if self.light_button:
            self.light_button.deselect()

        return file_handler.update_settings(settings)

    def set_light_mode(self) -> None:
        ctk.set_appearance_mode("Light")
        settings["gui"]["appearance_mode"] = "Light"

        if self.dark_button:
            self.dark_button.deselect()

        return file_handler.update_settings(settings)
