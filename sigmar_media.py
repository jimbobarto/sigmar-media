from utilities.credentials import Credentials
from channels.twitter_channel import TwitterChannel
from channels.discord_channel import DiscordChannel
from channels.reddit_channel import RedditChannel

#credentials = Credentials().getCredentials()
start = Credentials()
credentials = start.get_credentials()

message = "the fourth message to be shared across multiple platforms"

discord = DiscordChannel()
twitter = TwitterChannel()
reddit = RedditChannel()

discord.send_message(credentials, message)
twitter.send_message(credentials, message)
reddit.send_message(credentials, message)