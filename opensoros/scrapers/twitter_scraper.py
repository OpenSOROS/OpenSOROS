import tweepy #https://github.com/tweepy/tweepy
import csv
import sys
from . import config


def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
	enc = file.encoding
	if enc == 'UTF-8':
		print(*objects, sep=sep, end=end, file=file)
	else:
		f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
		print(*map(f, objects), sep=sep, end=end, file=file)

# Taken from https://gist.github.com/yanofsky/5436496

def get_tweets_from_screenname(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(config.TWITTER_C_KEY, config.TWITTER_C_SECRET)
	auth.set_access_token(config.TWITTER_A_KEY, config.TWITTER_A_SECRET)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	if len(new_tweets) > 0:
		oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		
		#all subsiquent requests use the max_id param to prevent duplicates
		try:
			new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		except Exception as e:
			pass
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1


	outtweets = [(tweet.text.encode('utf-8').decode('utf-8'), tweet.created_at) for tweet in alltweets]

	return outtweets

def get_messages_from_comments(comments):

	return [comment[0] for comment in comments]


