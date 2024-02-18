# HW 4 code -- Ana Mazmishvili
## Correction of the code after reviewing Dylan's answers


# Clear all - following code clears the working envirioment
from IPython import get_ipython
get_ipython().magic('reset -sf')

#pip install tabulate
#from tabulate import tabulate

# Import packages 
import os
# import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
# import seaborn as sns
import statsmodels.api as sm
# from scipy import stats
# import csv
# from scipy.optimize import minimize
# from sklearn.linear_model import LinearRegression as lr
from stargazer.stargazer import Stargazer as stargazer
from stargazer.stargazer import LineLocation


# Set working directories and seed

#If working from home:

datapath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 4\data'
outputpath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 4\output'

# If working on campus: 

#datapath = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 4\data'
#outputpath = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 4\output'

# Changes the current working directory to the one specified by the variable datapath.
# 'os' stands for the operating system
# 'chdir' stands for "change directory" 

os.chdir(datapath)

# Questions for Dylan - why do you chose such a big number for seed?
random.seed(20121159)
np.random.seed(411128)

# Load dataset in the system 
data=pd.read_csv('fishbycatch.csv')


# print(data.info())
# Convert the panel data from wide form to long form
df = pd.wide_to_long(data, stubnames=["shrimp", "salmon", "bycatch"], i='firm', j='month')

# this code returned back the firm and month as variables while after transforming dataset they were used as indeces. 
df = df.reset_index(level=['firm', 'month'])


## Define Treatment group and treated variables
df['treatgroup'] = df['treated'] # Static variable for which firms are in the treatment group. Even before treatment period terated group is 1, control is 0 for the whole period. 
df['treated2'] = np.where((df['treated'] == 1) & (df['month']>12) & (df['month']<25), 1, 0)
df['treated3'] = np.where((df['month']>24), 1, 0)

## I do not understand why do we need to add these two variables, treated3 is all 0s. 
## we rewrote the values in treated column. The new values are sum of two columns. 
df['treated'] = df['treated2'] + df['treated3'] # Dynamic variable for when firms receive treatment

df = df.drop(columns = ['treated2', 'treated3']) # drop extra variables


# Problem 1 ------------------------------------------------------------------
trends = df.groupby(['treatgroup','month']).mean()

## Here we do the same, but also resetting the index. Keep for future use 
#grouped_data =df.groupby(by = ['treatgroup', 'month']).mean().reset_index()

## created the dataframe for control group.
# 'loc' indexer selects rows and columns by labels. 
# It's selecting all columns (:) for the row with the label (index) 0.
controltrends = trends.loc[0, :]
controltrends = controltrends.reset_index()

## created the dataframe for treated group.
treattrends = trends.loc[1, :]
treattrends = treattrends.reset_index()

## Build the plot
plt.plot(controltrends['month'], controltrends['bycatch'], marker = 'o')
plt.plot(treattrends['month'], treattrends['bycatch'], marker = 'o')
plt.axvline(x=12.5, color = 'red', linestyle = 'dashed') # Vertical line to indicate treatment year
plt.xlabel('Month')
plt.ylabel('Mean bycatch per firm (lbs)')
plt.legend(['Control', 'Treatment','Treatment date'])
plt.title('Line Plot for Treated and Control Groups Over Months')
os.chdir(outputpath) # Change directory
plt.savefig('trend1.pdf',format='pdf')
plt.show()



### My initial version

# 1.  Group by 'group' and 'month' and calculate the mean for each group in each month
#grouped_data =df.groupby(by = ['treated', 'month']).mean().reset_index()


# Plotting
#plt.figure(figsize=(7, 4))
#for group in df['treated'].unique():
#    group_data = grouped_data[grouped_data['treated'] == group]
#   plt.plot(group_data['month'], group_data['bycatch'], label=group)

#plt.title('Line Plot for Treated and Control Groups Over Months')
#plt.xlabel('Month')
#plt.xticks(range(1,25))
#plt.ylabel('Average bycatch')
#plt.axvline(x=13, color='red', linestyle='--', label='Treatment Month')
## Rename legends
#new_legend_labels = ['Control Group', 'Treated Group']
#plt.legend(labels=new_legend_labels)
#plt.savefig(outputpath + '/figure/trend1.pdf',format='pdf')
#plt.show()

# Problem 2 ------------------------------------------------------------------

DID = (trends.loc[(1,13),'bycatch'] - trends.loc[(1,12),'bycatch']) - (trends.loc[(0,13),'bycatch'] - trends.loc[(0,12),'bycatch'])
print (DID)

