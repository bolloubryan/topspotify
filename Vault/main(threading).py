from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivy.clock import Clock

from database import DataBase
from whichtrack import *

import threading
import time

class MainWindow(Screen):
	label1 = ObjectProperty(None)
	label2 = ObjectProperty(None)
	label3 = ObjectProperty(None)
	label4 = ObjectProperty(None)
	label5 = ObjectProperty(None)
	newsong = ObjectProperty(None)
	# def getTrack(self):
	# 	pass

	def placeSong(self, bId):
		print("button pressed")
		if bId == 1 :
			self.label1.text = "pressed"
		if bId == 2 :
			self.label2.text = "pressed"
		if bId == 3 :
			self.label3.text = "pressed"
		if bId == 4 :
			self.label4.text = "pressed"
		if bId == 5 :
			self.label5.text = "pressed"

	def discardSong(self, *args):
		self.newsong.text = "Waiting on new song..."
		for arg in args: 
			self.newsong.text = str(arg) 
		#print(trackinfo)
		#print(SendTrack())
		#self.newsong.text = trackinfo
		print("discard song")

	def updateSong (self, *args):
		print("ran")
		self.newsong.text = time.asctime()
		
class WindowManager(ScreenManager):
	pass

kv = Builder.load_file("my.kv")
sm = WindowManager()
db = DataBase("placedSongs.txt")

screens = [MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"

class MyApp (App):
	def build(self):
		themain = MainWindow()
		Clock.schedule_interval(themain.discardSong, 3)
		return sm

if __name__ == "__main__":
	MyApp().run()