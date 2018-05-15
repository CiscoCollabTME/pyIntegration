from ciscosparkapi import CiscoSparkAPI
from flask import Flask, redirect, request, render_template, session
import os
from requests_oauthlib import OAuth2Session

app = Flask(__name__)


# This information is obtained upon registration of a new GitHub
client_id = os.environ.get("client_id", 'C423a10911a7a146506667581402cce863ce5d5ec77c0f28908e011066fa046ea')
client_secret = os.environ.get("client_secret", '12b87a83974a21d5d5a2c65fa80d8778f1daba96fb7f20b63869fc9143354a13')
authorization_base_url = 'https://api.ciscospark.com/v1/authorize'
token_url = 'https://api.ciscospark.com/v1/access_token'
scopes = os.environ.get('scopes', 'spark:all')

"""
https://api.ciscospark.com/v1/authorize?client_id=C423a10911a7a146506667581402cce863ce5d5ec77c0f28908e011066fa046ea&response_type=code&redirect_uri=https%3A%2F%2Fpyintegrationdev.herokuapp.com%2F&scope=spark%3Aall%20spark%3Akms&state=set_state_here
"""

def get_name():
    if 'token' not in session:
        return None
    wxapi = CiscoSparkAPI(session['token'])
    resp = wxapi.people.me()
    return resp.displayName
    
###########
#  ROUTES #
###########

@app.route('/')
def index():
    print("INDEX")
    return render_template('index.html')

@app.route("/login")
def login():
    redirect = '{}/callback'.format(request.base_url)
    print("LOGIN")
    wxteams = OAuth2Session(client_id, scope=scopes, redirect_uri=redirect)
    authorization_url, state = wxteams.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    
    print(authorization_url, state)

    print(authorization_url)
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    wxteams = OAuth2Session(client_id, state=session['oauth_state'])
    token = wxteams.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)
    session['token'] = token
    
    return token


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.secret_key = os.urandom(24)
    #app.jinja_env.auto_reload = True
    #app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=port, debug=True)