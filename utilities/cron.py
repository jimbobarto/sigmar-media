import sys
import os
import json
from datetime import datetime
from crontab import CronTab

import utilities.config

#print(sys.executable)
#print( os.path.dirname(sys.executable) )

#print(os.path.realpath(__file__) )
#print( os.path.dirname(os.path.realpath(__file__)) )

def schedule_message(message, channels, base_config):
    print(message)
    path_addition = os.path.dirname(sys.executable)
    main_directory = os.path.dirname(os.path.realpath(__file__)) + "/.."

    date_time = get_date_time(message['dateTime'])
    filename = get_cron_filename(date_time)
    create_message_file(message, main_directory, filename)

    add_command_to_cron(date_time, create_cron_command(main_directory, path_addition, filename))

def create_cron_command(main_directory, path_addition, filename):
    wrapper_script = get_wrapper_script_name()
    return f'{main_directory}/{wrapper_script} "{path_addition}" "{main_directory}" "{filename}"'

def get_wrapper_script_name():
    platform = sys.platform
    base_config = utilities.config.get_base_config()

    if (base_config['scheduling_wrappers'][platform]):
        return base_config['scheduling_wrappers'][platform]['location']
    else:
        print(f"no wrapper script found for {platform}")

def add_command_to_cron(date_time, command):
    cron_string = get_cron_timestamp(date_time)

    cron = CronTab(user=True)
    job  = cron.new(command=command)
    job.setall(cron_string)
    cron.write()

def get_date_time(date_time_string):
    return datetime.strptime(date_time_string, '%d/%m/%Y %H:%M')

def create_message_file(message, main_directory, filename):
    message_details = create_message_json(message)
    if ('error' in message_details):
        return message_details

    file = open(main_directory + '/scheduling/posts/' + filename, "w")
    file.write(json.dumps(message_details))
    file.close()

    return filename

def get_cron_filename(date_time):

    filename = f"{date_time.minute}_{date_time.hour}_{date_time.day}_{date_time.month}.json"
    return filename

def get_cron_timestamp(date_time):

    cron_string = f"{date_time.minute} {date_time.hour} {date_time.day} {date_time.month} *"
    return cron_string

def create_message_json(message):
    message_details = {}
    channel_paths = []
    if ( ('title' in message['message']) and ('body' in message['message']) and ('channels' in message) ):
        message_details['message'] = {'title': message['message']['title'], 'body': message['message']['body']}
        message_details['channels'] = message['channels']
        message_details['dateTime'] = message['dateTime']

    else:
        error_messages = []
        if ('title' not in message['message']):
            error_messages.append("missing message title")
        if ('body' not in message['message']):
            error_messages.append("missing message body")
        if ('channels' not in message):
            error_messages.append("missing channel info")
        message_details['error'] = ', '.join(error_messages)

    return message_details
