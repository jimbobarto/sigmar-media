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
