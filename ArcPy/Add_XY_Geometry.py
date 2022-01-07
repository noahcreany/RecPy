# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 10:51:58 2021

@author: Noah Creany
Note: Requires ESRI on machine w/ arcpy environment configured

This script adds X,Y coordinates for all shape files in a folder
"""
import arcpy

folder = r'file\path'
srs = 'NAD_1983_UTM_Zone_12N' #Spatial Reference System

#set environment workspace
arcpy.env.workspace = folder

#Query workspace for point feature classes and assign to points_list
points_list = arcpy.ListFeatureClasses(feature_type='Point')

#Print the list of shapefiles that are Points
print points_list


#For loop to iterate through list of points_List
for i in points_list:
    #Assign spatial reference name to sr
    sr = arcpy.Describe(i).spatialReference.name
    #if Sr is the same as srs, then
    if sr == srs:
        #add XY Coordinates to Point
        arcpy.AddXY_management(i)
        #set environment variables listing fields in the shapefile
        field = arcpy.ListFields(i)
        #print the fieldnames in the shapefile
        print i, [field.name for field in arcpy.ListFields(i)]
