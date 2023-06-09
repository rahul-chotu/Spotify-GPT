import re
import openai

from tkinter.messagebox import showerror
from threading import Thread

from setup import Setup
from packages.utilities.parser import Parser
from packages.utilities.logger import Logger

logger = Logger("chatgpt")
config = Setup()


class ChatGPT:
    API_KEY = config.API_KEY
    MODEL = config.CHATGPT_MODEL

    match config.MODE:
        case "1" | "3":
            CONTENT = "You are a music recommendation generator"

        case "2":
            CONTENT = """You are a music recommendation generator that provides music recommendations with 
            spotify song code in json format only in plain text. Provide no text before and after the json.
            The response should look like this:
            {
                "recommendations": [
                    {
                    "name": "song one"
                    "artist": "song artist"
                    "track_id": "track id"
                    },
                    {
                    "name": "song two"
                    "artist": "song artist"
                    "track_id": "track id"
                    }
                ]
            }
            """

    def __init__(self, music_list: list, result_number: int):

        self.result_number = result_number
        self.music_list = music_list

        self.chat = None
        self.response = None

        # get response in new thread
        self.thread = Thread(target=self.get_response)
        self.thread.start()

    def get_response(self):
        openai.api_key = ChatGPT.API_KEY

        messages = [
            {"role": f"system", "content": f"{ChatGPT.CONTENT}"}
        ]

        message = f"Can you recommend {self.result_number} songs similar to {self.music_list}. With no text before or after the list."

        try:
            if message:
                messages.append({"role": "user", "content": message})
                self.chat = openai.ChatCompletion.create(model=f"{ChatGPT.MODEL}", messages=messages)

        except Exception as e:
            if isinstance(e, openai.error.RateLimitError):
                showerror(title="Rate Error", message="Too many Requests!\nPlease wait 20s and try again.")
                logger.log("error", f"Rate Error: {e}")

            elif isinstance(e, openai.error.AuthenticationError):
                showerror(title="Authentication Error", message="Please check API key.")
                logger.log("error", f"Authentication Error: {e}")

            else:
                showerror(title="Error", message="ChatGPT API error has occurred.")
                logger.log("error", "OpenAI API Error")

        response = self.chat.choices[0].message.content
        messages.append({"role": "assistant", "content": response})
        self.response = response

    def get_track_ids(self) -> list[str]:
        parser = Parser()

        # wait for chatgpt thread to stop
        self.thread.join()

        # convert string response to dict
        json_blocks = parser.find_json(self.response)

        # get id's from dict
        track_ids = [track["track_id"] for track in json_blocks["recommendations"]]

        return track_ids

    def get_list(self) -> list:
        # wait for chatgpt thread to stop
        self.thread.join()

        music_list = re.findall(r"\d+\.\s(.+)", self.response)

        logger.log("debug", f"Result List created. Number of results: '{self.result_number}'")

        return music_list
