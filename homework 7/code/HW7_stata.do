**** HW 7 ****
**** Economics 7103  ****
**** Ana Mazmishvili ****
******************************************************************************


*** Problem 1 *********
******************************************************************************
clear all

set more off

global path ""

local datapath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 7\data"

*local datapath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 6\data"

local figure "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 7\output\figure"
local table "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 7\output\table"

cd "`datapath'"

* Load data

import delimited "instrumentalvehicles.csv", clear
	 
*******************************************************************************
***     Question 1 - 2SLS using the rdrobust command                        ***
*******************************************************************************
* First stage with firt-level polynomial
	rdrobust mpg length car, c(225) p(1) bwselect(mserd)
* Obtain fitted values
	rdplot mpg length, c(225) p(1) bwselect(mserd) covs(car) genvars ///
	graph_options(ytitle(Fuel efficiency (miles per gallon)) ///
	xtitle(Vehicle length (inches)) legend(off))

	cd "`figure'"	
	* Export graph
	graph export "ScatterRD.pdf", replace
	
	rename rdplot_hat_y mpg_fitted
		
	reg price mpg_fitted car, robust
	la var mpg_fitted "ATE" 
	
	estimates store model
	
	outreg2 [model ] using hw7_stata.tex, tex(frag) replace label ctitle("Average treatment effect from the second-stage regression results")

