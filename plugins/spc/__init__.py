################################################################################
## SPC Outlook Plugin:
## 
## Reads the shape files for day 1, 2, and 3 of the SPC outlooks from the SPC
## website. If there is any activity at our current lat/lon location
## (defined as location below) OR if there is unusually severe weather anywhere
## across the country, the appropriate maps will be shown for those days.
## Additionally, if our location has hail, tornado, wind probabilities, those
## maps are shown as well
##
## TODO: Still has some bugs, sometimes our locations is not correctly
##   determined to be in the TSTM shape, other times it is when it should
##   not be
################################################################################
import datetime as dt
import os
import spc
import urllib

## Configurables
#########################

location = (38.8967, 76.9275)   # College Park, MD

## The categorical outlook levels in ascending order of severity are:
##   (TSTM, MRGL, SLGT, ENH, MDT, HIGH)

minLocOutlook = "TSTM"          # minimum level of convection probability
                                # for our local area to trigger the map shown

minNatOutlook = "ENH"           # same as above, except for the whole nation


dispTime = 6000                 # time (msec) to show each image in slideshow


#####################################################################

htmlpfx = os.path.abspath(os.path.dirname(__file__))

globalParams = {
    'enabled'     : False,
    'updateFreq'  : dt.timedelta(minutes=30),
    'dispDuration': dt.timedelta(seconds=45),
    'priority'    : (1,2.0),
    'location'    : 'half',
}

class SPC:
    def getPage(self):
        return  'file://'+htmlpfx+'/spc_outlook.html'


    def getParams(self):
        params =  globalParams

        ## determine which day outlooks we need to display
        allOutlooks = spc.getOutlooksForLoc()
        myOutlooks  = spc.getOutlooksForLoc(location)
        imgToShow=[]
        for day in allOutlooks:

            ## if there is no categorical probability at all, skip this day
            category = 'CATEGORICAL'
            if not category in allOutlooks[day]:
                continue

            ## make sure the probability meets the minimum level
            ## for either our location, or the whole nation
            if minNatOutlook in allOutlooks[day][category] or \
               minLocOutlook in myOutlooks[day][category] :
                imgToShow.append("day{0}otlk_prt.gif".format(day))
                ## search also to see if hail, tornado, or wind
                ## maps should be shown (only if there is a probability
                ##  for our current location)
                for c in myOutlooks[day]:
                    urlWord = None
                    if c == 'TORNADO':
                        urlWord = "torn"
                    elif c == "WIND":
                        urlWord = "wind"
                    elif c == "HAIL":
                        urlWord = "hail"
                    if urlWord and len(myOutlooks[day][c]) > 0:
                        imgToShow.append("day{0}probotlk_{1}.gif".format(day,urlWord))

        ## download the images
        for img in imgToShow:
            dl = urllib.URLopener()
            dl.retrieve("http://www.spc.noaa.gov/products/outlook/"+img, htmlpfx+'/'+img)
        
        ## Create the html file to display
        with open(htmlpfx+'/spc_outlook.html','w') as html:
            slideshow = ""
            if len(imgToShow) > 1:
                slideshow = 'id="slideshow"'
            
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
    <style>
      #slideshow > div {
        position: absolute;}
    </style>
 </head>
<body>
  <div '''+slideshow+'''>''');
            for img in imgToShow:
                dayNum = img[3]
                html.write('<div class="slide"><h1>Severe Weather Outlook  (Day {1})</h1><img src="{0}"/></div>'.format(img,dayNum))
            html.write('''
  </div>
</body>
</html>''')
        params['enabled'] = len(imgToShow) > 0
        return params


## the list of all available displays in this plugin,
## as required by the plugin loader
displays = [SPC]