# This is a result -9591.349503863777


# Problem 3a ------------------------------------------------------------------
twoperiod = df[(df['month'] == 12) | (df['month'] == 13)]
pre = pd.get_dummies(twoperiod['month'],prefix = 'pre', drop_first = True)
## here we have only two periods. 'drop_first=True' drops the first level of each categorical variable. iN this case month 12. 
## prefix='pre' adds a prefix to the column names of the resulting dummy variables. 
twoperiod = pd.concat([twoperiod,pre],axis = 1)

yvar3a = twoperiod['bycatch']
xvar3a = twoperiod[['treatgroup','treated','pre_13']]


DID3a = sm.OLS(yvar3a,sm.add_constant(xvar3a, prepend = False).astype(float)).fit() 
# astype(float) ensures that the data types are consistent (converted to float).
# When prepend is set to False, it means that the constant term should be added as the last column of the array. 
# If prepend were set to True (which is the default behavior if not specified), the constant term would be added as the first column.
DID3arobust = DID3a.get_robustcov_results(cov_type = 'cluster', groups = twoperiod['firm']) # Cluster-robust confidence intervals


# Problem 3b ------------------------------------------------------------------
yvar3b = df['bycatch']
tvars3b = pd.get_dummies(df['month'],prefix = 'time',drop_first = True) # creates dummies from time variables
xvar3b = pd.concat([df[['treatgroup','treated']],tvars3b],axis = 1)

DID3b = sm.OLS(yvar3b,sm.add_constant(xvar3b,prepend = False).astype(float)).fit()
DID3brobust = DID3b.get_robustcov_results(cov_type = 'cluster', groups = df['firm'])


# Problem 3c ------------------------------------------------------------------
yvar3c = df['bycatch']
tvars3c = pd.get_dummies(df['month'],prefix = 'time',drop_first = True) # creates dummies from time variables
xvar3c = pd.concat([df[['treatgroup','treated','shrimp','salmon','firmsize']],tvars3c],axis = 1)

DID3c = sm.OLS(yvar3c,sm.add_constant(xvar3c,prepend = False).astype(float)).fit()
DID3crobust = DID3c.get_robustcov_results(cov_type = 'cluster', groups = df['firm'])



# Output table with Stargazer package  ----------------------------------------
output = stargazer([DID3a,DID3b,DID3c])

output.covariate_order(['treated','treatgroup','pre_13','shrimp', 'salmon'])
output.rename_covariates({'treated':'Treated','treatgroup':'Treatment group','pre_13':'Pre-period','shrimp':'Shrimp','salmon':'Salmon'})
output.add_line('Month indicators',['Y','Y','Y'], LineLocation.FOOTER_TOP)
output.significant_digits(2)
output.show_degrees_of_freedom(False)

file_name = "test.tex" #Include directory path if needed
tex_file = open('report.tex', "w" ) #This will overwrite an existing file
tex_file.write( output.render_latex() )
tex_file.close()

# Export long data for use in Stata

# df.to_csv('longdata_stata.csv', index = None, header=True)






# ----------------------------------------------------------------------------

# 2. Manually calculating DiD estimator

## No need to use this code because we reset the index initially
#df['months'] = (df.index.get_level_values('month'))
#df['firms'] = (df.index.get_level_values('firm'))

# Filter data for December 2017 and January 2018
dec_2017 = df[(df['month'] == 12)]
jan_2018 = df[(df['month'] == 13)]

## Calculate means for the treatment group
treated_dec_mean = dec_2017[df['treatgroup'] == 1]['bycatch'].mean()
#treated_dec_mean = treated_dec_mean.map('{:.2f}'.format)
treated_jan_mean = jan_2018[df['treatgroup'] == 1]['bycatch'].mean()


## Calculate means for the control group
control_dec_mean = dec_2017[df['treatgroup'] == 0]['bycatch'].mean()
control_jan_mean = jan_2018[df['treatgroup'] == 0]['bycatch'].mean()


## Calculate the DiD estimate
T = 1  # The post-treatment period is one month
DiD_estimate = ((treated_jan_mean - treated_dec_mean) / T) - ((control_jan_mean - control_dec_mean) / T)

