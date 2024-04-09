**** HW 9 ****
**** Economics 7103  ****
**** Ana Mazmishvili ****
******************************************************************************

clear all

set more off

local datapath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 9\data"


*local datapath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 8\data"
*local figure "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 8\output\figure"
*local table "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 8\output\table"

cd "`datapath'"

* Load data

use "recycling_hw", clear

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


ssc install sdid, replace
ssc install synth, replace all


	 
*******************************************************************************
***                           Question 1.1                                  ***
*******************************************************************************
* Yearly plot of recycling rate for NYC, NJ, and MA for 1997-2008
	local figure "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 9\output\figure"
	cd "`figure'"
	
	collapse (mean) recyclingrate, by(nyc ma nj year)
	twoway (line recyclingrate year if nyc == 1, lcolor(blue) lpattern(solid)) ///
	   (line recyclingrate year if nj == 1, lcolor(red) lpattern(dash)) ///
       (line recyclingrate year if ma == 1, lcolor(green) lpattern(dash)), ///
       legend(label(1 "NYC") label(2 "NJ") label(3 "MA")) ylabels(0(0.1)0.5, nogrid) xlabels( 1997(1)2008, nogrid) xline(2001.5 2004.5) ///
       ytitle(Recycling Rate) xtitle(Year) title("Treatment vs Controls")
  
	cd "`figure'"
	graph export "treatedvscontrol.pdf", replace 
	

* Yearly plot of recycling rate for NYC and the sum of NJ and MA for 1997-2008
	
		
	collapse (mean) recyclingrate, by(nyc year)
	twoway 	(line recyclingrate year if nyc == 1, lcolor(blue) lpattern(solid)) ///
			(line recyclingrate year if nyc == 0, lcolor(green) lpattern(dash)), ///
			legend(label(1 "NYC") label(2 "NJ + MA")) ylabels(0(0.1)0.7, nogrid) xlabels( 1997(1)2008, nogrid) xline(2001.5 2004.5) xtitle(Year) ytitle(Recycling Rate) title("Treatment vs Control") 
			
	
	graph export "linechartrecyclingrate.pdf", replace 
	

*******************************************************************************
***                           Question 1.2                                  ***
*******************************************************************************
* The effect of the pause on the recycling rate in NYC using a TWFE regression from 1997-2004, cluster at region level

	local datapath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 9\data"
	cd "`datapath'"
	
	use "recycling_hw", clear
	keep if year < 2005
	gen treatment=0
	replace treatment=1 if nyc & year>2001
	ivreghdfe recyclingrate treatment, absorb(region year) vce(cluster region)
	
*******************************************************************************
***                           Question 1.3                                  ***
*******************************************************************************
* SDID version of the TWFE regression 
	local figure "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 9\output\figure"
	cd "`figure'"
	
	sdid recyclingrate region year treatment, vce(bootstrap) seed(123) reps(100)  ///
	graph g2_opt(legend(ring(0) pos(11) order(1 "NYC" 2 "NJ+MA") region(style(none)) rows(2)) ///
	xtitle(Year) xlabel(1997(1)2004,nogrid) text(0.25 2003 "ATT = -0.06436" " SE = (0.00685)") scheme(plotplainblind))
	
		
	graph export "sdid.pdf", replace
	
