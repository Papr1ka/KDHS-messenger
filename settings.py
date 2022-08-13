from pathlib import Path
from os import path

#path to project directory
BASE_DIR = Path(__file__).resolve().parent

SOURCE_DIR = BASE_DIR.joinpath('libs')


#paths to folders with .kv files

Templates = [
    SOURCE_DIR.joinpath('components'),
    SOURCE_DIR.joinpath('screens'),
    SOURCE_DIR.joinpath('screen_manager'),
]
