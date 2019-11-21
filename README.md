# Sigmar Media

A very (very) simple tool for posting updates to multiple social media channels. It currently supports Discord, Reddit and Twitter. And Facebook, although this is via Selenium and I don't like to talk about that.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for all purposes. This tool is not currently intended to be deployed on a live system. Please note this was written in Python3.

### Prerequisites

You will need to install the following modules for the base system:
* flask
* datetime

And then whatever you need for the channels. The base implementation has:
* praw
* python-twitter
* requests (the Discord channel currently makes a simple request to each channel via a webhook)
* selenium (Facebook - just don't ask...)

If you have pip installed, this can be achieved with

```
pip install -r requirements.txt
```

in the top-level project directory.

### Installing

Clone the repository and install the modules listed above. You will also need the Chrome webdriver placed in the drivers/ subdirectory.

On mac you may wish to grant terminal 'Full Disk Access' in order to prevent pop-ups, but this obviously has security implications.

Once you've got that (assuming you want to post to Facebook as well) you can run the app as per any flask app

Install virtualenv (if you see 'python2' or 'python3' in any of these instructions, just type 'python'):
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

## Configuration

The bulk of the config is in .channels at the top level of the project (a json file). An example is provided in the examples/ directory.

The top level map has keys as the social media platform names (e.g. twitter). These keys must match to platform names in the platforms/ directory (e.g. twitter_platform.py) for a platform to have both driver and config.
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
```

### Credentials
The 'credentials' maps have special functionality. They are aggregated as you traverse the config, so a channel nested within groups will have credentials built up (conceivably) from the top level, each ancestor group and the channel itself. This allows you to have config that spans a platform along with config specific to the channel.
```
"discord": {
   "credentials": {
      "credential_item_1": "credential_value_1"
   },
   "groups": [
      {
         "credentials": {
            "credential_item_2": "credential_value_2"
         },
         "name": "<server name>",
         "channels": [
            {
               "name: "general",
               "credentials": {
                  "credential_item_3": "credential_value_3"
               }
            }
         ]
      }
   ]
}
```
the above credentials hierarchy results in the following set of credentials below
```
{
   "credential_item_1": "credential_value_1",
   "credential_item_2": "credential_value_2",
   "credential_item_3": "credential_value_3"
}
```

'config' maps on the other hand are not aggregated and just apply at the level they are found.
