from pathlib import Path
from kivy.core.window import Window
from kivymd.uix.controllers import WindowController
from kivy.core.text import LabelBase
from logging import config, getLogger


Window.minimum_height = 500
Window.minimum_width = 400

LabelBase.register(name='Nunito', fn_regular='assets/fonts/Nunito.ttf')
LabelBase.register(name='InterM', fn_regular='assets/fonts/Inter-Medium.otf')
LabelBase.register(name='InterR', fn_regular='assets/fonts/Inter-Regular.otf')

#path to project directory
BASE_DIR = Path(__file__).resolve().parent

SOURCE_DIR = BASE_DIR.joinpath('libs')


#paths to folders with .kv files

Templates = [
    SOURCE_DIR.joinpath('components'),
    SOURCE_DIR.joinpath('screens'),
    SOURCE_DIR.joinpath('screen_manager'),
]


Widths = {
    'mobile': 700,
    'tablet': 1100,
}


def on_size(self, instance, size: list) -> None:
    """Called when the application screen size changes."""

    window_width = size[0]

    if window_width < Widths['mobile']:
        self.real_device_type = "mobile"
    elif window_width < Widths['tablet']:
        self.real_device_type = "tablet"
    else:
        self.real_device_type = "desktop"


WindowController.on_size = on_size

SERVER_URL = "http://127.0.0.1:8000"
SERVER_URL = "http://193.124.115.112:7000"


"""
Logging
"""

from kivy.logger import Logger, LOG_LEVELS

Logger.setLevel(LOG_LEVELS["debug"])

# from logging import Formatter

# class simpleFormatter(Formatter):
#     __fmt = "%(name)s : %(funcName)s : %(lineno)d : %(asctime)s : %(levelname)s : %(message)s"
#     __datefmt = "%d/%m/%Y %I:%M:%S %p"

#     def __init__(self):
#         super().__init__(fmt=simpleFormatter.__fmt, datefmt=simpleFormatter.__datefmt)



# config.fileConfig('./logging.ini', disable_existing_loggers=False)
# Logger = getLogger('KDHS_Messanger')
# import logging




# for i in logging.Logger.manager.loggerDict:
#     print(i)


# getLogger('requests').setLevel('WARNING')
# getLogger('urllib3').setLevel('WARNING')
# getLogger('asyncio').setLevel('WARNING')
# getLogger('kivy').setLevel('WARNING')


# Logger.info("test value")
