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
ols = sm.add_constant(df2_in[['Dec2017', 'treated', 'treated_post']])
model = sm.OLS(df2_in['bycatch'], ols).fit()
params = model.params.to_numpy()
nobs = model.nobs

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


# Get the list of variable names with the same base
base_name = 'm_'
var_names = [f'{"m_"}{i}' for i in range(1, 25)]

other_variables = [' treated ', ' treated_post']

# Combine variable names and other variables
all_variables = other_variables + var_names

# Create the formula for the regression
formula = 'bycatch ~' + ' + '.join(all_variables)


# Fit the OLS regression model
model1 = sm.OLS.from_formula(formula, data=df)
results1 = model1.fit()
params1 = model1.params1.to_numpy()
nobs1 = model1.nobs

## Display the regression results
print(model1.summary())
print(model1.params)


## Regression results using the full monthly sample
ols1 = sm.add_constant(df[['treated', 'treated_post', 'm_1']])

model = sm.OLS(df2_in['bycatch'], ols).fit()
params = model.params.to_numpy()
nobs = model.nobs

## Display the regression results
print(model.summary())
print(model.params)


# Get the OLS estimates
ols_b=feols(fml="bycatch ~ treated + treatit | Month", data=data_long, vcov={'CRV1': 'firm'})
beta_b=ols_b.coef()
se_b=ols_b.se()
ci_b=ols_b.confint()
ols_b.summary()

# Question 3 c
# Create the indicator variable
data_long['treatit']=np.where((data_long['year']==2018) & (data_long['treated']==1),1,0)
# Get the OLS estimates
ols_c=feols(fml="bycatch ~ treated + treatit + firmsize + salmon + shrimp | Month", data=data_long, vcov={'CRV1': 'firm'})
beta_c=ols_c.coef()
se_c=ols_c.se()
ci_c=ols_c.confint()
ols_c.summary()

# Export to latex
report_table=pd.DataFrame({'(a)': ["{:0.2f}".format(ols_a.coef()['treatit']), "({:0.2f})".format(ols_a.se()['treatit']), "\checkmark", "\checkmark", "$\\times$","Dec 2017 - Jan 2018"],
                           '(b)': ["{:0.2f}".format(ols_b.coef()['treatit']), "({:0.2f})".format(ols_b.se()['treatit']), "\checkmark", "\checkmark", "$\\times$","Jan 2017 - Dec 2018"],
                           '(c)': ["{:0.2f}".format(ols_c.coef()['treatit']), "({:0.2f})".format(ols_c.se()['treatit']), "\checkmark", "\checkmark", "\checkmark","Jan 2017 - Dec 2018"]},
                        index=['DID estimates', 
                               ' ',
                               '\midrule Group FE',
                               'Month Indicator' ,
                               'Controls', 
                               'Sample'])
report_table.to_latex(outputpath + '/table/reporttable1.tex', column_format='rccc', float_format="%.2f", escape=False)




