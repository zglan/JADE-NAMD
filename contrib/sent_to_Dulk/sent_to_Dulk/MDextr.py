#!/usr/bin/python

#-------------------------------------------------------------------------------#
#                                    MDextr                                     #
#                                                                               #
# This script extracts data from surface hopping output files                   #
# It requires to work:                                                          #
#   MNDO input file         The value of NCIGRD, IROOT and IUVCD is read        #
#                           If the file can not be read the program stops       #
#                           with exit code 1                                    #
#                           If one of NCIGRD or IROOT is not found the program  #
#                           stops with exit code 2                              #
#                           if no keyword IUCVD if found it is assumed iuvcd=0  #
#   dynavar.in file         The value of IOUT, NSTEP, NUM_CC and AN_CC is read  #
#                           If no IOUT is found it is assumed iout=0            #
#                           If no NSTEP is found it is just ignored             #
#                           If no NUM_CC is found it is assumed num_cc=False    #
#                           IF no AN_CC is found it is assumed an_cc=False      #
#   hopping data file       Hopping data are read                               #
#   MNDO output file        It is required only if numerical CC have to be read #
#                                                                               #
#                                                                               #
#      NOTES                                                                    #
#                                                                               #
# The value of IROOT and IUVCD is actually not used. It is read in view of      #
# implementing the extraction of oscilator strenghts and dipole moments.        #
#                                                                               #
# The value of NSTEP is actually not used. It can be usefull to check           #
# consistency of data (to be implemented)                                       #
#                                                                               #
# Actually MDextr only works for 2 and 3 states (to be extended to 4 states)    #
# [is 1 state meaningfull? I think it isn't]                                    #
#                                                                               #
#...............................................................................#
# AUTHOR: E. Fabiano                                                            #
# MAIL: efabiano@mpi-muelheim.mpg.de                                            #
# DATE: August 2007                                                             #
#-------------------------------------------------------------------------------#


#----------------------#
#      IMPORTS         #
#----------------------#

import sys
import string
import os

#----------------------------------------------------------#

#----------------------#
#      CLASSES         #
#----------------------#


# ifile

class ifile:

#  This class reads the file <filename>. It implements the following
#  methods:
#     print_file     print the content of the file
#     inline_str     given a string <stringa> and the position <pos>
#                    after <stringa> it creates a list containing
#                    the <pos>-th word following <stringa> for all
#                    occurrences of <stringa>
#     outline_str    given a string <stringa>, the number of lines to
#                    skip <linea> and the position in the line <pos>
#                    creates a list containing the word <pos>-th word
#                    in the <linea>-th line after the line where
#                    <stringa> appears. This is done for all occurrences
#                    of <stringa>

#---------------#

    def __init__(self, filename):
        try:
            self.excod = True
            file = open(filename,'r')
            self.__file_cont = file.readlines()
            file.close()
        except:
            print "I can not read file %s\n" % filename
            self.excod = False
        

    def print_file(self):
        print self.__file_cont


    def inline_str(self,stringa,pos):
        value = []
        chk = True
        par_str = string.split(stringa)
        for i in range(len(self.__file_cont)):
            parole = string.split(self.__file_cont[i])
            for j in range(len(parole)):
                if parole[j].find(par_str[0]) != -1:
                    if j+len(par_str) > len(parole):
                        break
                    for l in range(1,len(par_str)):
                        if parole[j+l].find(par_str[l]) == -1:
                            chk = False
                            break
                    if chk:
                        value.append(parole[j+pos])
        return value




    def outline_str(self,stringa,linea,pos):
        value = []
        pos = pos-1
        chk = True
        par_str = string.split(stringa)
        for i in range(len(self.__file_cont)):
            parole = string.split(self.__file_cont[i])
            for j in range(len(parole)):
                if parole[j].find(par_str[0]) != -1:
                    if j+len(par_str) > len(parole):
                        break
                    for l in range(1,len(par_str)):
                        if parole[j+l].find(par_str[l]) == -1:
                            chk = False
                            break
                    if chk:
                        parole2 = string.split(self.__file_cont[i+linea])
                        value.append(parole2[pos])
        return value



#.............................................................#

# ofile

class ofile:

#  This class writes the file <filename>. It implements the following
#  methods:
#     pr             open the file with "write" attribute
#     outpr          write the content of the list <lista> in the format
#                            1     lista[0]
#                            2     lista[1]
#                            .       .
#                            .       .

