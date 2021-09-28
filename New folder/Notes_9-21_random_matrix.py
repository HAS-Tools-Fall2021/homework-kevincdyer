# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
# %%
#
test= np.random.randint(1,100, (6,12))
# %%
test2= [[1,2,3,4,5,6,7,8,9,10,11,12],
        [1,2,3,4,5,6,7,8,9,10,11,12],
        [1,2,3,4,5,6,7,8,9,10,11,12],
        [1,2,3,4,5,6,7,8,9,10,11,12],
        [1,2,3,4,5,6,7,8,9,10,11,12],
        [1,2,3,4,5,6,7,8,9,10,11,12]]
array1 = np.ones((6,12))*8

##2
#done in one step
np.round(np.mean(test2),2)
#done in two steps
mean=np.mean(test)
meanround=np.round(mean,2)

print("Average =", np.round(np.mean(rand), 2),
    "stdev=", np.round(np.std(rand),2))

##3
np.round(np.mean(test[:,2]),2)
print("3rd Column Mean =", np.round(np.mean(rand[:, 2]), 2))

##4
print("Row Averages =", np.round(np.mean(rand, axis=1), 2))
print()