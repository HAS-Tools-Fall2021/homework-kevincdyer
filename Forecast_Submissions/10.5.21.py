# Starter code for week 6 illustrating how to build an AR model 
# and plot it

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd

#note you may need to do pip install for sklearn

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week6.txt'
filepath = os.path.join('../../data', filename)
print(os.getcwd())
print(filepath)


# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code'],
        parse_dates=['datetime']
        )

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek


# %%
## Column names?
print(data.columns)

i = data["month"] == 10
for i in range(31):
        print(np.mean(data["flow"]))

#%%
oct_mean = np.zeros(31)
for d in range(31):
        daytemp = d+1
        tempdata = data[(data['month']==10) & (data['day'] == daytemp)]
        oct_mean[d] = np.mean(tempdata['flow'])
        print('Iteration', d,'Day=', daytemp, 'Flow=', oct_mean[d])

#%%

def day_mean(month, daysinmonth, data):
        month_mean = np.zeros(daysinmonth)
        for d in range(daysinmonth):
                daytemp = d+1
                tempdata = data[(data['month']==month) & (data['day'] == daytemp)]
                month_mean[d] = np.mean(tempdata['flow'])print('Iteration', d,'Day=', daytemp, 'Flow=', oct_mean[d])
        return month_mean
# %%
