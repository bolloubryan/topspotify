import json
#from flask import Flask, request, redirect, g, render_template #original import
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, g
import requests
from urllib.parse import quote
from gettrack import *

import time

# from flask_sqlalchemy import SQLAlchemy
# from send_mail import send_mail

app = Flask(__name__)

#  Client Keys
CLIENT_ID = "f49b4e460bec4f4ba54aeed004a46e04"
CLIENT_SECRET = "aa7872b2ae574d71a1fd03139746fb5e"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "user-read-currently-playing"
#STATE = ""
#SHOW_DIALOG_bool = True
#SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

# ENV = 'prod'

# if ENV == 'dev':
# 	app.debug = True
# 	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:post123$@localhost/lexus'
# else:
# 	app.debug = False
# 	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mcyzfidjetnxyb:0d2511855c302904f471d5bf24fe4ea011842cf39bb4aa0848995692a2bd4537@ec2-34-237-89-96.compute-1.amazonaws.com:5432/ded406llgp6ft1'

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# class Feedback(db.Model):
# 	__tablename__ = 'feedback'
# 	id = db.Column(db.Integer, primary_key=True)
# 	customer = db.Column(db.String(200), unique = True)
# 	dealer = db.Column(db.String(200))
# 	rating = db.Column(db.Integer)
# 	comments = db.Column(db.Text())

# 	def __init__ (self, customer, dealer, rating, comments):
# 		self.customer = customer
# 		self.dealer = dealer
# 		self.rating = rating
# 		self.comments = comments

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
	if request.method == 'POST':
		username = request.cookies.get('userID')
		#username = request.form['username'] #this is without the cookie
		#print(username)
	# Auth Step 1: Authorization
	url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
	auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
	return redirect(auth_url)

@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access Tokens
	auth_token = request.args['code']
	code_payload = {
		"grant_type": "authorization_code",
		"code": str(auth_token),
		"redirect_uri": REDIRECT_URI,
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET,
		}
	post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

	# Auth Step 5: Tokens are Returned to Application
	response_data = json.loads(post_request.text)
	access_token = response_data["access_token"]
	refresh_token = response_data["refresh_token"]
	token_type = response_data["token_type"]
	expires_in = response_data["expires_in"]

	#add a expires at date uusing the expires_in and the current time
	#post into a cache file nwith the entered username as the cache
	#will maintain a list of usernames and their cache files
	now = time.time()
	response_data ["expires_at"] = now-expires_in
	response_data = json.dumps(response_data)
	

	#get the user's name from the databse to add to the "cache-username"
	username = "default" #update to ge the username from the database
	username = request.cookies.get('userID') #getting username from cookie
	print(username)
	filewriter = open(".cache-"+username, "w")
	filewriter.write(response_data)
	filewriter.close()

	return render_template('success.html')

# 		if customer == '' or dealer == '':
# 			return render_template('index.html', message='Please enter required files')

# 		if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
# 			data = Feedback(customer, dealer, rating, comments)
# 			db.session.add(data)
# 			db.session.commit()
# 			send_mail(customer, dealer, rating, comments)
# 			return render_template('success.html')
# 		else:
# 			return render_template('index.html', message='You have already submitted feedback')


@app.route('/success', methods=['POST'])
def success():
	print("after success")
	if request.method == 'POST' or apiaction != None:
		apiaction = request.form['apiaction']
		#use cookie to set username and get the cache created under the right name
		username = request.cookies.get('userID')
		#print(apiaction)
		if apiaction == "currentsong":
			# WhoseTrack(username)
			print(username + "before whatrack")
			info = WhatTrack(username)
		elif apiaction == "finishsong":
			# WhoseTrack(username)
			info = SendTrack(username)
		else:
			info = "No action."
	return render_template('success.html', message=info)

########### Cookie Stuff ########################################
@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
	if request.method == 'POST':
		user = request.form['username']
		if user == '':
			return render_template('index.html', message="Please enter a username.")
		newcookie = make_response(render_template('cookie.html'))
		newcookie.set_cookie('userID', value=user, max_age=None)
		return newcookie

	#return render_template('success.html')
		

if __name__ == '__main__':
	app.run(debug=True, port=PORT)