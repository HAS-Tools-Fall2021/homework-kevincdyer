# Kevin Dyer's week 7 Forecast Prediction Code

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

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
month_median = np.zeros(31)
for d in range(31):
        daytemp = d+1
        tempdata = data[(data['year']) & (data['month']) & (data['day'] == daytemp)]
        month_median[d] = np.median(tempdata['flow'])
        print('Iteration', d, 'Day=', daytemp, 'Flow=', month_median[d])

# %%
# My Function

def flow_median(year, month, daysinmonth, data):
        flow_median = np.zeros(daysinmonth)
        for d in range(daysinmonth):
                daytemp = d+1
                tempdata = data[(data['year']>=year) & (data['month'] == month) & (data['day'] == daytemp)]
                flow_median[d] = np.median(tempdata['flow'])
                #print('Iteration', d,'Day=', daytemp, 'Flow=', month_median[d])
        return flow_median
# %%
# Change to represent the subset of data you want to see

Year = 2016
Month = 10
Days = 31

flow_subset = flow_median(Year, Month, Days, data)

# %%
print('My one week prediction for average flow is', np.max(flow_subset), \
        'ft^3/s, and my two week prediction is', np.median(flow_subset), \
        'ft^3/s. Both predictions are based off the median flow rates of Camp Verde from the Month of October since 2016. The 1 week prediction is the max of this subset of data due to the unusually high amount of rainfall recently, and the two week preidction is the median of this subset of data.')

# %%
# Line graph of This week's flow so far
fig, ax = plt.subplots()
ax.plot(data['datetime'], data['flow'], color='magenta', label='this week')
ax.set(title="This Week's Flow, 9/30 - 10/6", xlabel='Date', ylabel='Flow in CFS',
        xlim = [datetime.date(2021, 9, 30), datetime.date(2021, 10, 6)],
        ylim = [130, 250])
ax.legend(loc='lower right')
plt.show
fig.savefig("Week7Flow.png")


# %%
# Graph 2: Scatterplot of flow in October 2020 and 2019
fig, ax = plt.subplots(1, 2)
oct_two_year = data[(data['month'] == 10) & (data['year'] == 2019)]
ax[0].scatter(oct_two_year['day'], oct_two_year['flow'], alpha=0.8,
            s = 0.02*oct_two_year['flow'], c=oct_two_year['year'], cmap='magma')

ax[0].set(yscale='log')
ax[0].set_xlabel('Day of the month in Oct, 2019')
ax[0].set_ylabel('Flow')

oct_last_year = data[(data['month'] == 10) & (data['year']==2020)]
ax[1].scatter(oct_last_year['day'], oct_last_year['flow'], alpha=0.8,
            s = 0.02*oct_last_year['flow'], c=oct_last_year['year'], cmap='magma')

ax[1].set(yscale='log')
ax[1].set_xlabel('Day of the month in Oct, 2020')
ax[1].set_ylabel('Flow')
plt.show()
fig.savefig("Oct_2019_2020.png")


# %%
# Graph 3 Scatterplots of Flow this week in 2018 and 2019
fig, ax = plt.subplots(1, 2)
ax[0].scatter(data['datetime'], data['flow'], color='orange', marker='o')
ax[0].set(title="This Week's Flow, 2019", xlabel='Date', ylabel='Flow in CFS',
        xlim =[datetime.date(2019, 10, 10), datetime.date(2019, 10, 16)],
        ylim =[0, 300])

ax[1].scatter(data['datetime'], data['flow'], color='violet', marker='o')
ax[1].set(title="This Week's Flow, 2018", xlabel='Date', ylabel='Flow in CFS',
        xlim =[datetime.date(2018, 10, 10), datetime.date(2018, 10, 16)],
        ylim =[0, 600])
plt.show()
fig.set_size_inches(12, 4)
fig.savefig("This_week_2018_2019")