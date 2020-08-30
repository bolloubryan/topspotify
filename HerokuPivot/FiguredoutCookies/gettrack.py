import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-currently-playing"

username = "default"

def WhoseTrack (thisuser):
	username = thisuser

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,username=username))

def SendTrack ():
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

	endinfo = "Track: " + trackname + " by " + artist + " -- Album: " + albumname
	return endinfo

def WhatTrack():
	results = sp.current_user_playing_track()
	trackname= results ["item"]["name"]
	albumname= results ["item"]["album"]["name"] 
	artist= results ["item"]["album"]["artists"][0]["name"]

	trackinfo = "Track: " + trackname + " by " + artist + " -- Album: " + albumname
	return trackinfo