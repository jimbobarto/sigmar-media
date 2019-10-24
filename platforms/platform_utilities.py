import time
import datetime
import os

def get_timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def add_to_path(new_path):
    os.environ["PATH"] += os.pathsep + new_path

