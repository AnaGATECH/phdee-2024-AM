**** HW 6 ****
**** Economics 7103  ****
**** Ana Mazmishvili ****
******************************************************************************


*** Problem 1 *********
******************************************************************************
clear all

set more off

* local outputpath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 6\output"

local datapath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 6\data"

cd "`datapath'"

* Load data

	 use "energy_staggered.dta" , clear
	 
*** Question 1. ***
********************************************************************************
	 		 
* Generate time format of the datetime variable
	gen double day_time = clock(datetime, "MDYhms")
	format day_time %tc
	
	la var day_time "Date and Time in time format"
	order day_time id treatment
	

* Generate treatment cohort 
	egen treated=csgvar(treatment), ivar(id) tvar(day_time)
	format treated %tc
	
	
* Generate hour variable 
	sort day_time
	egen hour=seq(), by(id)
	

	
*** Question 2. ***
********************************************************************************

* Estimate TWFE weights
	twowayfeweights energy treated hour treatment, type(feTR)
	
	
*** Question 3. ***
********************************************************************************

	
local tablepath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 6\output\table"

cd "`tablepath'"
	
	reghdfe energy treatment temperature precipitation relativehumidity, absorb(day_time id) vce(cluster id)
	
	estimates store model1
	
	outreg2 [model1 ] using hw6_output1_stata.tex, tex(frag) replace label ctitle("TWFE regression results on hourly data")
	

	
* Save hourly data
	save "energy_staggered_hr", replace
