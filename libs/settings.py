import pickle
from os.path import exists
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Params:
    font_size: str
    notifications: bool

class Settings():
    def __init__(self) -> None:
        if exists(Path('/settings.pickle')):
            with open(Path('settings.pickle'), 'rb') as settings:
                data = pickle.load(settings)
            self._font_size = data.font_size
            self._notifications = data.notifications
        else:
            self._font_size = 18
            self._notifications = True

    @property
    def font_size(self):
        if isinstance(self._font_size, int):
            if (12 <= self._font_size <= 12):
                return self._font_size
            else:
                return 12
        else:
            return 12
    
    @font_size.setter
    def font_size(self, font_size: int):
        if (12 <= font_size <= 40):
            self._font_size = font_size
        else:
            raise ValueError("Шрифт должен быть от 12 до 40")
        self.save()
    
    @property
    def notifications(self):
        if isinstance(self._notifications, bool):
            return self._notifications
        return True
    
    @notifications.setter
    def notifications(self, flag: bool):
        self._notifications = flag
        self.save()
    
    def save(self):
        data = Params(self._font_size, self._notifications)
        with open(Path('settings.pickle'), 'rb') as settings:
            pickle.dump(data, settings)
