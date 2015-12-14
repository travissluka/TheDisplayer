################################################################################
## NHC Graphics Plugin:
## 
## Reads the RSS feeds from the NHC and shows the appropriate graphics
##  if there are any storms in the Atlantic basin
################################################################################
import displayplugin as dp

import datetime as dt
import os, shutil
import urllib
import urllib2
import feedparser
import xmltodict
import re

## configurables

dispTime = 15000


#####################################################################

htmlpfx = os.path.abspath(os.path.dirname(__file__))


rssUrl = 'http://www.nhc.noaa.gov/index-at.xml'
#rssUrl = 'http://www.nhc.noaa.gov/rss_examples/index-at-20130605.xml' ## testing feed
stormGraphics = "http://www.nhc.noaa.gov/storm_graphics"


class NHC:
    def update(self):
        tmpdir = dp.gentmpdir()
        params = {
            'enabled'     : False,
            'updateFreq'  : dt.timedelta(minutes=30),
            'dispDuration': dt.timedelta(seconds=90),
            'priority'    : (1,2.0),
            'location'    : 'half',
            'html'        : 'file://'+tmpdir+'/nhc.html'
        }
        shutil.copy('style.css',tmpdir)
        
        activeStorms = {}
        
        feed = xmltodict.parse(urllib2.urlopen(rssUrl).read())

        ## get a list of all active storms
        def proc(item):
            if 'nhc:Cyclone' in item.keys():
                s = item['nhc:Cyclone']
                s_id = '{0:02d}'.format(int(s['nhc:atcf'][2:4]))
                s_name = (s['nhc:type']+' '+s['nhc:name']).title()
                activeStorms[s_id]=s_name
        ## if there are more then one items
        if type(feed['rss']['channel']['item']) == type([]):       
            for f in feed['rss']['channel']['item']:
                proc(f)
        else:
            proc(feed['rss']['channel']['item'])
                
        print activeStorms
        params['enabled'] = len(activeStorms) > 0

        ## download images for each storm, and generate html content for each
        blocks = []
        yr = str(dt.datetime.now().year)[2:]
        for s in activeStorms:
            stormNum = s
            stormName = activeStorms[s]

            ## plot the 5 day warning cones
            plots = ['W5']
            ## only if the wind speed is > tropical storm, plot the wind speed probabilities
#            windSpeed = int(re.search('[0-9]+', s['nhc:wind']).group(0))
#            if windSpeed > 39:
            plots += ['R']
                
            for t in plots:
                src = stormGraphics+'/AT{0}/AL{0}{1}{2}.gif'.format(stormNum,yr,t)
                dst = tmpdir+'/AT{0}{1}.gif'.format(stormNum,t)
                urllib.URLopener().retrieve(src,dst)
                blocks.append('''
<div class="slide wrapper">
  <div class="header"> <h1>'''+stormName+'''</h1></div>
  <div class="content">
    <img src="'''+dst+'''"/>
  </div>
</div>''')


        ## write out the final html file
        with open(tmpdir+'/nhc.html','w') as html:
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

def init():
    return [ NHC() ]
