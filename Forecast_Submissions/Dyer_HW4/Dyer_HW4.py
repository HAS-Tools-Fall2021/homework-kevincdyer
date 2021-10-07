# Kevin Dyer's code for Homework 4

# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
filename = 'streamflow_week4.txt'
filepath = os.path.join('../../data', filename)
print(os.getcwd())
print(filepath)

# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# Make a numpy array of this data
flow_data = data[['year', 'month','day', 'flow']].to_numpy()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %%

# 1a. Here is how to do that on one line of code
flow_count = np.sum((flow_data[:,3] > 85) & (flow_data[:,1]==9) & (flow_data[:,0] >=2000))
print(flow_count)

# Here is the same thing broken out into multiple lines:
flow_test = flow_data[:, 3] > 600  # Note that this returns a 1-d array that has an entry for every day of the timeseies (i.e. row) with either a true or a fals
month_test = flow_data[:, 1] ==7   # doing the same thing but testing if month =7 
year_test = flow_data[:, 0] ==2020
combined_test = flow_test & month_test  # now looking at our last two tests and finding when they are both true
flow_count = np.sum(combined_test) # add up all the array (note Trues = 1 and False =0) so by default this counts all the times our criteria are true
print(flow_count)

#__________________________

flow_mean = np.mean(flow_data[(flow_data[:,3] > 600) & (flow_data[:,1]==7),3])

# 2.b The same thing split out into multiple steps
criteria = (flow_data[:, 3] > 600) & (flow_data[:, 1] == 7)  # This returns an array of true fals values with an entrry for every day, telling us where our criteria are met
flow_pick = flow_data[criteria, 3] #Grab out the 4th column (i.e. flow) for every row wherer the criteria was true
flow_mean =  np.mean(flow_pick) # take the average of the values you extracted

print("Flow meets this critera", flow_count, " times")
print('And has an average value of', np.round(flow_mean,2), "when this is true")

#__________________________
## Histogram of data 1

# step 1: Use the linspace  funciton to create a set  of evenly spaced bins
mybins = np.linspace(0, 1000, num=10)
# another example using the max flow to set the upper limit for the bins
#mybins = np.linspace(0, np.max(flow_data[:,3]), num=15) 

#Step 2: plotting the histogram
plt.hist(flow_data[:,3], bins = mybins)
plt.title('Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#%%
## Histogram of data 2

# step 1: Use the linspace  funciton to create a set  of evenly spaced bins
mybins = np.linspace(0, 180, num=10)
# another example using the max flow to set the upper limit for the bins
#mybins = np.linspace(0, np.max(flow_data[:,3]), num=15) 

#Step 2: plotting the histogram
plt.hist(flow_data[:,3], bins = mybins)
plt.title('Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#__________________________
## Example 4: Get the quantiles of flow

# 4.a  Apply the np.quantile function to the flow column 
# grab out the 10th, 50th and 90th percentile flow values
flow_quants1 = np.quantile(flow_data[:,3], q=[0,0.1, 0.5, 0.9])
print('Method one flow quantiles:', flow_quants1)

# 4.b  use the axis=0 argument to indicate that you would like the funciton 
# applied along columns. In this case you will get quantlies for every column of the 
# data automatically 
flow_quants2 = np.quantile(flow_data, q=[0,0.1, 0.5, 0.9], axis=0)
#note flow_quants2 has 4 columns just like our data so we need to say flow_quants2[:,3]
# to extract the flow quantiles for our flow data. 
print('Method two flow quantiles:', flow_quants2[:,3]) 

# %%
#Solution to Assignment 4 Question 3:
flow_count = np.sum((flow_data[:,3] > 85) & (flow_data[:,1]==9))
print(flow_count)

#Solution to Assignment 4 Question 4:
flow_count = np.sum((flow_data[:,3] > 85) & (flow_data[:,1]==9) & (flow_data[:,0] <=2000))
print(flow_count)

flow_count = np.sum((flow_data[:,3] > 85) & (flow_data[:,1]==9) & (flow_data[:,0] >=2010))
print(flow_count)

#Solution to Assignment 4 Question 5:
##First Half of September
flow_count = np.sum((flow_data[:,3] > 85) & (flow_data[:,1]==9) & (flow_data[:,2] <=15))
print(flow_count)

##Second Half of September:
flow_count = np.sum((flow_data[:,3] > 85) & (flow_data[:,1]==9) & (flow_data[:,2] >=15))
print(flow_count)

