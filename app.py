from flask import Flask, render_template, session, redirect, request, url_for, g
from twitter_utils import consumer, get_request_token, get_auth_verifier_url, get_access_token
from user import User
from database import Database

Database.initilize(database="test",
                   user="postgres",
                   password="password",
                   host="localhost")

app = Flask(__name__)
app.secret_key = '123'


@app.before_request
def before_load():
    if 'session_name' in session:
        g.user = User.load_from_db_by_email(session['screen_name'])


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/login/twitter')
def twitter_login():
    if 'session_name' in session:
        return redirect(url_for('profile'))
    request_token = get_request_token()
    session['request_token'] = request_token

    return redirect(get_auth_verifier_url(request_token))


@app.route('/logout')
def twitter_logout():
    session.clear()
    return redirect(url_for('homepage'))


@app.route('/auth/twitter')
def twitter_auth():
    auth_verifier = request.args.get('oauth_verifier')
    access_token = get_access_token(session['request_token'], auth_verifier)

    user = User.load_from_db_by_email(access_token['screen_name'])
    if not user:
        user = User(None, access_token['screen_name'], access_token['oauth_token'],
                    access_token['oauth_token_secret'])
        user.save_to_db()
        session['screen_name'] = user.screen_name
    return redirect(url_for('profile'))  # url_for(method-name to which URL u want to reditect )


@app.route('/profile')
def profile():
    return render_template('profile.html', user=session['screen_name'])


app.run(port=9445, debug=True)
