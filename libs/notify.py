from plyer import notification

def notify(header: str, text: str):
    notification.notify(
        message=text,
        app_name="KDHS Messanger", 
        title=header,
        toast=True
    )