import os
import customtkinter as ctk

from PIL import Image
from threading import Thread

from packages.utilities.logger import Logger
from packages.gui.settings.settings import SettingsWindow
from packages.utilities.file_handler import FileHandler
from packages.utilities.manager import Manager, WidgetManager
from setup import Setup


logger = Logger("sidepanel")
config = Setup()
file_handler = FileHandler()


class SidebarFrame(ctk.CTkFrame):
    def __init__(self, master, main_frame):
        super().__init__(master)

        self.master = master
        self.main_frame = main_frame

        # set state of button to 'not pushed' when application run
        self.if_button_pushed = ctk.BooleanVar()
        self.if_button_pushed.set(False)

        # load image for explorer button
        self.explorer_image = ctk.CTkImage(dark_image=Image.open(config.EXPLORER_IMAGE),
                                           light_image=Image.open(config.EXPLORER_IMAGE),
                                           size=(20, 20))

        # configure grid
        self.configure(self.master, width=190, height=600, corner_radius=0)
        self.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        # ---OPTION MENU---
        self.dropdown_values = ["Top Songs", "Recent Songs", "Playlist"]
        self.option_menu = ctk.CTkOptionMenu(self,
                                             values=self.dropdown_values,
                                             font=("Verdana", 12),
                                             command=self.if_playlist)

        self.option_menu.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))

        # ---SONG SLIDER---
        self.song_slider = ctk.CTkSlider(self,
                                         width=140,
                                         from_=5,
                                         to=50,
                                         number_of_steps=9,
                                         command=self.update_song_number_label)

        self.song_slider.grid(row=2, column=0, columnspan=2, padx=(20, 20), pady=(0, 20), sticky="nsew")
        self.song_slider.set(10)

        # ---RESULT SLIDER---
        self.results_slider = ctk.CTkSlider(self,
                                            width=140,
                                            from_=3,
                                            to=10,
                                            number_of_steps=7,
                                            command=self.update_result_number_label)

        self.results_slider.grid(row=4, column=0, columnspan=2, padx=(20, 20), pady=(0, 20), sticky="nsew")
        self.results_slider.set(5)

        # ---RESULT SLIDER LABEL---
        self.result_slider_value = ctk.IntVar()
        self.result_slider_value.set(5)
        self.result_slider_label = ctk.CTkLabel(self,
                                                text=f"Number of results: {self.get_result_number()}",
                                                font=("Verdana", 12))

        self.result_slider_label.grid(row=3, column=0, columnspan=2, pady=(10, 5), sticky="nsew")

        # ---SONG SLIDER LABEL---
        self.song_slider_value = ctk.IntVar()
        self.song_slider_value.set(10)
        self.song_slider_label = ctk.CTkLabel(self,
                                              text=f"Number of songs: {self.get_song_number()}",
                                              font=("Verdana", 12))
        self.song_slider_label.grid(row=1, column=0, columnspan=2, pady=(10, 5), sticky="nsew")

        # ---MAIN BUTTON---
        self.main_button = ctk.CTkButton(self,
                                         text="Generate",
                                         font=("Verdana", 14),
                                         command=lambda: Thread(target=self.button_pushed).start())

        self.main_button.grid(row=7, column=0, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # ---SETTINGS BUTTON---
        self.settings_button = ctk.CTkButton(self,
                                             text="Settings",
                                             font=("Verdana", 14),
                                             fg_color="transparent",
                                             border_width=1,
                                             text_color=("#3d3d3d", "#dedcdc"),
                                             border_spacing=0,
                                             command=self.open_settings)
        self.settings_button.grid(row=8, column=0, columnspan=2, padx=(20, 20), pady=(0, 20), sticky="nsew")

        self.settings_window = None

    def button_pushed(self) -> None:
        selection = self.dropdown_selection()
        song_number = self.get_song_number()
        result_number = self.get_result_number()

        values = {
            "song_number": song_number,
            "result_number": result_number,
            "selection": selection,
            "dropdown_values": self.dropdown_values
        }

        manager = Manager()
        track_data = manager.get_results(values)
        widget_manager = WidgetManager(self.main_frame, track_data)
        widget_manager.update_main_frame()

        music_list = None

        self.if_button_pushed.set(True)
        self.main_button.configure(text="Reload")
        self.main_button.grid(row=7, column=0, columnspan=2, padx=(20, 20), pady=(10, 20), sticky="nsew")

    def open_settings(self) -> None:
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self)
            self.settings_window.attributes("-topmost", True)
            self.settings_window.grab_set()
        else:
            self.settings_window.focus()

    def get_song_number(self) -> int:
        value = int(self.song_slider.get())
        self.song_slider_value.set(value)
        song_number = self.song_slider_value.get()

        return song_number

    def get_result_number(self) -> int:
        value = int(self.results_slider.get())
        self.result_slider_value.set(value)
        result_number = self.result_slider_value.get()

        return result_number

    def dropdown_selection(self, *args) -> str:
        dropdown_selection = self.option_menu.get()

        return dropdown_selection

    def update_result_number_label(self, _) -> None:
        result_number = self.get_result_number()
        self.result_slider_label.configure(text=f"Number of results: {result_number}")

    def update_song_number_label(self, _) -> None:
        song_number = self.get_song_number()
        self.song_slider_label.configure(text=f"Number of songs: {song_number}")

    def if_playlist(self, _) -> None:
        dropdown_selection = self.dropdown_selection()

        if dropdown_selection == self.dropdown_values[2]:
            self.main_button.configure(text="Open Spotify")

            self.song_slider.grid_forget()
            self.song_slider_label.grid_forget()

        else:
            # checks if button has been pushed
            if self.if_button_pushed.get():
                self.main_button.configure(text="Reload")  # if button pushed, set text to 'Reload'
            else:
                self.main_button.configure(text="Generate")  # if button not pushed, set text to 'Generate'

            self.song_slider.grid(row=2, column=0, columnspan=2, padx=(20, 20), pady=(0, 20), sticky="nsew")
            self.song_slider_label.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="nsew")
