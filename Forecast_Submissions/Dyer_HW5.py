# Kevin Dyer's code for homework 5

# %%
# Import the modules we will use
import os
import numpy as np
from numpy.core.fromnumeric import shape
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week5.txt'
filepath = os.path.join('data', filename)
print(os.getcwd())
print(filepath)

filepath = '../data/streamflow_week5.txt'

# %%
# Read the data into a pandas dataframe
data = pd.read_table(filepath, sep = '\t', skiprows=30,
        names =['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] = data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# %%
## Column names?
print(data.columns)

## What is its index?
print(data.index)

## What data types do the columns have?
data.dtypes

# %%
## Min, Max, Mean, Median, Std Dev, and Quantiles?
print(data["flow"].min())
print(data["flow"].max())
print(data["flow"].mean())
print(data["flow"].median())
print(data["flow"].std())
print(data["flow"].quantile([0,0.1,0.5,0.9]))

# %%
## Same but on a monthly basis
data.groupby(['month'])[['flow']].describe()

# %%
## Sorting by 5 highest and 5 lowest flow values
data.sort_values(by='flow', ascending=False).head() # Top 5 highest
data.sort_values(by='flow', ascending=False).tail() # Bottom 5 lowest

# %%
## The highest and lowest flow values for every month of the year 
mins = np.array([])
max = np.array([])

for month in data['month']:
        add = data.sort_values(by='flow', ascending=True).head(1)
        mins.append(add)
        add2 = data.sort_values(by='flow', ascending=False).head(1)
        max.append(add2)

# %%
## A list of historical dates with flows that are within 10% of your week 1 forecast value
data.loc[data['flow']] >= 102

t1 = ['flow']
t2 = data('flow')

data.loc[data['flow'] <= 91.8, '<=91.8'] = 'True'
data.loc[data['flow'] >= 112.2, '>=112.2'] = 'True'

data

data.loc[(data['flow'] >= 91.8) and (data['flow'] <= 112.2)].values


print(data.loc[(data['flow'] >= 91.8)] and data.loc[(data['flow'] <= 112.2)])

print(data.loc[(data['flow'] <= 112.2) and data.loc[(data['flow'] >= 91.8)])
