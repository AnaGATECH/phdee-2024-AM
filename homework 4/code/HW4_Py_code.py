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
                        index=['$\E [Y_{igt}|g(i) = treat, t=Dec2017] = $', 
                               '$\E [Y_{igt}|g(i) = treat, t=Jan2018] = $', 
                               '$\E [Y_{igt}|g(i) = control, t=Dec2017] = $', 
                               '$\E [Y_{igt}|g(i) = control, t=Jan2018] = $', 
                               '$\midrule DID$ = '])
did_results.to_latex(outputpath + '/table/DIDResults.tex', column_format='rl', float_format="%.2f", escape=False)



print("DiD Estimate:", DiD_estimate)

## Create indicator variables for post-treatment period
df['post_treatment'] = (df.index.get_level_values('month') >= 13).astype(int)
df['treated_post'] = (df['post_treatment']*df['treated'])



## Estimate the DiD effect using linear regression
ols = sm.add_constant(df[['treated', 'post_treatment', 'treated_post']])
model = sm.OLS(df['bycatch'], ols).fit()
params = model.params.to_numpy()
nobs = model.nobs

## Display the regression results
print(model.summary())

print(model.params)





#Question 3
#Shaping the data matrix
data_q1a=data_long.loc[data_long['Month'].isin([12,13])]
data_q1a['t2017']=np.where(data_q1a['year']==2017,1,0)
data_q1a['treatit']=np.where((data_q1a['year']==2018) & (data_q1a['treated']==1),1,0)
data_q1a.head()


# Estimate the DID model using pyfixest the python equivalent of R fixest package
from pyfixest.estimation import feols, fepois
from pyfixest.utils import get_data
from pyfixest.summarize import etable

#Qustion 3a
ols_a=feols(fml="bycatch ~ treated + treatit | t2017", data=data_q1a, vcov={'CRV1': 'firm'})
beta_a=ols_a.coef()
se_a=ols_a.se()
ci_a=ols_a.confint()
ols_a.summary()

# Question 3 b
# Create the indicator variable
data_long['treatit']=np.where((data_long['year']==2018) & (data_long['treated']==1),1,0)
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

## Save the original standard output
#original_stdout = sys.stdout

# Redirect standard output to a file
#with open(outputpath + '/table/DIDoutput1.tex', 'w') as f:
#    sys.stdout = f
#    print(model.params)

## Restore the original standard output
#sys.stdout = original_stdout




