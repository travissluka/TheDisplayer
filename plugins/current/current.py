
################################################################################
## Support library for current conditions display :
## will grab data from a JSON query on a webpage and format it in an image/html
################################################################################

## NOTE: Requires the following Python modules:
import requests, json

## NOTE: This url is on sense.umd.edu now , move it to a UMD Weather server once configured
## We should be archiving the weatherbug data somewhere more centralized/relevant
url = 'http://sense.umd.edu/aether/api/wxbug_recent.php'

response = requests.get(url,verify=False)
data = response.json()

## get data from JSON query
mslp = data[0]['MSLP'] # millibars
temp = data[0]['Temp'] # celsius
dew = data[0]['DewPoint'] # celsius
time = data[0]['Timestamp'] # YYYY-MM-DD HH:MM:SS in UTC
icon = data[0]['IconID'] # can use this for icons from weatherbug api
wetbulb = data[0]['WetBulb'] # celsius
hourrain = data[0]['HourlyRainRate'] # mm
wspd = data[0]['WindSpeed'] # m/s
wdir = data[0]['WindDirection'] # degrees
dailyrain = data[0]['DailyRain'] # mm
rh = data[0]['RH'] # percentage

### TODO: Now take this information and either create an image or create an HTML page
### TODO: Also, use this method to get data from another JSON php page for 6 hourly graphs
