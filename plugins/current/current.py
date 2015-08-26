
################################################################################
## Support library for current conditions display :
## will grab data from a JSON query on a webpage and format it in an image/html
################################################################################

## NOTE: Requires the following Python modules:
import requests, json, os
import urllib

iconsize = '400x336'  # see http://weather.weatherbug.com/corporate/products/API/help.aspx for details


def downloadIcons(outDir, size=iconsize):
    ## downloads the weatherbug icons
    ## get files condXXX.png where XXX is from 001 to 176, and 999
    for i in ['{0:03d}'.format(n) for n in  [999,]+range(1,177)]:
        filename='cond{0}.png'.format(i)
        filepath='http://img2.weather.weatherbug.com/forecast/icons/localized/400x336/en/trans/'
        urllib.URLopener().retrieve(filepath+filename, outDir+'/'+filename)
        
            
def getCSSwxbug(filename):
    ## NOTE: This url is on sense.umd.edu now , move it to a UMD Weather server once configured
    ## We should be archiving the weatherbug data somewhere more centralized/relevant
    url = 'http://sense.umd.edu/aether/api/wxbug_recent.php'

    response = requests.get(url,verify=False)
    data = response.json()

    ## get data from JSON query
    mslp = data[0]['MSLP'] # millibars
    temp = data[0]['Temp'] # celsius
    temp = float(temp) * (9./5.) + 32. # convert to Fahrenheit
    dew = data[0]['DewPoint'] # celsius
    dew = float(dew) * (9./5.) + 32. # convert to Fahrenheit
    time = data[0]['Timestamp'] # YYYY-MM-DD HH:MM:SS in UTC
    icon = data[0]['IconID'] # can use this for icons from weatherbug api
    iconstr = "%03d" % int(icon) # converts iconID to 3 digit code with leading zeros for URL
    wetbulb = data[0]['WetBulb'] # celsius
    wetbulb = float(wetbulb) * (9./5.) + 32. # convert to Fahrenheit
    hourrain = data[0]['HourlyRainRate'] # mm
    wspd = float(data[0]['WindSpeed']) * 0.621371 # m/s to mph

    ## convert wind degrees to direction
    wdir = data[0]['WindDirection'] # degrees   
    windCuttoffs = [
        ('N',   11.25),
        ('NNE', 33.75),
        ('NE',  56.25),
        ('ENE', 78.75),
        ('E',   101.25),
        ('ESE', 123.75),
        ('SE',  146.25),
        ('SSE', 168.75),
        ('S',   191.25),
        ('SSW', 213.75),
        ('SW',  236.25),
        ('WSW', 258.75),
        ('W',   281.25),
        ('WNW', 303.75),
        ('NW',  326.25),
        ('NNW', 348.75),
        ('N',   360.0),        
    ]        
    for w in windCuttoffs:
        if float(wdir) < w[1]:
            wdir = w[0]
            break

    dailyrain = data[0]['DailyRain'] # mm
    rh = data[0]['RH'] # percentage

    with open(filename,'w') as html:
        html.write('''
<html>
<head>
<link rel="stylesheet" type="text/css" href="../common/style.css">
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<div id="InfoBox">
    <div id="Title">
        Computer and Space Sciences Building - University of Maryland
    </div>
    <div id="SubBox1">
        <div id="SubBox1left">
            <div id="ForecastIcon">
                <img src="cond'''+iconstr+'''.png"/>
            </div>
        </div>
        <div id="SubBox1right">
            <div id="Temperature">
                '''+str(int(round(temp,0)))+'''&deg;F
            </div>
            <div id="DewPt">
                '''+str(int(round(dew,0)))+'''&deg;F Dew
            </div>
            <div id="RH">
                '''+str(rh)+'''% RH
            </div>
        </div>
    </div>
    <div id="Wind">
        Wind from '''+str(wdir)+''' at '''+str(int(round(wspd,0)))+''' MPH
    </div>
    <div id="Timestamp">
        Last updated: '''+str(time)+''' UTC
    </div>
</div>
</body>
</html>
        ''')

    ### TODO: Now take this information and either create an image or create an HTML page
### TODO: Also, use this method to get data from another JSON php page for 6 hourly graphs
