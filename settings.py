from pathlib import Path
from os import path
from kivy.core.window import Window
from kivymd.uix.controllers import WindowController
from kivy.core.text import LabelBase


Window.minimum_height = 500
Window.minimum_width = 400

LabelBase.register(name='Nunito', 
                   fn_regular='assets/fonts/Nunito.ttf')

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
