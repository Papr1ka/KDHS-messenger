from kivymd.app import MDApp


class GetApp():
    __app = None
    
    @property
    def app(self):
        if not self.__app:
            self.__app = MDApp.get_running_app()
        return self.__app
