import json

from packages.utilities.logger import Logger

logger = Logger("parser")


class Parser:
    """Takes string and returns the json block only"""

    @staticmethod
    def find_json(text: str) -> dict:
        """idk chatgpt wrote this"""

        json_blocks = []
        stack = []
        start = None

        for i, char in enumerate(text):
            if char == "{":
                if not stack:
                    start = i
                stack.append(char)
            elif char == "}":
                if stack:
                    stack.pop()
                    if not stack:
                        json_blocks.append(text[start:i + 1])
                else:
                    logger.log("error", "ValueError: Mismatched curly braces")
                    raise ValueError("Mismatched curly braces.")

        for json_block in json_blocks:
            try:
                data = json.loads(json_block)
                return data

            except json.JSONDecodeError:
                logger.log("error", "JSONDecodeError -> Invalid JSON block")
