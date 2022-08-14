from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import StringProperty, ColorProperty, DictProperty, ListProperty, ObjectProperty

class TextInputBase():
    hint_text = StringProperty('')
    back_color = ColorProperty([0, 0, 0, 1])
    text_color = ColorProperty([1, 1, 1, 1])


class TextInputRound(MDFloatLayout, TextInputBase):
    textinput = ObjectProperty(None)
    def get_text(self):
        return self.textinput.text

class TextInputRoundIcon(TextInputRound):
    icon_pos = DictProperty({"center_x": 0.92, "center_y": 0.5})
    icon_source = StringProperty('')
