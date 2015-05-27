#!/usr/bin/env python
""" Module to parse NWS RSS/XML feeds
    C. Martin - 5/2015

    Required Modules:
        feedparser
        from xml.dom.minidom import parse
        import xml.dom.minidom
        import urllib

"""
import feedparser

# function to grab NWS Public Alerts feed list for a given county code
def CurrentAlerts(countycode):
    """ Returns NWS Public Alert Feed Links for a given county code string.
    See https://alerts.weather.gov for code listing.
    Usage:
        feeds, status = CurrentAlerts('countycode')
    """
    url='https://alerts.weather.gov/cap/wwaatmget.php?' # base URL
    url=url+'x='+countycode+'&y=0' # add x=county and y=0
    feed = feedparser.parse(url) # get feed
    feeds = []
    for post in feed.entries:
        feeds.append(post.links[0].href)    # append all urls to list

    # determine status of this feed
    status = 1
    if len(feeds) == 1 :
        if feeds[0] == url: # this means no active alerts
            status = 0

    return feeds, status

# function to parse NWS Public Alert feed
def ParseFeed(url):
    """ Returns numerous variables by parsing a given NWS
    Common Alerting Protocol (CAP) message.

    """
    from xml.dom.minidom import parse
    import xml.dom.minidom
    import urllib
    tree = xml.dom.minidom.parse(url)
