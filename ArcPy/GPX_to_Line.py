# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 16:46:07 2021

@author: Noah Creany
"""
# =============================================================================
#  This python script is to transform a gpx file into a line shapefile 
#=============================================================================


import os
import arcpy

while len(os.sys.path) != 0:  
      for elems in os.sys.path:  
           os.sys.path.remove(elems)  
os.sys.path.append(r'C:\Python27\ArcGIS10.6\Lib\xml') #for etree lib  
os.sys.path.append(r'C:\Python27\ArcGIS10.6\Lib\xml\parsers') #for expat lib  
os.sys.path.append(r'C:\Python27\ArcGIS10.6\DLLs') #for arc to run it, at least  
  
from xml.etree import ElementTree  
import arcpy as AP  
  
tree = ElementTree.parse(r'C:\MyFile.xml')  
Node = tree.getiterator('MyNode')  
MyNode = Node[0].text  


source_folder = r'file\path\containing_gpx_files'
out_fc = r'output\file\path\for_shapefile_layers'

#Set environment workspace within the folder
arcpy.env.workspace = source_folder

#build list of gpx files from source folder
gpx_files = []
for root, dir, files in os.walk(source_folder):
  for file in files:
    if os.path.splitext(file)[1] == '.gpx':
      gpx_files.append(os.path.join(root,file))
      arcpy.GPXtoFeatures_conversion(gpx_files[0], out_fc)
