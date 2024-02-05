# HW 3 code -- Ana Mazmishvili

from IPython import get_ipython
get_ipython().magic('reset -sf')

# Import packages 
import os
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

datapath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 2\data'
outputpath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 2\output'

# If working on campus: 

#datapath = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 3\data'
#outputpath = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 3\output'


np.random.seed(4)

# Load dataset in the system 

data=pd.read_csv(datapath +'/kwh.csv')


### Question 1.e ###
# -------------------------------------------------------------------------- #


## Transform data in natural log form
data['ln_electricity'] = np.log(data['electricity'])
data['ln_sqft'] = np.log(data['sqft'])
data['ln_temp'] = np.log(data['temp'])

## Estimate parameter from the log-log model
ols = sm.OLS(data['ln_electricity'],sm.add_constant(data[['retrofit','ln_sqft','ln_temp']])).fit()
coef_ols = ols.params.to_numpy() # save estimated parameters
params, = np.shape(coef_ols) # save number of estimated parameters
nobs1 = int(ols.nobs)
coef_ols[1] = np.exp(coef_ols[1]) # convert retrofit coefficient (ln delta) back to delta

## Calculate average marginal effects estimates(AME) of zi and di 
# Calculate AME for di
ame_di = data.apply(lambda x: (coef_ols[1]-1)*x['electricity']/(coef_ols[1]**x['retrofit']),axis=1) 

# Calculate AME for zi: sqft & temp
ame_sqft = data.apply(lambda x: coef_ols[2]*x['electricity']/x['sqft'],axis=1) 
ame_temp = data.apply(lambda x: coef_ols[3]*x['electricity']/x['temp'],axis=1) 

#save estimated AME
ame = [ame_di.mean(),ame_sqft.mean(),ame_temp.mean()] 

# Bootstrap by hand and get confidence intervals.
## Set values and initialize arrays to output to
breps = 1000 # number of bootstrap replications
olscoefblist = np.zeros((breps,params))  # for parameters
ameblist = np.zeros((breps,params-1))    # for AME

## Get an index of the data we will sample by sampling with replacement
bidx = np.random.choice(nobs1,(nobs1,breps)) # Generates random numbers on the interval [0,nobs1] and produces a nobs1 x breps sized array

## Sample with replacement to get the size of the sample on each iteration
for r in range(breps):
    ### Sample the data
    datab = data.iloc[bidx[:,r]]
    
    ### Perform the estimation
    olsb = sm.OLS(datab['ln_electricity'],sm.add_constant(datab[['retrofit','ln_sqft','ln_temp']])).fit()
    coef_olsb = olsb.params.to_numpy() # save estimated parameters
    coef_olsb[1]=np.exp(coef_olsb[1]) # convert retrofit coefficient (ln delta) to delta
    
    ### Compute the marginal effect
    me_di = datab.apply(lambda x: (coef_olsb[1]-1)*x['electricity']/(coef_olsb[1]**x['retrofit']),axis=1) # calculate AME for di
    me_sqft = datab.apply(lambda x: coef_olsb[2]*x['electricity']/x['sqft'],axis=1) # calculate AME for sqft
    me_temp = datab.apply(lambda x: coef_olsb[3]*x['electricity']/x['temp'],axis=1) # calculate AME for temp
    me = [ me_di.mean(), me_sqft.mean(),me_temp.mean()]
    ameblist[r,:] = me
    
    ### Output the parameter estimates result
    olscoefblist[r,:] = coef_olsb
    
## Extract 2.5th and 97.5th percentile for each parameter
lb_ols = np.percentile(olscoefblist,2.5,axis = 0,interpolation = 'lower')
ub_ols = np.percentile(olscoefblist,97.5,axis = 0,interpolation = 'higher')

## Extract 2.5th and 97.5th percentile for AMEs
lb_ame = np.percentile(ameblist,2.5,axis = 0,interpolation = 'lower')
ub_ame = np.percentile(ameblist,97.5,axis = 0,interpolation = 'higher')

# Regression output table with CIs
## Format parameter estimates and confidence intervals
coefP_ols = np.round(coef_ols,3)

lbP_ols = pd.Series(np.round(lb_ols,3)) # Round to two decimal places and get a Pandas Series version
ubP_ols = pd.Series(np.round(ub_ols,3))
ci_ols = '[' + lbP_ols.map(str) + ', ' + ubP_ols.map(str) + ']'

## Format AME estimates and confidence intervals
ameP = np.round(ame,3)

lbP_ame = pd.Series(np.round(lb_ame,3)) # Round to two decimal places and get a Pandas Series version
ubP_ame = pd.Series(np.round(ub_ame,3))
ci_ame = '[' + lbP_ame.map(str) + ', ' + ubP_ame.map(str) + ']'

## Get parameter estimates output in order
output_ols = pd.DataFrame(np.column_stack([coefP_ols,ci_ols]))
col1=pd.concat([output_ols.stack(),pd.Series(nobs1)])

## Get AME estimates output in order
output_ame = pd.DataFrame(np.column_stack([ameP,ci_ame]))
output_ame.loc[len(output_ame.index)]=[' ',' '] # shift the dataframe down one row
output_ame=output_ame.shift()
output_ame.loc[0]=[' ',' ']
col2=pd.concat([output_ame.stack(),pd.Series(nobs1)])

## Row and column names
rownames = pd.concat([pd.Series(['Constant','=1 if home received retrofit','Square feet of home','Outdoor average temperature (\\textdegree F)','Observations']),pd.Series([' ',' ',' ',' '])],axis = 1).stack() # Note this stacks an empty list to make room for CIs

## Append CIs, # Observations, row and column names
#order = [1,2,3,0]
col = pd.DataFrame({'Parameter estimates': col1, 'AME estimates': col2})
#col.reindex(order)
col.index = rownames
col.to_latex(outputpath + '/table/hw31e.tex',column_format='lccc',escape=False)


### Question 1.f ###
# -------------------------------------------------------------------------- #

# Plot AME with error bars for sqft and temp 
lowbar = np.array(ame[1:3] - lb_ame[1:3])
highbar = np.array(ub_ame[1:3] - ame[1:3])
plt.errorbar(y = ame[1:3], x = np.arange(params-2), yerr = [lowbar,highbar], fmt = 'o', capsize = 6)
plt.ylabel('AME estimates')
plt.xticks(np.arange(params-2),['Square feet of home', 'Outdoor average temperature ($\degree$F)'])
plt.xlim((-0.5,1.5)) # Scales the figure more nicely
plt.axhline(linewidth=2, color='y')
plt.savefig(outputpath + '/figure/hw3ame.pdf',format='pdf')