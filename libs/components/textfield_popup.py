from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, ObjectProperty


class TextFieldPopup(MDBoxLayout):
    hint_text = StringProperty("")
    textinput = ObjectProperty(None)

    def get_text(self):
        return self.textinput.text
