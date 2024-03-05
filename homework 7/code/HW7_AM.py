# HW 7 code -- Ana Mazmishvili

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
from sklearn.linear_model import LinearRegression
from numpy.polynomial.polynomial import Polynomial



# Set working directories and seed

#If working from home:

datapath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 7\data'
outputpath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 7\output'
figure = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 7\output\figure'
table = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 7\output\table'

# If working on campus: 

#datapath = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 7\data'
#outputpath = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 7\output'
#figure = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 7\output\figure'
#table = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 7\output\table'

os.chdir(datapath)

random.seed(20121159)
np.random.seed(4)

# Load dataset in the system 

data=pd.read_csv('instrumentalvehicles.csv')

# Problem 2 ------------------------------------------------------------------
## Scatter plot with mpg on the y-axis and length − cutoff on the x-axis 
## with a line at the RD cutoff.

## Create variable for cutoff  
## 'cutoff' = 1 if length>225 and 0 otherwise

data['cutoff'] = np.where(data['length'] > 225, 1, 0)

print(data['mpg'].describe())
print(data['length'].describe())


## Scatter plot 
os.chdir(figure) # Change directory

plt.figure()
plt.scatter(data['length'], data['mpg'], c=data['cutoff'], cmap='PuOr', s=5, alpha=0.7)
plt.axvline(x=225, color='red', linestyle='--')
plt.xlabel('Length (inches)')
plt.ylabel('Fuel efficiency (miles per gallon)')
plt.xlim(40, 340)
plt.ylim(5, 55)
plt.savefig('scatterplot1.pdf')


# Problem 3 ------------------------------------------------------------------
## Fit first order polynomial on both sides of the cutoff in RD design

# Interact length with cutoff
formula1 = 'mpg ~ cutoff * length'


# RD regression with first order polynomial
rd1=sm.OLS.from_formula(formula1, data=data).fit()
beta=rd1.params
rd1=rd1.get_robustcov_results(cov_type='HC1')


## Scatter plot raw data
plt.figure()
plt.scatter(data['length'], data['mpg'], c=data['cutoff'], cmap='PuOr', s=5, alpha=0.3)
plt.axvline(x=225, color='red', linestyle='--')
plt.xlabel('Length (inches)')
plt.ylabel('Fuel efficiency (miles per gallon)')
plt.xlim(40, 340)
plt.ylim(5, 55)

# Add linear equation of length before and after the cutoff
x_below = np.linspace(40, 225, 100)
y_below = beta['Intercept'] + beta['length'] * x_below
plt.plot(x_below, y_below, color='green', linestyle='--')
x_above = np.linspace(225, 340, 100)
y_above = beta['Intercept'] + beta['length'] * x_above + beta['cutoff'] + beta['cutoff:length']*x_above
plt.plot(x_above, y_above, color='green', linestyle='--')
#plt.show()
plt.savefig('scatterplot2.pdf')


# Problem 4 ------------------------------------------------------------------
## Fit second order polynomial on both sides of the cutoff in RD design
## Create quadratic to fifth-order terms to use later
data['length2'] = data['length']**2

## Interact length with cutoff
formula2 = 'mpg ~ cutoff * (length + length2)'


## RD regression with second order polynomial
rd2=sm.OLS.from_formula(formula2, data=data).fit()
beta=rd2.params
rd2=rd2.get_robustcov_results(cov_type='HC1')



## Scatter plot 
plt.figure()
plt.scatter(data['length'], data['mpg'], c=data['cutoff'], cmap='PuOr', s=5, alpha=0.3)
plt.axvline(x=225, color='red', linestyle='--')
plt.xlabel('Length (inches)')
plt.ylabel('Fuel efficiency (miles per gallon)')
plt.xlim(40, 340)
plt.ylim(5, 55)


