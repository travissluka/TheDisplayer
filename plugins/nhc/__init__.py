################################################################################
## NHC Graphics Plugin:
## 
## Reads the RSS feeds from the NHC and shows the appropriate graphics
##  if there are any storms in the Atlantic basin
################################################################################

import datetime as dt
import os
import urllib
import urllib2
import feedparser
import xmltodict
import re

## configurables

dispTime = 15000


#####################################################################

htmlpfx = os.path.abspath(os.path.dirname(__file__))

globalParams = {
    'enabled'     : False,
    'updateFreq'  : dt.timedelta(minutes=30),
    'dispDuration': dt.timedelta(seconds=90),
    'priority'    : (1,2.0),
    'location'    : 'half',
}

rssUrl = 'http://www.nhc.noaa.gov/index-at.xml'
#rssUrl = 'http://www.nhc.noaa.gov/rss_examples/index-at-20130605.xml' ## testing feed
stormGraphics = "http://www.nhc.noaa.gov/storm_graphics"


class NHC:
    
    def getPage(self):
        return  'file://'+htmlpfx+'/nhc.html'


    def getParams(self):
        params =  globalParams
        activeStorms = []
        
        feed = xmltodict.parse(urllib2.urlopen(rssUrl).read())

        ## get a list of all active storms
        for f in feed['rss']['channel']['item']:
            if 'nhc:Cyclone' in f.keys():
                activeStorms.append( f['nhc:Cyclone'] )
        params['enabled'] = len(activeStorms) > 0

        ## download images for each storm, and generate html content for each
        blocks = []
        yr = str(dt.datetime.now().year)[2:]
        for s in activeStorms:
            stormNum = '{0:02d}'.format(int(s['nhc:wallet'][2:]))
            stormName = (s['nhc:type']+' '+s['nhc:name']).title()
            ## plot the 5 day warning cones
            plots = ['W5']
            ## only if the wind speed is > tropical storm, plot the wind speed probabilities
#            windSpeed = int(re.search('[0-9]+', s['nhc:wind']).group(0))
#            if windSpeed > 39:
            plots += ['R']
                
            for t in plots:
                src = stormGraphics+'/AT{0}/AL{0}{1}{2}.gif'.format(stormNum,yr,t)
                dst = htmlpfx+'/AT{0}{1}.gif'.format(stormNum,t)
                urllib.URLopener().retrieve(src,dst)
                blocks.append('''
<div class="slide wrapper">
  <div class="header"> <h1>'''+stormName+'''</h1></div>
  <div class="content">
    <img src="'''+dst+'''"/>
  </div>
</div>''')


        ## write out the final html file
        with open(htmlpfx+'/nhc.html','w') as html:
            html.write('''
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="../common/style.css">
    <link rel="stylesheet" type="text/css" href="style.css">
    <script src="../common/jquery.min.js"></script>
    <script>
      $(function() {
        $("#slideshow > div:gt(0)").hide();
        setInterval(function() {
          $('#slideshow > div:first')
           .hide()
          .next()
          .show()
          .end()
          .appendTo('#slideshow');
        },  '''+str(dispTime)+''');
      });
    </script>
  </head>
  <body>
  <div id="slideshow">'''+' '.join(blocks)+'''
</div>
  </body>
</html>
''')

        return params


displays = [NHC]
