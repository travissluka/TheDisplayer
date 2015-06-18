import datetime as dt
import os
import nwsfeed as nwsf

location = 'MDC003'
#location = 'TXC001'

htmlpfx = os.path.abspath(os.path.dirname(__file__))

## initial work with warnings.... much left to be done...


class Header:
    def getParams(self):
        params = {}
        params['enabled']       = False
        params['updateFreq']    = dt.timedelta(seconds=60)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (3,1.0)
        params['location']      = 'header'

        feeds,status = nwsf.CurrentAlerts(location)
        if status:
            params['enabled'] = True
            self.feeds = feeds

        return params

    def getPage(self):
        htmlFile = htmlpfx+"/header.html"
        html = open(htmlFile,'w')
        html.write('''
        <html>
        <head><link rel="stylesheet" type="text/css" href="style.css"></head>
        <body><h1>''')
        for feed in self.feeds:
            f = nwsf.ParseFeed(str(feed))
            alertdict = nwsf.AlertInfo(f)
            html.write(alertdict['type']+', ')
        html.write('</h1>')
        html.write('<div class="office">'+alertdict['office']+"</div>")
        html.write('<div class="issued">'+alertdict['issued']+"</div>")
        html.close()

        return 'file://'+htmlFile

class Footer:
    # for now just copy the header logic
    def getParams(self):
        params = {}
        params['enabled']       = False
        params['updateFreq']    = dt.timedelta(seconds=60)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (3,1.0)
        params['location']      = 'footer'

        feeds,status = nwsf.CurrentAlerts(location)
        if status:
            params['enabled'] = True
            self.feeds = feeds

        return params

    def getPage(self):
        htmlFile = htmlpfx+"/header.html"
        return 'file://'+htmlFile


## the list of all available displays in this plugin,
## as required by the plugin loader
displays = [Header, Footer]
