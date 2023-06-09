import customtkinter as ctk
import requests

from PIL import Image
from io import BytesIO

from packages.spotify.spotify_api import SpotifyAPI
from packages.utilities.logger import Logger
from setup import Setup

config = Setup()
logger = Logger("song_frame")


class SongFrame(ctk.CTkFrame):
    def __init__(self, master, track_data: dict):
        super().__init__(master)

        self.master = master

        # unpack track data dict
        self.name = track_data["name"]
        self.track_id = track_data["track_id"]
        self.artist = track_data["artist"]
        self.image_url = track_data["image_url"]
        self.preview_url = track_data["preview_url"]

        self.configure(width=650, height=105)

        # noinspection PyTypeChecker
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.grid_propagate(False)

        response = requests.get(self.image_url)
        image_data = response.content
        song_image = Image.open(BytesIO(image_data))
        original_width, original_height = song_image.size
        new_width, new_height = int(original_width / 6.5), int(original_height / 6.5)
        ctk_image = ctk.CTkImage(song_image, size=(new_width, new_height))

        self.play_btn = ctk.CTkImage(dark_image=Image.open(config.PLAY_BTN_IMAGE),
                                     light_image=Image.open(config.PLAY_BTN_IMAGE),
                                     size=(40, 40))

        self.add_btn = ctk.CTkImage(dark_image=Image.open(config.ADD_BTN_IMAGE),
                                    light_image=Image.open(config.ADD_BTN_IMAGE),
                                    size=(40, 40))

        self.image_label = ctk.CTkLabel(self, text="", image=ctk_image)
        self.image_label.place(x=5, y=3)

        self.title_label = ctk.CTkLabel(self,
                                        text=self.name,
                                        fg_color="gray30",
                                        corner_radius=5,
                                        wraplength=370,
                                        justify="left",
                                        font=("Verdana", 16, "bold"),
                                        anchor="w")
        self.title_label.place(x=115, y=10)

        self.artist_label = ctk.CTkLabel(self, text=self.artist, fg_color="gray30", corner_radius=5)
        self.artist_label.place(x=115, y=50)

        self.play_button = ctk.CTkButton(self,
                                         text="",
                                         image=self.play_btn,
                                         fg_color="transparent",
                                         height=40,
                                         width=40,
                                         command=self.play_button_push)
        self.play_button.place(x=500, y=35)

        self.add_button = ctk.CTkButton(self,
                                        text="",
                                        image=self.add_btn,
                                        fg_color="transparent",
                                        height=40,
                                        width=40,
                                        command=self.add_to_saved)
        self.add_button.place(x=570, y=35)

        logger.log("debug", f"Result displayed: {self.name} by {self.artist}")

    def play_button_push(self) -> None:
        self.master.open_player(self.name, self.image_url, self.preview_url)

    def add_to_saved(self):
        spotify = SpotifyAPI()
        spotify.add_track(self.track_id)
