# -*- coding: utf-8 -*-

import os
from functools import wraps

import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

app = flask.Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super secret app key")


def login_required(f):
    """
        Decorator to check whether the user is logged in or not.
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        if flask.session.get("logged_in"):
            return f(*args, **kwargs)
        else:
            flask.flash("Login Required")
            return flask.redirect(flask.url_for("authorize"))

    return wrap


""" Main application views """


@app.route("/login")
def login():
    return flask.redirect(flask.url_for("authorize"))


@app.route("/")
def home():
    return flask.redirect(flask.url_for("search"))


@app.route("/search", methods=["POST", "GET"])
@login_required
def search():
    if flask.request.method == "POST":
        flask.session["querry"] = flask.request.form["querry"]
        return flask.redirect(flask.url_for("result"))
    return flask.render_template("index.html")


@app.route("/result")
@login_required
def result():
    # The user is already logged in here, load the credentials from the session.
    credentials = google.oauth2.credentials.Credentials(**flask.session["credentials"])

    client = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials
    )
    querry = flask.session.get("querry")
    if not querry:
        return flask.redirect(flask.url_for("search"))
    response = search_list_by_keyword(
        client, part="snippet", maxResults=25, q=querry, type=""
    )
    length = len(response["items"])
    flask.session.pop("querry", None)
    return flask.render_template("results.html", response=response, length=length)


""" Authentication related views using google oauth """


@app.route("/authorize")
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES
    )

    flow.redirect_uri = flask.url_for("oauth2callback", _external=True)
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )

    flask.session["state"] = state
    return flask.redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():
    state = flask.session["state"]
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
    )
    flow.redirect_uri = flask.url_for("oauth2callback", _external=True)

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials in the session.
    credentials = flow.credentials
    flask.session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
    flask.session["logged_in"] = True
    return flask.redirect(flask.url_for("home"))


@app.route("/logout")
def logout():
    flask.session.clear()
    flask.flash("You are logged out, login to use the application")
    return flask.redirect(flask.url_for("index"))


""" Utility methods used by the application views """


def channels_list_by_username(client, **kwargs):
    response = client.channels().list(**kwargs).execute()
    return flask.jsonify(**response)


def search_list_by_keyword(client, **kwargs):
    response = client.search().list(**kwargs).execute()
    return response


if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.run(host="localhost", port=5000, debug=True)
