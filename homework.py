#!/usr/bin/env python

import requests
from requests_oauthlib import OAuth1
import json
import time
import random
import datetime as dt
import argparse

# Take the info from the command line input
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-c', type=str, help="class")
parser.add_argument('-a', type=str, help="assignment")
args = parser.parse_args()

# Parse arguments
group = args.c
TITLE = args.a

# Set class_id so things get posted to the right spot
if group == '6':
	class_id = '1178062708'
elif group == '7':
	class_id = '1178062718'
elif group == '9':
	class_id = '1178062730'
elif group == '11':
	class_id = '1178062696'		
elif group == '12':
	class_id = '1178062686'
elif group == '13':
	class_id = '1235289292'	
else:
	print "Class error!"
# 	sys.exit	

# Set some initial stuff up
group_meetings = {}
today = dt.datetime.now()

# Get my list of classes
with open('timetable.csv') as f:
	dates = f.readlines()
	for line in dates:
		# Split and name variables
		info = line.split(",")
		level = info[3]
		day = info[0]
		start_time = info[1]
		grade = level.split(" ")[-1].strip('\n')
		
		# Check if the day has passed
		dt_day = dt.datetime.strptime(day, '%m-%d-%y')
		difference = dt_day - today
		
		# If the grade is the same and time > 0, write to new dictionary
		if grade == group and difference > dt.timedelta(minutes=0):
			group_meetings.setdefault(difference,[]).append(day)
			group_meetings.setdefault(difference,[]).append(start_time)
			
			
# Find the next meeting time
idx = min(group_meetings)
next_meeting_time = group_meetings[idx][1]


# Convert day to proper format
meeting_day_string = group_meetings[idx][0]
informat = '%m-%d-%y'
the_day = dt.datetime.strptime(meeting_day_string, informat)
outformat = '%Y-%m-%d'
next_meeting_day = the_day.strftime(outformat)		
DUE = next_meeting_day+' '+next_meeting_time	
print DUE
	

# API information and initial settings
KEY = 'YOUR_KEY'
SECRET = 'YOUR_SECRET'
AUTH = OAuth1(KEY, SECRET, '', '')
NONCE = ''.join([str(random.randint(0, 9)) for i in range(16)])
TIMESTAMP = str(int(time.time()))


# Headers for schoology 
HEADERS = {
	 'realm' : 'Schoology API',
	 'oauth_consumer_key' : KEY,
	 'oauth_token' : '',
	 'oauth_nonce' : NONCE,
	 'oauth_timestamp' : TIMESTAMP,
	 'oauth_signature_method' : 'PLAINTEXT',
	 'oauth_version' : '1.0',
	 'oauth_signature' : SECRET,
	 'content-type': 'application/json'
	 }


# The assignment that gets posted
payload = {
    "title": TITLE,
    "description": "",
    "due": DUE,
    "grading_scale": "0",
    "grading_period": "0",
    "grading_category": "0",
    "max_points": "0",
    "factor": "1",
    "is_final": "0",
    "show_comments": "0",
    "grade_stats": "0",
    "allow_dropbox": "0",
    "allow_discussion": "1",
    "published": 1,
    "type": "assignment"
    }


# Convert to JSON for posting
DATA = json.dumps(payload)
url =  'https://api.schoology.com/v1/sections/%s/assignments' %class_id


print requests.post(url,data=DATA,headers=HEADERS,auth=AUTH)