# Add quadratic equation of length before and after the cutoff
x_below = np.linspace(40, 225, 100)
y_below = beta['Intercept'] + beta['length'] * x_below + beta['length2']*x_below**2
plt.plot(x_below, y_below, color='green', linestyle='--')
x_above = np.linspace(225, 340, 100)
y_above = beta['Intercept'] + beta['length'] * x_above + beta['cutoff'] + beta['cutoff:length']*x_above + beta['length2']*x_above**2 + beta['cutoff:length2']*x_above**2
plt.plot(x_above, y_above, color='green', linestyle='--')
plt.savefig('scatterplot3.pdf')


# Problem 5 ------------------------------------------------------------------
## Fit fifith order polynomial on both sides of the cutoff in RD design

## Create cube to fifth-order terms 
data['length3'] = data['length']**3
data['length4'] = data['length']**4
data['length5'] = data['length']**5

## Interact length with cutoff
formula5 = 'mpg ~ cutoff * (length + length2 + length3 + length4 + length5)'


## RD regression with second order polynomial
rd5=sm.OLS.from_formula(formula5, data=data).fit()
beta=rd5.params
rd5=rd5.get_robustcov_results(cov_type='HC1')


# Scatter plot 
plt.figure()
plt.scatter(data['length'], data['mpg'], c=data['cutoff'], cmap='PuOr', s=5, alpha=0.3)
plt.axvline(x=225, color='red', linestyle='--')
plt.xlabel('Length (inches)')
plt.ylabel('Fuel efficiency (miles per gallon)')
plt.xlim(40, 340)
plt.ylim(5, 55)

# Add fifth order polynomial equation of length before and after the cutoff
x_below = np.linspace(40, 225, 100)
y_below = beta['Intercept'] + beta['length'] * x_below + beta['length2']*x_below**2 + beta['length3']*x_below**3 + beta['length4']*x_below**4 + beta['length5']*x_below**5
plt.plot(x_below, y_below, color='green', linestyle='--')
x_above = np.linspace(225, 340, 100)
y_above = beta['Intercept'] + beta['length'] * x_above \
            + beta['cutoff']+beta['cutoff:length']*x_above+beta['length2']*x_above**2 \
            +beta['cutoff:length2']*x_above**2+beta['length3']*x_above**3+beta['cutoff:length3']*x_above**3 \
            +beta['length4']*x_above**4+beta['cutoff:length4']*x_above**4+beta['length5']*x_above**5+beta['cutoff:length5']*x_above**5
plt.plot(x_above, y_above, color='green', linestyle='--')
plt.savefig('scatterplot5.pdf')

## Create regression table

os.chdir(table)

output = stargazer([rd1,rd2,rd5])

output.rename_covariates({'cutoff':' Treatment effect'})
output.covariate_order(['cutoff'])
output.show_stars=True
output.significant_digits(2)
output.show_degrees_of_freedom(False)

tex_file = open('RD2_5.tex', "w" ) 
tex_file.write( output.render_latex(only_tabular=True) )
tex_file.close()



# Problem 6 ------------------------------------------------------------------
# 2SLS

# Interact length with treatment
formula_1st= 'mpg ~ car + cutoff * length'


# RD regression with the first order polynomial
first_stage=sm.OLS.from_formula(formula_1st, data=data).fit()
first_stage=first_stage.get_robustcov_results(cov_type='HC1')


data['mpg_hat']=first_stage.predict()


## 2nd Stage
formula_2nd= 'price ~ mpg_hat + car'


second_stage=sm.OLS.from_formula(formula_2nd, data=data).fit()
second_stage=second_stage.get_robustcov_results(cov_type='HC1')


## Create regression output table

output1 = stargazer([second_stage])

output1.rename_covariates({'mpg_hat':' Miles per gallon', 'car':'Car'})
output1.show_stars=True
output1.significant_digits(2)
output1.show_degrees_of_freedom(False)

tex_file = open('2SLS.tex', "w" ) 
tex_file.write( output.render_latex(only_tabular=True) )
tex_file.close()

