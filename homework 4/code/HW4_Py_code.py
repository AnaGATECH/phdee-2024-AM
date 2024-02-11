# HW 4 code -- Ana Mazmishvili

from IPython import get_ipython
get_ipython().magic('reset -sf')

# Import packages 
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy import stats
import csv
from scipy.optimize import minimize
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression as lr


# Set working directories and seed

#If working from home:

datapath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 4\data'
outputpath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 4\output'

# If working on campus: 

#datapath = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 4\data'
#outputpath = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 4\output'


np.random.seed(4)

# Load dataset in the system 

data=pd.read_csv(datapath +'/fishbycatch.csv')


print(data.info())
# Convert the panel data from wide form to long form
df = pd.wide_to_long(data, stubnames=["shrimp", "salmon", "bycatch"], i='firm', j='month')



# 1.  Group by 'group' and 'month' and calculate the mean for each group in each month
grouped_data =df.groupby(by = ['treated', 'month']).mean().reset_index()


# Plotting
plt.figure(figsize=(10, 6))
for group in df['treated'].unique():
    group_data = grouped_data[grouped_data['treated'] == group]
    plt.plot(group_data['month'], group_data['bycatch'], label=group)

plt.title('Line Plot for Treated and Control Groups Over Months')
plt.xlabel('Month')
plt.xticks(range(1,25))
plt.ylabel('Average bycatch')
plt.axvline(x=12, color='red', linestyle='--', label='Treatment Month')
## Rename legends
new_legend_labels = ['Control Group', 'Treated Group']
plt.legend(labels=new_legend_labels)
plt.savefig(outputpath + '/figure/trend1.pdf',format='pdf')
plt.show()

# 2. 

## Create indicator variables for post-treatment period
df['post_treatment'] = (df.index.get_level_values('month') >= 13).astype(int)
df['trt_posttrt'] = (df['post_treatment']*df['treated'])



## Estimate the DiD effect using linear regression
ols = sm.add_constant(df[['treated', 'post_treatment', 'trt_posttrt']])
model = sm.OLS(df['bycatch'], ols).fit()
params = model.params.to_numpy()
nobs = model.nobs

## Display the regression results
print(model.summary())

print(model.params)

# Save the original standard output
original_stdout = sys.stdout

# Redirect standard output to a file
with open(outputpath + '/table/DIDoutput1.tex', 'w') as f:
    sys.stdout = f
    print(model.params)

# Restore the original standard output
sys.stdout = original_stdout




