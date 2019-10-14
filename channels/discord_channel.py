import requests
import json

class DiscordChannel:
	def send_message(self, credentials, message):

		payload = {"content":message['body'], "username":"Something else", "avatar_url":""}
		headers = {'Content-type': 'application/json'}

		response = requests.post(credentials['webhook'], data=json.dumps(payload), headers=headers)
		print(response.status_code)
		print(response.reason)
		print(response.text)

	def get_channel_name(self):
		return "discord"