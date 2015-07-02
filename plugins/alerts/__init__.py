#!/usr/bin/env python
import feedparser
import urllib2
import xmltodict
import datetime as dt
import os
import re

#countycode='MDC510' # baltimore city
countycode='MDC033' # College Park
url='http://alerts.weather.gov/cap/wwaatmget.php?x='+countycode+'&y=0'
#url='http://alerts.weather.gov/cap/md.php?x=0'

#TODO, wrap these variables with a lock
mainAlert = None
topAlerts = None
severity = None

htmlpfx = os.path.abspath(os.path.dirname(__file__))


################################################################################

def getAlerts():
    # get the feed and parse it
    atomfeed=feedparser.parse(url)
  
    ## the following lists and function are used later
    ##  to sort the feed list base on priorities
    severityList = ['extreme', 'severe', 'moderate', 'minor','unknown']
    certaintyList = ['observed', 'likely', 'possible', 'unknown']
    urgencyList = ['immediate','expected','future','unknown']
    def selectBy(alerts, key, priorityList):
        # filter out competely unwanted values that aren't mentioned
        #  in the above lists
        alerts = filter(
            lambda a: a[key].lower() in priorityList,
            alerts)
        # sort by priority given
        alerts = sorted(
            alerts,
            key=lambda a: priorityList.index(a[key].lower()))
        # select only items equal to the highest priority
        alerts = filter(
            lambda a: a[key] == alerts[0][key],
            alerts)
        return alerts
    
    # consider only actual active alerts 
    alerts = atomfeed.entries  
    alerts = filter(
        lambda a: 'cap_status' in a and a['cap_status'].lower() == 'actual',
        alerts)
    if len(alerts) == 0:
        return None, None, None

    # filter to only show the most severe alerts
    severeAlerts = selectBy(alerts, 'cap_severity', severityList)

    # get the most urgent of the most severe alerts to feature
    mainAlert = selectBy(severeAlerts, 'cap_urgency', urgencyList)
    mainAlert = selectBy(mainAlert, 'cap_certainty', certaintyList)

    # get the most recent if there is still more than one
    mainAlert = sorted(
        mainAlert,
        key=lambda a: a['updated'])[-1]

    # determine an level of severity, used for background colors
    #  and such
    if mainAlert['cap_severity'].lower() == 'extreme':
        severity = 3
    if mainAlert['cap_severity'].lower() == 'severe':
        if mainAlert['cap_urgency'].lower() == 'immediate':
            severity = 2
        else:
            severity = 1
    else:
        severity = 0
    
    # get a simple list of the other alerts of the same severity
    topAlerts = []
    for a in severeAlerts:
        n = a['cap_event']
        if (n not in topAlerts) and (n !=  mainAlert['cap_event']):
            topAlerts.append(n)
    return mainAlert, topAlerts, severity



################################################################################


    
class Header:
    def getParams(self):
        global mainAlert, topAlerts, severity
        mainAlert, topAlerts, severity = getAlerts()
        
        params = {}
        params['enabled']      = mainAlert != None
        params['updateFreq']   = dt.timedelta(minutes=1)
        params['dispDuration'] = dt.timedelta(minutes=1)
        params['priority']     = (3,1.0)
        params['location']     = 'header'

        if mainAlert:
            with open(htmlpfx+'/header.html','w') as html:
                html.write('''
  <html><head><link rel="stylesheet" type="text/css" href="style.css"></head>
  <body class="header severity'''+str(severity)+'''">
      <div class="mainAlert">{0}</div>
  </body>
  </html>'''.format(mainAlert['cap_event']))           
        return params
        
    def getPage(self):
        return 'file://'+htmlpfx+'/header.html'


################################################################################

    
class Footer:
    def getParams(self):
        global mainAlert, topAlerts       
        params = {}
        params['enabled']      = mainAlert != None
        params['updateFreq']   = dt.timedelta(minutes=1)
        params['dispDuration'] = dt.timedelta(minutes=1)
        params['priority']     = (3,1.0)
        params['location']     = 'footer'
        if mainAlert:
            with open(htmlpfx+'/footer.html','w') as html:
                html.write('''
  <html><head><link rel="stylesheet" type="text/css" href="style.css"></head>
  <body class="footer severity'''+str(severity)+'''">
      <div class="mainAlert">'''+mainAlert['cap_event']+'''</div>
      <div class="topAlerts">'''+','.join(topAlerts)+''' </div>
  </body>
  </html>''')
        return params
    
    def getPage(self):
        return 'file://'+htmlpfx+'/footer.html'


################################################################################

    
class AlertText:
    def getParams(self):
        params = {}
        params['enabled']      = mainAlert != None
        params['updateFreq']   = dt.timedelta(minutes=1)
        params['dispDuration'] = dt.timedelta(minutes=1)
        params['priority']     = (1,1.0)
        params['location']     = 'half'
        if severity > 0:
            params['priority']     = (3,1.0)

        ####################
        # generate the html
        if mainAlert:
            # get the full info
            xmldata = urllib2.urlopen(mainAlert['link']).read()
            fullAlert =  xmltodict.parse(xmldata)
            faInfo = fullAlert['alert']['info']
            desc = '<p>'+faInfo['description'].replace('\n','</br>')+'</p>'
            desc = desc.replace('*','</p><p>*')
            inst = faInfo['instruction']
            desc = desc+'<p class="instructions">'+inst+'</p>'
            with open(htmlpfx+'/alerthalf.html','w') as html:
                html.write('''
  <html><head>
   <link rel="stylesheet" type="text/css" href="jscroller2-1.1.css">
   <link rel="stylesheet" type="text/css" href="style.css">

   <script type="text/javascript" src="jscroller2-1.61.js"></script>            
  </head>
  <body>
      <div class="scrollcontainer">
      <div class="summary jscroller2_up jscroller2_delay-2 jscroller2_speed-40">'''+desc+'''</div>
      <div class="summary jscroller2_up_endless jscroller2_speed-40">'''+desc+'''</div>
</div>
  </body>
  </html>''')
        return params

    def getPage(self):
        return 'file://'+htmlpfx+'/alerthalf.html'


################################################################################    
    


displays = [Header, Footer, AlertText]
    
