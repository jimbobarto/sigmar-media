from twitter import *
import channels.channel_utilities as channel_utilities

class TwitterChannel:
    #https://python-twitter.readthedocs.io/en/latest/getting_started.html

    def send_message(self, credentials, config, message):

        if (config['stubbed']):
            return {"status": "succeeded", "message": "message posted successfully", "timestamp": channel_utilities.get_timestamp()}
        else:
            t = Twitter(
                auth=OAuth(credentials['access_token'], credentials['access_token_secret'], credentials['consumer_key'], credentials['consumer_secret'])
            )

            response = t.statuses.update(status=message['body'])
            if ('id' in response):
                link = credentials['base_url'] + '/status/' + response['id_str']
                return {"status": "succeeded", "message": "message posted successfully", "link": link, "timestamp": channel_utilities.get_timestamp()}
            
            return {"status": "failed", "message": response['text'], "timestamp": channel_utilities.get_timestamp()}                

    def get_channel_name(self):
        return "twitter"