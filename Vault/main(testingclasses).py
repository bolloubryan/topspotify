from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.lang import Builder

kv = '''
<MainScreen>:
    label1:lb1
    ns:self.ns

    Label:
        text:"Top Spotify Songs"
        pos_hint: {"top":1}
        size_hint: 1, 0.15

    FloatLayout:
        id: MainLayout

        Label:
            text:"1"
            pos_hint: {"x":0.1, "top":0.9}
            size_hint: 0.01, 0.15
        Label:
            id: lb1
            text: "Song Name"
            pos_hint: {"x":0.2, "top":0.9}
            size_hint: 0.35, 0.15
        Button:
            text: "Place Here"
            pos_hint: {"x":0.7, "top":0.9}
            size_hint: 0.15, 0.10

    UpdateSong:
        Label:
            id:ns
            text: "needtoupdate"
            size_hint: 0.35, 0.15
            pos_hint: {"x":1, "top":1}
'''

Builder.load_string(kv)

class MainScreen(FloatLayout):
    pass

class UpdateSong(Widget):
    def __init__(self, **kwargs):
        super(UpdateSong, self).__init__(**kwargs)
        self.update
    def update(self, *args):
        mainone = MainScreen()
        mainone.label1.text="hi"
        print("w")

class MyApp(App):
    def build(self):
        mainone = MainScreen()
        updateone = UpdateSong()
        Clock.schedule_interval(updateone.update, 3)
        return mainone

if __name__ == '__main__':
    MyApp().run()