
################################################################################
## Support library for current conditions display :
## will grab data from a JSON query on a webpage and format it in an image/html
################################################################################

## NOTE: Requires the following Python modules:
import requests, json, os
htmlpfx = os.path.abspath(os.path.dirname(__file__))

def getCSSwxbug():
    ## NOTE: This url is on sense.umd.edu now , move it to a UMD Weather server once configured
    ## We should be archiving the weatherbug data somewhere more centralized/relevant
    url = 'http://sense.umd.edu/aether/api/wxbug_recent.php'

    response = requests.get(url,verify=False)
    data = response.json()
    iconsize = '500x420'  # see http://weather.weatherbug.com/corporate/products/API/help.aspx for details

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
    wspd = float(wspd) * 2.24 # miles per hour
    wdir = data[0]['WindDirection'] # degrees
    ### TODO: add algorithm to determine degrees -> NW/W/etc.
    dailyrain = data[0]['DailyRain'] # mm
    rh = data[0]['RH'] # percentage

    with open(htmlpfx+'/currently.html','w') as html:
        html.write('''
<html>
<head>
</head>
<body>
<div id="Title">
Current Conditions:
</div>
<div id="Temperature">
'''+str(temp)+'''F
</div>
<div id="DewPt">
'''+str(dew)+'''F
</div>
<div id="RH">
'''+str(rh)+'''%
</div>
<div id="WindSpeed">
'''+str(wspd)+'''MPH
</div>
<div id="WindDir">
'''+str(wdir)+'''Degrees
</div>
<div id="ForecastIcon">
<img src="http://img.weather.weatherbug.com/forecast/icons/localized/'''+iconsize+'''/en/trans/cond'''+iconstr+'''.png"/>
</div>
</body>
</html>
        ''')

    ### TODO: Now take this information and either create an image or create an HTML page
### TODO: Also, use this method to get data from another JSON php page for 6 hourly graphs
