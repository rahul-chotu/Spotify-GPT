import logging
import datetime
import os

from setup import Setup

config = Setup()


class Logger:
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

    def __init__(self, logger_name: str, log_to_console=True, log_to_file=True):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')

        if log_to_file:
            file_path = config.LOG_PATH
            file_handler = logging.FileHandler(f"{file_path}\\application_log {current_time}.log", encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def log(self, log_type: str, message: str):

        match log_type:
            case "debug":
                self.logger.debug(f"{message}")

            case "info":
                self.logger.info(f"{message}")

            case "warning":
                self.logger.warning(f"{message}")

            case "error":
                self.logger.error(f"{message}")

    def clear_logs(self, log_path: str = Setup.LOG_PATH) -> None:
        try:
            for filename in os.listdir(log_path):
                file_path = os.path.join(log_path, filename)
                os.remove(file_path)
        except PermissionError:
            pass

        return self.log("debug", "Cleared log folder")
