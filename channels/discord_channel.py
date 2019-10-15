import requests
import json
import channels.channel_utilities as channel_utilities

class DiscordChannel:
   def send_message(self, credentials, config, message):

        if (config['stubbed']):
            return {"status": "succeeded", "message": "message posted successfully", "timestamp": channel_utilities.get_timestamp()}
        else:
            payload = {"content":message['body'], "username":"Something else", "avatar_url":""}
            headers = {'Content-type': 'application/json'}

            response = requests.post(credentials['webhook'], data=json.dumps(payload), headers=headers)
            if (response.status_code == 204):
                return {"status": "succeeded", "message": "message posted successfully", "timestamp": channel_utilities.get_timestamp()}
            
            return {"status": "failed", "message": response.reason, "timestamp": channel_utilities.get_timestamp()}

   def get_channel_name(self):
      return "discord"