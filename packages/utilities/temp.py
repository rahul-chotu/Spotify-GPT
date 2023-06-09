import tempfile as tf

from packages.utilities.logger import Logger

logger = Logger("temp")


class TempDir:
    def __init__(self):
        self.temp_dir = None

    def create_dir(self):
        self.temp_dir = tf.TemporaryDirectory()
        logger.log("debug", f"Temporary directory created: {self.temp_dir.name}")

        return self.temp_dir

    def close_dir(self):
        logger.log("debug", f"Temporary directory closed")

        return self.temp_dir.cleanup()
