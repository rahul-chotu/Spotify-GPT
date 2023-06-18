from argparse import Namespace, ArgumentParser

from packages.gui.app import App
from packages.utilities.logger import Logger

logger = Logger("main")


def main():
    app = App()
    app.mainloop()

    parser = ArgumentParser()

    parser.add_argument("-cl", "--clearlogs", action="store_true")

    args: Namespace = parser.parse_args()

    if args.clearlogs:
        logger.clear_logs()


if __name__ == "__main__":
    main()
