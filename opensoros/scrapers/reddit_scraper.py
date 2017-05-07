"""
Scrapes data from an arbitrary subreddit.

Use a CL argument to specify the subreddit
    EG: `python redditscraper.py canada`
        `python redditscraper.py ubc`
TODO: get textual data from comment threads
TODO: get an API key
"""

from lxml import html
import requests
import time
import sys
import csv
import praw 
from datetime import datetime
try:
    from . import config
except Exception as e:
    pass


def zeropad(n): 
    if(n<10):
        return "0"+str(n)
    else:
        return str(n)

def printTitles(subreddit):
    """
    prints the titles from the frontpage of r/canada
    """

    # We must specify a non-public user-agent to acquire data from reddit's servers.
    # It will probably be good practice to get an API key for the future but this
    # currently works fine.
    page = requests.get('http://reddit.com/r/'+subreddit,headers = {'user-agent': 'SOROS'})
    tree = html.fromstring(page.content)

    # a list of titles constructed from the title element's xpath
    titles = tree.xpath('//p[@class="title"]/a/text()')

    return titles

def get_comments_from_subreddit(subreddit_name, num_comments):

    r = praw.Reddit(user_agent="George Soros", client_id=config.REDDIT_ID, client_secret=config.REDDIT_SECRET)
    comments = []

    for sub in r.subreddit(subreddit_name).new(limit=num_comments):
        submission = r.submission(id=sub.id)
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            comments.append((comment.body.encode('utf-8').decode('utf-8'), datetime.fromtimestamp(comment.created)))

    return comments

def makeFileName(subreddit,date):
    return "r_  "+subreddit+"_"+date+".csv"

def get_messages_from_comments(comments):

    return [comment[0] for comment in comments]

def main():
    currentdatetime = str(time.localtime()[1])+"-"+str(time.localtime()[2])+"-"+str(time.localtime()[0])+"_"+str(time.localtime()[3])+":"+str(time.localtime()[4])+":"+zeropad(time.localtime()[5])
    subreddit = sys.argv[1]    
    print("scraping r/"+subreddit+" at: "+currentdatetime)
    
    titles = printTitles(subreddit)

    # ensure utf-8 encoding --
    encodedTitles = []
    for t in titles:
        encodedTitles.append(t.encode('utf-8'))
    
    fileName = makeFileName(subreddit,currentdatetime)
    
    # write csv -- 
    with open(filepath+fileName, 'wb') as f:
        writer = csv.writer(f)
        for t in encodedTitles:
            writer.writerow([t])


if __name__ == "__main__":
    main()