#---------------#

    def __init__(self,filename):
            self.filename = filename
            

    def pr(self,stringa):
        try:
            self = open(self.filename,'w')
        except:
            print "I can not create file %s\n" % self.filename
            sys.stderr.write("Abnormal termination in ofile\n")
            sys.exit(1)
        self.write(stringa)
        

    def outpr(self,lista):
        try:
            self = open(self.filename,'w')
        except:
            print "I can not create file %s\n" % self.filename
            sys.stderr.write("Abnormal termination in ofile\n")
            sys.exit(1)
        for i in range(len(lista)):
            stringa = str(i+1) + "    " + lista[i] + "\n"
            self.write(stringa)
        self.close()
            
    
#-----------------------------------------------------------#    
#-----------------------------------------------------------#

#----------------------#
#      FUNCTIONS       #
#----------------------#

def line_arg():

# This function manages the command line options and the initialization
# of variables. It gives in output a list with the value of (in order)
# mnin_file,dynvar_file,hop_file,mnout_file,out_dir,num_cc

#---------------#

# initialize variables

    mnin_file = "mndo.inp"
    dynvar_file = "dynvar.in"
    hop_file = "hopping.out"
    mnout_file = "mn.out"
    outdir = "MD_data"
    num_cc = True

    opt_list = []


#  Read command line options
    clo = sys.argv
    

    j = 1
    while j < len(clo):
        op = clo[j]
        if op == "-n" or op == "-nonumCC":
            num_cc = False
            j = j + 1
            continue
        elif op == "--mndo-in":
            j = j + 1
            mnin_file = clo[j]
            j = j + 1
            continue
        elif op == "--dynvar":
            j = j + 1
            dynvar_file = clo[j]
            j = j + 1
            continue
        elif op == "--hop-file":
            j = j + 1
            hop_file = clo[j]
            j = j + 1
            continue
        elif op == "--mndo-out":
            j = j + 1
            mnout_file = clo[j]
            j = j + 1
            continue
        elif op == "-o" or op == "--out-dir":
            j = j + 1
            outdir = clo[j]
            j = j + 1
            continue
        elif op == "-h" or op == "--help":
            help()
            sys.exit(0)
        else:
            print "\n%s is not a valid option" % op
            print "Use -h or --help for help\n"
            sys.stderr.write("Abnormal termination in MDextr\n")
            sys.exit(1)


    opt_list.append(mnin_file)
    opt_list.append(dynvar_file)
    opt_list.append(hop_file)
    opt_list.append(mnout_file)
    opt_list.append(outdir)
    opt_list.append(num_cc)

    return opt_list

#.............................................................#


def help():

# this function prints the help 

    print
    print "  +----------------+"
    print "  | MDextr -- HELP |"
    print "  +----------------+"
    print
    print "MDextr extracts data from the output files \n"
    print "of a surface hopping run"
    print
    print "USAGE:   MDextr.py [options]"
    print "  options:"
    print "    --mndo-in <file>        MNDO input file name"
    print "                            (default: mndo.in)"
    print "    --dynvar <file>         dynamics input file name"
    print "                            (default: dynvar.in)"
    print "    --hop-file <file>       hopping file name"
    print "                            (default: hopping.out)"
    print "    --mndo-out <file>       MNDO output file name"
    print "                            (default: mndo.out)"
    print "    -o or --out-dir <name>  prefix for output directory name"
    print "                            (default: MD_data)"
    print "    -n or --nonumCC         do not extract numerical CC"
    print "                            (by default extracted if both"
    print "                             analytical and numerical couplings"
    print "                             have been computed)"
    print "    -h or --help            display this help"
    print

#-----------------------------------------------------------#    
#-----------------------------------------------------------#


#----------------------#
#     MAIN CODE        #
#----------------------#

# Read command line options
# and initialize variables

la = line_arg()

mnin_file = la[0]
dynvar_file = la[1]
hop_file = la[2]
mnout_file = la[3]
outdir = la[4]
num_cc = la[5]




# Header

print
print "           +----------------------+"
print "           |        MDextr        |"
print "           +----------------------+"
print



#.............................#
#
# read MNDO options
#

mnin = ifile(mnin_file)

