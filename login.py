from flask import Blueprint, redirect, url_for, session, request, jsonify, render_template
from flask_login import login_required, login_user, \
    logout_user, current_user
from config import Auth
import json
from app import oauth, login_manager, db


google = oauth.remote_app(
    'google',
    consumer_key=Auth.CLIENT_ID,
    consumer_secret=Auth.CLIENT_SECRET,
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email'
    },
    base_url=Auth.BASE_URL,
    request_token_url=None,
    access_token_method='POST',
    access_token_url=Auth.ACCESS_TOKEN_URL,
    authorize_url=Auth.AUTHORIZE_URL,
)

login_routes = Blueprint('login', __name__)


@login_routes.route('/')
def index():
    # if current_user.is_authenticated:
    #     return jsonify(current_user.email)
    return render_template('index.html')


@login_routes.route('/login')
def login():
    return google.authorize(callback=url_for('login.authorized', _external=True))


@login_routes.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('google_token', None)
    return redirect(url_for('login.index'))


@login_routes.route('/oauth2callback')
@google.authorized_handler
def authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    user_data = me.data
    print(user_data)
    return redirect(url_for('login.index'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))