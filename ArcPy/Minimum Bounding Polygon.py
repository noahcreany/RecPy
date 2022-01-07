# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 16:39:52 2021

@author: A02242626
"""

import arcpy
import pandas as pd

#Folder Address containing files
folder = r'E:\file\path'


arcpy.env.workspace = folder
filelist = arcpy.ListFeatureClasses(feature_type = 'Point')
arcpy.env.overwriteOutput = True

#Create Dataframe with Columns Track ID and Area
#df =pd.DataFrame({'Track_ID':[],'Trip':[],"Area":[]})
df = pd.DataFrame()
#Re-order columns
df = df[['Track_ID','Trip',"Area"]]
df = df.astype({'Track_ID':str})
df = df.astype({'Trip': int})
df.dtypes



for i in filelist:
    print "Processing: " + i # print list to view the status of the script 
    #rename file with suffix, removing .shp([:-4])
    newname = i[:-4] + "_mbp"
    #turn points into minimum bounding polygon
    mbp=arcpy.management.MinimumBoundingGeometry(i, newname,"CONVEX_HULL",group_option = "LIST", group_field=["trip"])
    #Add Fields to polygon
    arcpy.AddField_management(mbp, "Area", "FLOAT")
    #Specify type of area measurement
    exp = "!SHAPE.AREA@SQUAREKILOMETERS!"
    #Calculate Area
    arcpy.CalculateField_management(mbp, "Area", exp, "PYTHON_9.3")
    with arcpy.da.SearchCursor(mbp, 'Shape@Area',spatial_reference=arcpy.SpatialReference(6341)) as cursor:
        trip = 1
        for row in cursor:
            area = row[0]
            area = float(area)
            filename = str(newname)
            obs = trip
            df = df.append([[filename,obs,area]], ignore_index=True)
            trip = trip + 1
    
    #geometry = arcpy.CopyFeatures_management(mbp,arcpy.Geometry())
    #Area = geometry.getArea("Planar","SQUAREKILOMETERS")
    #Save TrackID and Area to DataFrame 
    
    
    
 