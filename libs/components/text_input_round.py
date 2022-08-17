from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, ColorProperty, DictProperty, ListProperty, ObjectProperty, NumericProperty

class TextInputBase():
    hint_text = StringProperty('')
    back_color = ColorProperty([0, 0, 0, 1])
    text_color = ColorProperty([1, 1, 1, 1])
    radius = ListProperty([8])
    font_size = NumericProperty(15)
    
    def __init__(self) -> None:
        self.radius = [8]


class TextInputRound(MDFloatLayout, TextInputBase):
    textinput = ObjectProperty(None)
    def get_text(self):
        return self.textinput.text

class TextInputRoundIcon(TextInputRound):
    icon_pos_hint = DictProperty({"center_x": 0.92, "center_y": 0.5})
    icon_pos = ListProperty([0, 0])
    icon_source = StringProperty('')

class TextInputString(MDBoxLayout):
    textinput = ObjectProperty(None)
    button = ObjectProperty(None)

    def get_text(self):
        return self.textinput.text
