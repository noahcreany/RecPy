# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 16:26:58 2021

@author: Noah Creany
Note: Requires ESRI on machine w/ arcpy environment configured

This script will append fields from a csv to a shapefile layer with a matching identifier.
"""

import arcpy
import pandas as pd

#Specify folder path containing shapefiles
folder = r'I:\SheeprocksOHV\GPS_Data\Shapefiles\Points_FactorScores\AllTracks'


arcpy.env.workspace = folder
filelist = arcpy.ListFeatureClasses(feature_type = 'Point')
arcpy.env.overwriteOutput = True
filelist.sort() # sort filelist 

print filelist
df=pd.read_csv(r'E:\SheeprocksOHV\CFAscores.csv')
dflist= df.values.tolist()
dflist[0]


counter = 0
for row in dflist:
    CFAscore=dflist[counter]
    globals()['CFAscore'+str(counter)]=CFAscore
    counter = counter + 1


for i in filelist:
    print "Processing: " + i # print list to view the status of the script 
    # Set local variables
    inFeatures = i
    fieldName1 = "Achieve"
    fieldName2 = "Family"
    fieldName3 = "Learning"
    arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE")
    arcpy.AddField_management(inFeatures, fieldName2,  "DOUBLE")
    arcpy.AddField_management(inFeatures, fieldName3,  "DOUBLE")

runs = 54
print range(runs)


df.iloc[53,0]      
for j in range(runs):
    with arcpy.da.UpdateCursor(filelist[j], ['Achieve','Family','Learning']) as cursor:
        for row in cursor:
            row[0] = df.iloc[j,0] #df subset df.iloc[rows ie. 9:25 (10-25),colums2:5 (3 to 5)]
            row[1] =  df.iloc[j,1]
            row[2]= df.iloc[j,2]
            #row[3] = scores[3]
            cursor.updateRow(row)
        print "Updated rows for file: {0}".format(filelist[j])


