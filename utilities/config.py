import json

def get_credentials():
    return get_config('.credentials')

def get_config(filePath):
    with open(filePath) as json_file:  
        credentials = json.load(json_file)

    return credentials
