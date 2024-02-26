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
	 
*******************************************************************************
***                    Part 1 - Hourly Data                                  ***
*******************************************************************************
	 
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
	
	levelsof treated, local(unique_values)
	local num_unique : word count `unique_values'
	display "Number of unique values in the variable: " `num_unique'
	

	
*** Question 2. ***
********************************************************************************

* Estimate TWFE weights
	twowayfeweights energy treated hour treatment, type(feTR)
	
	
*** Question 3. ***
****************************************************************************
	
local tablepath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 6\output\table"

cd "`tablepath'"
	
	reghdfe energy treatment temperature precipitation relativehumidity, absorb(day_time id) vce(cluster id)
	
	estimates store model1
	
	outreg2 [model1 ] using hw6_output1_stata.tex, tex(frag) replace label ctitle("TWFE")
	

	
* Save hourly data
*save "energy_staggered_hr", replace


*******************************************************************************
***                    Part 2 - Daily Data                                  ***
*******************************************************************************
	clear all

	set more off

	local datapath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 6\data"

	cd "`datapath'"

* Load data

	 use "energy_staggered.dta" , clear
	 
 
*** Question 1. ***
*******************************************************************************
* Generate time format of the datetime variable
	gen double day_time = clock(datetime, "MDYhms")
	format day_time %tc
	
* Collapse to daily
	gen day=dofc(day_time)
	format day %td
	la var day "Day in time format"
		
	collapse (max) treatment=treatment (sum) energy=energy (mean) temperature precipitation relativehumidity zip size occupants devicegroup, by(id date)
	
* Generate day
	sort day
	egen day_num=seq(), by(id)
	
* Generate cohort
	bysort id treatment: egen treated=min(day) if treatment==1
	bysort id (first_treated): replace first_treated=first_treated[1] if missing(first_treated)
	
* Generate treatment cohort variable using canned procedure from csdid
	egen treated=csgvar(treatment), ivar(id) tvar(day)










*** Question 1. ***
*******************************************************************************













*** Question 2. ***
*******************************************************************************


*** Question 3. ***
*******************************************************************************


*** Question 4. ***
*******************************************************************************


