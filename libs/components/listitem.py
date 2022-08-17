from kivy.lang import Builder
from kivy.properties import BooleanProperty, ColorProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior

from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors.hover_behavior import HoverBehavior
from kivymd.app import MDApp


Builder.load_string(
    """
<ListItem>
    spacing: dp(15)
    padding: dp(10)
    adaptive_height: True

    MDBoxLayout:
        adaptive_size: True
        pos_hint: {"center_y": .5}

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(7)
        adaptive_height: True
        pos_hint: {"center_y": .5}

        MDLabel:
            text: root.text
            adaptive_height: True
            shorten: True
            shorten_from: 'right'
            text_size: self.width, None

        MDLabel:
            text: root.secondary_text
            font_name: 'Roboto-Regular'
            text_color: 0.5, 0.5, 0.5, 0.5
            adaptive_height: True
            shorten: True
            shorten_from: 'right'
            text_size: self.width, None


<-ChatListItem>
    padding: [dp(10), dp(15)]
    spacing: dp(10)
    adaptive_height: True

    canvas.before:
        Color:
            rgba: root.bg_color
        RoundedRectangle:
            radius: [dp(18),]
            size: self.size
            pos: self.pos

    MDBoxLayout:
        adaptive_size: True
        pos_hint: {"center_y": .5}

        FitImage:
            source: root.image
            size_hint: None, None
            size: dp(50), dp(50)
            radius: [dp(18),]

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(7)
        adaptive_height: True
        pos_hint: {"center_y": .5}

        MDLabel:
            text: root.text
            adaptive_height: True
            shorten: True
            shorten_from: 'right'
            text_size: self.width, None

        MDLabel:
            text: root.secondary_text
            font_name: 'Roboto-Regular'
            text_color: 0.5, 0.5, 0.5, 0.5
            adaptive_height: True
            shorten: True
            shorten_from: 'right'
            text_size: self.width, None

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(7)
        adaptive_size: True
        pos_hint: {"center_y": .5}

        MDLabel:
            text: root.time
            font_name: 'Roboto-Regular'
            adaptive_size: True

        Widget:
            size_hint: None, None
            size: dp(10), dp(10)

            canvas.before:
                Color:
                    rgba:
                        root.theme_cls.primary_color if root.unread_messages \
                        else (0, 0, 0, 0)
                Ellipse:
                    size: self.size
                    pos: self.pos
    """
)


class ListItem(ThemableBehavior, MDBoxLayout):

    bg_color = ColorProperty([0, 0, 0, 0])

    text = StringProperty()

    secondary_text = StringProperty()

    icon = StringProperty()
    
    app = None
    
    def get_app(self):
        if not self.app:
            self.app = MDApp.get_running_app()
        return self.app
    
    def on_enter(self):
        self.bg_color = self.get_app().colors['SecondColor']
    
    def on_leave(self):
        self.bg_color = self.get_app().colors['ThirdAccentColor']


class ChatListItem(ListItem, HoverBehavior):
    image = StringProperty()

    time = StringProperty()

    unread_messages = BooleanProperty()
