import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from urllib3.exceptions import MaxRetryError, ProtocolError

from packages.utilities.logger import Logger
from setup import Setup

config = Setup()
logger = Logger("selenium logger")

username = config.USERNAME
password = config.PASSWORD


class SpotifyPlaylist:
    def __init__(self):
        self.driver_path = config.CHROME_DRIVER_PATH
        self.service = Service(self.driver_path)
        self.driver = None
        self.driver = webdriver.Chrome(service=self.service)
        # Thread(target=self.login).start()

        logger.log("info", "Selenium driver initialized")

        self.login()

    def login(self) -> None:
        if self.driver:

            try:
                self.driver.get("https://www.spotify.com/login/")

                # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located("login-username"))
                username_input = self.driver.find_element(By.ID, 'login-username')
                password_input = self.driver.find_element(By.ID, 'login-password')

                username_input.send_keys(username)
                password_input.send_keys(password)
                password_input.send_keys(Keys.RETURN)

                logger.log("debug", "Login successful")

                WebDriverWait(self.driver, 10).until(ec.url_contains("https://www.spotify.com/mu/account/"))
                self.driver.get("https://www.spotify.com/")

                logger.log("debug", "Home page loaded")

            except selenium.common.exceptions.NoSuchWindowException:
                logger.log("error", "Browser window closed before task completed")

                self.close_browser()

            except ProtocolError:
                logger.log("error", "Connection aborted. An existing connection was forcibly closed by the remote host")

                self.close_browser()

            except Exception as e:
                logger.log("error", f"Login failed - {e}")

                self.close_browser()

    def get_playlist(self) -> str:

        wait_time = 300
        if self.driver:
            try:
                WebDriverWait(self.driver, wait_time).until(ec.url_contains("https://open.spotify.com/playlist/"))

                playlist_url = self.driver.current_url

                logger.log("info", f"Current playlist retrieved: '{playlist_url}'")

                self.close_browser()

                return playlist_url

            except selenium.common.exceptions.TimeoutException:
                logger.log("error", f"Timeout exception. Selection not made within {wait_time}s")

                self.close_browser()

            except selenium.common.exceptions.NoSuchWindowException:
                logger.log("error", "Browser window closed before task completed")

                self.close_browser()

            except MaxRetryError:
                logger.log("error", "Max retries exceeded")

                self.close_browser()

    def close_browser(self) -> None:
        self.driver.quit()

        logger.log("debug", "Browser driver exited")
