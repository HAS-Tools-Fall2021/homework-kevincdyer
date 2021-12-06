# %%
import pandas as pd
import os
import numpy as np

# %%
filename = 'streamflow_week15.txt'
filepath = os.path.join(filename)
print(os.getcwd())
print(filepath)

# %%
#Read the data into a pandas dataframe
flow_data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code'],
        parse_dates=['datetime']
        )

# %%
# Expand the dates to year month day, set index as base datetime
flow_data['year'] = pd.DatetimeIndex(flow_data['datetime']).year
flow_data['month'] = pd.DatetimeIndex(flow_data['datetime']).month
flow_data['day'] = pd.DatetimeIndex(flow_data['datetime']).day
flow_data['dayofweek'] = pd.DatetimeIndex(flow_data['datetime']).dayofweek
flow_data = flow_data.set_index('datetime')

month_median = np.zeros(31)
for d in range(31):
        daytemp = d+1
        tempdata = flow_data[(flow_data['year']) & (flow_data['month']) & (flow_data['day'] == daytemp)]
        month_median[d] = np.median(tempdata['flow'])
        print('Iteration', d, 'Day=', daytemp, 'Flow=', month_median[d])

# %%
def flow_median(startyear, month, daysinmonth, flow_data):
        '''
        This function determines the median flow for any month, day, or year in the range of the data.

        Parameters:
        "month" represents the number of the month you want, int (October = 10)
        "startyear" the year range you want, int (year =< 2021)
        "daysinmonth" represents the amount of days in month, which for October, is 31.
        "flow_data" is my dataframe

        Output:
        This function returns a print statement that provides the median flow of that range
        '''
        flow_median = np.zeros(daysinmonth)
        for d in range(daysinmonth):
                daytemp = d+1
                tempdata = flow_data[(flow_data['year']>=startyear) & (flow_data['month'] == month) & (flow_data['day'] == daytemp)]
                flow_median[d] = np.median(tempdata['flow'])
        return flow_median

print('Iteration', d,'Day=', daytemp, 'Flow=', month_median[d])

# %%
startyear = 2016
month = 12
daysinmonth = 31

flow_subset = flow_median(startyear, month, daysinmonth, flow_data)

print(flow_subset)

# %%
print('My one week prediction for average flow is', np.mean(flow_subset[4:14]), \
        'ft^3/s, and my two week prediction is', np.median(flow_subset), \
        'ft^3/s. Both predictions are based off the median flow rates of Camp Verde from the Month of October since 2011. The 1 week prediction is the max of this subset of data due to the unusually high amount of rainfall recently, and the two week preidction is the median of this subset of data.')

