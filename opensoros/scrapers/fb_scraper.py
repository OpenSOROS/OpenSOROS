import urllib.request
import re
import json
from datetime import datetime
import csv
import time
import sys
import os
import os.path

#You'll need to get your own access token 
try:
	from . import config
except Exception as e:
	pass
#from config import ACCESS_TOKEN


BASE = "https://graph.facebook.com/v2.9"

DATA_DIR = "../data"
HEADERS = ["message", "id", "date"]

def get_json_from_request(node, fields, parameters):
	url = BASE + node + fields + parameters
	
	# retrieve data
	response = urllib.request.urlopen(url)
	data = json.loads(unicode_normalize(response.read().decode(response.headers.get_content_charset())))
	return data


def unicode_normalize(text):
	return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22,
							0xa0:0x20 })

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
	enc = file.encoding
	if enc == 'UTF-8':
		print(*objects, sep=sep, end=end, file=file)
	else:
		f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
		print(*map(f, objects), sep=sep, end=end, file=file)

def get_datetime_from_string(dt):


	result = None

	try:

		# Facebook format: 2017-02-18T18:06:39+0000
		ymd = dt.split('-')
		daytime = ymd[2].split('T')
		year = int(ymd[0])
		month = int(ymd[1])
		day = int(daytime[0])
		hrs = daytime[1].split(':')
		hour = int(hrs[0])
		minutes = int(hrs[1])

		result = datetime(year, month, day, hour=hour, minute = minutes)

	except Exception as e:

		print(e)

	return result 

def get_comments_from_id(page_id, num_posts, num_comments):

	# retrieve data
	data = get_json_from_request("/%s/feed" % page_id, "/?fields=message,created_time,type,name,id," + \
			"comments.limit(0).summary(true),shares,reactions" + \
			".limit(0).summary(true)", "&order=chronological&limit=%s&access_token=%s" % \
			(num_posts, config.ACCESS_TOKEN))
	post_ids = [item['id'] for item in data['data']]
	print(str(post_ids))

	docvecs = []


	for id in post_ids:

			# retrieve data
			data = get_json_from_request("/%s/comments" % id, "?fields=id,message,like_count,created_time,comments,from,attachment", "&order=chronological&limit=%s&access_token=%s" % \
						(num_comments, config.ACCESS_TOKEN) )


			docvec = [(item['message'], get_datetime_from_string(item['created_time'])) for item in data['data']]
			docvecs += docvec

			uprint(str(docvec))

	return docvecs

def get_messages_from_comments(comments):

	return [comment[0] for comment in comments]

