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
	 
*******************************************************************************
***                           Question 1                                    ***
*******************************************************************************
	
* Generate a log outcome variable and a binary treatment variable 
	gen log_mw=log(mw)
	
	format date %td
	gen treatment=1 if date>mdy(3,1,2020)
	replace treatment=0 if treatment==.
	
	
* (a) Estimate equation 1.
	ivreghdfe log_mw treatment temp pcp, absorb(zone month dow hour) robust
	
* (b) Estimate treatment effect matching estimator using the Mahalanobis distance norm and one nearest neighbor
	encode zone, gen(zone_fac)
	drop if inrange(month,1,2)
	teffects nnmatch (log_mw temp pcp) (treatment), metric(maha) ematch(i.zone_fac i.month i.dow i.hour)
	teffects nnmatch (log_mw temp pcp) (treatment), metric(maha) ematch(i.zone_fac i.month i.dow i.hour) biasadj(temp pcp)
	
*******************************************************************************
***                           Question 2                                    ***
*******************************************************************************
	
* (a) Estimate equation 2
	ivreghdfe log_mw treatment temp pcp, absorb(zone month dow hour year) robust


*******************************************************************************
***                           Question 3                                    ***
*******************************************************************************
* Generate a new binary variable year2020
	gen year2020=1 if year==2020
	replace year2020=0 if year==.

* Generate a new variable logmw_hat equal to the matched electricity consumption
	teffects nnmatch (log_mw temp pcp) (year2020), metric(maha) ematch(i.zone_fac i.dow i.hour i.month) biasadj(temp pcp) generate(match)
	predict logmw_hat, po tlevel(0)

* (a) Estimate equation 3 on the 2020 data only
	gen diff_mw=log_mw-logmw_hat
	drop if year<2019
	drop treatment
	gen treatment=1 if year==2020
	replace treatment=0 if treatment==.
	
	reg diff_mw treatment, robust
