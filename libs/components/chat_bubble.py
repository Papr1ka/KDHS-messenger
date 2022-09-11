from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.metrics import dp


class ChatBubble(MDLabel, RecycleDataViewBehavior):
    send_by_user = BooleanProperty(False)
    halign = StringProperty('left')
    width = NumericProperty(0)
    text_width = NumericProperty(0)
    
    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.send_by_user = data['send_by_user']
        self.halign = data['halign']
        self.text_width = min(data['max_text_width'], self.width) + dp(18)
        return super().refresh_view_attrs(
            rv, index, data)
