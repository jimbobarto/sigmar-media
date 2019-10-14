import praw

class RedditChannel:
	def send_message(self, credentials, message):

		reddit = praw.Reddit(client_id=credentials['client_id'],
		                     client_secret=credentials['client_secret'],
		                     password=credentials['password'],
		                     user_agent='test script by ' + credentials['username'],
		                     username=credentials['username'])

		reddit.subreddit('reddit_api_test').submit(message['title'], selftext=message['body'])

	def get_channel_name(self):
		return "reddit was ere"