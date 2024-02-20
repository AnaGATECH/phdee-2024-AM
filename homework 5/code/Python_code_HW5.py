# HW 5 code -- Ana Mazmishvili

# Clear all
from IPython import get_ipython
get_ipython().magic('reset -sf')

# Import packages
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import statsmodels.api as sm

# For stargazer I opened Anaconda Prompt using start and wrote there pip install stargazer. 
# After that this code was executed. 
from stargazer.stargazer import Stargazer as stargazer
from stargazer.stargazer import LineLocation
from linearmodels import IVGMM




# Set working directories and seed

#If working from home:

datapath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 5\data'
outputpath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 5\output'
figure = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 5\output\figure'
table = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 5\output\table'

# If working on campus: 

#datapath = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 5\data'
#outputpath = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 5\output'
#figure = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 5\output\figure'
#table = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 5\output\table'

os.chdir(datapath)

random.seed(20121159)
np.random.seed(4)

# Load dataset in the system 

data=pd.read_csv('instrumentalvehicles.csv')

# Problem 1 ------------------------------------------------------------------

yvar1 = data['price']
xvar1 = data[['mpg','car']]

os.chdir(table)
ols = sm.OLS(yvar1,sm.add_constant(xvar1, prepend = False).astype(float)).fit() 


latex_output = ols.summary().as_latex()

with open('ols_summary.tex', 'w') as f:
    f.write(latex_output)
    
# Problem 3.a ------------------------------------------------------------------

## The First Stage
yvar3a = data['mpg']
xvar3a_1 = sm.add_constant(data[['weight','car']])


ols3a_1 = sm.OLS(yvar3a,xvar3a_1.astype(float)).fit()
fit_mpg3a = ols3a_1.fittedvalues.to_frame()

## This gives me F value for the whole regression.
fstat_a = ols3a_1.fvalue
fstat_a = round(fstat_a, 2)
print (fstat_a)
fpval_a = ols3a_1.f_pvalue
fpval_a = round(fpval_a,4)
print (fpval_a)



## The Second Stage
xvar3a_2 = pd.concat([data[['car']], fit_mpg3a], axis=1)
xvar3a_2.rename(columns={0: 'fit_mpg'}, inplace=True)

ols3a_2 = sm.OLS(yvar1,sm.add_constant(xvar3a_2, prepend = False).astype(float)).fit()


##I did not use these series because Stagazer did not needed to produce the results table
#ols3a_2_ci = ols3a_2.conf_int()
#ols3a_2_coef = ols3a_2.params
#ols3a = pd.DataFrame({'Parameters': ols3a_2_coef, 'Lower CI': ols3a_2_ci[0], 'Upper CI': ols3a_2_ci[1]})



# Problem 3.b-------------------------------------------------
## Create variable that equals to square of weight

data['weight2'] = np.square(data['weight'])

## The First Stage
yvar3b = data['mpg']
    
xvar3b_1 = sm.add_constant(data[['weight2','car']])

ols3b_1 = sm.OLS(yvar3a,xvar3b_1.astype(float)).fit()
fit_mpg3b = ols3b_1.fittedvalues.to_frame()

## This gives me F value for the whole regression.
fstat_b = ols3b_1.fvalue
fstat_b = round(fstat_b, 2)
print (fstat_b)
fpval_b = ols3b_1.f_pvalue
fpval_b = round(fpval_b,4)
print (fpval_b)


## The Second Stage
xvar3b_2 = pd.concat([data[['car']],fit_mpg3b], axis=1)
xvar3b_2.rename(columns={0: 'fit_mpg'}, inplace=True)

ols3b_2 = sm.OLS(yvar1,sm.add_constant(xvar3b_2, prepend = False).astype(float)).fit()


# Problem 3.c ------------------------------------------------------------------

## The First Stage
yvar3c = data['mpg']
xvar3c_1 = sm.add_constant(data[['height','car']])


ols3c_1 = sm.OLS(yvar3c,xvar3c_1.astype(float)).fit()
fit_mpg3c = ols3c_1.fittedvalues.to_frame()

## This gives me F value for the whole regression.
fstat_c = ols3c_1.fvalue
fstat_c = round(fstat_c, 2)
print (fstat_c)
fpval_c = ols3c_1.f_pvalue
fpval_c = round(fpval_c,4)
print (fpval_c)

## The Second Stage
xvar3c_2 = pd.concat([data[['car']],fit_mpg3c], axis=1)
xvar3c_2.rename(columns={0: 'fit_mpg'}, inplace=True)

ols3c_2 = sm.OLS(yvar1,sm.add_constant(xvar3c_2, prepend = False).astype(float)).fit()


# Output table with Stargazer package  ----------------------------------------

output = stargazer([ols3a_2, ols3b_2, ols3c_2])

print(output)



output.covariate_order(['fit_mpg','car'])
output.rename_covariates({'fit_mpg':'Miles per gallon','car':'Car'})
output.add_line('F-statistics from the 1st Stage',[fstat_a,fstat_b,fstat_c], LineLocation.FOOTER_TOP)
output.add_line('F-stat p-value',[fpval_a,fpval_b,fpval_c], LineLocation.FOOTER_TOP)
output.significant_digits(2)
output.show_degrees_of_freedom(False)

os.chdir(table) # Change directory

tex_file = open('3RegResults.tex', "w" ) #This will overwrite an existing file
tex_file.write( output.render_latex() )
tex_file.close()




# Problem 4 ------------------------------------------------------------------

endog = data['mpg']
exog = sm.add_constant(data['car'])
instrument = data['weight']

ivgmm=IVGMM(yvar1, exog,  endog, instrument).fit()

# Output table with Stargazer package  ----------------------------------------

coef_gmm = ivgmm.params
se_gmm = ivgmm.std_errors

GMM_table=pd.DataFrame(
    {'IVGMM': ["{:0.2f}".format(coef_gmm['mpg']), "({:0.2f})".format(se_gmm['mpg']), 
             "{:0.2f}".format(coef_gmm['car']), "({:0.2f})".format(se_gmm['car'])]},
     index=['Miles per gallon', ' ',
            '=1 if the vehicle is sedan', ' '])
os.chdir(table)
GMM_table.to_latex('IVGMM.tex', column_format='lcc', float_format="%.2f", escape=False)





