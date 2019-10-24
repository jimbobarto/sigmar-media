import utilities.config
import facebook

channel_config = utilities.config.get_config('.channels')
access_token = channel_config['facebook']['channels'][0]['credentials']['facebook_access_token']

graph = facebook.GraphAPI(access_token=access_token)
print(graph)

graph.put_object("me", "feed", message="Just testing, nothing to see here...")
