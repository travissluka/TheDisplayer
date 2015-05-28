""" Module to parse NWS RSS/XML feeds
    C. Martin - 5/2015

    Required Modules:
        feedparser
        urllib2
        xmltodict

"""
import feedparser
import urllib2
import xmltodict

# function to grab NWS Public Alerts feed list for a given county code
def CurrentAlerts(countycode):
    """ Returns NWS Public Alert Feed Links for a given county code string.
    See https://alerts.weather.gov for code listing.
    Usage:
        feeds, status = CurrentAlerts('countycode')
        feeds is a list of current valid alert urls
        status is 1 if there are alerts, 0 if no alerts

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
    Usage:
        xmldict = ParseFeed(url)
        where xmldict is a dictionary containing all data from the alert

    """
    xmlfile = urllib2.urlopen(url)  # open url
    xmldata = xmlfile.read()    # read url into memory
    xmlfile.close()
    xmldict = xmltodict.parse(xmldata)  # parse xml file
    return xmldict

def AlertInfo(xmldict):
    """ Returns key information from a given XML dictionary
    returned from NWS CAP XML feed
    Usage:
        AlertDict = AlertInfo(xmldict)
        AlertDict['type'] : event type (Tornado Warning, etc.)
        AlertDict['issued'] : issued time string
        AlertDict['expires'] : expiration time
        AlertDict['office'] : NWS office name
        AlertDict['short'] : short, one line description
        AlertDict['detail'] : paragraph detailing alert
    """
    AlertInfo = xmldict['alert']['info']    # we just want this part of the XML
    AlertDict = {}
    ### may modify below if you decide you want more/less information
    AlertDict.update({'type':AlertInfo['event']}) # alert type
    AlertDict.update({'issued':AlertInfo['effective']}) # start time string
    AlertDict.update({'expires':AlertInfo['expires']}) # expiration time string
    AlertDict.update({'office':AlertInfo['senderName']}) # NWS office
    AlertDict.update({'short':AlertInfo['headline']}) # one line description
    AlertDict.update({'detail':AlertInfo['description']}) # detailed paragraph
    #AlertDict.update({'polygon':AlertInfo['area']['polygon']}) # didn't work?

    return AlertDict
