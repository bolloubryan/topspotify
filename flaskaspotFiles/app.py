import json
#from flask import Flask, request, redirect, g, render_template #original import
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, g, jsonify
import requests
from urllib.parse import quote
from gettrack import *

from flask_sqlalchemy import SQLAlchemy

# ################################################################################
# from apscheduler.schedulers.background import BackgroundScheduler              #
# from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor #
# ################################################################################

import time

# from flask_sqlalchemy import SQLAlchemy
# from send_mail import send_mail

app = Flask(__name__)

# ##########################################################################
# executors = {                                                            #
#     'default': ThreadPoolExecutor(16),                                   #
#     'processpool': ProcessPoolExecutor(4)                                #
# }                                                                        #
# sched = BackgroundScheduler(timezone='Asia/Seoul', executors=executors)  #
# ##########################################################################

#  Client Keys
CLIENT_ID = "f49b4e460bec4f4ba54aeed004a46e04"
CLIENT_SECRET = "aa7872b2ae574d71a1fd03139746fb5e"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

inDEV = False
PORT = 8080

# Server-side Parameters
if (inDEV):
	#dev redirect
	CLIENT_SIDE_URL = "http://127.0.0.1"
	REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
	# dev databse
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:post123$@localhost/flaskaspotusers'
	#debugging option for more logs -- ON
	app.debug = True

else :
	# prod databse
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pwronuwmvnpceu:f6a306f214ca315c38bb781f108f308a33a8817050167fa4f34588d8c936982c@ec2-54-86-57-171.compute-1.amazonaws.com:5432/d38634uljvehgv'
	#prod redirect
	REDIRECT_URI= "http://flaskaspot.herokuapp.com/callback/q"
	#debugging option for more logs -- OFF
	app.debug = False

#dont want a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#creating a databse object to query our app
db = SQLAlchemy(app)

#create a databse class
class userdb(db.Model):
	__tablename__ = 'userdb'
	id = db.Column(db.Integer, primary_key=True)
	userlogin = db.Column(db.String(200), unique = True)
	songjson = db.Column(db.Text())
	spotifyid = db.Column(db.String(200), unique = True)

	def __init__ (self, userlogin, songjson, spotifyid):
		self.userlogin = userlogin
		self.songjson = songjson
		self.spotifyid = spotifyid

SCOPE = "user-read-recently-played user-read-currently-playing"
#SCOPE = "user-read-currently-playing"
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
	#print("PRINTED THIS: @@@@@@@@@@@@@ "+auth_token)
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
	#print(username)
	filewriter = open(".cache-"+username, "w")
	filewriter.write(response_data)
	filewriter.close()
	return redirect('/success')

@app.route('/success')
def success():
	username = request.cookies.get('userID')
	return render_template('success.html', nametitle=username)

# saving the state of the page by sending the username and current topsong json to the db
@app.route('/save')
def save():
	#get username
	username = request.cookies.get('userID')
	#print("username="+username)
    # here we want to get the value of the key (i.e. ?key=value)
	value = request.args.get('key')
    #get top10 list in json
	#top10list = json.loads(value)
	top10list = value
	#print("top 10 list is "+ top10list)
    #print(top10list)
	#if request.method == 'POST':
	userlogin = username
	songjson = top10list
	spotid = WhoTrack(username)#run the gettrack and get id?
	#if db.session.query(userdb).filter(userdb.userlogin == userlogin).count() == 0:
	#print(spotifyid)
	found_user = userdb.query.filter_by(spotifyid=spotid).first()
	if found_user:
		#print("user exists")
		found_user.songjson = songjson
		db.session.commit()
	else:
		#create a new user entry
		data = userdb(userlogin, songjson,spotid)
		db.session.add(data)
		db.session.commit()
	return value

@app.route('/updatetop')
def updatetop():
	username = request.cookies.get('userID')
	spotid = WhoTrack(username)
	found_user = userdb.query.filter_by(spotifyid=spotid).first()
	if found_user:
		return found_user.songjson
	else:
		return ("[]")
	

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

#OLD API TESTING
# @app.route('/success', methods=['POST'])
# def success():
# 	if request.method == 'POST' or apiaction != None:
# 		apiaction = request.form['apiaction']
# 		#use cookie to set username and get the cache created under the right name
# 		username = request.cookies.get('userID')

# 		if apiaction == "currentsong":
# 			# WhoseTrack(username)
# 			#print(username + "before whatrack")
# 			info = WhatTrack(username)
# 		elif apiaction == "finishsong":
# 			# WhoseTrack(username)
# 			info = SendTrack(username)
# 		else:
# 			info = "No action."

# 	return render_template('success.html', message=info)

########### Cookie Stuff ########################################
@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
	if request.method == 'POST':
		user = request.form['username']
		if user == '' or user == 'default':
			return render_template('index.html', message="Please enter a username. Can't be 'default'.")
		newcookie = make_response(render_template('cookie.html'))
		newcookie.set_cookie('userID', value=user, max_age=None)
		return newcookie

	#return render_template('success.html')

@app.route('/_stuff', methods = ['GET'])
def stuff():
	username = request.cookies.get('userID')
	if (username):
		return jsonify(result=LinkTrack(username))

@app.route('/_stuff2', methods = ['GET'])
def stuff2():
	username = request.cookies.get('userID')
	if (username):
		return jsonify(result=HistoryTrack(username))

@app.route('/example')
def example():
    # here we want to get the value of the key (i.e. ?key=value)
    value = request.args.get('key')
    #print("@@@@@@@@@@@@@@@@@queue to save: "+value)
    top10list = json.loads(value)
    #print(top10list)
    return value

if __name__ == '__main__':
	app.run(debug=True, port=PORT)