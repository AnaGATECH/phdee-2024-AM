clear all
set more off

* Set local paths

	global datapath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 4\data"
	global  outputpath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 4\output"
	
	
	global table_path "$outputpath\table" 
    global figure_path "$outputpath\figure"
	
	*cd "`datapath'"
	
* Load data

	import delimited "$datapath\fishbycatch.csv", clear

* Reshape file

	reshape long shrimp salmon bycatch, i(firm) j(month)
	
* Sort and define the panel data
	sort firm month
	tsset firm month
	
* Label variables

	la var firm "Firm identification number"
	la var shrimp "Pounds of shrimp"
	la var salmon "Pounds of salmon"
	la var bycatch "Pounds of bycatch"
	la var firmsize "Size of fishing fleet"
	la var treated "=1 if firm received information treatment in January 2018"
	la var month "All months during 2017 & 2018"

********************************************************************************
* Question 1.a
********************************************************************************
** Generate indicator variables for each firm and month
	
	foreach f_id of num 1/50 {

			gen firm_`f_id' = (firm == `f_id')
												}
												
												
	foreach m of num 1/24 {

			gen month_`m' = (month == `m')
												}				
												
** Generate treatment variable
	
	gen treat=1 if month>=13 & treated==1
	replace treat=0 if treat==. 
	la var treat "Treatment"
 
												
** OLS Regression with firm and month FE

	reg bycatch treat shrimp salmon firmsize firm_* month_*, vce(cluster firm)
	eststo Model1
	estadd local method "With FEs"
	
********************************************************************************
* Question 1.b
********************************************************************************
** Demeaning each variable 
** Comment: firmsize and firm variables will be eliminated after demeaning, but month variable will get negative results after demeaning. I am not sure what we should do with time dummies

	foreach z of varlist bycatch treat shrimp salmon {
		egen mean_`z' = mean(`z'), by(firm)
		gen dem_`z' = `z' - mean_`z'
		drop mean_*
				
	}
	
la var dem_treat "Treatment"

** OLS Regression of the demeaned variables without time FE	
	reg dem_bycatch dem_treat dem_shrimp dem_salmon, vce(cluster firm)
	eststo Model3
	estadd local method "Demeaned"
	
** Combine results 
	esttab using "$table_path\summary_table.tex", rename(dem_treat treat) label replace ///
		keep(treat) ///
		b(2) se(2) ////
		mtitle("(a) Original" "(b) No FE") collabels(none) nostar nonote nonum ///
		coeflabels(treat "Treatment Effect Estimates") ///
		scalars("method Method") obslast 

	
