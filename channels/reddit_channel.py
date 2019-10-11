import praw

class RedditChannel:
	def send_message(self, credentials, message):

		reddit = praw.Reddit(client_id=credentials['reddit_client_id'],
		                     client_secret=credentials['reddit_client_secret'],
		                     password=credentials['reddit_password'],
		                     user_agent='test script by ' + {credentials['reddit_username']},
		                     username=credentials['reddit_username'])

		title = 'Multiple channel messages'
		reddit.subreddit('reddit_api_test').submit(title, selftext=message)

	def get_channel_name(self):
		return "reddit was ere"