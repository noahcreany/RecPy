# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: Noah Creany
This script is to add a speed or velocity field to a shapefile layer for analysis.  
"""

import arcpy
from datetime import datetime


filename = arcpy.GetParameterAsText(0)

# Add a new field that will store the time difference data
arcpy.AddField_management(filename, "time_diff", "Float")

# Create the update cursor, time_diff is where we will store our data and time is where we are pulling data from
with arcpy.da.UpdateCursor(in_table=filename, field_names= ['time_diff','time']) as updater:
    
# row is used to continue to get the time between the next point in the updater we created
    row = next(updater)
    
# row 1 refers to the 'time above as this is considered 1, as it is the second in our field_name list.
    var = row[1]
# use datetime.strptime to convert the time which is stored as a string into datetime, and now we can subract with it.
    var1 = datetime.strptime(var, '%Y/%m/%d %H:%M:%S')
    
# We will start looping through the updater we created. 
    for row in updater:
        current = row [1]
# use datetime.strptime to convert the time which is stored as a string into datetime, and now we can subract with it.
        current1 = datetime.strptime(current, '%Y/%m/%d %H:%M:%S')
        
# this shows the difference between current1 and var1 which gives us the time.
        diff = current1 - var1
        
# we need to get the minutes from the seconds in our diff variable as this is what our time difference will be
        minute = (diff.seconds/60)
        
# write this to row [0] which is time_diff in our field_name list
        row[0] = minute
       
#this will update the rows in our shapefile. 
        updater.updateRow(row)
        
# this ensures we are calculating the time between adjacent points
        var1 = current1
  
        

# Add a new field that will store the time difference data
arcpy.AddField_management(filename, "distance", "Float")

# Create the update cursor, distance is where we will store our data and SHAPE@ is where we are pulling the geometry data from
with arcpy.da.UpdateCursor(in_table=filename, field_names= ['distance', 'SHAPE@']) as updater:
    
# row is used to continue to get the distance between the next point in the updater we created
    row = next(updater)
    
# row 1 refers to the geometry 'SHAPE@' above as this is considered 1
    sg = row[1]
    
# We will start looping through the updater we created. 
    for row in updater:
        current = row [1]
        
#this shows the distance between var and current to get the distnace.
        dist = sg.distanceTo(current)

# write this to row [0] which is distance in our field_name list    
        row[0] = dist
        
#this will update the rows in our shapefile. 
        updater.updateRow(row)
    
# this ensures we are calculating the time between adjacent points
        sg = current
        

# Add a new field that will store the speed difference data
arcpy.AddField_management(filename, "speed", "Float")

# Create the update cursor, speed is where we will store our data and time_diff and distance is where we are pulling data from
with arcpy.da.UpdateCursor(in_table=filename, field_names= ['speed', 'time_diff', 'distance']) as updater:
    
# row is used to continue to get the distance between the next point in the updater we created
    row = next(updater)
    
# row 1 refers to the geometry 'SHAPE@' above as this is considered 1
    td = row[1]
    dista = row[2]
    
# We will start looping through the updater we created. 
    for row in updater:
        time = row [1]
        dis = row [2]
        
# to calculate speed you must divide distance from time 
        spd = dis / time

#  write speed into the row [0] which is the first item in or field_name list, speed.        
        row[0] = spd

# this will update the rows in our shapefile. 
        updater.updateRow(row)
    
# this ensures we are calculating the time between adjacent points
        td = current
        
    
        
arcpy.AddMessage('Done!')