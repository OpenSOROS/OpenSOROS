"""
Currently just scrapes title data from the frontpage of r/canada.
TODO: get textual data from comment threads
TODO: get an API key
"""

from lxml import html
import requests

# We must specify a non-public user-agent to acquire data from reddit's servers.
# It will probably be good practice to get an API key for the future but this
# currently works fine.

page = requests.get('http://reddit.com/r/canada',headers = {'user-agent': 'SOROS'})
tree = html.fromstring(page.content)


def printTitles():
    """
    prints the titles from the frontpage of r/canada
    """

    # a list of titles constructed from the title element's xpath
    titles = tree.xpath('//p[@class="title"]/a/text()')

    print "Titles:\n"
    for t in titles:
        print t+"\n"


printTitles()