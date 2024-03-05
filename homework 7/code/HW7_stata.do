**** HW 7   ****
**** Economics 7103  ****
**** Ana Mazmishvili ****
******************************************************************************


*** Problem 1 *********
******************************************************************************
clear all

set more off

* local outputpath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 5\output"

local datapath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 7\data"

cd "`datapath'"

* Load data

	import delimited instrumentalvehicles.csv, clear
	
	la var mpg "Miles per gallon"
	la var price "Sales price"
	la var car "=1 if the vehicle is a sedan"
	la var weight "Weight of the vehicle in pounds"
	la var height "Height of the vehicle in inches"
	la var length "Length of the vehicle in inches"
	
	
* Question 1

local tablepath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 5\output\table"

cd "`tablepath'"

Using the discontinuity as an instrument for miles per gallon, estimate the impact of mpg on the
vehicle's sale price. Use the rdrobust command in Stata. Use whatever degree polynomial you see
fit for the first stage. Use the CCT optimal bandwidth: bwselect(mserd). In the hedonic regression,
control for the class of the vehicle by including carv as in Homework 6.
(a) Report the average treatment effect from the second-stage regression results.
(b) Generate and report a plot of the results using rdplot.
2. Do you think this is a valid instrument?

    ivregress liml price car (mpg=weight), robust
	
	estimates store model1
	
	outreg2 [model1 ] using hw5_output1_stata.tex, tex(frag) replace label ctitle("The limited information maximum likelihood estimate")
	
* Question 2
		
** I needed to install weakivtest and avar packages
** ssc install weakivtest
** ssc install avar

	ivregress liml price car (mpg=weight), robust
	weakivtest
	
	
*** Comment: The Montiel-Olea-Pflueger effective F-statistic estimated using 'weakivtest' is 78.362 at 5% confidence level. 
*** At 5% confidence level TSLS is 37.418 and LIML is 37.418. 

	
