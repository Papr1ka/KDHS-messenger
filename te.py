from functools import partial
from random import randint
from time import time
from kivy.clock import Clock

KV = '''
<CustomView@BoxLayout>:
    size_hint: 1, None
    text: ''
    Label:
        id: test_label
        size_hint: 1, None
        on_size: root.height = self.height
        text_size: root.width, None
        size: self.texture_size
        text: root.text


RecycleView:
    viewclass: 'CustomView'
    data: [{"text": f"{i} {'test'*i}"} for i in range(300)]
    scroll_y: 0
    RecycleBoxLayout:
        id: layout
        default_size: None, None
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
'''

class Invoke():
    """
    декоратор для функций, которые обязательно должны быть выполнены, если не получилось, следующая попытка через recall_interval * 2
    """

    def __init__(self, recall_inverval):
        self.recall_interval = recall_inverval

    def __call__(self, function):
        def wrapped(*args, **kwargs):
            try:
                r = function(*args, **kwargs)
            except Exception as E:
                self.recall_interval *= 2
                print("мы пытались")
                Clock.schedule_once(partial(wrapped, *args, **kwargs), self.recall_interval)
                print("но сложились")
            else:
                print("получилось")
                return r
        return wrapped

from kivy.app import App
from kivy.lang import Builder

@Invoke(1)
def do(number: int):
    print("called", number)
    a = randint(1, 2)
    if a == 2:
        raise ValueError("asdasdas")
    
class TestApp(App):
    def build(self):
        do(100)
        return Builder.load_string(KV)

if __name__ == '__main__':
    TestApp().run()

do(100)
