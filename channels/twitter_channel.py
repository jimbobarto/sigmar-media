from twitter import *

class TwitterChannel:
	def send_message(self, credentials, message):

		t = Twitter(
    		auth=OAuth(credentials['access_token'], credentials['access_token_secret'], credentials['consumer_key'], credentials['consumer_secret'])
    	)

		response = t.statuses.update(status=message['body'])
		print(response)

	def get_channel_name(self):
		return "twitter"