if mnin.excod:
    
    # read NCIGRD
    tmp = mnin.inline_str('ncigrd',0)
    if tmp == []:
        tmp = mnin.inline_str('NCIGRD',0)
        if tmp == []:
            print "No keyword NCIGRD in MNDO input file!"
            sys.exit(2)
    tmp2 = string.split(tmp[0],'=')
    ncigrd = tmp2[1]
        


    # read iroot
    tmp = mnin.inline_str('iroot',0)
    if tmp == []:
        tmp = mnin.inline_str('IROOT',0)
        if tmp == []:
            print "No keyword IROOT in MNDO input file!"
            sys.exit(2)
    tmp2 = string.split(tmp[0],'=')
    iroot = tmp2[1]



# read iuvcd
    tmp = mnin.inline_str('iuvcd',0)
    if tmp == []:
        tmp = mnin.inline_str('IUVCD',0)
        if tmp == []:
            tmp = ["iuvcd=0"]
    tmp2 = string.split(tmp[0],'=')
    iuvcd = tmp2[1]

else:

    sys.stderr.write("Abnormal termination in ifile\n")
    sys.exit(1)

#.............................#


#.............................#
#
# read dynvar.in options
#

dynvarin = ifile(dynvar_file)

if dynvarin.excod:
    
# read IOUT
    tmp = dynvarin.inline_str('IOUT',2)
    if tmp == []:
        tmp = dynvarin.inline_str('iout',2)
        if tmp == []:
            print "No keyword IOUT in dynvar file!"
            print "Assumed IOUT=0\n"
            iout = 0
        else:
            pass
    else:
        tmp2 = tmp[0]
        ln = len(tmp2)
        iout = tmp2[0:ln-1]


# read NSTEP
    tmp = dynvarin.inline_str('NSTEP',2)
    if tmp == []:
        tmp = dynvarin.inline_str('nstep',2)
        if tmp == []:
            print "No keyword NSTEP in dynvar file!\n"
    tmp2 = tmp[0]
    ln = len(tmp2)
    nstep = tmp2[0:ln-1]



    if num_cc == True:
        
# read NUM_CC
        num_cc = False
        tmp = dynvarin.inline_str('NUM_CC',2)
        if tmp == []:
            tmp = dynvarin.inline_str('num_cc',2)
            if tmp == []:
                print "No keyword NUM_CC in dynvar file!"
                print "Assumed NUM_CC = F\n"
                tmp = "F"
        tmp2 = tmp[0]
        if tmp2 == "T,":
            num_cc = True


# read AN_CC
    an_cc = False
    tmp = dynvarin.inline_str('AN_CC',2)
    if tmp == []:
        tmp = dynvarin.inline_str('an_cc',2)
        if tmp == []:
            print "No keyword AN_CC in dynvar file!"
            print "Assumed AN_CC = F\n"
            tmp = "F"
    tmp2 = tmp[0]
    if tmp2 == "T,":
        an_cc = True

else:
    print "Assumed IOUT = 0"
    iout = 0
    print "Assumed NUM_CC = F"
    num_cc = False
    print "Assumed AN_CC = F"
    an_cc = False
    print
#.............................#



#.............................#
#
# read hopping file
#

hopout = ifile(hop_file)

if hopout.excod:
    
# read state
    print "Extracting: state\n"
    state = hopout.inline_str('state:',1)
#print state


# read energy
    if ncigrd == "2":
        print "Extracting: E1\n"
        E1 = hopout.outline_str('mdstep:',1,2)
        print "Extracting: E2\n"
        E2 = hopout.outline_str('mdstep:',1,3)
    elif ncigrd == "3":
        print "Extracting: E1\n"
        E1 = hopout.outline_str('mdstep:',1,2)
        print "Extracting: E2\n"    
        E2 = hopout.outline_str('mdstep:',1,3)
        print "Extracting: E3\n"    
        E3 = hopout.outline_str('mdstep:',1,4)


# read energy differences
    if ncigrd == "2":
        print "Extracting: E12\n"
        E12 = hopout.outline_str('differences',1,1)
    elif ncigrd == "3":
        print "Extracting: E12\n"    
        E12 = hopout.outline_str('differences',1,1)
        print "Extracting: E13\n"    
        E13 = hopout.outline_str('differences',2,1)
        print "Extracting: E23\n"   
        E23 = hopout.outline_str('differences',2,2)


