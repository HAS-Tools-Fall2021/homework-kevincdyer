# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
import json 
import urllib.request as req
import urllib


# %%

# Get data from online, read into pandas dataframe
flow_url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb" \
           "&site_no=09506000&referred_module=sw" \
           "&period=&begin_date=1989-01-01&end_date=2021-10-23"
flow_data = pd.read_table(flow_url, sep='\t', skiprows=30,
                          names=['agency_cd', 'site_no', 'datetime', 'flow',
                                 'code'], parse_dates=['datetime'])

# Expand the dates to year month day, set index as base datetime
flow_data['year'] = pd.DatetimeIndex(flow_data['datetime']).year
flow_data['month'] = pd.DatetimeIndex(flow_data['datetime']).month
flow_data['day'] = pd.DatetimeIndex(flow_data['datetime']).day
flow_data['dayofweek'] = pd.DatetimeIndex(flow_data['datetime']).dayofweek
flow_data = flow_data.set_index('datetime')

# %%
# First Create the URL for the rest API
# Insert your token here
mytoken = '303f810eafb74f30acf3c9903bc984c0'

# This is the base url that will be the start our final url
base_url = "http://api.mesowest.net/v2/stations/timeseries"

# First Source - Sedona Airport Station
# Specific Arguments for Sedona Airport
args = {
    'start': '199701010000',
    'end': '202012310000',
    'obtimezone': 'UTC',
    'vars': 'air_temp',
    'stids': 'KSEZ',
    'units': 'precip|mm',
    'token': mytoken} 

# Takes your arguments and paste them together
# into a string for the api
# (Note you could also do this by hand, but this is better)
apiString = urllib.parse.urlencode(args)
print(apiString)

# add the API string to the base_url
fullUrl = base_url + '?' + apiString
print(fullUrl)

# Now we are ready to request the data
# this just gives us the API response... not very useful yet
response = req.urlopen(fullUrl) 
responseDict = json.loads(response.read())
dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
precip = responseDict['STATION'][0]['OBSERVATIONS']['precip_accum_24_hour_set_1']

precip_data = pd.DataFrame({'Precipitation (mm)': precip},
                           index=pd.to_datetime(dateTime))

rain_daily = precip_data.resample('D').max()
rain_daily['Precipitation (mm)'] = rain_daily['Precipitation (mm)'].fillna(0)
rain_daily['year'] = pd.DatetimeIndex(rain_daily.index).year
rain_daily['month'] = pd.DatetimeIndex(rain_daily.index).month
rain_daily['day'] = pd.DatetimeIndex(rain_daily.index).day

# %%

# Second source - Flagstaff, Arizona
# Specific arguments for Flagstaff
args = {
    'start': '199701010000',
    'end': '202012310000',
    'obtimezone': 'UTC',
    'vars': 'precip_accum_24_hour',
    'stids': 'KFLG',
    'units': 'precip|mm',
    'token': mytoken}

# Take arguments and paste them together into a string for the api
apiString = urllib.parse.urlencode(args)
print(apiString)

# add the API string to the base_url
fullUrl = base_url + '?' + apiString
print(fullUrl)

# Request and read the data
response = req.urlopen(fullUrl)
responseDict = json.loads(response.read())
dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
precip = responseDict['STATION'][0]['OBSERVATIONS']['precip_accum_24_hour_set_1']

# Now we can combine this into a pandas dataframe
precip_data = pd.DataFrame({'Precipitation (mm)': precip},
                           index=pd.to_datetime(dateTime))

# Now convert this to daily data using resample
# Data has nan values for all non-2f-hour interval timestamps, must remove
fgz_daily = precip_data.resample('D').max()
fgz_daily['Precipitation (mm)'] = fgz_daily['Precipitation (mm)'].fillna(0)
fgz_daily['year'] = pd.DatetimeIndex(fgz_daily.index).year
fgz_daily['month'] = pd.DatetimeIndex(fgz_daily.index).month
fgz_daily['day'] = pd.DatetimeIndex(fgz_daily.index).day

# %%
# Third source - Camp Verde Area

url = "https://daymet.ornl.gov/single-pixel/api/data?lat=34.9455" \
       "&lon=-113.2549&vars=prcp&start=1989-01-01&end=2021-10-24" \
       "&format=csv"
csv_data = pd.read_table(url, delimiter=',', skiprows=6)

# %%

oct_rain = rain_daily[rain_daily['month'] == 10]
rain_mean = oct_rain.groupby('day')['Precipitation (mm)'].mean()
oct_fgz = fgz_daily[fgz_daily['month'] == 10]
fgz_mean = oct_fgz.groupby('day')['Precipitation (mm)'].mean()
oct_cvd = csv_data[csv_data['yday'] >= 274]
oct_cvd = oct_cvd[oct_cvd['yday'] <= 304]
cvd_mean = oct_cvd.groupby('yday')['prcp (mm/day)'].mean()
rain_climo = rain_mean.cumsum()
fgz_climo = fgz_mean.cumsum()
cvd_climo = cvd_mean.cumsum()

fig, ax = plt.subplots()
ax.plot(psr_mean.index, psr_climo, color='steelblue',
        label='Prescott')
ax.plot(fgz_mean.index, fgz_climo, color='crimson',
        label='Flagstaff')
ax.plot(fgz_mean.index, cvd_climo, color='gold',
        label='Camp Verde')
ax.set(title="Mean Monthly Precipitation", xlabel="Day of Month",
       ylabel="Cumulative Precipitation Totals (mm)")
ax.legend()
plt.show()
fig.savefig('Mean_precip_cumulative.png')

# %%
# Week 9 Flow

recent_flow = flow_data.tail(30)
xformat = df("%m-%d")
plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots()
ax.plot(recent_flow['flow'], color='steelblue', label='Last Month')
ax.xaxis.set_major_formatter(xformat)
ax.xaxis.set_major_locator(dl(interval=4))
ax.set(title="Observed Flow", xlabel="Date",
       ylabel="Weekly Avg Flow [CFS]")
ax.legend()
plt.show()
fig.savefig('flow_week9.png')

# %%
month_median = np.zeros(31)
for d in range(31):
        daytemp = d+1
        tempdata = flow_data[(flow_data['year']) & (flow_data['month']) & (flow_data['day'] == daytemp)]
        month_median[d] = np.median(tempdata['flow'])
        print('Iteration', d, 'Day=', daytemp, 'Flow=', month_median[d])

# %%
# My Function

def flow_median(startyear, month, daysinmonth, data):
        '''
        This function determines the median flow for any month, day, or year in the range of the data.

        Parameters:
        "month" represents the number of the month you want, int (October = 10)
        "startyear" the year range you want, int (year =< 2021)
        "daysinmonth" represents the amount of days in month, which for October, is 31.
        "data" is my dataframe

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
# Change to represent the subset of data you want to see

Startyear = 2012
Month = 10
Days = 31

flow_subset = flow_median(Startyear, Month, Days, flow_data)

print(flow_subset)

# %%
print('My one week prediction for average flow is', np.max(flow_subset), \
        'ft^3/s, and my two week prediction is', np.median(flow_subset), \
        'ft^3/s. Both predictions are based off the median flow rates of Camp Verde from the Month of October since 2011. The 1 week prediction is the max of this subset of data due to the unusually high amount of rainfall recently, and the two week preidction is the median of this subset of data.')

# %%
