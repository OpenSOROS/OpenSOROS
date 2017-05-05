import urllib.request
import re
import json
import datetime
import csv
import time
import sys

#You'll need to get your own access token 
from config import ACCESS_TOKEN

BASE = "https://graph.facebook.com/v2.9"

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

def get_comments_from_id(page_id, num_posts, num_comments):

	# retrieve data
	data = get_json_from_request("/%s/feed" % page_id, "/?fields=message,created_time,type,name,id," + \
			"comments.limit(0).summary(true),shares,reactions" + \
			".limit(0).summary(true)", "&order=chronological&limit=%s&access_token=%s" % \
				(num_posts, ACCESS_TOKEN))
	post_ids = [item['id'] for item in data['data']]
	print(str(post_ids))

	docvecs = []


	for id in post_ids:

			# retrieve data
			data = get_json_from_request("/%s/comments" % id, "?fields=id,message,like_count,created_time,comments,from,attachment", "&order=chronological&limit=%s&access_token=%s" % \
						(num_comments, ACCESS_TOKEN) )
			docvec = [item['message'] for item in data['data']]
			docvecs += docvec

			uprint(str(docvec))

	return docvecs


