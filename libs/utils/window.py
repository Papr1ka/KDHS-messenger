from kivy.uix.widget import Widget
from kivy.metrics import dp
from settings import Widths

def get_window_type(wd: Widget):
    if wd.width < Widths['mobile']:
        return 'mobile'
    elif wd.width < Widths['tablet']:
        return 'tablet'
    else:
        return 'desktop'