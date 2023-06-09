import os

from dotenv import load_dotenv


class Setup:
    """Stores project information and environment variables"""

    # --- About ---
    NAME = "Spotify-GPT"
    VERSION = "2.0.0"
    URL = "https://github.com/rahul-chotu/Spotify-GPT"
    AUTHOR = "Rahul Chotu"
    #######################

    # --- Project directory ---
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # --- Paths ---
    SETTINGS_PATH = os.path.join(BASE_DIR, "resources\\settings.json")
    ICON = os.path.join(BASE_DIR, "resources\\images\\logo.ico")
    EXPLORER_IMAGE = os.path.join(BASE_DIR, "resources\\images\\explorer_icon.png")
    PLAY_BTN_IMAGE = os.path.join(BASE_DIR, "resources\\images\\play_btn.png")
    PAUSE_BTN_IMAGE = os.path.join(BASE_DIR, "resources\\images\\pause_btn.png")
    ADD_BTN_IMAGE = os.path.join(BASE_DIR, "resources\\images\\add.png")
    CHROME_DRIVER_PATH = os.path.join(BASE_DIR, "resources\\chromedriver.exe")
    LOG_PATH = os.path.join(BASE_DIR, "resources\\logs")
    THEME_PATH = os.path.join(BASE_DIR, "resources\\themes")

    if os.path.exists(os.path.join(BASE_DIR, ".env.secret")):
        ENV_PATH = os.path.join(BASE_DIR, ".env.secret")
    else:
        ENV_PATH = os.path.join(BASE_DIR, ".env")

    # --- Environment Variables ---
    load_dotenv(ENV_PATH)

    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    USERNAME = os.getenv("USER_NAME")
    PASSWORD = os.getenv("PASSWORD")
    API_KEY = os.getenv("API_KEY")
    CHATGPT_MODEL = os.getenv("CHATGPT_MODEL")
    MODE = os.getenv("MODE")
