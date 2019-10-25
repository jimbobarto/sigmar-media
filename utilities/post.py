import sys
import os

def post_message(message, channels, base_config):
	base_config['cwd'] = os.getcwd()

	results = {}
	if ( ('title' in message['message']) and ('body' in message['message']) and ('channels' in message) ):
		for requested_channel in message['channels']:
			media = requested_channel.split('.', 1)[0]
			path = requested_channel.replace(f'{media}.', "")

			if (path in channels[media]['credentials']):
				driver = channels[media]['instance']
				try:
					results[requested_channel] = driver.send_message(channels[media]['credentials'][path], base_config, message['message'])
				except KeyError as e:
					results[requested_channel] = {"status": "failed", "message": f'Attempt to publish message to {media} at {path} failed {str(e)}'}
				except:
					results[requested_channel] = {"status": "failed", "message": f'Attempt to publish message to {media} at {path} failed {sys.exc_info()[0]}\n{sys.exc_info()[1]}\n{sys.exc_info()[2]}'}
	else:
		error_messages = []
		if ('title' not in message['message']):
			error_messages.append("missing message title")
		if ('body' not in message['message']):
			error_messages.append("missing message body")
		if ('channels' not in message):
			error_messages.append("missing channel info")
		results['general'] = {"status": "failed", "message": ', '.join(error_messages)}

	return results

