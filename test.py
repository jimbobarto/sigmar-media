from requests_oauthlib import OAuth1Session

import json
import requests
import oauth_utilities
import sys


REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'

credentials = oauth_utilities.getCredentials()

oauth_client = OAuth1Session(credentials['twitter_consumer_key'], client_secret=credentials['twitter_consumer_secret'], callback_uri='oob')

print('\nRequesting temp token from Twitter...\n')

resp = oauth_client.fetch_request_token(REQUEST_TOKEN_URL)

url = oauth_client.authorization_url(AUTHORIZATION_URL)

print('\nGo to {u}'.format(u=url))

verifier = raw_input('Please enter the verifier code (q to quit):\n')
if verifier == 'q':
    sys.exit(1)
else:
    oauth_client = OAuth1Session(credentials['twitter_consumer_key'], client_secret=credentials['twitter_consumer_secret'],
                                 resource_owner_key=resp.get('oauth_token'),
                                 resource_owner_secret=resp.get('oauth_token_secret'),
                                 verifier=verifier)

try:
    resp = oauth_client.fetch_access_token(ACCESS_TOKEN_URL)
except ValueError as e:
    raise 'Invalid response from Twitter requesting temp token: {0}'.format(e)

print('''Your tokens/keys are as follows:
    access_token_key     = {atk}
    access_token_secret  = {ats}'''.format(
        atk=resp.get('oauth_token'),
        ats=resp.get('oauth_token_secret')))


'''
print('1. Get request token')
print('2. Get auth token')
choice = raw_input('Please choose your auth operation (q to quit):\n')
if choice == 'q':
    print
    sys.exit(1)
elif choice == '1':
    get_request_token(base_url)
elif choice == '2':
    get_auth_token(base_url)
else:
    print('Unknown option')
    sys.exit(1)
'''

