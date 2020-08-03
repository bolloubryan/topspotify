import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

#imports from spotipy
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

sp =spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,username="cache"))

class MyGrid(GridLayout):
	def __init__ (self, **kwargs):
		super(MyGrid, self).__init__(**kwargs)

		self.cols = 1

		self.inside = GridLayout()
		self.inside.cols = 2

		self.inside.add_widget(Label(text="FirstName: "))
		self.name = TextInput (multiline=False)
		self.inside.add_widget(self.name)

		self.add_widget(self.inside)

		self.submit = Button(text="submit", font_size=40)
		self.submit.bind(on_press=self.pressed)
		self.add_widget(self.submit)

	def pressed(self, instance):
		results = sp.current_user_saved_tracks()
		saved="nothing"
		for idx, item in enumerate(results['items']):
			track = item['track']
			saved = idx, track['artists'][0]['name'], " – ", track['name']
		saved = str(saved)
		name=self.name.text
		word = saved
		self.name.text =word

class MyApp(App):
	def build(self):
		return MyGrid()

#if __name__ == "__main__":
MyApp().run()
