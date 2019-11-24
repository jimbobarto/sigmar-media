import sys
import os
from os import listdir
from os.path import isfile, join
from crontab import CronTab
from datetime import datetime
import pytz
import logging

import utilities.config

logging.basicConfig(filename='media.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

def get_events(start, end):
	cwd = os.getcwd()

	path = cwd + '/scheduling/posts'
	scheduled_files = get_scheduled_files(path)

	cron = CronTab(user=True)
	valid_files = compare_files_to_cron(cron, scheduled_files)
	compare_cron_to_files(cron, scheduled_files)

	utc=pytz.UTC

	events = []
	for file in valid_files:
		try:
			post_details = utilities.config.get_config(f"{path}/{file}")

			# you can only compare date_time objects if they are both naive or aware...
			# https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end/32926295
			date_time = datetime.strptime(post_details['dateTime'], '%d/%m/%Y %H:%M').replace(tzinfo=utc)

			if (date_time > start and date_time < end):
				events.append(build_event(post_details, date_time, date_time))
		except:
			print(f'{sys.exc_info()[0]}\n{sys.exc_info()[1]}\n{sys.exc_info()[2]}')

	return events

def build_event(post_file_contents, start, end):
	date_time_format = '%Y-%m-%dT%H:%M:%S'
	return {"title": post_file_contents['message']['title'], "start": start.strftime(date_time_format), "end": end.strftime(date_time_format)}

def get_scheduled_files(path):
	all_files = [f for f in listdir(path) if isfile(join(path, f))]
	scheduled_files = []
	for file_name in all_files:
		if ('.json' in file_name):
			scheduled_files.append(file_name)

	return scheduled_files


def compare_files_to_cron(cron, scheduled_files):
	valid_files = []
	for job in cron:
		job_has_matching_file = False
		cron_file_equivalent = f"{job.minute}_{job.hour}_{job.day}_{job.month}"
		for file in scheduled_files:
			file_cron_equivalent = file.replace('.json', '')
			if (cron_file_equivalent == file_cron_equivalent):
				job_has_matching_file = True
				valid_files.append(file)
				break

		if (not job_has_matching_file):
			logging.error(f"Cron job '{job}' does not have a matching post file")

	return valid_files

def compare_cron_to_files(cron, scheduled_files):
	valid_files = []
	for file in scheduled_files:
		file_cron_equivalent = file.replace('.json', '')
		file_has_matching_cron = False

		for job in cron:
			cron_file_equivalent = f"{job.minute}_{job.hour}_{job.day}_{job.month}"
			if (cron_file_equivalent == file_cron_equivalent):
				file_has_matching_cron = True
				valid_files.append(file)
				break

		if (not file_has_matching_cron):
			logging.error(f"File '{file}' does not have a matching cron entry")

	return valid_files	