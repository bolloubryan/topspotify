from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from client import * #changed to client from gettrack
#from gettrack import *
import time

class WhatSong(Label):
    def getsong(self, *args):
    	#self.text = WhatTrack ()
        self.text = main()

class MyApp(App):
    def build(self):
        mainapp = WhatSong()
        Clock.schedule_interval(mainapp.getsong, 1)
        return mainapp

if __name__ == "__main__":
    MyApp().run()