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
# U can manually set qmlist and activelist here.
set qmlist "all"
#set activelist "same residue as within 15 of resname SUS"
#set wat_list "same residue as resname WAT"
# check if qmlist and activelist variable exists?
if { [info exists qmlist] } {
        puts "the qmlist is set as: \n $qmlist"
        } else {
        puts "the variable 'qmlist' is not defined."
        exit(1)
        }
#if { [info exists activelist] } {
#        puts "the qmlist is set as: \n $activelist"
#        } else {
#        puts "the variable 'active' is not defined."
#        exit(1)
#        }

# Open file to write.
set fh [open type-region w]

# initialize activelist selection
#set sel [ atomselect top $activelist ]
#set nactivelist [$sel num]
#puts "$nactivelist active atom you selected."
#set active [$sel list]
#set a {}
#foreach i $active {
#lappend a [ incr i 1]
#}
#puts $a
#puts $fh "set active [list $a]"

# initialize qmlist selection
set sel [ atomselect top $qmlist ]
set nqmlist [$sel num]
puts "$nqmlist QM atom you selected."
set types [$sel get type]
#set q {}
#foreach i $qmatoms {
#lappend q [ incr i 1]
#}
#puts $fh "set qmatoms [list $i]"
puts $fh "set types [list $types]"




set sel [ atomselect top $qmlist ]
#set segid [$sel get segid]
#puts $segid

#set lseglist [lsort -unique $segid]
set groups {}
set lseglist {{}}
#set lseglist [lsort -unique [$sel get segid]]
  # 
#  set selover [atomselect top "segid $lseg"]
#  puts $selover
  # 
  set resover [lsort -unique [$sel get resid]]
  foreach res $resover {
	set selid [atomselect top "resid $res"]
	set res_name [$selid list]
	set id {}
	foreach i $res_name {
		lappend id [ incr i 1]
		}
	lappend groups $id
	
    # $selid $res_name
  }

puts $fh "set groups [list $groups]"


close $fh


