import datetime as dt
import os

priority = 0,0
htmlpfx = 'file://'+os.path.abspath(os.path.dirname(__file__))

class Get2Know:
    def getParams(self):
        params = {}
        params['enabled']       = True
        params['updateFreq']    = dt.timedelta(seconds=60)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (1,1.0)
        params['location']      = 'half'
        return params
    def getPage(self):
        html = htmlpfx+'/get2know.html' # point to external website for PHP?
        return html

class MetoGradsNews:
    def getParams(self):
        params = {}
        params['enabled']       = True
        params['updateFreq']    = dt.timedelta(seconds=60)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (1,1.0)
        params['location']      = 'half'
        return params
    def getPage(self):
        html = htmlpfx+'/news.html' # point to external website for PHP?
        return html

class StudentSeminar:
    def getParams(self):
        params = {}
        params['enabled']       = True
        params['updateFreq']    = dt.timedelta(seconds=60)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (1,1.0)
        params['location']      = 'half'
        return params
    def getPage(self):
        html = htmlpfx+'/seminar.html' # point to external website for PHP?
        return html

class MetoGradsEvents:
    def getParams(self):
        params = {}
        params['enabled']       = True
        params['updateFreq']    = dt.timedelta(seconds=60)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (1,1.0)
        params['location']      = 'half'
        return params
    def getPage(self):
        html = htmlpfx+'/events.html' # point to external website for PHP?
        return html

## the list of all available displays in this plugin,
## as required by the plugin loader
displays = [Get2Know,MetoGradsNews,StudentSeminar,Events]
