import json
from os import listdir
from os.path import isfile, join
import re
from importlib import import_module

credentials_file = '.credentials'
channels_file = '.channels'
config_file = 'config/config.json'
platform_suffix = "_platform"

def get_credentials():
    return get_config(credentials_file)

def get_config(filePath):
    with open(filePath) as json_file:  
        credentials = json.load(json_file)

    return credentials

def form_name(current_name_path, new_name):
    if (current_name_path == ""):
        return new_name
    return current_name_path + '.' + new_name

def get_platform_credentials(root, current_credentials, current_name, channel_credentials):
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
                channel_credentials = get_platform_credentials(group, current_credentials, current_name, channel_credentials)

    return channel_credentials

def get_platform_config(root, current_name, platform_config):
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
                child = get_platform_config(group, current_name, child)
                platform_config['children'].append(child)

    return platform_config

def get_base_config():
    return get_config(config_file)

def get_channel_config():
    platform_config = get_config(channels_file)

    platform_classes = [filename for filename in listdir('platforms') if (re.search(platform_suffix, filename) )]

    channels = {}

    for filename in platform_classes:
        filename_without_extension = filename.replace('.py', '')
        platform_name = filename_without_extension.replace(platform_suffix, '')

        platform_driver_found = False
        for config_platform_name in platform_config:
            if (config_platform_name == platform_name):
                channel_driver_found = True
                class_name = platform_name.capitalize() + 'Platform'

                mod = import_module(f'platforms.{filename_without_extension}')
                instance = getattr(mod, class_name)

                channels[config_platform_name] = {'instance': instance(), 'credentials': get_platform_credentials(platform_config[config_platform_name], {}, "", {})}
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

def get_channel_hierarchy():
    platform_config = get_config(channels_file)

    platform_classes = [filename for filename in listdir('platforms') if (re.search(platform_suffix, filename) )]

    hierarchy = {}
    for filename in platform_classes:
        filename_without_extension = filename.replace('.py', '')
        platform_name = filename_without_extension.replace(platform_suffix, '')

        for config_platform_name in platform_config:
            if (config_platform_name == platform_name):
                hierarchy[config_platform_name] = get_platform_config(platform_config[config_platform_name], config_platform_name, {})
                break

    return hierarchy
