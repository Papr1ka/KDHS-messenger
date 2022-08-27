from kivy.properties import ColorProperty, StringProperty, ObjectProperty
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineAvatarIconListItem, IRightBodyTouch
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDTextButton
from libs.components.textfield_popup import TextFieldPopup
from libs.utils.behaviors import GetApp


class SettingsItem(OneLineAvatarIconListItem):
    bg_color = ColorProperty([0, 0, 0, 0])
    text = StringProperty("")
    secondary_text = StringProperty("")
    textinput = ObjectProperty(None)


class RightTextInput(IRightBodyTouch, MDTextButton, GetApp):
    dialog = None
    title = StringProperty("")
    
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.register_event_type('on_submit')
    
    def on_submit(self, text: str):
        pass

    def show_username_change_dialog(self):

        def close_dilog(obj):
            self.dialog.dismiss()
        
        def use_input(obj):
            text = self.dialog.content_cls.get_text()
            self.dispatch("on_submit", text)
            close_dilog(obj)

        if not self.dialog:
            self.dialog = MDDialog(
                title=self.title,
                type="custom",
                content_cls=TextFieldPopup(),
                buttons=[
                    MDFlatButton(
                        text="Отменить",
                        theme_text_color="Custom",
                        text_color=self.app.colors['SecondAccentColor'],
                        on_press = close_dilog,
                        radius=[dp(18)]
                    ),
                    MDFlatButton(
                        text="Сохранить",
                        theme_text_color="Custom",
                        text_color=self.app.colors['SecondAccentColor'],
                        on_press = use_input,
                        radius=[dp(18)]
                    ),
                ],
            )
        self.dialog.open()
