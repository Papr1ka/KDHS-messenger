from kivy.properties import NumericProperty


class Settings():
    font_size = NumericProperty(18)
    
    def change_font_size(self, font_size: int):
        self.font_size = font_size
