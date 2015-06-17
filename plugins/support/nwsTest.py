#!/usr/bin/env python
import nwsfeed

county = 'TXC211'
#county = 'MDC003'
#county = 'OHC157'
feeds,status = nwsfeed.CurrentAlerts(county)

if status == 1:
    for feed in feeds:
            #feed = 'http://alerts.weather.gov/cap/wwacapget.php?x=TX1253A8F521D0.FlashFloodWarning.1253A9013088TX.FWDFFWFWD.989125f0c5d821dcbc26f91893061aed'
            out = nwsfeed.ParseFeed(str(feed))
            alertdict = nwsfeed.AlertInfo(out)
            print alertdict['expires']
            print alertdict['type']
            print alertdict['short']
            print alertdict['detail']

elif status == 0:
    print('There are no active watches, warnings or advisories.')
