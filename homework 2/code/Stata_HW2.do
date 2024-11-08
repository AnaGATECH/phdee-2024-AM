*** Author : Ana Mazmishvili
*** Course : Environmental Economics II (ECON7103 )
***   Task : Homework 2  
*****************************************************

* Prepare file for work

clear all
set more off 

* Set up my working directories

global path "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 2"

cd "`path'

global datapath = "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 2\data"

global table_path "$path\output\table" 
global figure_path "$path\output\figure"


* Download and use plotplainblind scheme

	ssc install blindschemes, all
	ssc install outreg2
	set scheme plotplainblind, permanently
	

*****************************************************
***                 Questions 2.1                 ***
*****************************************************

*** Check for balance between the treatment and control groups using Stata. Create a table that displays each variable's sample mean, sample standard deviation, and p-values for the two-way t-test between treatment and control group means. Your table should have four columns: one with variable names, one with sample mean and standard deviation for the control group, one with sample mean and standard deviation for the treatment group, and one with the p-value for the difference-inmeans test.

** Import data and label variables

import delimited "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 2\data\kwh.csv", varnames(1) 
label variable electricity "Monthly kWh electricity usage by HH"
label variable sqft "Square feet of the home"
label variable retrofit "= 1 if the home received a retrofit"
label variable temp "The outdoor average temperature (◦F) during the month at the home's location"

eststo control: quietly estpost summarize electricity sqft temp if retrofit == 0
eststo treatment: quietly estpost summarize electricity sqft temp if retrofit == 1
eststo differences: quietly estpost ttest electricity sqft temp, by(retrofit) unequal

esttab control treatment differences using "$table_path\summarytable.tex", cell( mean(pattern(1 1 0) fmt(2) label(Mean)) & p(pattern(0 0 1) fmt(3)) sd(pattern(1 1 0) fmt(2) par(( )) label(Std. Dev.)) & t(pattern(0 0 1) fmt(3) par([ ]) ) ) mtitle("Control" "Treatment" "P-value")  collabels(none) nonum stats(N, fmt(%15.0fc) label("Observations"))


*****************************************************
***                 Questions 2.2                 ***
*****************************************************
* Create a two-way scatterplot with electricity consumption on the y-axis and square feet on the x-axis using Stata's twoway command. Make sure to label the axes.

twoway  (scatter electricity sqft, mcolor(%30)), title("{bf} Two-way Scatterplot", pos(16) size(4)) subtitle("Electricity consumption vs. Square feet of home", pos(12) size(2.5))
		
graph export "$figure_path\scatterplot.pdf", replace


*****************************************************
***                 Questions 2.3                 ***
*****************************************************
* Estimate the same regression as in #3 above using Stata's regress command, estimating heteroskedasticityrobust standard errors. Report the results in a new LaTeX table (including standard errors) using Stata's outreg2 command.

reg electricity retrofit sqft temp, robust

outreg2 using "$table_path\robustOLS.tex", replace
