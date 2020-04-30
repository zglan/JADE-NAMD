#! /usr/bin/env python

import re

# make the input for transition density analysis

n_state = -1
n_atom = -1


def make_control(filename = "pop.inp"):
    """ main pop inpu """
    global n_state
    global n_atom
    
    line = raw_input("enter number of atoms: \n > ")
    n_atom = int(line.strip())
    line = raw_input("enter number of states (INCLUDE ground state): \n > ")
    n_state = int(line.strip())
    line = raw_input("enter number of total, occupied (i.e. 100,20 or 100 20): \n > ")
    n_ao, n_occ = [int(x) for x in line.replace(',',' ').split()]
    n_vir = n_ao - n_occ
    if n_vir < 0:
        print "n_ao should be larger than n_occ, %d %d" % (n_occ, n_ao)
        exit(1)

    # type input:
    # 0 for std.; 1 for turbo-td; 2 for turbo-cc; 3 for orca; 4 for gaussian
    print "Please select a number:"
    line = raw_input("enter the input file type: \n (0:std; 1:turbo-td; 2:turbo-ricc; 3:orca; 4:gaussian): \n > ")
    type_input = int(line.strip())
    # if 2 debug
    output_level = 1
    line = raw_input("output level: no-debug:1; debug: 2 [default: 1]\n > ")
    if line.strip() != "":
        output_level = int(line)

    fp = open(filename, "w") 
    print >>fp, "" 
    print >>fp, "%-10d       n_atom" % n_atom
    print >>fp, "%-10d       n_ao" % n_ao
    print >>fp, "%-10d       n_occ" % n_occ
    print >>fp, "%-10d       n_vir" % n_vir
    print >>fp, "" 
    print >>fp, "%-10d       n_state" % n_state
    print >>fp, ""
    print >>fp, "%-10d       type_input" % type_input
    print >>fp, "x          filename_input1"
    print >>fp, "x          filename_input2"
    print >>fp, "x          filename_input3"
    print >>fp, "x          filename_input4"
    print >>fp, "x          filename_input5"
    print >>fp, "x"
    print >>fp, "%-10d       output_level" % output_level
    print >>fp, "1.out      filename_output"
    fp.close()
    return

# extend the fragment index
def ext_frg_ndx(frg_ndx, flag = 0):
    """
    extend it in to actual list
    [0-17, 38, 40]
    """
    #print frg_ndx
    frg_list = []
    pat = re.compile("([0-9]+)-([0-9]+)")
    r = frg_ndx.replace(',', ' ').split()
    for ir in r:
        m = pat.search(ir)
        if m is not None:
            a, b = [int(x) for x in m.group(1,2)]
            for i in xrange(a, b+1):
                frg_list.append(i-flag)
        else:
            frg_list.append(int(ir)-flag)
    return frg_list


def make_block(filename = "block.in"):
    """
    make up block file
    """
    print "------------------------------------"
    print "BLOCK BUILDER version 1.0a"
    print "------------------------------------"
    print ""
    print "you can enter a list of atom index for a block!!!"
    print "starting..."
    print "enter 'quit' to finalize block builder.."
    print "# note: use 'other' to sample lefted atoms"
    print ""
    print "------------------------------------"
    global n_atom
    if n_atom < 0:
        line = raw_input("how many atoms?")
        n_atom = int(line)
        
    i_block = 0
    t_block = []
    while True:
        mystr = "@ atom index for block: %d \n > " % i_block
        line = raw_input(mystr)
        line = line.strip()
        if line.strip() == 'quit':
            break
        if line.strip() == "other":
            atot = []
            aother = []
            for a in t_block:
                atot.extend(a)
            for i in xrange(1, n_atom+1):
                if i  not in set(atot):
                    aother.append(i)
            t_block.append(aother)
            break
        atom_list = ext_frg_ndx(line)
        t_block.append(atom_list)
        i_block += 1
    # dump data
    print "totally, %d blocks buided up..\n" % i_block
    
    fp = open(filename, "w")
    for atom_list in t_block:
        print >>fp, "%-10d" % len(atom_list)
        for ndx in atom_list:
            print >>fp, "%d " % ndx,
        print >>fp, ""
    fp.close()

    return

def make_plot(filename = "plot_counter.sh"):
    """
    counter script sh
    """
    global n_state
    
    if n_state < 0:
        line = raw_input("how many states?")
        n_state = int(line)
    
    n_state = n_state - 1

    fp = open(filename, "w")
    print >>fp, "#! /usr/bin/env bash"
    print >>fp, "state=%d" % n_state
    
    script = """
    for ((i=1; i<=$state; i++))
    do
    {

    echo $i

    gnuplot << EOF
    set terminal jpeg  enhanced 
    set output "state_mod_$i.jpg"

    #set terminal postscript color  enhanced
    #set output "state_mod_$i.eps"
    unset key
    unset xtics
    unset ytics
    set pm3d map

    #set palette rgb 7,5,15
    set palette gray
    #set palette rgb 23,28,3
    #set palette model CMY rgbformulae 7,5,15

    #set palette rgb 3,11,6

    #set palette defined ( 0 "blue", 1 "violet", 2 "red", 3 "white" ) 

    set size square
    unset colorbox
    splot "state_mod_$i.dat"  u 1:2:3
    set output
    quit
EOF
    }
    done
    """
    print >>fp, "%s" % script

    fp.close()

    return
        
# MAIN PROGRAM
if __name__ == "__main__":
    print "### DEFINE POPULATION ANALYSIS CONDITION ###"
    print "\n"
    print "@ This program would guide you to setup input file for transition density analysis (TDA)"
    print "\n\n"
    print "Three standalone program is used to do this analysis."
    print "The first is this one, pop_inp.py, prepare input file"
    print "The second is pop_main.py, do TDA work"
    print "The third is pop_parser.py, do the block/fragment analysis"
    print ""
    print "you can use pop_inp.py to set up input for pop_main.exe or pop_parser.exe"
    print "you can also setup gnuplot input"
    print "\n"
    print "---------------------------------------------------------------------"
    print "> Select which option do you want to setup:"
    print ">> 1: input for pop_main.exe"
    print ">> 2: input for block analysis, pop_parser.exe"
    print ">> 3: template to plot the fragment analysis, plot_contour.sh"
    print ">> 0: all above"
    print ""
    i_opt = 0
    line = raw_input("enter a number above [default: 0]")
    if line.strip() != "":
        i_opt = int(line)
        
    print ""
    if i_opt == 0:
        print "@ 1. make pop.inp" 
        make_control( filename = "pop.inp")

        print "@ 2. build block file"
        make_block()

        print "@ 3. plot shell script."
        make_plot()

    elif i_opt == 1:
        print "@ 1. make pop.inp" 
        make_control( filename = "pop.inp")        
    elif i_opt == 2:
        print "@ 2. build block file"
        make_block()
    elif i_opt == 3:
        print "@ 3. plot shell script."
        make_plot()        
    else:
        print "NOTHING DONE"
