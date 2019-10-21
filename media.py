from importlib import import_module
import os
import re
from flask import Flask
from flask import render_template, request, jsonify, send_from_directory
from os import listdir
from os.path import isfile, join
import json
import sys

import utilities.config

app = Flask(__name__)

channels = {}
hierarchy = {}
base_config = {}
platform_suffix = "_platform"

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

def get_config(root, current_name, platform_config):
	if ('name' in root):
		current_name = form_name(current_name, root['name'])
		platform_config['path'] = current_name

	if ('display_name' in root):
		platform_config['display_name'] = root['display_name']

	if ('config' in root):
		platform_config['config'] = root['config']

	if ('channels' in root):
		for channel in root['channels']:
			if ('name' in channel):
				if ('children' not in platform_config):
					platform_config['children'] = []
				child = {"name": channel['name'], "channel": True, "path": form_name(current_name, channel['name'])}
				if ('config' in channel):
					child['config'] = channel['config']
				platform_config['children'].append(child)

	if ('groups' in root):
		for group in root['groups']:
			if ('name' in group):
				if ('children' not in platform_config):
					platform_config['children'] = []
				child = {"name": group['name'], "channel": False, "path": form_name(current_name, group['name'])}
				child = get_config(group, current_name, child)
				platform_config['children'].append(child)

	return platform_config

def get_all_config():
	platform_config = utilities.config.get_config('.channels')
	global base_config
	base_config = utilities.config.get_config('config/config.json')

	platform_classes = [filename for filename in listdir('platforms') if (re.search(platform_suffix, filename) )]

	credentials = {}
	for media in platform_config:
		credentials[media] = get_credentials(platform_config[media], {}, "", {})	

	for filename in platform_classes:
		filename_without_extension = filename.replace('.py', '')
		platform_name = filename_without_extension.replace(platform_suffix, '')

		platform_driver_found = False
		for config_platform_name in platform_config:
			if (config_platform_name == platform_name):
				channel_driver_found = True
				hierarchy[config_platform_name] = get_config(platform_config[config_platform_name], config_platform_name, {})
				class_name = platform_name.capitalize() + 'Platform'

				mod = import_module(f'platforms.{filename_without_extension}')
				instance = getattr(mod, class_name)

				channels[config_platform_name] = {'instance': instance(), 'config': credentials[config_platform_name], 'hierarchy': hierarchy[config_platform_name]}
				break

		if (channel_driver_found == False):
			print(f'No config for {platform_name} but a driver exists')

	for config_platform_name in platform_config:
		config_platform_found = False
		for filename in platform_classes:
			platform_name = filename.replace(platform_suffix + '.py', '')
			if (config_platform_name == platform_name):
				config_platform_found = True
				break

		if (config_platform_found == False):
			print(f'No driver for {config_platform_name} but config exists')

	return channels



@app.route('/')
def init():
	get_all_config()
	base_config['maximum_characters'] = get_maximum_characters(hierarchy)

	return render_template('main.html', hierarchy = hierarchy, base_config = base_config)

def get_maximum_characters(hierarchy):
	maximum_characters = 0 
	for platform in hierarchy:
		if ('config' in hierarchy[platform] and 'maximum_characters' in hierarchy[platform]['config']):
			if (hierarchy[platform]['config']['maximum_characters'] > maximum_characters):
				maximum_characters = hierarchy[platform]['config']['maximum_characters']	

	return maximum_characters

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/post_message', methods=['POST'])
def post_message():
	body = request.get_json(force=True)

	message = body['message']

	results = {}
	if ( ('title' in message) and ('body' in message) ):
		for requested_channel in body['channels']:
			media = requested_channel.split('.', 1)[0]
			path = requested_channel.replace(f'{media}.', "")

			if (path in channels[media]['config']):
				driver = channels[media]['instance']
				try:
					results[requested_channel] = driver.send_message(channels[media]['config'][path], base_config, message)
				except KeyError as e:
					results[requested_channel] = {"status": "failed", "message": f'Attempt to publish message to {media} at {path} failed {e.message}'}
				except:
					results[requested_channel] = {"status": "failed", "message": f'Attempt to publish message to {media} at {path} failed {sys.exc_info()[0]}\n{sys.exc_info()[1]}\n{sys.exc_info()[2]}'}
	else:
		if ('title' in message):
			results['general'] = {"status": "failed", "message": "Missing message body"}
		else:
			results['general'] = {"status": "failed", "message": "Missing message title"}

	return render_template('results.html', results=results)

@app.route('/format_results')
def format_results():
	results = request.get_json(force=True)
	return render_template('results.html', results=results)


#get_content
@app.route('/get_content', methods=['POST'])
def get_content():
	body = request.get_json(force=True)

	if (body['content'] and body['content'] == "post"):
		get_all_config()
		return render_template('post.html', hierarchy = hierarchy, base_config = base_config)

	if (body['content'] and body['content'] == "calendar"):
		return render_template('calendar.html')