*******************************************************************************
***                           Question 1.4                                  ***
*******************************************************************************
* Event Study

	local datapath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 9\data"
	cd "`datapath'"
	use "recycling_hw", clear
	
	
	local table "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 9\output\figure"
	cd "`figure'"
		
	reghdfe recyclingrate b2001.year##1.nyc incomepercapita nonwhite munipop2000 collegedegree2000 democratvoteshare2000 democratvoteshare2004, absorb(region year) vce(cluster region)
	
	coefplot, baselevels omitted xline(5.5) yline(0) title(Coefficients) keep(*.year#1.nyc) ///
			coeflabels( 1997.year#1.nyc="1997" 1998.year#1.nyc="1998" 1999.year#1.nyc="1999" ///
						2000.year#1.nyc="2000" 2001.year#1.nyc="2001" 2002.year#1.nyc="2002" ///
						2003.year#1.nyc="2003" 2004.year#1.nyc="2004" 2005.year#1.nyc="2005" ///
						2006.year#1.nyc="2000" 2007.year#1.nyc="2007" 2008.year#1.nyc="2008") vertical
	
	

	graph export "eventstudy.pdf", replace
	
*******************************************************************************
***                           Question 1.5                                  ***
*******************************************************************************
* Synthetic Control 

	local datapath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 9\data"
	cd "`datapath'"
	use "recycling_hw", clear
	
* Collapse data

	collapse (mean) recyclingrate incomepercapita collegedegree2000 democratvoteshare2000 democratvoteshare2004 nonwhite (first) nj ma munipop2000, by(id nyc year)
	save "recycling_hw_sc", replace
	
	
	collapse (mean) recyclingrate incomepercapita collegedegree2000 democratvoteshare2000 democratvoteshare2004 nonwhite (first) nj ma id munipop2000, by(nyc year)
	drop if !nyc
	save "recycling_hw_sc_nyc", replace
	
	use "recycling_hw_sc", clear
	drop if nyc
	append using "recycling_hw_sc_nyc"
	save "recycling_hw_sc", replace
	
* Synthetic Control
	use "recycling_hw_sc", clear
	la var recyclingrate "Recycling Rate"
	xtset id year
	
	local figure "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 9\output\figure"
	cd "`figure'"
	
	
	
	synth recyclingrate recyclingrate(1997) recyclingrate(1998) recyclingrate(1999) ///
			recyclingrate(2000) recyclingrate(2001) democratvoteshare2000(2000) collegedegree2000(2000) ///
			nonwhite incomepercapita, trunit(27) trperiod(2002) fig keep(scresult) replace
			
	synth_runner recyclingrate recyclingrate(1997) recyclingrate(1998) recyclingrate(1999) ///
			recyclingrate(2000) recyclingrate(2001) democratvoteshare2000(2000) collegedegree2000(2000) ///
			nonwhite incomepercapita, trunit(27) trperiod(2002) mspeperiod(1998(1)2001) gen_vars

	single_treatment_graphs, treated_name(NYC) trlinediff(-0.5) effects_ylabels(-.4(.1).5) do_color(gs13) raw_options(scale(1.4) xlabel(1997(2)2008, nogrid) xmtick(1997(1)2008) xtitle(Year) legend(pos(7) ring(0) region(style(none))) xline(2004.5) title("Synthetic control raw outcomes:") subtitle("Recycling rate")) effects_options(scale(1.6) xlabel(1997(2)2008, nogrid) xmtick(1997(1)2008) xtitle(Year) ytitle("") legend(pos(7) ring(0) region(style(none))) xline(2004.5) title(Synthetic control effects and placebos) subtitle("Coefficient estimates"))

	effect_graphs, treated_name(NYC) trlinediff(-0.5) tc_options(scale(1.4) xlabel(1997(2)2008, nogrid) xmtick(1997(1)2008) ylabel(,nogrid) xtitle(Year) legend(pos(7) ring(0) region(style(none))) xline(2004.5) title(NYC and synthetic control) subtitle(Recycling rate)) effect_options(xlabel(1997(2)2008, nogrid) xmtick(1997(1)2008) ylabel(, nogrid) xtitle(Year) legend(pos(7) ring(0) region(style(none))) xline(2004.5) title(Synthetic control) subtitle("Coefficient estimates") yline(0))
	
	graph export "raw.pdf", name(raw) replace
	graph export "placebo.pdf", name(effects) replace
	graph export "effect.pdf", name(effect) replace
	graph export "treatmentcontrol.pdf", name(tc) replace