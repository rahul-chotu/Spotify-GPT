import customtkinter as ctk
import requests

from PIL import Image
from io import BytesIO
from threading import Thread

from setup import Setup
from packages.utilities.player_engine import PlayerEngine, EngineState
from packages.utilities.logger import Logger

logger = Logger("player")
config = Setup()


class Player(ctk.CTkFrame):
    def __init__(self, master, name: str, image_url: str, preview_url: str, temp_dir):
        super().__init__(master)

        self.pos_x = -100
        self.start_pos = -200
        self.end_pos = 5

        self.master = master
        self.configure(width=180, height=200, fg_color="#333333", corner_radius=15)
        self.grid_propagate(False)

        self.name = name
        self.image_url = image_url
        self.preview_url = preview_url
        self.temp_dir = temp_dir

        logger.log("info", f"Player opened: {self.name}")

        response = requests.get(self.image_url)
        image_data = response.content
        song_image = Image.open(BytesIO(image_data))
        original_width, original_height = song_image.size
        new_width, new_height = int(original_width / 6.4), int(original_height / 6.4)
        ctk_image = ctk.CTkImage(song_image, size=(new_width, new_height))

        self.play_btn_img = ctk.CTkImage(dark_image=Image.open(config.PLAY_BTN_IMAGE),
                                         light_image=Image.open(config.PLAY_BTN_IMAGE),
                                         size=(20, 20))

        self.pause_btn_img = ctk.CTkImage(dark_image=Image.open(config.PAUSE_BTN_IMAGE),
                                          light_image=Image.open(config.PAUSE_BTN_IMAGE),
                                          size=(20, 20))

        self.image_label = ctk.CTkLabel(self, text="", image=ctk_image)
        self.image_label.place(x=40, y=5)

        self.title_label = ctk.CTkLabel(self,
                                        text=self.name,
                                        corner_radius=5,
                                        width=60,
                                        font=("Verdana", 10),
                                        fg_color="#262626",
                                        anchor="w")
        self.title_label.place(x=20, y=115)

        if len(self.name) >= 16:
            short_name = self.name[0:16]
            new_name = short_name + "..."
            self.title_label.configure(text=new_name)
        else:
            self.title_label.place(x=40, y=115)

        # self.progress_bar = ctk.CTkProgressBar(self, width=100)
        # self.progress_bar.place(x=40, y=150)
        # self.progress_bar.set(0.7)

        self.vol_slider = ctk.CTkSlider(self, width=100,
                                        from_=0,
                                        to=1,
                                        number_of_steps=100,
                                        command=self.update_volume)
        self.vol_slider.place(x=40, y=150)
        self.vol_slider.set(EngineState.VOLUME)

        self.play_button = ctk.CTkButton(self,
                                         text="",
                                         image=self.play_btn_img,
                                         fg_color="transparent",
                                         height=20,
                                         width=20,
                                         command=self.resume_playback)
        # self.play_button.place(x=70, y=160)

        self.pause_button = ctk.CTkButton(self,
                                          text="",
                                          image=self.pause_btn_img,
                                          fg_color="transparent",
                                          height=20,
                                          width=20,
                                          command=self.pause_playback)
        self.pause_button.place(x=70, y=165)

        self.close_button = ctk.CTkButton(self,
                                          text="X",
                                          fg_color="transparent",
                                          height=5,
                                          width=5,
                                          command=self.animate_close)
        self.close_button.place(x=160, y=5)

        self.engine = PlayerEngine(self.preview_url, self.name, self.temp_dir)

        PlayerState.PLAYER_OPEN = True

    def start_playback(self):
        return Thread(target=self.engine.start_playback).start()

    def pause_playback(self) -> None:
        self.pause_button.place_forget()
        self.play_button.place(x=70, y=165)

        return self.engine.pause_playback()

    def resume_playback(self) -> None:
        self.play_button.place_forget()
        self.pause_button.place(x=70, y=165)

        return Thread(target=self.engine.resume_playback).start()

    def update_volume(self, _):
        volume = self.vol_slider.get()

        return self.engine.update_volume(volume)

    def animate_open(self) -> None:
        self.place(x=self.pos_x, y=220)
        if self.pos_x < self.end_pos:
            self.pos_x += 1
            self.after(1, self.animate_open)

    def animate_close(self) -> None:
        self.place(x=self.pos_x, y=220)

        if self.pos_x > self.start_pos:
            self.pos_x -= 1
            self.after(1, self.animate_close)
        elif self.pos_x == self.start_pos:
            self.engine.stop_playback()
            logger.log("info", "Player closed")
            PlayerState.PLAYER_OPEN = False
            self.destroy()


class PlayerState:
    PLAYER_OPEN = False
