import oauth_utilities
import facebook

#credentials = oauth_utilities.getCredentials()

graph = facebook.GraphAPI(access_token="EAAUoBjqafjgBANYWrG3CPYFvrzm41Tt0ZAnZCkqVEpKBD5XafmksTzdK03Hrysr5S2PZB5lxZCWDRx06kq31xZBwgVAfJ41q2ZCqsNtqUhzfZBYrYMho502r5M5dOtDKBB3ZAfdWU8r6U9B6llfmZCOZBbCosvnbrY30MZD")
print graph

graph.put_object("me", "feed", message="Just testing, nothing to see here...")
