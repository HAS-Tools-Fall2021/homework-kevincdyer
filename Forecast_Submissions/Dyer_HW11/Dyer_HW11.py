# This script assumes you have already downloaded several netcdf files
# see the assignment instructions for how to do this
# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# netcdf4 needs to be installed in your environment for this to work
import xarray as xr
import rioxarray
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns
import geopandas as gpd
import fiona
import shapely
from netCDF4 import Dataset

#NOTE To install the packages you need you should use the followin line:
# conda install xarray dask netCDF4 bottleneck


# %%
# Net CDF file historical time series
# https://towardsdatascience.com/handling-netcdf-files-using-xarray-for-absolute-beginners-111a8ab4463f
data_path = os.path.join('..', '..', 'data',
                         'air.sig995.2021.nc')

# Read in the dataset as an x-array
dataset = xr.open_dataset(data_path)
# look at it
dataset


# We can inspect the metadata of the file like this:
metadata = dataset.attrs
metadata
# And we can grab out any part of it like this:
metadata['dataset_title']

# we can also look at other  attributes like this
dataset.values
dataset.dims
dataset.coords

# Focusing on just the precip values
airtemp = dataset['air']
airtemp

# Now to grab out data first lets look at spatail coordinates:
dataset['air']['lat'].values.shape
# The first 4 lat values
dataset['air']['lat'].values
dataset['air']['lon'].values

# Now looking at the time;
dataset["air"]["time"].values
dataset["air"]["time"].values.shape


# Now lets take a slice: Grabbing data for just one point
lat = dataset["air"]["lat"].values[0]
lon = dataset["air"]["lon"].values[0]
print("Long, Lat values:", lon, lat)
one_point = dataset["air"].sel(lat=lat,lon=lon)
one_point.shape

# use x-array to plot timeseries
one_point.plot.line()
precip_val = one_point.values

# Make a nicer timeseries plot
fig, ax = plt.subplots(figsize=(12, 6))
one_point.plot.line(hue='lat',
                    marker="o",
                    ax=ax,
                    color="grey",
                    markerfacecolor="purple",
                    markeredgecolor="purple")
ax.set(title="Time Series For a Single Lat / Lon Location")
fig.savefig("Air_Temp")

#Conver to dataframe
one_point_df = one_point.to_dataframe()

# %%
# Making a spatial map of one point in time
start_date = "2000-01-01"
end_date = "2000-01-01"

timeslice = dataset["air"].sel(
    time=slice(start_date, end_date))

timeslice.plot()

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

month_median = np.zeros(10)
for d in range(10):
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

Startyear = 2017
Month = 11
Days = 10

flow_subset = flow_median(Startyear, Month, Days, flow_data)

print(flow_subset)

# %%
print('My one week prediction for average flow is', np.max(flow_subset), \
        'ft^3/s, and my two week prediction is', np.median(flow_subset), \
        'ft^3/s. Both predictions are based off the median flow rates of Camp Verde from the Month of October since 2016. The 1 week prediction is the max of this subset of data due to the unusually high amount of rainfall recently, and the two week preidction is the median of this subset of data.')

# %%
