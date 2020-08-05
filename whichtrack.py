import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
scope = "user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,username="cache"))

while (True):
	canexit=5
	while(canexit >= 0): #may need to modify due to playlist doing the fade out
		time.sleep(5)
		results = sp.current_user_playing_track()

		currentpos= results["progress_ms"]
		totaltime= results["item"]["duration_ms"]
		#print(canexit)

		canexit = ((totaltime-currentpos)/1000)-7

	trackname= results ["item"]["name"]
	albumname= results ["item"]["album"]["name"] 
	artist= results ["item"]["album"]["artists"][0]["name"]

	trackinfo = "Track: " + trackname + " by " + artist + " -- Album: " + albumname
	print(trackinfo)

#need to listen to the whole song
# while (True):
# 	time.sleep(5)
# 	results = sp.current_user_playing_track()

# 	trackname= results ["item"]["name"]
# 	albumname= results ["item"]["album"]["name"] 
# 	artist= results ["item"]["album"]["artists"][0]["name"]

# 	trackinfo = "Track: " + trackname + " by " + artist + " -- Album: " + albumname

# 	print(trackinfo)

# 	currentpos= results["progress_ms"]
# 	totaltime= results["item"]["duration_ms"]

# 	time.sleep(((totaltime-currentpos)/1000)-2)

# 	print("where would you like to rank this song?")