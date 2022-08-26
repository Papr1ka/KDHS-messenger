from os import path
from PIL import Image


def check_password_length(password: str):
    return password.__len__() >= 8

def is_image(path_to_image):
    way = path.abspath(path_to_image)
    if not path.exists(way) or not path.isfile(way) or not check_image_with_pil(way):
        return False
    return True

def check_image_with_pil(path):
    try:
        Image.open(path)
    except IOError:
        return False
    return True
