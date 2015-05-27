import nwsfeed

county = 'TXC363'
#county = 'MDC003'
#county = 'OHC157'
feeds,status = nwsfeed.CurrentAlerts(county)

for feed in feeds:
     #feed = 'http://alerts.weather.gov/cap/wwacapget.php?x=TX1253A8F521D0.FlashFloodWarning.1253A9013088TX.FWDFFWFWD.989125f0c5d821dcbc26f91893061aed'
     out = nwsfeed.ParseFeed(feed)
     print out
