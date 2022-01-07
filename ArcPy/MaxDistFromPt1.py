# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 16:30:44 2021

@author: A02242626
"""
# =============================================================================
#  This python script is to determine the maximum distance from the first 
# point in the shapefile, as a measure of dispersion behavior
#=============================================================================

import arcpy
import arcpy
import pandas as pd
import numpy as np

#Folder Address containing files
folder = r'I:\GPS_Data\Shapefiles\'


arcpy.env.workspace = folder
filelist = arcpy.ListFeatureClasses(feature_type = 'Point')
arcpy.env.overwriteOutput = True
filelist.sort()


#Create Dataframe with Columns Track ID and Area
df =pd.DataFrame()


#Add field called Depth
for i in filelist:
    print "Processing: " + i # print list to view the status of the script 
    #rename file with suffix, removing .shp([:-4])
    arcpy.AddField_management(i,"Depth","FLOAT")
    
#Calculate Depth Between Pt 1 and Point N    
for i in filelist:
    print "Processing: " + i  
    with arcpy.da.UpdateCursor(in_table =i ,field_names =["Depth","SHAPE@"],explode_to_points = "TRUE") as updater:
        row = next(updater)
        start = row[1]
        for row in updater:
            nextpt = row[1]
            depth = start.distanceTo(nextpt)
            row[0]=depth
            updater.updateRow(row)

for i in filelist:
    print "Procesing: " + i
    arr = arcpy.da.TableToNumPyArray(i,['Depth'])  # pick a field
    # nan functions account for nulls, cast to the dtype of the field using astype  
    maxdepth = np.nanmax(arr.astype('float'))
    df = df.append([[i,maxdepth]], ignore_index=False)
df.columns=['Track ID','Max Depth']
    
        
                
    
    