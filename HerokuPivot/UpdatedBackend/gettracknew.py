import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth

# scope = "user-read-currently-playing"
# scope = "user-read-recently-played"

scope = "user-read-recently-played user-read-currently-playing"

username = "default"

# def WhoseTrack (thisuser):
# 	username = thisuser
# 	print(username)

def SendTrack (username):
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,username=username))
	canexit=5
	try:
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
	except:
		return ("Playback paused or not logged in.")
	return endinfo

def WhatTrack(username):
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,username=username))
	try:
		results = sp.current_user_playing_track()
		trackname= results ["item"]["name"]
		albumname= results ["item"]["album"]["name"] 
		artist= results ["item"]["album"]["artists"][0]["name"]
		trackinfo = "Track: " + trackname + " by " + artist + " -- Album: " + albumname
	except:
		return ("Playback paused or not logged in.")
	return trackinfo

def LinkTrack(username):
	if username != "default":
		sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,username=username))
	try:
		results = sp.current_user_playing_track()
		trackuriraw=results["item"]["uri"]
		trackuri=trackuriraw.split(":")[2]
		trackinfo = "https://open.spotify.com/embed/track/"+trackuri
	except:
		return ("Playback paused or not logged in.")
	return (trackinfo)

def HistoryTrack(username):
	if username != "default":
		sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,username=username))
	try:
		results = sp.current_user_recently_played(limit=50, after=None, before=None)
		songlinks = []
		for jsons in results["items"]:
			trackuriraw=jsons["track"]["uri"]
			trackuri=trackuriraw.split(":")[2]
			trackinfo = "https://open.spotify.com/embed/track/"+trackuri
			songlinks.append(trackinfo)
	except:
		return ("Playback paused or not logged in.")
	return (songlinks)

	# try:
	# 	results = sp.current_user_recently_played(limit=50, after=None, before=None)
	# 	print(results)
	# 	# trackuriraw=results["item"]["uri"]
	# 	# trackuri=trackuriraw.split(":")[2]
	# 	# trackinfo = "https://open.spotify.com/embed/track/"+trackuri
	# except:
	# 	return ("Playback paused or not logged in.")
	# return (trackinfo)

# username = "default"

# def WhoseTrack (thisuser):
# 	username = thisuser
# 	print(username)

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,username=username))

# def SendTrack ():
# 	canexit=5
# 	while(canexit >= 0): 
# 		time.sleep(3)
# 		results = sp.current_user_playing_track()

# 		currentpos= results["progress_ms"]
# 		totaltime= results["item"]["duration_ms"]
# 		canexit = ((totaltime-currentpos)/1000)-3

# 	trackname= results ["item"]["name"]
# 	albumname= results ["item"]["album"]["name"] 
# 	artist= results ["item"]["album"]["artists"][0]["name"]

# 	endinfo = "Track: " + trackname + " by " + artist + " -- Album: " + albumname
# 	return endinfo

# def WhatTrack():
# 	results = sp.current_user_playing_track()
# 	trackname= results ["item"]["name"]
# 	albumname= results ["item"]["album"]["name"] 
# 	artist= results ["item"]["album"]["artists"][0]["name"]

# 	trackinfo = "Track: " + trackname + " by " + artist + " -- Album: " + albumname
# 	return trackinfo