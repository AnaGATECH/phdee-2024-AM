**** HW 6 ****
**** Economics 7103  ****
**** Ana Mazmishvili ****
******************************************************************************


*** Problem 1 *********
******************************************************************************
clear all

set more off

* local outputpath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 5\output"

local datapath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 6\data"

cd "`datapath'"

* Load data

	 use "energy_staggered.dta" , clear
	 
		 
* Generate time format of the datetime variable
	 
	gen double day_time = clock(datetime, "MDYhms")
	format day_time %tc
	
	la var day_time "Date and Time in time format"
	
* Sort date variables and regroup it

	sort day_time
	egen hour_count = group(day_time)
	list day_time hour_count