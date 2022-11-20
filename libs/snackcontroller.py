from functools import partial
from kivy.clock import Clock

class Controller():
    interval: int
    def __init__(self) -> None:
        self.interval = 0
    
    def show(self, func, interval):
        interval += 1
        Clock.schedule_once(func, self.interval)
        Clock.schedule_once(partial(self.__decrement_interval, interval), self.interval + interval)
        self.interval += interval
    
    def __decrement_interval(self, interval, pt):
        self.interval -= interval
