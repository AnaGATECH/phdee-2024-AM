**** HW 9 ****
**** Economics 7103  ****
**** Ana Mazmishvili ****
******************************************************************************

clear all

set more off

local datapath "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 9\data"
local figure "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 9\output\figure"
local table "C:\Users\Owner\Dropbox\phdee-2024-AM\homework 9\output\table"

*local datapath "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 8\data"
*local figure "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 8\output\figure"
*local table "C:\Users\amazmishvili3\Dropbox\phdee-2024-AM\homework 8\output\table"

cd "`datapath'"

* Load data

use "recycling_hw", clear
