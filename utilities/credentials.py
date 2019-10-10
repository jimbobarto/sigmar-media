import json

class Credentials:
    def get_credentials(self):
        with open('.credentials') as json_file:  
            credentials = json.load(json_file)

        return credentials
