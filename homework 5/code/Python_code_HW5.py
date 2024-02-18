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

# For stargazer I opened Anaconda Prompt using start and wrote there pip install stargazer. After that this code was executed. 
from stargazer.stargazer import Stargazer as stargazer
from stargazer.stargazer import LineLocation



# Set working directories and seed

#If working from home:

datapath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 5\data'
outputpath = r'C:\Users\Owner\Dropbox\phdee-2024-AM\homework 5\output'

# If working on campus: 

#datapath = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 5\data'
#outputpath = r'C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 5\output'

os.chdir(datapath)

random.seed(20121159)
np.random.seed(4)

# Load dataset in the system 

data=pd.read_csv('instrumentalvehicles.csv')
l