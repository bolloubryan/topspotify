from bottle import route, run, request
import spotipy
from spotipy import oauth2

PORT_NUMBER = 8080
# SPOTIPY_CLIENT_ID = 'f49b4e460bec4f4ba54aeed004a46e04'
# SPOTIPY_CLIENT_SECRET = 'aa7872b2ae574d71a1fd03139746fb5e'
# SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-read-currently-playing'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )
token_info = sp_oauth.get_cached_token() 
if not token_info:
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    response = input('Paste the above link into your browser, then paste the redirect url here: ')

    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_cached_token()

    token = token_info['access_token']
    print(token)

print(token_info)
token = token_info['access_token']
sp = spotipy.Spotify(auth=token)