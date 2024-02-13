clear all
set more off

* Set local paths

	local datapath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 4\data"
	local outputpath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 4\output"
	
	cd "`datapath'"
	
* Load data

	import delimited fishbycatch.csv, clear

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
 
												
** OLS Regression with firm and month FE

	reg bycatch treat shrimp salmon firmsize firm_* month_*, vce(cluster firm)

	
********************************************************************************
* Question 1.b
********************************************************************************
** Demeaning each variable 
** Comment: firmsize and firm variables will be eliminated after demeaning, but month variable will get negative results after demeaning. I am not sure what we should do with time dummies

	foreach z of varlist bycatch treat shrimp salmon month_* {
		egen mean_`z' = mean(`z'), by(firm)
		gen dem_`z' = `z' - mean_`z'
		drop mean_*
				
	}



** OLS Regression of the demeaned variables with time FE
	reg dem_bycatch dem_treat dem_shrimp dem_salmon dem_month_*, vce(cluster firm)
	

** OLS Regression of the demeaned variables without time FE	
	reg dem_bycatch dem_treat dem_shrimp dem_salmon, vce(cluster firm)

* Balance table

	local summarylist "electricity sqft temp"

	eststo treated: quietly estpost summarize `summarylist' if retrofit == 1
	eststo controls: quietly estpost summarize `summarylist' if retrofit == 0
	eststo diff: quietly estpost ttest `summarylist', by(retrofit) unequal
	
	cd "`outputpath'"
	
	esttab treated controls diff using summarystats.tex, tex cells("mean(pattern(1 1 0) fmt(%9.2fc) label(Mean))  b(star pattern(0 0 1) fmt(%9.2fc) label(Diff.))" "sd(pattern(1 1 0) par label(SD)) p(pattern(0 0 1) par fmt(%9.2fc) label(p-value))") stats(N obs, fmt(%9.0fc) labels("Observations")) starlevels(* 0.05 ** 0.01) mtitles(Treated Controls Difference) label replace prehead({\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi} \begin{tabular}{l*{3}{cc}} \hline) prefoot( & & & \\) postfoot(\hline \multicolumn{4}{c}{ ** p$<$0.01, * p$<$0.05} \\ \end{tabular} })
	
********************************************************************************
* Question 2
********************************************************************************

* Scatter plot

	twoway scatter electricity sqft, ytitle("Electricity consumption (kwh)") xtitle("Square feet") title(Question 2)
	graph export question2_scatterplot.pdf, replace
	
********************************************************************************
* Question 3
********************************************************************************

* Label variables

	la var electricity "Electricity (kwh)"
	la var sqft "Square feet"
	la var retrofit "Treatment"
	la var temp "Temperature"

* Regression

	reg electricity sqft retrofit temp, vce(robust)
	
* Table output
	
	outreg2 using question3_output.tex, label tex(fragment) replace