## Creating table
did_results = pd.DataFrame({'Sample analog of the population DID': [treated_dec_mean, 
                                      treated_jan_mean, 
                                     control_dec_mean, 
                                      control_jan_mean, 
                                      DiD_estimate]},
                        index=['$\E[Y_{igt}|g(i)=treat, t=Dec2017]=$', 
                               '$\E[Y_{igt}|g(i)=treat, t=Jan2018]=$', 
                               '$\E[Y_{igt}|g(i)=control, t=Dec2017]=$', 
                               '$\E[Y_{igt}|g(i)=control, t=Jan2018]=$', 
                               '\midrule DID ='])
did_results.to_latex(outputpath + '/table/DIDResults.tex', column_format='rl', float_format="%.3f", escape=False)


# 3. Estimate the treatment effect using the regression specifications

## Create the subsample 
df2=df.loc[df['month'].isin([12,13])]

## Dylan's code
#twoperiod = df[(df['month'] == 12) | (df['month'] == 13)]

## Reset the index of the subsample
df2 = df2.reset_index(drop=True)

## Create variables for the regression
df2['Dec2017']=np.where(df2['month']==12,1,0)


## 3.a. Estimate the treatment effect of the program on bycatch using two-period DID
ols = sm.add_constant(df2[['treatgroup','treated', 'Dec2017']])
model = sm.OLS(df2['bycatch'], ols).fit()

par_keep = ['treated', 'treatgroup']

params = model.params[par_keep].to_numpy()
params = pd.Series(params).map('{:.2f}'.format)
se = model.bse[par_keep]
nobs = model.nobs







## Display the regression results
#print(model.summary())
#print(model.params)


## Question 3.b. Estimate the treatment effect of the program on bycatch using the full monthly sample

## Create variables for the regression
df['treatment']=np.where((df['months']>=13) & (df['treated']==1),1,0)

# Create dummy variables for each month
m_dummies = pd.get_dummies(df['months'], prefix='m')

# Concatenate the dummy variables with the original DataFrame
df = pd.concat([df, m_dummies], axis=1)

df = df.replace({True: 1, False: 0})

# Print the DataFrame with firm ID dummy variables
print(df)


## Regression results using the full monthly sample
ols1 = sm.add_constant(df[['treated','treatment','m_1', 'm_2','m_3','m_4','m_5','m_6','m_7','m_8','m_9','m_10','m_11','m_12',\
                           'm_13','m_14','m_15','m_16','m_17','m_18','m_19','m_20','m_21','m_22','m_23','m_24' ]])

model1 = sm.OLS(df['bycatch'], ols1).fit(cov_type='cluster', cov_kwds={'groups': df['firms']})


par_keep1 = ['treated','treatment']

params1 = model1.params[par_keep].to_numpy()
params1 = pd.Series(params1).map('{:.2f}'.format)
se1 = model1.bse[par_keep]
nobs1 = model1.nobs

## Display the regression results
#print(model1.summary())
#print(model1.params)



## 3.c. Estimate the treatment effect of the program on bycatch using the full monthly sample and control for firm size and other covariates
ols2 = sm.add_constant(df[['treated','treatment','firmsize','salmon','shrimp','m_1', 'm_2','m_3','m_4','m_5','m_6','m_7','m_8','m_9','m_10','m_11','m_12',\
                           'm_13','m_14','m_15','m_16','m_17','m_18','m_19','m_20','m_21','m_22','m_23','m_24' ]])

model2 = sm.OLS(df['bycatch'], ols2).fit(cov_type='cluster', cov_kwds={'groups': df['firms']})

par_keep2 = ['treated','treatment','firmsize','salmon','shrimp']

params2 = model2.params[par_keep].to_numpy()
params2 = pd.Series(params2).map('{:.2f}'.format)
se2 = model2.bse[par_keep]
nobs2 = model2.nobs

## Create the table

output = pd.DataFrame(np.column_stack([params]))


# Set the row and column names
rownames = pd.Series(['Treated','Treatment'])

cl1 = params
cl2 = params1
cl3 = params2

cl = pd.DataFrame({'Two Period Sample': cl1, 'All Months': cl2, 'With Covariates': cl3})
cl.index = rownames
cl.to_latex(outputpath + '/table/report.tex')


## Display the regression results
#print(model2.summary())
#print(model2.params)


### Different ways that i tried but did not give the desiried outcome

## I tried to append results these way but row names were missing and also, there were all variables. 
#results=[]
#results.append(model)
#results.append(model1)
#results.append(model2)


# I tried Stargazer's package but overleaf does not read it properly

#os.chdir(outputpath)

#stargazer = Stargazer([model, model1, model2])
#with open((outputpath + '/table/sumreport.tex'), "w") as f:
#    f.write(stargazer.render_latex())






