import os

from dotenv import load_dotenv

import src.app as app
from ui import launch_ui


def main():
    load_dotenv()
    os.getenv('OPENAI_API_KEY')
    app.init()

    launch_ui()


if __name__ == '__main__':
    main()
