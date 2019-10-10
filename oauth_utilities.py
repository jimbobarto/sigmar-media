import urllib
import random
import base64
import hmac
import binascii
import time
import collections
import hashlib
import requests
import json

# appropriated from http://mkelsey.com/2013/05/01/authorizing-and-signing-a-twitter-api-call-using-python/
#
# which links to https://github.com/kelsmj/twitter_signature/blob/master/twitter_sign.py
# for the missing definition of collect_parameters()

def generate_signature(method, url, url_parameters, oauth_parameters,
                       oauth_consumer_key, oauth_consumer_secret,
                       oauth_token_secret=None, status=None):
    """Create the signature base string"""

    #Combine parameters into one hash
    temp = collect_parameters(oauth_parameters, status, url_parameters)

    #Create string of combined url and oauth parameters
    parameter_string = stringify_parameters(temp)

    #Create your Signature Base String
    signature_base_string = (
        method.upper() + '&' +
        escape(str(url)) + '&' +
        escape(parameter_string)
    )

    #Get the signing key
    signing_key = create_signing_key(oauth_consumer_secret, oauth_token_secret)

    return calculate_signature(signing_key, signature_base_string)

def stringify_parameters(parameters):
    """Orders parameters, and generates string representation of parameters"""
    output = ''
    ordered_parameters = {}
    ordered_parameters = collections.OrderedDict(sorted(parameters.items()))

    counter = 1
    for k, v in ordered_parameters.iteritems():
        output += escape(str(k)) + '=' + escape(str(v))
        if counter < len(ordered_parameters):
            output += '&'
            counter += 1

    return output

def create_signing_key(oauth_consumer_secret, oauth_token_secret=None):
    """Create key to sign request with"""
    signing_key = escape(oauth_consumer_secret) + '&'

    if oauth_token_secret is not None:
        signing_key += escape(oauth_token_secret)

    return signing_key

def calculate_signature(signing_key, signature_base_string):
    """Calculate the signature using SHA1"""
    hashed = hmac.new(signing_key, signature_base_string, hashlib.sha1)

    sig = binascii.b2a_base64(hashed.digest())[:-1]

    return escape(sig)

def collect_parameters(oauth_parameters, status, url_parameters):
    """Combines oauth, url and status parameters"""
    #Add the oauth_parameters to temp hash
    temp = oauth_parameters.copy()

    #Add the status, if passed in.  Used for posting a new tweet
    if status is not None:
        temp['status'] = status

    #Add the url_parameters to the temp hash
    for k, v in url_parameters.iteritems():
        temp[k] = v

    return temp

def create_auth_header(parameters):
    """For all collected parameters, order them and create auth header"""
    ordered_parameters = {}
    ordered_parameters = collections.OrderedDict(sorted(parameters.items()))
    auth_header = (
        '%s="%s"' % (k, v) for k, v in ordered_parameters.iteritems())
    val = "OAuth " + ', '.join(auth_header)
    return val

def get_oauth_parameters(consumer_key, access_token):
    """Returns OAuth parameters needed for making request"""
    oauth_parameters = {
        'oauth_timestamp': str(int(time.time())),
        'oauth_signature_method': "HMAC-SHA1",
        'oauth_version': "1.0",
        'oauth_token': access_token,
        'oauth_nonce': get_nonce(),
        'oauth_consumer_key': consumer_key
    }

    return oauth_parameters

def get_nonce():
    """Unique token generated for each request"""
    n = base64.b64encode(
        ''.join([str(random.randint(0, 9)) for i in range(24)]))
    return n

def escape(s):
    """Percent Encode the passed in string"""
    return urllib.quote(s, safe='~')

def get_response_parameters(response):
    parameters = {}
    parameter_list = response.split("&")
    for parameter in parameter_list:
        if "=" in parameter:
            key_and_value = parameter.split("=")
            parameters[key_and_value[0]] = key_and_value[1]

    return parameters

def getCredentials():
    with open('.credentials') as json_file:  
        credentials = json.load(json_file)

    return credentials


#oauth_token=6253282-eWudHldSbIaelX7swmsiHImEL4KinwaGloHANdrY
#oauth_token_secret=2EEfA6BG3ly3sR3RjE0IBSnlQu4ZrUzPiYKmrkVU
#user_id=6253282&screen_name=twitterapi