# read coupling (analitical or numerical)
    if ncigrd == "2":
        print "Extracting: CC12\n"
        CC12 = hopout.outline_str('coupling',1,1)
    elif ncigrd == "3":
        print "Extracting: CC12\n"
        CC12 = hopout.outline_str('coupling',1,1)
        print "Extracting: CC13\n"
        CC13 = hopout.outline_str('coupling',2,1)
        print "Extracting: CC23\n"
        CC23 = hopout.outline_str('coupling',2,2)


# read population
    if ncigrd == "2":
        print "Extracting: pop1\n"
        pop1 = hopout.outline_str('population',1,1)
        print "Extracting: pop2\n"
        pop2 = hopout.outline_str('population',2,1)
    elif ncigrd == "3":
        print "Extracting: pop1\n"
        pop1 = hopout.outline_str('population',1,1)
        print "Extracting: pop2\n"
        pop2 = hopout.outline_str('population',2,1)
        print "Extracting: pop3\n"
        pop3 = hopout.outline_str('population',3,1)


# read probability
    if ncigrd == "2":
        print "Extracting: prob1\n"
        prob1 = hopout.outline_str('probability',1,2)
        print "Extracting: prob2\n"
        prob2 = hopout.outline_str('probability',2,2)
    elif ncigrd == "3":
        print "Extracting: prob1\n"
        prob1 = hopout.outline_str('probability',1,2)
        print "Extracting: prob2\n"
        prob2 = hopout.outline_str('probability',2,2)
        print "Extracting: prob3\n"
        prob3 = hopout.outline_str('probability',3,2)


# read random number
    print "Extracting: rnd_num\n"
    rnd = hopout.inline_str("rnd",2)

else:

    sys.stderr.write("Abnormal termination in ifile\n")
    sys.exit(1)   
#.............................#



#.............................#
#
# read MNDO output file
#


if num_cc and an_cc:

    outf = ifile(mnout_file)

    if outf.excod:
    
# read numerical nonadiabatic coupling
        print "Extracting: num_CC12\n"
        num_CC12 = outf.outline_str("Numerical non-adiabatic",2,2)
        if ncigrd == "3":
            print "Extracting: num_CC13\n"
            num_CC13 = outf.outline_str("Numerical non-adiabatic",2,3)
            print "Extracting: num_CC23\n" 
            num_CC23 = outf.outline_str("Numerical non-adiabatic",3,2)

    else:
        print "Numerical coupling will be not extracted\n"
        num_cc = False
#.............................#     
    




#.............................#
#
# output
#

# prepare output directory
test_dir = outdir
i = 0
while os.path.isdir(test_dir):
    i = i + 1    
    test_dir = outdir + str(i)
outdir = test_dir
os.mkdir(outdir)

tmpoutdir = "./" + outdir
print
print "Data will be saved in: %s\n" %tmpoutdir



# change to output directory
os.chdir(outdir)


# write state
out = ofile("state.dat")
out.outpr(state)


# write energy
out = ofile("E1.dat")
out.outpr(E1)
out = ofile("E2.dat")
out.outpr(E2)
if ncigrd == "3":
    out = ofile("E3.dat")
    out.outpr(E3)


# write energy differences
out = ofile("E12.dat")
out.outpr(E12)
if ncigrd == "3":
    out = ofile("E13.dat")
    out.outpr(E13)
    out = ofile("E23.dat")
    out.outpr(E23)


# write coupling
out = ofile("CC12.dat")
out.outpr(CC12)
if ncigrd == "3":
    out = ofile("CC13.dat")
    out.outpr(CC13)
    out = ofile("CC23.dat")
    out.outpr(CC23)


# write population
out = ofile("pop1.dat")
out.outpr(pop1)
out = ofile("pop2.dat")
out.outpr(pop2)
if ncigrd == "3":
    out = ofile("pop3.dat")
    out.outpr(pop3)


# write probability
out = ofile("prob1.dat")
out.outpr(prob1)
out = ofile("prob2.dat")
out.outpr(prob2)
if ncigrd == "3":
    out = ofile("prob3.dat")
    out.outpr(prob3)


# write random number
out = ofile("rnd_num.dat")
out.outpr(rnd)


# write numerical nonadiabatic coupling
if num_cc and an_cc:
    out = ofile("num_CC12.dat")
    out.outpr(num_CC12)
    if ncigrd == "3":
        out = ofile("num_CC13.dat")
        out.outpr(num_CC13)
        out = ofile("num_CC23.dat")
        out.outpr(num_CC23)

