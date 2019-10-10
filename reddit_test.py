import oauth_utilities
import praw

credentials = oauth_utilities.getCredentials()

reddit = praw.Reddit(client_id=credentials['reddit_client_id'],
                     client_secret=credentials['reddit_client_secret'],
                     password=credentials['reddit_password'],
                     user_agent='test script by /u/like_a_fontanelle',
                     username=credentials['reddit_username'])
print(reddit.user.me())

title = 'Checking for a friend...'
selftext = 'We thought we’d jump on board the API train and show off our first experiences with Warcry! Don’t forget to subscribe and hit the like button if you want to see more! https://youtu.be/-r96UgdB_Jw'
reddit.subreddit('reddit_api_test').submit(title, selftext=selftext)