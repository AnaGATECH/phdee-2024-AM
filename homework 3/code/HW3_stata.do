*** Author : Ana Mazmishvili
*** Course : Environmental Economics II (ECON7103 )
***   Task : Homework 3  
*****************************************************

* Prepare file for work

clear all
set more off 

* Set up my working directories

* While working at home: 
*******************************************************************************
*global path "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 3"

*cd "`path'

*global datapath = "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 3\data"
*global table_path "$path\output\table" 
*global figure_path "$path\output\figure"

* While working on campus: 
*******************************************************************************
global path "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 3"

cd "`path'

global datapath = "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 3\data"
global table_path "$path\output\table" 
global figure_path "$path\output\figure"



* Download and use plotplainblind scheme

	ssc install blindschemes, all
	ssc install outreg2
	set scheme plotplainblind, permanently
	
* Import dataset

import delimited "$datapath\kwh.csv"

*****************************************************
***                 Questions 1.e                 ***
*****************************************************
* Estimate the log-transformed equation via ordinary least squares on the transformed parameters using any algorithm you would like. Save the coefficient estimates and the average marginal effects estimates of zi and di. Bootstrap the 95% confidence intervals of the coefficient estimates and the marginal effects estimates using 1000 sampling replications (note that each bootstrap replication should perform both the regression and the second stage calculation of the marginal effect). Display the results in a table with three columns (one for the variable name, one for the coefficient estimate, and one for the marginal effect estimate). Show the 95% confidence intervals for each estimate under each number.

** Response**

* Generate logarithm of the variables and label them
	
	gen ln_electr=ln(electricity)
	gen ln_sqft=ln(sqft)
	gen ln_temp=ln(temp)
	
	
	
	label variable electricity "Monthly kWh electricity usage by HH"
    label variable sqft "Square feet of the home"
    label variable retrofit "= 1 if the home received a retrofit"
    label variable temp "The outdoor average temperature (◦F) during the month at the home's location"
	
	label variable ln_electr "log kWh electricity"
    label variable ln_sqft "log of square feet of the home"
    label variable ln_temp "log of the outdoor average temperature (◦F)"
	
	
	* Fit linear regression model

	reg ln_electr ln_sqft ln_temp retrofit // this is the basic regression.  It calculates standard errors assuming homoskedasticity by default.
	
	* Bootstrap

		reg ln_electr ln_sqft ln_temp retrofit, vce(bootstrap, reps(1000))
	
	* If we need to bootstrap ourselves (to incorporate two steps in the estimation for example), we can draw bootstrap samples and repeatedly estimate our regression:
	
		mat betas = J(1000,3,.) // pre-allocate a matrix for the outcomes of our 1000 regressions
	
		forvalues i = 1/1000 {
			preserve // preserves the data as it was in the memory at this point
				bsample // samples with replacement up to the number of observations
				
				reg ln_electr ln_sqft ln_temp retrofit
				
				    mat `betas'[`i',1] = _b[ln_sqft] // save both
					mat `betas'[`i',2] = _b[ln_temp]
					mat `betas'[`i',3] = _b[retrofit]
					mat `betas'[`i',4] = _b[_cons]
			restore // restores the data as you preserved it originally
		}
		
	* You can just use the 25th and 975th largest estimates (2.5 and 97.5 percentiles) as the confidence interval, take the standard deviation of all the estimates as the standard error, or calculate the full covariance matrix of the boostrap estimates.  You can look at the "betas" by typing "mat list betas"
	
	* What I will do is get the full covariance matrix.
	
	* You can write a program to get Stata to replace the covariance matrix with the bootstrapped covariance matrix.  Doing this will let you use postestimation commands like outreg2 that make creating tables really easy.
	
		capture program drop bootstrapsample
		program define bootstrapsample, eclass
			tempname betas betas1 betas2 betas3 betas4
			mat `betas' = J(1000,3,.)
			forvalues i = 1/1000 {
				preserve
					bsample 
					quietly: reg ln_electr ln_sqft ln_temp retrofit
					
					mat `betas'[`i',1] = _b[ln_sqft] // save both
					mat `betas'[`i',2] = _b[ln_temp]
					mat `betas'[`i',3] = _b[retrofit]
					mat `betas'[`i',4] = _b[_cons]
					di `i' // lets you know the progress
				restore
			}
			svmat `betas', name(temp)
				corr temp1 temp2 temp3 temp4, cov // get the covariance matrix
				mat A = r(C) // save covariance matrix
				drop temp1 temp2 temp3 temp4
				
			reg ln_electr ln_sqft ln_temp retrofit // rerun the regression
			ereturn repost V = A // post the new covariance matrix as the covariance matrix V that Stata uses
		end
		
		bootstrapsample // runs the program we wrote
		estimates store bootreg
		
	* Write a table using outreg2
	
		outreg2 [bootreg] using sampleoutput_stata.tex, label 2aster tex(frag) dec(2) replace ctitle("Ordinary least squares")
		
* Plot coefficients using coefplot
	
	coefplot, vertical yline(0) rename(_cons = "Constant") ytitle("Coefficient estimate")
	
	graph export samplebars_stata.pdf, replace



*****************************************************
***                 Questions 1.f                 ***
*****************************************************
* Graph the average marginal effects of outdoor temperature and square feet of the home with bands for their bootstrapped confidence intervals so that they are easy to interpret and compare.

