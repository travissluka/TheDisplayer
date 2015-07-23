
################################################################################
## Support library for current conditions display :
## will grab data from a JSON query on a webpage and format it in an image/html
################################################################################

## NOTE: Requires the following Python modules:
import requests, json, os

def getCSSwxbug(filename):
    ## NOTE: This url is on sense.umd.edu now , move it to a UMD Weather server once configured
    ## We should be archiving the weatherbug data somewhere more centralized/relevant
    url = 'http://sense.umd.edu/aether/api/wxbug_recent.php'

    response = requests.get(url,verify=False)
    data = response.json()
    iconsize = '400x336'  # see http://weather.weatherbug.com/corporate/products/API/help.aspx for details

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
    wspd = data[0]['WindSpeed'] # m/s
    wspd = float(wspd) * 0.621371 # miles per hour
    wdir = data[0]['WindDirection'] # degrees
    ### TODO: add algorithm to determine degrees -> NW/W/etc.
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
                <img src="http://img.weather.weatherbug.com/forecast/icons/localized/'''+iconsize+'''/en/trans/cond'''+iconstr+'''.png"/>
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
        Wind from '''+str(wdir)+'''&deg; at '''+str(int(round(wspd,0)))+''' MPH
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
