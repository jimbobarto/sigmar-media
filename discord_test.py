import requests
import oauth_utilities
import json

credentials = oauth_utilities.getCredentials()

payload = {"content":"Message is here 3","username":"Something else","avatar_url":""}
headers = {'Content-type': 'application/json'}

response = requests.post(credentials['discord_webhook'], data=json.dumps(payload), headers=headers)
print(response.status_code)
print(response.reason)
print(response.text)