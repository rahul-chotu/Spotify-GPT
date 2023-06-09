import functools

from packages.spotify.spotify_api import SpotifyAPI
from packages.ai.chatgpt import ChatGPT
from packages.utilities.file_handler import FileHandler
from packages.utilities.logger import Logger
from setup import Setup

config = Setup()
spotify = SpotifyAPI()
file_handler = FileHandler()
logger = Logger("manager")


def mode(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        match config.MODE:
            case "1":
                music_list, result_number = func(*args, **kwargs)
                chatgpt = ChatGPT(music_list, result_number)
                results = chatgpt.get_list()

                return results

            case "2":
                music_list, result_number = func(*args, **kwargs)
                chatgpt = ChatGPT(music_list, result_number)
                results = chatgpt.get_list()
                # Testing -----------------------------------------
                # results = ["5xlLG6RthtyXShVhGA3ojN", "2LNmtYttwHQqRUc7Hbf0bk"]
                track_data = spotify.get_tracks(results)

                return track_data

            case "3":
                music_list, result_number = func(*args, **kwargs)
                chatgpt = ChatGPT(music_list, result_number)
                results = chatgpt.get_list()
                # Testing -----------------------------------------
                # track_ids = ["5xlLG6RthtyXShVhGA3ojN", "2LNmtYttwHQqRUc7Hbf0bk"]
                track_ids = spotify.search(results)
                track_data = spotify.get_tracks(track_ids)

                return track_data

    return wrapper


class Manager:
    @mode
    def get_results(self, values: dict):
        selection = values["selection"]
        dropdown_values = values["dropdown_values"]
        song_number = values["song_number"]
        result_number = values["result_number"]

        match selection:
            case "Top Songs":
                music_list = spotify.get_top_songs(limit=song_number)

                return music_list, result_number

            case "Recent Songs":
                music_list = spotify.get_recently_played(limit=song_number)

                return music_list, result_number

            case "Playlist":
                music_list = spotify.get_playlist_items()

                return music_list, result_number


class WidgetManager:
    def __init__(self, main_frame, track_data: dict):
        self.main_frame = main_frame
        self.track_data = track_data

    def update_main_frame(self) -> None:
        self.main_frame.destroy_text_boxes()

        match config.MODE:
            case "1":
                if self.track_data:
                    for track in self.track_data:
                        self.main_frame.create_textbox(track)

                    logger.log("info", f"Result displayed: {self.track_data}")

            case "2" | "3":
                for track in self.track_data:
                    data = self.track_data[track]
                    self.main_frame.display_result(data)
