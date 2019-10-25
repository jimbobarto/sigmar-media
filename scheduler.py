import argparse
import json

import utilities.config
import utilities.post

posts_directory = 'scheduled_posts/'

parser = argparse.ArgumentParser()
parser.add_argument("--f")

args = parser.parse_args()
post_file = args.f
body = utilities.config.get_config(posts_directory + post_file)

channels = utilities.config.get_channel_config()
base_config = utilities.config.get_base_config()
results = utilities.post.post_message(body, channels, base_config)
print(results)
