# HW 4 code -- Ana Mazmishvili

from IPython import get_ipython
get_ipython().magic('reset -sf')

#pip install tabulate
from tabulate import tabulate

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
from stargazer.stargazer import Stargazer


# Set working directories and seed

#If working from home:

#datapath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 4\data'
#outputpath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 4\output'

# If working on campus: 

datapath = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 4\data'
outputpath = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 4\output'


np.random.seed(4)

# Load dataset in the system 

data=pd.read_csv(datapath +'/fishbycatch.csv')


print(data.info())
# Convert the panel data from wide form to long form
df = pd.wide_to_long(data, stubnames=["shrimp", "salmon", "bycatch"], i='firm', j='month')



# 1.  Group by 'group' and 'month' and calculate the mean for each group in each month
grouped_data =df.groupby(by = ['treated', 'month']).mean().reset_index()


# Plotting
plt.figure(figsize=(7, 4))
for group in df['treated'].unique():
    group_data = grouped_data[grouped_data['treated'] == group]
    plt.plot(group_data['month'], group_data['bycatch'], label=group)

plt.title('Line Plot for Treated and Control Groups Over Months')
plt.xlabel('Month')
plt.xticks(range(1,25))
plt.ylabel('Average bycatch')
plt.axvline(x=13, color='red', linestyle='--', label='Treatment Month')
## Rename legends
new_legend_labels = ['Control Group', 'Treated Group']
plt.legend(labels=new_legend_labels)
plt.savefig(outputpath + '/figure/trend1.pdf',format='pdf')
plt.show()

# 2. Manually calculating DiD estimator


df['months'] = (df.index.get_level_values('month'))
df['firms'] = (df.index.get_level_values('firm'))

# Filter data for December 2017 and January 2018
dec_2017 = df[(df['months'] == 12)]
jan_2018 = df[(df['months'] == 13)]

## Calculate means for the treatment group
treated_dec_mean = dec_2017[df['treated'] == 1]['bycatch'].mean()
#treated_dec_mean = treated_dec_mean.map('{:.2f}'.format)
treated_jan_mean = jan_2018[df['treated'] == 1]['bycatch'].mean()


## Calculate means for the control group
control_dec_mean = dec_2017[df['treated'] == 0]['bycatch'].mean()
control_jan_mean = jan_2018[df['treated'] == 0]['bycatch'].mean()


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
df2=df.loc[df['months'].isin([12,13])]

## Reset the index of the subsample
df2_in = df2.reset_index(drop=True)

## Create variables for the regression
df2_in['Dec2017']=np.where(df2_in['months']==12,1,0)
df2_in['treated_post']=np.where((df2_in['months']==13) & (df2_in['treated']==1),1,0)
df2_in.head()


## 3.a. Estimate the treatment effect of the program on bycatch using two-period DID
ols = sm.add_constant(df2_in[['treated', 'treated_post', 'Dec2017']])
model = sm.OLS(df2_in['bycatch'], ols).fit()


results=[]
results.append(model)



params = model.params.to_numpy()
se = model.bse
# par_k = ['treated', 'treated_post', 'Dec2017']
par_k = ['treated']
params_keep = model.params[par_k]
se_keep = model.bse[par_k]
nobs = model.nobs

#sum_results = []
#sum_results.append(params_keep)

## Display the regression results
print(model.summary())
print(model.params)


## Question 3.b. Estimate the treatment effect of the program on bycatch using the full monthly sample

## Create variables for the regression
df['treated_post']=np.where((df['months']>=13) & (df['treated']==1),1,0)

# Create dummy variables for each month
m_dummies = pd.get_dummies(df['months'], prefix='m')

# Concatenate the dummy variables with the original DataFrame
df = pd.concat([df, m_dummies], axis=1)

df = df.replace({True: 1, False: 0})

# Print the DataFrame with firm ID dummy variables
print(df)


## Regression results using the full monthly sample
ols1 = sm.add_constant(df[['treated','treated_post','m_1', 'm_2','m_3','m_4','m_5','m_6','m_7','m_8','m_9','m_10','m_11','m_12',\
                           'm_13','m_14','m_15','m_16','m_17','m_18','m_19','m_20','m_21','m_22','m_23','m_24' ]])

model1 = sm.OLS(df['bycatch'], ols1).fit(cov_type='cluster', cov_kwds={'groups': df['firms']})



results.append(model1)



params1 = model1.params.to_numpy()
par_keep = ['treated']
#par_keep = ['treated','treated_post']
params1_keep = model1.params[par_keep]
se1 = model1.bse
se1_keep = model1.bse[par_keep]
nobs1 = model1.nobs

## Display the regression results
print(model1.summary())
print(model1.params)



## 3.c. Estimate the treatment effect of the program on bycatch using the full monthly sample and control for firm size and other covariates
ols2 = sm.add_constant(df[['treated','treated_post','firmsize','salmon','shrimp','m_1', 'm_2','m_3','m_4','m_5','m_6','m_7','m_8','m_9','m_10','m_11','m_12',\
                           'm_13','m_14','m_15','m_16','m_17','m_18','m_19','m_20','m_21','m_22','m_23','m_24' ]])

model2 = sm.OLS(df['bycatch'], ols2).fit(cov_type='cluster', cov_kwds={'groups': df['firms']})



results.append(model2)



params2 = model2.params.to_numpy()
se2 = model2.bse
par2_keep = ['treated']
#par2_keep = ['treated','treated_post','firmsize','salmon','shrimp']
params2_keep = model2.params[par2_keep]
se2_keep = model2.bse[par2_keep]
nobs2 = model2.nobs


## Display the regression results
print(model2.summary())
print(model2.params)



#os.chdir(outputpath)

stargazer = Stargazer([model, model1, model2])
with open((outputpath + '/table/sumreport.tex'), "w") as f:
    f.write(stargazer.render_latex())









