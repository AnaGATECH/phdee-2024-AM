# HW 2 code -- Ana Mazmishvili

# Clear all

from IPython import get_ipython
get_ipython().magic('reset -sf')

# Import packages - you may need to type "conda install numpy" the first time you use a package, for example.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy import stats
import csv

# Set working directories and seed

datapath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 2\data'
outputpath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 2\output'


np.random.seed(6578103)

# Load dataset in the system 

data=pd.read_csv(datapath +'/kwh.csv')

#-----------------------------------------------------
### Questions 1.1
#-----------------------------------------------------
## a. Create a table that displays each variable’s sample mean, sample standard deviation, and p-values for the two-way t-test between treatment and control group means. 

# Create subsamples for treated and nontreated HHs.
treat=data.loc[data['retrofit']==1].drop('retrofit',axis=1)
notreat=data.loc[data['retrofit']==0].drop('retrofit',axis=1)

# Generate means, standard deviations, and number of observations and format then to two decimal places

means_control = notreat.mean().map('{:.2f}'.format)
stdev_control = notreat.std().map('{:.2f}'.format)
nobs_control = pd.Series(notreat.count().min())

means_treatment = treat.mean().map('{:.2f}'.format)
stdev_treatment = treat.std().map('{:.2f}'.format)
nobs_treatment = pd.Series(treat.count().min())


# Compute P-values and t-statistics
p_vals = []
t_stats = []    
for col in treat.columns:
    p_vals.append(stats.ttest_ind(notreat[col],treat[col],)[1])
    t_stats.append(stats.ttest_ind(notreat[col],treat[col],)[0])
p_vals = pd.Series(p_vals, index = treat.columns).map('{:.3f}'.format)
t_stats = pd.Series(t_stats, index = treat.columns).map('[{:.3f}]'.format)

# Set the row and column names
rownames = pd.concat([pd.Series(['Monthly electricity usage by HHs (kWh)','Square feet of home','Outdoor average temperature (\\textdegree F)', 'Observations']),
                    pd.Series([' ',' ',' '])],axis = 1).stack() 


# Align std deviations under means and add observations
col1 = pd.concat([means_control,stdev_control,nobs_control],axis = 1).stack()
col2 = pd.concat([means_treatment,stdev_treatment,nobs_treatment],axis = 1).stack()
col3 = pd.concat([p_vals,t_stats,pd.Series([' '])],axis = 1).stack()

# Add column and row labels.  Convert to dataframe 
col = pd.DataFrame({'Control': col1, 'Treatment': col2, 'P-value': col3})
col.index = rownames
col.to_latex(outputpath + '/table/SummaryTablePy.tex',column_format='lccc',escape=False)

## b. Does it appear that the randomization worked? If so, what can we say about the simple difference-in-means estimate?
## See final document

#-----------------------------------------------------------------------
## Question 1.2 
#-----------------------------------------------------------------------

# Plot kernel density plots of the electricity use for treated group and control group on the same graph using Python.


fig = sns.kdeplot(treat['electricity'], color="r")
fig = sns.kdeplot(notreat['electricity'], color="g")
plt.xlabel('Monthly electricity usage by HHs (kWh)')
plt.legend(labels = ['Treatment','Control'],loc = 'best')
plt.show
plt.savefig(outputpath + '/figure/densityplotpy.pdf',format='pdf')


#-----------------------------------------------------------------------
## Question 3
#-----------------------------------------------------------------------
# a. Estimate β manually 

# I should calculate beta by hand. Use the Numpy package in Python to create an array X that is the n×p+1 matrix of the predictor variables in table 1 
# and a column of ones and an array Y that is the n×1 vector of the dependent variable. Use matrix operations to calculate ˆ β. Recall that ˆ β = (X′X)−1X′Y
# is the closed-form solution to the least-squares minimization problem.


# Define the values of n and p
n = 1000  # Number of observations
p = 3  # Number of predictor variables

# Add a column of 1s to main dataset
data_with1 = data.assign(constant=1)

X_with1 = data_with1.drop('electricity',axis=1)


# Convert DataFrame to NumPy array
X = X_with1.to_numpy()

# Transpose X, square X and inverse the square of X
tr_X = np.transpose(X) 
XX = np.dot(tr_X, X) 
XX_inverse = np.linalg.inv(XX)


# Select dependent variable from the matrix
outcome = data['electricity']
Y = outcome.to_numpy()

XY = np.dot(tr_X,Y)
β = np.dot(XX_inverse, XY)

print (β )


