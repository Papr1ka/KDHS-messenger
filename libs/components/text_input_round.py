from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import StringProperty, ColorProperty

class TextInputRound(MDFloatLayout):
    hint_text = StringProperty('')
    back_color = ColorProperty([0, 0, 0, 1])
    text_color = ColorProperty([1, 1, 1, 1])