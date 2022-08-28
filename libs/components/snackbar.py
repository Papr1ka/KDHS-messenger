from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, ColorProperty

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import BaseSnackbar


class ExtendedBaseSnackbar(BaseSnackbar):
    pass


class ErrorSnackbar(ExtendedBaseSnackbar):
    text = StringProperty("")


class SuccessSnackbar(ExtendedBaseSnackbar):
    text = StringProperty("")


def show_error_snackbar(text):
    ErrorSnackbar(text=text).open()

def show_success_snackbar(text):
    SuccessSnackbar(text=text).open()
