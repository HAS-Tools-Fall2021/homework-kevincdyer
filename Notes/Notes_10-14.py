# Kevin Dyer's week 7 Forecast Prediction Code

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from matplotlib.dates import DateFormatter

# %%
# Set the file name and path to where you have stored the data
filename = 'streamflow_week7.txt'
filepath = os.path.join('..\..\data', filename)
print(os.getcwd())
print(filepath)

# %%
# Read the data into a pandas dataframe
data = pd.read_table(filepath, sep = '\t', skiprows=30,
        names = ['agency_cd', 'site_no', 'datetime', 'flow', 'code'],
        parse_dates=['datetime']
        )

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# %%
data = data.set_index('datetime')
oct_flow = data[data.index.month == 10]
data['day'] = data.index.day
oct_median = data.groupby(data.index.day).median()
oct_max = data.groupby(data.index.day).max()
oct_min = data.groupby(data.index.day).max()

# %%
data = df.groupby('day')['flow'].agg({'Low Value':'min','High Value':'max','Median':'median'})
data.reset_index(inplace=True)

ax  = data.plot(x='day', y='flow', c='white')
plt.fill_between(x='flow',y1='Low Value',y2='High Value', data=data)
# %%
