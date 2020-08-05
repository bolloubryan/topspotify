import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth

trackinfo=""

def GetTrack():
		scope = "user-read-currently-playing"
		sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,username="cache"))

		while (True):
			canexit=5
			while(canexit >= 0):
				time.sleep(3)
				results = sp.current_user_playing_track()
				currentpos= results["progress_ms"]
				totaltime= results["item"]["duration_ms"]
				canexit = ((totaltime-currentpos)/1000)-3
				
			trackname= results ["item"]["name"]
			albumname= results ["item"]["album"]["name"] 
			artist= results ["item"]["album"]["artists"][0]["name"]

			trackinfo = "Track: " + trackname + " by " + artist + " -- Album: " + albumname
			update_label()

class MainWindow(Screen):
	def update_label(self):
		self.newsong.text = trackinfo

class WindowManager(ScreenManager):
	pass		

kv = Builder.load_file("my.kv")

class MyApp(App):
	def build(self):
		return kv

if __name__ == "__main__":
	MyApp().run()
	GetTrack()