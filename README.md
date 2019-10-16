# Sigmar Media

A very (very) simple tool for posting updates to multiple social media channels. It currently supports Discord, Reddit and Twitter.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for all purposes. This tool is not currently intended to be deployed on a live system. Please note this was written in Python3.

### Prerequisites

You will need to install the following modules for the base system:
* importlib
* os
* re
* flask
* json
* sys
* time
* datetime

And then whatever you need for the channels. The base implementation has:
* praw
* python-twitter
* requests (the Discord channel currently makes simple requests to a webhook per channel)


### Installing

Once you've cloned the repository and installed the modules listed above, you can run the app as per any flask app

Once you've cloned this repository locally, install virtualenv (if you see 'python2' or 'python3' in any of these instructions, just type 'python'):
http://flask.pocoo.org/docs/1.0/installation/#install-install-virtualenv

Now (as per http://flask.pocoo.org/docs/1.0/installation/#python-version):

cd into the project directory and run the following commands

```
virtualenv venv
```
```
. venv/bin/activate
```
```
export FLASK_APP=media.py
```

You should be ready to go now...

Just type:
```
flask run
```

### Configuring

The bulk of the config is in .channels at the top level of the project (a json file). An example is provided in the examples/ directory.

The top level map has keys as the social media channel names (e.g. twitter). These keys must match to channel names in the channels/ directory (e.g. twitter_channel.py) for a channel to have both driver and config.
```
{
  "discord": {...}
  "reddit": {...}
  "twitter": {...}
}
```

Each social media channel in config can then have an list of 'groups' (which can be nested arbitrarily). These structures can be used to correspond to concepts within the particular social media channel. The best example is in this tool's implementation of Discord. Each group corresponds to a server.
```
"discord": {
   "groups": [
      {
         "name": "<server name>",
         "channels": [...]
      }
   ]
}
```

Finally, each level of the config (e.g. top level or within a 'group') can have a list of 'channels'. Each 'channel' represents the actual 'thing' the tool will post to, e.g. subreddit, twitter user's status or discord text channel.
```
{
  "twitter": {
     "channels": [
        {
           "name": "<twitter user name>"
        }
     ]
  }
}



The 'credentials' maps have special functionality. They are aggregated as you traverse the config, so a channel nested with groups will have credentials built up (conceivably) from the top level, each ancestor group and the channel itself. This allows you to have config that spans a channel alongw ith config specific to the channel.

'config' maps on the other hand are not aggregated and just apply at the level they are found.
