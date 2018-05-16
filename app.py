from ciscosparkapi import CiscoSparkAPI
from flask import Flask, redirect, request, render_template, session
import json
import os
import requests
from requests_oauthlib import OAuth2Session

app = Flask(__name__)


# This information is obtained upon registration of a new GitHub
client_id = os.environ.get("client_id", 'C423a10911a7a146506667581402cce863ce5d5ec77c0f28908e011066fa046ea')
client_secret = os.environ.get("client_secret", '12b87a83974a21d5d5a2c65fa80d8778f1daba96fb7f20b63869fc9143354a13')
authorization_base_url = 'https://api.ciscospark.com/v1/authorize'
token_url = 'https://api.ciscospark.com/v1/access_token'
scopes = os.environ.get('scopes', 'spark:all')

###########
#FUNCTIONS#
###########

def get_name():
    if 'token' not in session:
        return None
    wxapi = CiscoSparkAPI(session['token'])
    resp = wxapi.people.me()
    return resp.displayName

###########
#  ERRORS #
###########

@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    print(e)
    return render_template('500.html'), 500
    
###########
#  ROUTES #
###########

@app.route('/')
def index():
    print("INDEX")
    return render_template('index.html')

@app.route("/login")
def login():
    print("Hit the: Login")
    redirect_url = request.url_root + 'callback'  # redirect to the callback route
    wxteams = OAuth2Session(client_id, scope=scopes, redirect_uri=redirect_url)
    authorization_url, state = wxteams.authorization_url(authorization_base_url)

    '''
    # For Testing
    print("===========\nredirect: {}\nclient: {}\nauth_url: {}\nstate:{}"
          .format(redirect_url, wxteams, authorization_url, state))
    '''

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state

    return redirect(authorization_url)

@app.route("/callback", methods=["GET"])
def callback():
    print("Hit the: Callback")
    # Due to difficulty implementing with the callback with the requests_oauthlib library,
    # implmenting the callback with requests

    code = request.args.get('code') # Get the code provided by the URL from the auth

    # Webex Teams needs grant_type, client_id, client_secret, code, redirect_uri
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    grant_type = "authorization_code"
    body = {
        "grant_type": grant_type,
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": request.base_url
    }

    resp = requests.post(token_url, data=body, headers=headers)

    response_data = json.loads(resp.text)
    try:
        token = response_data['access_token']
    except KeyError:
        return internal_error(response_data)

    session['token'] = token
    if session.get('redirect_to'):
        #print(session)
        redirect_to = session['redirect_to']
        session['redirect_to'] = None
        return redirect(redirect_to)

    return token

@app.route("/test", methods=["GET"])
def test():
    if not session.get('token'):
        session['redirect_to'] = request.base_url
        return redirect('/login')

    else:
        return "Hello {}".format(get_name())

@app.route("/hello", methods=["GET"])
def hello():
    if not session.get('token'):
        session['redirect_to'] = request.base_url
        return redirect('/login')

    else:
        return "Hello {}".format(get_name())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.secret_key = os.urandom(24)
    #app.jinja_env.auto_reload = True
    #app.config['TEMPLATES_AUTO_RELOAD'] = True
    #app.run(host='0.0.0.0', port=port, debug=True, ssl_context='adhoc') # For testing locally and SSL is needed
    app.run(host='0.0.0.0', port=port, debug=True)