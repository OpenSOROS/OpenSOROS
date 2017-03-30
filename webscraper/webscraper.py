"""
Currently just scrapes data from r/canada.
TODO: get Reddit API key

"""

from lxml import html
import requests

# Need to get an API key for this or else we will easily go over requests per second
# due to using a public user-agent account
# requests.get("http://reddit.com/r/canada", )

page = requests.get('http://reddit.com/r/canada',headers = {'user-agent': 'SOROS'})
tree = html.fromstring(page.content)


def printTitles():
    """
    prints the titles from the frontpage of r/canada
    TODO: get URL to go to comment page
    """

    # a list of titles constructed from the title element's xpath
    titles = tree.xpath('//p[@class="title"]/a/text()')

    print "Titles:\n"
    for t in titles:
        print t+"\n"


printTitles()