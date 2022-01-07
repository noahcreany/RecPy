pan# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: Noah Creany
This is a script to shift the time of Trafx data - which can be useful for time change due to daylight savings or if you notice strange temporal patterns that result from improper configuration or device malfunction. 
"""
#%% Imports
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
import matplotlib.ticker as mtick
from datetime import datetime
import math
from matplotlib.ticker import MaxNLocator
from textwrap import wrap

from dateutil.relativedelta import *
import tkinter
import tkinter.filedialog
import glob2
from tqdm import tqdm
from functools import partial

#%% Read file
path = '/User/file/path.csv'

df = pd.read_csv(path)
df.columns = ['Date', 'Count','None']
df.Date = pd.to_datetime(df['Date'], format = "%y-%m-%d %H:%M")

#Create new DF
df1hrshift = pd.DataFrame()

#create timeshift
ind = pd.date_range('06/ 21/ 2021 19:00:00', periods = 424, freq= '1H' )

#copy data with timeshift
df1hrshift = pd.DataFrame(data = df['Date'], index = ind)

#Make Date Column from index
df1hrshift['Date'] = df1hrshift.index

# Check data types
df1hrshift.dtypes

#Copy values from df count
df1hrshift['Count'] = df[['Count']].values

#Format new DF
df1hrshift.Date = pd.to_datetime(df1hrshift['Date'], format = "%y-%m-%d %H:%M")
df1hrshift = df1hrshift.reset_index(drop=True)
group24hr = df1hrshift.groupby(df1hrshift['Date'].dt.hour)['Count'].mean()
Chutes24hr = pd.DataFrame(group24hr)
Chutes24hr['Hour'] = Chutes24hr.index

#plot
def hourly(df):
    fig, ax = plt.subplots(figsize = (8,5),dpi = 200) #Figure size
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    sns.set(style = 'darkgrid') #Background style
    #Create Font dictionaries for plot fonts
    # Titlefont = {'family': 'serif', 
    #         'color':  'black',
    #         'weight': 'normal',
    #         'size': 16,}
    # #set fomt size for axes
    # AxesFont= {'family': 'serif',
    #         'color':  'black',
    #         'weight': 'normal',
    #         'size': 14,}
        
    ax = sns.barplot(
            x = 'Hour',
            y = 'Count',
            data = df,
            color='#69b3a2')
    plt.xticks(np.arange(0,24,2),['12 am', '2 am','4 am','6 am','8 am','10 am',
                                  '12 pm','2 pm','4 pm','6 pm','8 pm','10 pm'], rotation = 75)
    #plt.yticks(range(int(min(HourOfDay.Count)), int(math.ceil(max(HourOfDay.Count))+1)))
    ax.yaxis.set_major_locator(MaxNLocator(integer = True))
    # plt.xlabel('Hour of Day', fontdict = AxesFont)
    # plt.ylabel('Mean # of Visitors', fontdict = AxesFont)
    # plt.figtext(0.5, -.1, str(r'$Note:$'+ ' '+ data_range), ha="center", fontsize=12, fontdict = AxesFont)
    # plt.title(str('Average Counts for ' + name + ' by Hour of Day'), fontdict = Titlefont)
    plt.show()
    
hourly(Chutes24hr)   
  
#Prepare for export  
fixed = df1hrshift.copy()
fixed['Hour'] = fixed['Date'].dt.hour #Create Hour Column 
fixed.Hour = pd.to_datetime(fixed['Hour'], format = '%H') #Change format of Hour to 0 Padded

fixed['Date'] = fixed['Date'].dt.date #Extract Date
# fixed['Date'] = fixed['Date'].astype(str)
fixed['Date'] = pd.to_datetime(fixed['Date']).dt.strftime('%y-%m-%d') #Change to TRAFx Format


fixed['Hour'] = fixed['Hour'].astype(str) #Turn Hour to String

fixed['Hour'] = fixed['Hour'].str[11:-3] #Extract only HH:MM from Datetime format
fixed = fixed[['Date','Hour','Count']] #Reorder DataFrame
fixed['Count'] = fixed['Count'].astype(str) #Change Count to String
fixed['Count'] = fixed['Count'].apply(lambda x: x.zfill(5)) # Zero Pad Count
fixed['None'] = "" # Create Blank Column
fixed['None'] = fixed['None'].apply(lambda x: x.zfill(5)) #Zero Pad None Column

fixed.dtypes

# Export to .txt with no header, index, using ',' as separater
fixed.to_csv('/Users/iort10/Downloads/Chutes_shift.txt', header = None, index = None, sep = ',', mode = 'w')


