#! tcl
#
#
# 2015.4.23
# this version dump 'region' file about the frozen atom index..
# suppose to be used in onion or qm/mm calc.
# Author: Du Likai
# qibebt
##
# 2012-10
# c This is a tcl script, select the QM and Active Region in QM/MM calculation
# @ Used in Chemshell 
# @ address: chem306
# @ Usage:
# @ set qmlist for QM region
# @ set activelist for Active region.
# c

#                ================Select QM/Active Region================
#                @ chem306
#                @ usage: set qmlist/activelist value.
#                @                in vmd tk console, Run source select.tcl
#                @ U can set qmlist/activelist in tk console or
#                @ modify the script.
#                @
#                @ write out 'region' file, contain the qmlist/activelist
#                @ BY default, you shuold set qm/active list in scripts
#                @ If not, set console to yes in tk console.
#                @
#                --------------------------------------------------------
#
# CODE bg
# U can manually set the active list
# set activelist "same residue as within 15 of resname SUS"

# check if qmlist and activelist variable exists?
if { [info exists active] } {
    puts "the qmlist is set as: \n $active"
} else {
    puts "Error: the variable 'active' is not defined."
    puts "Usage: You should set active variable as a selection text in vmd-tcl format.., i.e."
    puts "set active \"resname MOL\""
    puts "enter the active region selection text:"
    
}


# Open file to write.
set fh [open region w]
# initialize activelist selection
set sel [ atomselect top $active ]
set nactive [$sel num]

puts "$nactive active atoms you selected."
set activelist [$sel list]

puts $fh "set active [list $activelist]"

close $fh


puts "active list has been dump into region file."
puts "WARNING: the activelist atom id start from zero."


