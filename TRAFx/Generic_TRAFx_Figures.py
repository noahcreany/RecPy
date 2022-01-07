#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 13:56:41 2021

@author: NoahCreany
"""
# =============================================================================
#  This python script is for manipulating TRAFx data from the 'Raw Export' file type
# which comes with two un-named columns but are effectively (Date | Count) 
#=============================================================================

#Highlight these 'import...' statements below and run them before running the code, otherwise it won't work.

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import io
import datetime
import xlrd
import os
import pyexcel as p
#stats, figs, and plots
from scipy import stats
import seaborn as sns
from scipy.interpolate import make_interp_spline, BSpline
import squarify
import matplotlib.ticker as mtick


#set pathname to TRAFx Datafile - you'll need the full path (on windows C:/...) - You're storing the csv in a DataFrame called Data - (Data = pd.read_csv('...'))
Data = pd.read_csv('file/path.csv', header = None)

#Next we'll add column names to the DataFrame
Data.columns=['Date','Count']

#We'll need to convert the timeformats to something that we can manipulate and work with. 
Data['Date'] = pd.to_datetime(Data.Date, format = "%Y-%m-%d %H:%M:%S")

#Optionally, If you want to look at only a specific Date Range you can enter it here in "YYYY-MM-DD" format: (You'll need to delete the '#' to the left of Data)
#   Data = Data[(Data['Date']> "2018-01-01") & (Data['Date']< "2019-07-01")] # This is saying after 2018-01-01 and before 2019-07-01

# =============================================================================
# We can then split the data by mean counts by Day of the Week:
# =============================================================================

GroupedByDayOfWeek = Data.groupby(Data['Date'].dt.day_name())['Count'].mean()

DayofWeek = pd.DataFrame(GroupedByDayOfWeek)
DayofWeek['Day']=DayofWeek.index

#Lets Visualize:
sns.set(style = 'darkgrid') #Background style
plt.figure(figsize = (10,7)) # Figure size
#Create Font dictionaries for plot fonts
Titlefont = {'family': 'serif', 
        'color':  'black',
        'weight': 'normal',
        'size': 16,}
#set fomt size for axes
AxesFont= {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 14,}
    
ax = sns.barplot(
        x = 'Day',
        y = 'Count',
        data = DayofWeek,
        order = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],
        color='#69b3a2')
plt.xlabel('Day of Week', fontdict = AxesFont)
plt.ylabel('Mean # of Visitors', fontdict = AxesFont)
plt.title('Average Counts for Counter Name by Day of Week', fontdict = Titlefont)
plt.show()

# =============================================================================
# Or perhaps we're interested in the Hour of the Day:
# =============================================================================
GroupedByHour = Data.groupby(Data['Date'].dt.hour)['Count'].mean()
HourOfDay = pd.DataFrame(GroupedByHour)
HourOfDay['Hour'] = HourOfDay.index

sns.set(style = 'darkgrid') #Background style
plt.figure(figsize = (10,7)) # Figure size
#Create Font dictionaries for plot fonts
Titlefont = {'family': 'serif', 
        'color':  'black',
        'weight': 'normal',
        'size': 16,}
#set fomt size for axes
AxesFont= {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 14,}
    
ax = sns.barplot(
        x = 'Hour',
        y = 'Count',
        data = HourOfDay,
        color='#69b3a2')
plt.xlabel('Hour of Day', fontdict = AxesFont)
plt.ylabel('Mean # of Visitors', fontdict = AxesFont)
plt.title('Average Hourly Counts for Counter Name', fontdict = Titlefont)
plt.show()


# =============================================================================
# Maybe hourly counts by Weekday vs Weekend:
# =============================================================================
# This first step is just to create a variable to determine which days are weekdays vs weekends
Data['Weekday'] = ((pd.DatetimeIndex(Data.Date).dayofweek) // 5 == 1).astype(float)

GroupedByDayHour = Data.groupby([Data['Weekday'], Data['Date'].dt.hour])['Count'].mean()
Weekday_vs_Weekend_Hourly = GroupedByDayHour.to_frame().reset_index()
Weekday_vs_Weekend_Hourly.columns = ['Weekday','Hour','Count']

sns.set(style = 'darkgrid') #Background style
plt.figure(figsize = (10,7)) # Figure size
#Create Font dictionaries for plot fonts
Titlefont = {'family': 'serif', 
        'color':  'black',
        'weight': 'normal',
        'size': 16,}
#set fomt size for axes
AxesFont= {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 14,}
sns.set(style = 'darkgrid') #Background style

plt.figure(figsize = (10,7)) # Figure size

#Create Font dictionaries for plot fonts
Titlefont = {'family': 'serif', 
        'color':  'black',
        'weight': 'normal',
        'size': 16,}
#set fomt size for axes
AxesFont= {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 14,}
colors = ["#69b3a2", "#4374B3"]
sns.set_palette(sns.color_palette(colors))
    
ax = sns.barplot(
        x = 'Hour',
        y = 'Count',
        data = Weekday_vs_Weekend_Hourly,
        hue = 'Weekday')
plt.xlabel('Hour of Day', fontdict = AxesFont)
plt.ylabel('Mean # of Visitors', fontdict = AxesFont)
plt.title('Weekday vs Weekend Hourly Counts for Counter Name', fontdict = Titlefont)
plt.legend(['Weekend','Weekday'])
plt.show()






