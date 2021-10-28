# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
import dataretrieval.nwis as nwis

# %%
# Option 3: Use a package to interact with the API for us
# Here we are using the NWIS package
station_id = "09506000"
start_date = '1989-01-01'
stop_date = '2020-10-18'
# Note that this actually gets it in a slightly better format for us
# we don't have to specify the column names it already knows
casa_verde = nwis.get_record(sites=station_id, service='dv',
                          start=start_date, end=stop_date, parameterCd='00060')
# %%
station_id = "09523200"
start_date = '1989-01-01'
stop_date = '2020-10-18'
# Note that this actually gets it in a slightly better format for us
# we don't have to specify the column names it already knows
Yuma = nwis.get_record(sites=station_id, service='dv',
                          start=start_date, end=stop_date, parameterCd='00060')
# %%
station_id = "09427500"
start_date = '1989-01-01'
stop_date = '2020-10-18'
# Note that this actually gets it in a slightly better format for us
# we don't have to specify the column names it already knows
Parker_Dam = nwis.get_record(sites=station_id, service='dv',
                          start=start_date, end=stop_date, parameterCd='00060')
# %%
#Plotting October flow
oct_flow = datai[datai.index.month == 10]
datai['day'] = datai.index.day
oct_median = datai.groupby(datai.index.day).median()
oct_median = datai.groupby('day').median()
oct_max = datai.groupby('day').max()
oct_min = datai.groupby('day').min()

# 1. Timeseries of observed weekly flow values
fig, ax = plt.subplots()
ax.plot(oct_median['flow'], color='grey',
        linestyle='dashed', label='Median')
ax.fill_between(oct_max.index, oct_min['flow'], oct_max['flow'], color = 'blue', alpha=0.1)
ax.plot(oct_min['flow'], color='blue', linestyle='dashed', label='Min')
ax.plot(oct_max['flow'], color='blue', linestyle='dashed', label='Max')
ax.plot(oct_flow["2020"].day, oct_flow["2020"].flow, color='black', label='2020 flow')
ax.set(title="Observed Flow", xlabel="Date",
       ylabel="Daily Avg Flow [cfs]",
       yscale='log')
ax.legend()

2. Timeseries of monthly flow
month_flow = datai.resample("M").sum()
month_flow['month'] = month_flow.index.month

mmean = month_flow.groupby('month').mean()
mmin = month_flow.groupby('month').min()
mmax = month_flow.groupby('month').max()

fig, ax = plt.subplots()
ax.plot(mmean['flow'], color='grey',
        linestyle='dashed', label='Mean')
ax.fill_between(mmin.index, mmin['flow'],
                mmax['flow'], color='blue', alpha=0.1)
ax.plot(mmin['flow'], color='blue', linestyle='dashed', label='Min')
ax.plot(mmax['flow'], color='blue', linestyle='dashed', label='Max')
ax.plot(month_flow["2020"].month, month_flow["2020"].flow,
        color='purple', label='2020')
ax.plot(month_flow["2021"].month, month_flow["2021"].flow,
        color='green', label='2021')
ax.set(title="Observed Monthly Flow", xlabel="Date",
       ylabel="Monthly Total Flow [cfs]",
       yscale='log')
ax.legend()