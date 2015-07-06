
################################################################################
## Support library to parse the shape files from the SPC to determine what
##  the outlook levels are for our location for the various days and categories
################################################################################
import feedparser
import urllib2
import datetime as dt
import time
import re
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry.linestring import LineString
import sys


## the distance from the shape boundary at which we say the point is
## close enough and consider it in the shape
deadzone = .05

## The following function gets the 3 day convective outlooks from the SPC
##  and for a given lat/lon, determines what the outlook levels are for that
##  location. Lat/Lon given as degrees N/W.
##  If no lat/lon is given, returns the highest values across the country.
##  Function works by reading the shape files from the SPC, which give a list of line
##  segments that define an area for each outlook level, we are IN the area if we are
##  to the right of the closest line segment that is near our location.
########################################################################################
def getOutlooksForLoc(center=None):
    ## build a box around our given location that we will test against
    if center:
        assert(center[0] > 0 and center[1] > 0)
        loc = Point(center)

    ## Get information about the outlooks for each lead day
    ####################################
    retVal = {}   ## the main dictionary that will be returned at the end
    for day in [1,2,3]: ## don't deal with 48 right now (4-8 day), as the images behave diferently
        retVal[day] = {}

        ## get the shapes file from the intertubes
        dy=str(day)
        if day < 10:
            dy = 'y'+dy
        shapeFileUrl = "http://weather.noaa.gov/pub/data/raw/wu/wuus{0:02d}.kwns.pts.d{1}.txt".format(day,dy)
        shapeFile = urllib2.urlopen(shapeFileUrl).read()
        
        ## split the file up into the individual outlook categories, and get the shapes for each
        ##  warning level within the outlook category
        ##  regular expression to match "... outlookShapeType ...   coordinatesList && "
        categories = re.findall(r'\.\.\. (.+?) \.\.\.(.+?)\&\&',shapeFile,flags=re.DOTALL)
        for category in categories:
            ## parse out a list of coords
            words = category[1].split()
            
            ## ignore if its empty
            if len(words) == 0:
                continue

            ## parse the category types and coordinates for the shape line segments
            shapes = []     # list of (category, lineList) pairs
            lines = []      # list of line segments to be added to "shapes" when done
            newLine = []    # list of (lat,lon) points to be added to "lines" when done
            idx = 0
            lbl = None
            while idx <= len(words):
                if idx == len(words) or not re.match('^[0-9]{8}$',words[idx]):
                    ## we found a label, start collecting a new list of line segments
                    ## for this category type, OR we have reached the end of the words
                    if len(newLine) > 0:
                        lines.append(newLine)
                        newLine=[]
                    if len(lines) > 0:
                        shapes.append((lbl,lines))
                        lines = []
                    if idx != len(words):
                        lbl = words[idx]
                elif words[idx] == "99999999":
                    ## found the end of a line segment, save it and start a new segment
                    lines.append(newLine)
                    newLine = []
                else:
                    ## convert the text into a coordinate and add it to the current
                    ##  line segment we are building
                    c = words[idx]
                    coord = (float(c[0:2]+"."+c[2:4]),float(c[4:6]+"."+c[6:8]))
                    ## lon >= 100 have the first 1 missing, add it back in
                    if coord[1] < 50:
                        coord = (coord[0], coord[1]+100)
                    newLine.append(coord)
                idx += 1

            ## test to see which shapes we are inside
            ##  find the closest line segment for each shape,
            ##  and test to make sure we are to the RIGHT of that segment
            shapesIn = []
            if center:
              for s in shapes:
                ## if coordinates were empty, ignore
                if len(s[1]) == 0:
                    continue

                ## find the closest line segment
                segments = sorted(s[1], key=lambda s: LineString(s).distance(loc))
                coords = segments[0]
                distance = LineString(coords).distance(loc)

                ## find the closest point in the closest line segment
                closestPoint = sorted(coords, key=lambda p: Point(p).distance(loc))[0]
                idx = coords.index(closestPoint)
                if idx == 0:
                    idx = 1

                ## take the cross product
                y1 = (coords[idx][0] - coords[idx-1][0])
                x1 = (coords[idx][1] - coords[idx-1][1])
                y2 = (center[0] - coords[idx-1][0])
                x2 = (center[1] - coords[idx-1][1])
                cp = (x1*y2)-(x2*y1)

                ## if cross product is negative (to the right of the line segment)
                ## or we are really close to the line, mark us as inside this segment
                if distance < deadzone or cp > 0:
                    shapesIn.append(s[0])
            else:
                ## If no coordinate was passed into this function, just get a
                ## list of the unique vales to pass back
                for s in shapes:
                    if not s[0] in shapesIn:
                        shapesIn.append(s[0])

            ## finished, save off the shapes found for this category, and
            ## go on to the next category for the day
            retVal[day][category[0]] = shapesIn
    return retVal
                
