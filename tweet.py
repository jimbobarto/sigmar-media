import twitter
import oauth_utilities

credentials = oauth_utilities.getCredentials()

api = twitter.Api(consumer_key=credentials['twitter_consumer_key'],
                      consumer_secret=credentials['twitter_consumer_secret'],
                      access_token_key=credentials['access_token'],
                      access_token_secret=credentials['access_token_secret'])

status = api.PostUpdate('The Agents of Sigmar are testing')
print(status.text)
