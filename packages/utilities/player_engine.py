import wget
import os
import pygame

from mutagen.mp3 import MP3

from packages.utilities.logger import Logger

logger = Logger("player_engine")


class PlayerEngine:
    def __init__(self, preview_url: str, name: str, temp_dir):
        self.preview_url = preview_url
        self.name = name
        self.temp_dir = temp_dir

        self.downloaded = False
        self.current_playback = 0
        self.length = None
        self.preview_file = None

        self.output_path = os.path.join(self.temp_dir.name, f"{self.name}.mp3")

        # initialize pygame player
        pygame.init()
        pygame.mixer.init()

    def start_playback(self) -> None:
        # download preview file if it's not already downloaded
        if not os.path.exists(self.output_path):
            self.preview_file = wget.download(self.preview_url, out=self.output_path)
            logger.log("debug", "mp3 download started")

        # wait until file downloaded
        while not self.downloaded:
            if os.path.exists(self.output_path):
                self.downloaded = True
                logger.log("debug", "mp3 download complete")

        # load preview file
        pygame.mixer.music.load(self.output_path)

        # get mp3 length
        audio = MP3(self.output_path)
        self.length = round(audio.info.length)

        # start
        pygame.mixer.music.set_volume(EngineState.VOLUME)
        pygame.mixer.music.play()
        EngineState.PLAYING = True
        logger.log("debug", "Playback started")

        # while playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
            self.current_playback += 1

        if self.current_playback >= self.length:
            self.stop_playback()

    @staticmethod
    def pause_playback() -> None:
        pygame.mixer.music.pause()
        logger.log("debug", "Playback paused")

    def resume_playback(self) -> None:
        pygame.mixer.music.unpause()
        EngineState.PLAYING = True
        logger.log("debug", "Playback unpaused")

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
            self.current_playback += 1
            EngineState.CURRENT_PLAYBACK += 1

        if self.current_playback >= self.length:
            self.stop_playback()

    @staticmethod
    def update_volume(volume: float) -> None:
        EngineState.VOLUME = volume

        return pygame.mixer.music.set_volume(volume)

    @staticmethod
    def stop_playback() -> None:
        pygame.mixer.music.stop()

        # unload preview file
        pygame.mixer.music.unload()

        EngineState.PLAYING = False

        return logger.log("debug", "Playback stopped")


class EngineState:
    CURRENT_PLAYBACK = 0
    PLAYING = False
    VOLUME = 0.5
