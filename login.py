import json
import urllib.parse as urlparse
from user import User
from database import Database
import constants
import oauth2
from twitter_utils import consumer, get_request_token, get_auth_verifier,get_access_token

Database.initilize(database="test",
                   user="postgres",
                   password="password",
                   host="localhost")

email = input('Enter your email: ')
user = User.load_from_db_by_email(email)
print(user)
if not user:
    request_token = get_request_token()

    # ask user to authorize app nd give the pin code
    oath_verifier = get_auth_verifier(request_token)

    # create a token object using req token and verifier
    access_token= get_access_token(request_token,oath_verifier)

    first_name = input('Enter First name: ')
    last_name = input('Enter Last Name: ')

    user = User(None, email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'])
    user.save_to_db()

# create an authrized token
# User.twitter_request('https://stream.twitter.com/1.1/statuses/sample.json', 'GET', consumer)
tweets = json.loads(
    User.twitter_request('https://api.github.com/users?since=1', 'GET'))
