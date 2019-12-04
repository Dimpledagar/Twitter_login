import oauth2
import constants
import urllib.parse as urlparse

consumer = oauth2.Consumer(constants.CONSUMER_KRY, constants.CONSUMER_SECRET)


def get_request_token():
    client = oauth2.Client(consumer)
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status != 200:
        print('An error occurred getting the request token from twitter!')

    return dict(urlparse.parse_qsl(content.decode('UTF-8')))


def get_auth_verifier(request_token):
    print('Go to the following site for pin: ')
    print(get_auth_verifier_url())
    return input('Please enter pin: ')


def get_auth_verifier_url(request_token):
    return '{}?oauth_token={}'.format(constants.AUTHORIZATION_URL, request_token['oauth_token'])


def get_access_token(request_token, oath_verifier):
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oath_verifier)

    # create a client with newly craeted token
    client = oauth2.Client(consumer, token)

    # ask twitter for an access token, as we have verified the req token
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    return dict(urlparse.parse_qsl(content.decode('UTF-8')))
