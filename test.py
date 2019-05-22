import base64
import json
import requests

def getCredentials():
    with open('.credentials') as json_file:  
        credentials = json.load(json_file)

    return credentials

def getEncodedKey(client_key, client_secret):
    #Reformat the keys and encode them
    key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')

    # Transform from bytes to bytes that can be printed
    b64_encoded_key = base64.b64encode(key_secret)

    #Transform from bytes back into Unicode
    return b64_encoded_key.decode('ascii')



credentials = getCredentials()
b64_encoded_key = getEncodedKey(credentials['client_key'], credentials['client_secret_key'])

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
auth_data = {
    'grant_type': 'client_credentials'
}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
print(auth_resp.status_code)
access_token = auth_resp.json()['access_token']
print(access_token)

