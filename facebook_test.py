import oauth_utilities
import facebook

credentials = oauth_utilities.getCredentials()

graph = facebook.GraphAPI(access_token=credentials['facebook_access_token'])
print(graph)

graph.put_object("me", "feed", message="Just testing, nothing to see here...")
