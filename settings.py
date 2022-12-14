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
PATH_TO_ICON = BASE_DIR.joinpath('assets/icons/app.ico')


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

from kivy.config import Config

Config.set('kivy', 'window_icon', str(PATH_TO_ICON))



SERVER_URL = "http://127.0.0.1:8000"
SERVER_URL = "http://193.124.115.112:7000"


"""
Logging
"""

from kivy.logger import Logger, LOG_LEVELS

Logger.setLevel(LOG_LEVELS["debug"])
