from plyer import notification
from libs.utils.behaviors import GetApp

class Notifier(GetApp):
    def notify(self, header: str, text: str):
        if self.app.notifications:
            notification.notify(
                message=text,
                app_name="KDHS Messanger", 
                title=header,
                toast=True
            )