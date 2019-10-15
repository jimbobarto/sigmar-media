import praw
import channels.channel_utilities as channel_utilities

class RedditChannel:
    def send_message(self, credentials, config, message):

        if (config['stubbed']):
            return {"status": "succeeded", "message": "message posted successfully", "timestamp": channel_utilities.get_timestamp()}
        else:
            reddit = praw.Reddit(client_id=credentials['client_id'],
                                 client_secret=credentials['client_secret'],
                                 password=credentials['password'],
                                 user_agent='test script by ' + credentials['username'],
                                 username=credentials['username'])

            submission = reddit.subreddit('reddit_api_test').submit(message['title'], selftext=message['body'])
            if (submission.permalink):
                return {"status": "succeeded", "message": "message posted successfully", "link": credentials['base_url'] + submission.permalink, "timestamp": channel_utilities.get_timestamp()}
            
            return {"status": "failed", "message": submission, "timestamp": channel_utilities.get_timestamp()}

    def get_channel_name(self):
        return "reddit was ere"