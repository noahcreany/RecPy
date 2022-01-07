# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 11:22:38 2021

@author: Noah Creany
Note: Requires ESRI on machine w/ arcpy environment configured

This script add new fields to all point shapefiles in a folder.  
"""

import arcpy
import pandas as pd
from datetime import datetime

#Folder Address containing files
folder = r'file\path'


arcpy.env.workspace = folder
filelist = arcpy.ListFeatureClasses(feature_type = 'Point')
arcpy.env.overwriteOutput = True

for i in filelist:
    print "Processing: " + i # print list to view the status of the script 
    # Set local variables
    inFeatures = i
    fieldName1 = "Value1"
    fieldName2 = "Value2"
    fieldName3 = "Value3"
    fieldName4 = "Value4"
    
    
    # Execute AddField for new fields
    arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE")
    arcpy.AddField_management(inFeatures, fieldName2,  "DOUBLE")
    arcpy.AddField_management(inFeatures, fieldName3,  "DOUBLE")
    arcpy.AddField_management(inFeatures, fieldName4,  "DOUBLE")

print "-----------All Done!----------- "    

#Add Integer for each unique value(TrackID) in attribute table    
import arcpy
import numpy
 
def unique_values(table,field):
     data = arcpy.da.TableToNumPyArray(table,[field])
     return numpy.unique(data[field]).tolist(0)
 
fc = r'file\path.shp'    
myvalues = unique_values(fc,'tident')
print myvalues