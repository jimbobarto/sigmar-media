from importlib import import_module
import utilities.config
import os
import re
from flask import Flask
from flask import render_template, request, jsonify, send_from_directory
from os import listdir
from os.path import isfile, join
import json
app = Flask(__name__)

channels = {}
hierarchy = {}

def form_name(current_name_path, new_name):
	if (current_name_path == ""):
		return new_name
	return current_name_path + '.' + new_name

def get_credentials(root, current_credentials, current_name, channel_credentials):
	if ('name' in root):
		current_name = form_name(current_name, root['name'])

	if ('credentials' in root):
		current_credentials.update(root['credentials'])

	if ('channels' in root):
		for channel in root['channels']:
			if ('name' in channel):
				current_channel_credentials = current_credentials.copy()
				if ('credentials' in channel):
					current_channel_credentials.update(channel['credentials'])

				channel_credentials[form_name(current_name, channel['name'])] = current_channel_credentials

	if ('groups' in root):
		for group in root['groups']:
			if ('name' in group):
				channel_credentials = get_credentials(group, current_credentials, current_name, channel_credentials)

	return channel_credentials

def get_hierarchy(credentials):
	hierarchy = {}
	top = hierarchy
	for path in credentials:
		names = path.split('.')
		for name in names:
			if (name not in hierarchy):
				hierarchy[name] = {}

			hierarchy = hierarchy[name]

		hierarchy = top

	return top

def get_all_config():
	channel_config = utilities.config.get_config('.channels')

	channel_classes = [filename for filename in listdir('channels') if (re.search('_channel', filename) )]

	credentials = {}
	for media in channel_config:
		credentials[media] = get_credentials(channel_config[media], {}, "", {})	
		hierarchy[media] = get_hierarchy(credentials[media])	

	for filename in channel_classes:
		filename_without_extension = filename.replace('.py', '')
		channel_name = filename_without_extension.replace('_channel', '')

		channel_driver_found = False
		for config_channel_name in channel_config:
			if (config_channel_name == channel_name):
				channel_driver_found = True
				class_name = channel_name.capitalize() + 'Channel'

				mod = import_module(f'channels.{filename_without_extension}')
				instance = getattr(mod, class_name)

				channels[config_channel_name] = {'instance': instance(), 'config': credentials[config_channel_name], 'hierarchy': hierarchy[config_channel_name]}
				break

		if (channel_driver_found == False):
			print(f'No config for {channel_name} but a driver exists')

	for config_channel_name in channel_config:
		config_channel_found = False
		for filename in channel_classes:
			channel_name = filename.replace('_channel.py', '')
			if (config_channel_name == channel_name):
				config_channel_found = True
				break

		if (config_channel_found == False):
			print(f'No driver for {config_channel_name} but config exists')

	return channels



@app.route('/')
def init():
	get_all_config()
	return render_template('main.html', hierarchy=json.dumps(hierarchy, ensure_ascii=False, indent=3))

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')




