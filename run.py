# -*- coding: utf-8 -*-
import os
import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from flask import render_template
from flask import request, url_for, redirect, session


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

app = flask.Flask(__name__)
# Note: A secret key is included in the sample so that it works, but if you
# use this code in your application please replace this with a truly secret
# key. See http://flask.pocoo.org/docs/0.12/quickstart/#sessions.
app.secret_key = 'secret key'

@app.route('/login')
def login():  
	return flask.redirect(flask.url_for('authorize'))

@app.route('/')
def index():  
	return render_template("header.html")

@app.route('/home')
def home():
	return flask.redirect(flask.url_for('search'))

@app.route('/search',methods=['POST','GET'])
def search(): 
	if request.method == "POST":
		session['querry'] = request.form['querry']
		return flask.redirect(flask.url_for('result'))
	return render_template("index.html")

@app.route('/result')
def result():
	if 'credentials' not in flask.session:
      		return flask.redirect('authorize')

  	# Load the credentials from the session.
	credentials = google.oauth2.credentials.Credentials(
		  **flask.session['credentials'])

	client = googleapiclient.discovery.build(
		API_SERVICE_NAME, API_VERSION, credentials=credentials) 
	querry = session['querry']
	print ( querry )
	response = search_list_by_keyword(client,
							part='snippet',
    					maxResults=25,
    					q=querry,
    					type='')
	length = len(response['items'])
	session.pop('querry' , None)
	return render_template("results.html", response = response, length = length)

@app.route('/authorize')
def authorize():
  # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow
  # steps.
	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
	CLIENT_SECRETS_FILE, scopes=SCOPES)

	flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
	authorization_url, state = flow.authorization_url(
      # This parameter enables offline access which gives your application
      # both an access and refresh token.
		access_type='offline',
      # This parameter enables incremental auth.
		include_granted_scopes='true')

  # Store the state in the session so that the callback can verify that
  # the authorization server response.
	flask.session['state'] = state
	return flask.redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verify the authorization server response.
	state = flask.session['state']
	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
	flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
	authorization_response = flask.request.url
	flow.fetch_token(authorization_response=authorization_response)

  # Store the credentials in the session.
  # ACTION ITEM for developers:
  #     Store user's access and refresh tokens in your data store if
  #     incorporating this code into your real app.
	credentials = flow.credentials
	flask.session['credentials'] = {
    'token': credentials.token,
  	'refresh_token': credentials.refresh_token,
  	'token_uri': credentials.token_uri,
  	'client_id': credentials.client_id,
  	'client_secret': credentials.client_secret,
  	'scopes': credentials.scopes
  	}
	flask.session['logged_in'] = True 
	return flask.redirect(flask.url_for('home'))

@app.route('/logout')
def logout():
  flask.session.clear()
  return redirect(url_for('index'))


def channels_list_by_username(client, **kwargs):
  	response = client.channels().list(
    **kwargs
  	).execute()
  	return flask.jsonify(**response)


def search_list_by_keyword(client, **kwargs):
  # See full sample for function
  # print (flask.session['credentials']['client_id'])
		response = client.search().list(
		**kwargs
		).execute()
		return response


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if flask.session.logged_in:
          	return f(*args,**kwargs)
        else:
            flash("Login Required")
            return redirect(url_for('index'))
    return wrap


if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification. When
  # running in production *do not* leave this option enabled.
	os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
	app.run(host='0.0.0.0', port=5000, debug=True)
