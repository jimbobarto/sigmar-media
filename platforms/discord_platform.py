import requests
import json
import platforms.platform_utilities as platform_utilities

class DiscordPlatform:
   def send_message(self, credentials, config, message):

        if (config['stubbed']):
            return {"status": "succeeded", "message": "message posted successfully", "timestamp": platform_utilities.get_timestamp()}
        else:
            payload = {"content":message['body'], "username":"Something else", "avatar_url":""}
            headers = {'Content-type': 'application/json'}

            response = requests.post(credentials['webhook'], data=json.dumps(payload), headers=headers)
            if (response.status_code == 204):
                return {"status": "succeeded", "message": "message posted successfully", "timestamp": platform_utilities.get_timestamp()}
            
            return {"status": "failed", "message": response.reason, "timestamp": platform_utilities.get_timestamp()}

   def get_platform_name(self):
      return "discord"