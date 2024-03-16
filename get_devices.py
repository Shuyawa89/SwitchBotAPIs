import os

from dotenv import load_dotenv
from switch_bot import SwitchBot


if __name__ == '__main__':
    load_dotenv()
    switch_bot = SwitchBot(
        os.environ['SWITCH_BOT_TOKEN'],
        os.environ['SWITCH_BOT_SECRET']
    )

    switch_bot.get_device_list()
