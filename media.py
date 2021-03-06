import os
from flask import Flask
from flask import render_template, request, jsonify, send_from_directory
import json
from datetime import datetime

import utilities.config
import utilities.post
import utilities.cron
import utilities.events

app = Flask(__name__)

channels = {}
hierarchy = {}
base_config = {}
platform_suffix = "_platform"

def get_all_config():
	global base_config
	base_config = utilities.config.get_base_config()

	global channels
	channels = utilities.config.get_channel_config()

	global hierarchy
	hierarchy = utilities.config.get_channel_hierarchy()

	base_config['maximum_characters'] = get_maximum_characters(hierarchy)

@app.route('/')
def init():
	get_all_config()

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
	message_details = request.get_json(force=True)

	results = utilities.post.post_message(message_details, channels, base_config)
	return render_template('results.html', results=results)

@app.route('/schedule_message', methods=['POST'])
def schedule_message():
	message_details = request.get_json(force=True)

	results = utilities.cron.schedule_message(message_details, channels, base_config)
	return render_template('results.html', results=results)

@app.route('/format_results')
def format_results():
	results = request.get_json(force=True)
	return render_template('results.html', results=results)

@app.route('/get_content', methods=['POST'])
def get_content():
	body = request.get_json(force=True)

	if (body['content'] and body['content'] == "post"):
		get_all_config()
		return render_template('post.html', hierarchy = hierarchy, base_config = base_config)

	if (body['content'] and body['content'] == "calendar"):
		return render_template('calendar.html')

@app.route('/get_events')
def get_events():
    start_date_time = datetime.strptime(request.args.get('start'), "%Y-%m-%dT%H:%M:%S%z")
    end_date_time = datetime.strptime(request.args.get('end'), "%Y-%m-%dT%H:%M:%S%z")

    events = utilities.events.get_events(start_date_time, end_date_time)

    return app.response_class(json.dumps(events), content_type='application/json')

@app.route('/event')
def get_event():
	filename = request.args.get('file')
	event_data = utilities.events.get_event_data(filename)

	return app.response_class(json.dumps(event_data), content_type='application/json')

@app.route('/event', methods=['DELETE'])
def delete_event():
	filename = request.args.get('file')
	results = utilities.events.delete_event(filename)

	return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
