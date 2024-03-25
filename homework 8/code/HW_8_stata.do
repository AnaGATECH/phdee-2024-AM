**** HW 8 ****
**** Economics 7103  ****
**** Ana Mazmishvili ****
******************************************************************************

clear all

set more off

*local datapath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 8\data"

local datapath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 8\data"

local figure "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 8\output\figure"
local table "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 8\output\table"

cd "`datapath'"

* Load data

use "electric_matching", clear


* Install needed packages

* Install ftools (remove program if it existed previously)
cap ado uninstall ftools
net install ftools, from("https://raw.githubusercontent.com/sergiocorreia/ftools/master/src/")

* Install reghdfe
cap ado uninstall reghdfe
net install reghdfe, from("https://raw.githubusercontent.com/sergiocorreia/reghdfe/master/src/")

* Install ivreg2, the core package
cap ado uninstall ivreg2
ssc install ivreg2

* Finally, install this package
cap ado uninstall ivreghdfe
net install ivreghdfe, from(https://raw.githubusercontent.com/sergiocorreia/ivreghdfe/master/src/)

	 
*******************************************************************************
***                           Question 1                                    ***
*******************************************************************************
	
* Generate a log outcome variable and a binary treatment variable 
	gen log_mw=log(mw)
	la var log_mw "Log(MW)" 
	
	format date %td
	gen treatment=1 if date>mdy(3,1,2020)
	replace treatment=0 if treatment==.
	
	save "modified_data.dta", replace
	
	cd "`table'"	
	
* (a) Estimate equation 1.
	eststo clear
		
	ivreghdfe log_mw treatment temp pcp, absorb(zone month dow hour) robust
	
	eststo
	esttab using "output1.tex", replace

	
* (b) Estimate treatment effect matching estimator using the Mahalanobis distance norm and one nearest neighbor
	
* Convert string variable "zone" into factor variable
	encode zone, gen(f_zone)
	drop if inrange(month,1,2)
	
	eststo clear
	
	teffects nnmatch (log_mw temp pcp) (treatment), metric(maha) ematch(i.f_zone i.month i.dow i.hour)
	
	eststo
	esttab using "output2.tex", replace
	
*******************************************************************************
***                           Question 2                                    ***
*******************************************************************************
	clear all 
	local datapath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 8\data"
	local figure "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 8\output\figure"
	local table "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 8\output\table"

	cd "`datapath'"

* Load data

	use "modified_data", clear

	cd "`table'"	
	
* (a) Estimate equation 2

	eststo clear
	ivreghdfe log_mw treatment temp pcp, absorb(zone month dow hour year) robust
	
	eststo
	esttab using "output3.tex", replace


*******************************************************************************
***                           Question 3                                    ***
*******************************************************************************
* Generate a new binary variable year2020
	encode zone, gen(f_zone)
	gen year2020=1 if year==2020
	replace year2020=0 if year2020==.

* Generate a new variable logmw_hat equal to the matched electricity consumption

	teffects nnmatch (log_mw temp pcp) (year2020), metric(maha) ematch(i.f_zone i.dow i.hour i.month) biasadj(temp pcp) generate(match)
	predict logmw_hat, po tlevel(0)

* (a) Estimate equation 3 on the 2020 data only
	gen diff_mw=log_mw-logmw_hat
	drop if year<2019
	drop treatment
	gen treatment=1 if year==2020
	replace treatment=0 if treatment==.
	
	eststo clear
	reg diff_mw treatment, robust
	
	eststo
	esttab using "output4.tex", replace
