# Display the default fallback displays for when there is nothing
# else to show, consisting of just the AOSC logo and a clock
################################################################################
import displayplugin as dp

import datetime as dt
import os, shutil

rssUrl = "http://www.atmos.umd.edu/~tsluka/seminar"
maxSeminars = 4

class Seminar:
    def update(self):
        tmpdir = dp.gentmpdir()
        params = {
            'enabled'     : True,
            'updateFreq'  : dt.timedelta(hours=24),
            'dispDuration': dt.timedelta(seconds=60),
            'priority'    : (1,1),
            'location'    : 'half',
            'html'        : "file://"+tmpdir+'/seminar.html'}
        timeToSeminar = genHtml(tmpdir+'/seminar.html')
        shutil.copy('style.css',tmpdir)
        shutil.copy('code.png',tmpdir)
        if timeToSeminar < dt.timedelta(hours=24):
            params['priority'] = (2,1)
        return params

def genHtml(filename):
    ## also returns the time until the next seminar
    import xmltodict, urllib2
    xmlfile = urllib2.urlopen(rssUrl)
    xmldata = xmlfile.read()
    xmlfile.close()
    data = xmltodict.parse(xmldata)['feed']
    nextSeminarTime = dt.timedelta(days=365)

    with open(filename,'w') as html:
        html.write('''
<html><head>
 <meta charset="UTF-8">
 <link rel="stylesheet" type="text/css" href="../common/style.css">
 <link rel="stylesheet" type="text/css" href="style.css">
</head><body><div class="wrapper"><div class="header"><h1>Department Seminar</h1></div>
<div class="content">''')
        first=True
        count=1
        for f in data['entry']:
            d = dt.datetime.strptime(f['seminar:date'],"%Y-%m-%d %H:%M:%S")
            delta = d - dt.datetime.now()
            if ( delta < dt.timedelta(hours=-2)):
                continue
            if delta < nextSeminarTime:
                nextSeminarTime=delta
            if count > maxSeminars:
                continue
            count+=1
            
            if not f['title']:
                f['title'] = "AOSC Seminar by:"
            if first:
                html.write('<div class="nextSeminar">')
            writeEntry(html,f, not first)
            if first:
                html.write('</div><div class="otherSeminars">')
                html.write('<h1>Upcoming seminars</h1>')
                first = False
            
        html.write('''</div></div></div></body></html>''')
        return nextSeminarTime

        
def writeEntry(html, xml, short=False):
    def w(text):
       html.write(text.encode('UTF-8'))

    date = dt.datetime.strptime(xml['seminar:date'], "%Y-%m-%d %H:%M:%S")
        
    w('<div class="seminar">')

    def print_speaker():
        w(' <div class="speaker">')
        w('  <div class="name">'+xml['seminar:speaker']['name']+'</div>')
        if 'institution' in xml['seminar:speaker']:
            w('<div class="institution">'+xml['seminar:speaker']['institution']+'</div>')
        if 'dept' in xml['seminar:speaker']:
            if not short or 'institution' not in xml['seminar:speaker']:
                w('<div class="dept">'+xml['seminar:speaker']['dept']+'</div>')
        w('</div>')

    if short:
        datestr = date.strftime("%a %b %d")   
        w(' <div class="date">'+datestr+'</div>')
        print_speaker()
        w(' <div class="title">'+xml['title']+'</div>')
        
    else:
        datestr = date.strftime("%A %b %d, %I:%M%p")
        w(' <div class="date">'+datestr+'</div>')
        w('<div class="separator"></div>')
        w(' <div class="title">'+xml['title']+'</div>')
        w('<div class="separator"></div>')
        print_speaker()
        w('<div class="info_wrapper">')
#        w('<div class="qrcode"><img id="qrcode" src="code.png" /></div>')
        w('<div class="more_info">For more information visit</br> https://www.atmos.umd.edu/seminar</br> or contact</br>')
        if('seminar:host' in xml):
            w(xml['seminar:host']['name']+' (')
            w(xml['seminar:host']['email']+')')
            w('</div>')
        w('</div>')
        
  
        w('</div>')

        
    w('</div>')
        
#        w('<div class="abstract">'+xml['content']['#text']+'</div>')

#    html.write('</div>')
    
    
## the list of all available displays in this plugin,
## as required by the plugin loader
#displays = [Header, Footer, Half, Half]
def init():
    return [Seminar()]
