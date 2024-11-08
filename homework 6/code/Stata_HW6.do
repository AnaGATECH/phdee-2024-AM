**** HW 6 ****
**** Economics 7103  ****
**** Ana Mazmishvili ****
******************************************************************************


*** Problem 1 *********
******************************************************************************
clear all

set more off

local datapath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 6\data"

*local datapath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 6\data"

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
	
* Calculate number of cohorts
	levelsof treated, local(unique_values)
	local num_unique : word count `unique_values'
	display "Number of unique values in the variable: " `num_unique'
	

	
*** Question 2. ***
********************************************************************************

* Estimate TWFE weights
	twowayfeweights energy treated hour treatment, type(feTR)
	
	
*** Question 3. ***
****************************************************************************
	
* local tablepath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 6\output\table"

local tablepath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 6\output\table"

cd "`tablepath'"
	
	reghdfe energy treatment temperature precipitation relativehumidity, absorb(day_time id) vce(cluster id)
	
	estimates store model1
	
	outreg2 [model1 ] using hw6_output1_stata.tex, tex(frag) replace label ctitle("TWFE (Hourly)")
	

	
* Save hourly data
*save "energy_staggered_hr", replace


*******************************************************************************
***                    Part 2 - Daily Data                                  ***
*******************************************************************************
	clear all

	set more off

	*local datapath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 6\data"
	local datapath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 6\data"

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
		
	collapse (max) treatment=treatment (sum) energy=energy (mean) temperature precipitation relativehumidity zip size occupants devicegroup, by(id day)
	
* Generate day
	sort day
	egen day_num=seq(), by(id)
	

* Generate treatment cohort variable 
	egen treated=csgvar(treatment), ivar(id) tvar(day)
	

* Calculate number of cohorts
	*levelsof treated, local(unique_values)
	*local num_unique : word count `unique_values'
	*display "Number of unique values in the variable: " `num_unique'

	la var treatment "Treatment"
	la var temperature "Temperature (F)"
	la var precipitation "Precipitation (in)"
	la var relativehumidity "Relative Humidity (%)"
					


*** Question 1. ***
*******************************************************************************
*local tablepath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 6\output\table"
local tablepath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 6\output\table"

cd "`tablepath'"
	
	reghdfe energy treatment temperature precipitation relativehumidity, absorb(day id) vce(cluster id)
	
	estimates store model2
	
	outreg2 [model2 ] using hw6_output2.tex, tex(frag) replace label ctitle("TWFE (Daily)")

	
	
*** Question 2. ***  
*******************************************************************************
*local figurepath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 6\output\figure"

local figurepath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 6\output\figure"

cd "`figurepath'"

* Create event_time variable
	gen event_time = day - treated
	
* Make dummies for period and omit -1 period
	char event_time[omit] -1
	xi i.event_time, pref(_T)
	
* Position of -2
	local pos_of_neg_2 = 28 

* Position of 0
	local pos_of_zero = `pos_of_neg_2' + 2

* Position of max
	local pos_of_max = `pos_of_zero' + 29

* Event study
	reghdfe energy  _T* temperature precipitation relativehumidity, absorb(id) vce(cluster id)
	
	
	
	
	forvalues i = 1(1)`pos_of_neg_2'{
		scalar b_`i' = _b[_Tevent_tim_`i']
		scalar se_v2_`i' = _se[_Tevent_tim_`i']
	}
		

	forvalues i = `pos_of_zero'(1)`pos_of_max'{
		scalar b_`i' = _b[_Tevent_tim_`i']
		scalar se_v2_`i' = _se[_Tevent_tim_`i']
	}

	capture drop order
	capture drop b 
	capture drop high 
	capture drop low

	gen order = .
	gen b =. 
	gen high =. 
	gen low =.

	local i = 1
	local graph_start  = 1
	forvalues day = 1(1)`pos_of_neg_2'{
		local event_time = `day' - 2 - `pos_of_neg_2'
		replace order = `event_time' in `i'
		
		replace b    = b_`day' in `i'
		replace high = b_`day' + 1.96*se_v2_`day' in `i'
		replace low  = b_`day' - 1.96*se_v2_`day' in `i'
			
		local i = `i' + 1
	}

	replace order = -1 in `i'

	replace b    = 0  in `i'
	replace high = 0  in `i'
	replace low  = 0  in `i'

	local i = `i' + 1
	forvalues day = `pos_of_zero'(1)`pos_of_max'{
		local event_time = `day' - 2 - `pos_of_neg_2'

		replace order = `event_time' in `i'
		
		replace b    = b_`day' in `i'
		replace high = b_`day' + 1.96*se_v2_`day' in `i'
		replace low  = b_`day' - 1.96*se_v2_`day' in `i'
			
		local i = `i' + 1
	}


	return list

	twoway rarea low high order if order<=29 & order >= -29 , fcol(gs14) lcol(white) msize(1) /// estimates
		|| connected b order if order<=29 & order >= -29, lw(0.6) col(white) msize(1) msymbol(s) lp(solid) /// highlighting
		|| connected b order if order<=29 & order >= -29, lw(0.2) col("71 71 179") msize(1) msymbol(s) lp(solid) /// connect estimates
		|| scatteri 0 -29 0 29, recast(line) lcol(orange) lp(longdash) lwidth(0.5) /// zero line 
			xlab(-30(10)30 ///
					, nogrid labsize(2) angle(0)) ///
			ylab(, nogrid labs(3)) ///
			legend(off) ///
			xtitle("Days to treatment", size(3)) ///
			ytitle("Daily energy consumption (kWh)", size(3)) ///
			xline(-.5, lpattern(dot) lcolor(red) lwidth(0.7)) 	
			
	graph export "event_study.pdf", replace 
	

*** Question 3. ***
*******************************************************************************
eventdd energy temperature precipitation relativehumidity, hdfe absorb(id) timevar(event_time) cluster(id) graph_op(ytitle("Daily energy consumption (kWh)", size(3)) xlabel(-30(5)30) xtitle("Days to treatment", size(3)))
	
	graph export "event_study_1.pdf", replace 

*** Question 4. ***
*******************************************************************************

	csdid energy temperature precipitation relativehumidity, ivar(id) time(day) gvar(treated) method(dripw) wboot reps(50)
	estat simple
	estat event
	csdid_plot, title("Event Study") ytitle("Daily energy consumption (kWh)", size(3)) xlabel(-30(5)30) xtitle("Days to treatment", size(3)) xline(-.5, lpattern(dash) lcolor(purple) lwidth(0.7))
	
	graph export "event_study_csdid.pdf", replace
		

	
			
			
*** Question 1. -  My version which is not correct ***
*******************************************************************************		
* Event study
*	reghdfe energy  _t* temperature precipitation relativehumidity, absorb(id) vce(cluster id)
	
*	estimates store model3
*	coefplot model3, level (95)
	
	


