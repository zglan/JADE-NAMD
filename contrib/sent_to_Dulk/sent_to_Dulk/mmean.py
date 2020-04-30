#!/usr/bin/python

#----------------------#
#      IMPORTS         #
#----------------------#

import sys
import string
from math import sqrt
import os

#-----------------------------------------------------------#

#----------------------#
#      CLASSES         #
#----------------------#

class data_set:

# this class defines a single data set


    # INITIALIZATION
    def __init__(self,filen):

        # read data
        try:
            data_file = open(filen,"r")
            print "processing: %s\n" % filen
            raw_data = data_file.readlines()
            data_file.close()

            # save length of the set
            self.num = len(raw_data)

            # discard index and save data
            self.data=[]
            for i in range(int(self.num)):
                linea = raw_data[i]
                tmp_dat = string.split(linea)
                self.data.append(tmp_dat[1])
        except:
            print
            print "I can not open file %s\n" % filen
            sys.stderr.write("Abnormal termination in mmean\n")
            sys.exit(1)



    # FIND THE MAXIMUM VALUE OF THE SET
    def max_val(self):
        macs = float(self.data[0])
        for i in range(1,int(self.num)):
            tmp = float(self.data[i])
            if tmp > macs:
                macs = tmp
        self.massimo = macs





    # FIND THE MINIMUM VALUE OF THE SET
    def min_val(self):
        mini = float(self.data[0])
        for i in range(1,int(self.num)):
            tmp = float(self.data[i])
            if tmp < mini:
                mini = tmp
        self.minimo = mini





    # FIND THE AVERAGE VALUE OF THE SET
    def ave_val(self):
        tot = 0.0
        for i in range(int(self.num)):
            tot = tot + float(self.data[i])
        self.average = float(tot) / float(self.num)




    # FIND THE VARIANCE OF THE SET
      # Note that in general the data are correlated!!!
    def get_sigma(self,bins,opt):

        # use the binning method
        if opt == 1:
            # get number of blocks <n_blocks>
            n_blocks = int(float(self.num)/float(bins))
            #get block's averages <bin_av>
            bin_av = []
            for i in range(1,n_blocks+1):
                tot = 0.0
                for j in range(bins):
                    k = (i-1)*bins + j
                    tot = tot + float(self.data[k])
                    tot = tot / float(bins)
                bin_av.append(tot)
            # get total average <average>
            tot = 0.0
            for j in range(n_blocks):
                tot = tot + float(bin_av[j])
            average = tot / float(n_blocks)
            # compute blocks variance 
            tot = 0.0
            for j in range(n_blocks):
                tot = tot + (float(bin_av[j])-float(average))*\
                      (float(bin_av[j])-float(average))
            self.variance = tot/float(n_blocks-1)

        # use the iterative method [JCP 91, 461]
        elif opt == 2:
            # inizialize old variance
            old_vari = 0.0
            #initialize dat
            dat = []
            for i in range(self.num):
                dat.append(self.data[i])
            #initialize nunmber of blocks
            N = self.num
            #cycle
            while N > 4:
                # compute number of blocks
                nn = int(N/2)
                # compute blocks average
                av = []
                for i in range(nn):
                    k = i*2
                    tmp = float(dat[k])+float(dat[k+1])
                    tmp = float(tmp)/2.0
                    av.append(tmp)
                # compute total average
                tmp = 0.0
                for i in range(nn):
                   tmp = tmp + float(av[i])
                average = float(tmp)/float(nn)
                # compute variance
                tmp = 0.0
                for i in range(nn):
                    tmp = tmp + (float(av[i])-float(average))*\
                                 (float(av[i])-float(average))
                vari = float(tmp)/float(nn-1)
                # check for convergency
                ##print "vari"
                #print vari
                # save old variance
                old_vari = vari
                # update number of blocks
                N = nn
                # update data
                dat = []
                for i in range(nn):
                    dat.append(av[i])
            self.variance = float(vari)




#............................................#            


class ensamble:
    
# This class defines an ensamble of data sets


    # INITIALIZATION OF THE ENSAMBLE
    
    def __init__(self,file_name):

        # read the file list
        try:
            lfile = open(file_name,"r")
            dflist = lfile.readlines()
            lfile.close()
        except:
            print
            print "I can not open file %s\n" % data_file
            sys.stderr.write("Abnormal termination in mmean\n")
            sys.exit(1)

        # save the number of sets
        self.nsets = len(dflist)

        # read all data sets
        self.dati=[]
        for i in range(len(dflist)):
            leng = len(dflist[i])
            filen = dflist[i][0:leng-1]
            self.dati.append(data_set(filen))

        # check that all data sets have the same length
        a = self.dati[0]
        N_old = a.num
        for i in range(1,len(dflist)):
            a = self.dati[i]
            N = a.num
            if N != N_old:
                print
                print "ERROR! Data set do not have"
                print "the same number of lines"
                sys.stderr.write("Abnormal termination in mmean\n")
                sys.exit(2)
            


            
    # FIND THE AVERAGE VALUE OVER ALL SETS LINE BY LINE
    # AND THE VARIANCE (if var = True)
    def ens_aver(self,var):
        # inizialization
        self.en_average = []
        if var:
            self.en_variance = []
        n = self.dati[0].num
        # cycle over all lines
        for i in range(n):
            tmp = 0.0
            for j in range(int(self.nsets)):
                a = self.dati[j]
                tmp = tmp + float(a.data[i])
            tmp = tmp/int(self.nsets)
            self.en_average.append(tmp)
            # compute variance
            if var:
                tmp = 0.0
                for j in range(int(self.nsets)):
                    a = self.dati[j]
                    tmp = tmp + (float(a.data[i])-float(self.en_average[i]))*\
                          (float(a.data[i])-float(self.en_average[i]))
                tmp = float(tmp)/float(self.nsets)
                self.en_variance.append(tmp)



            
    # FIND THE AVERAGE OCCUPATION OVER ALL SETS LINE BY LINE
    # AND VARIANCE [ = occ*(1-occ)]
    def ens_occ(self):
        # initialization
        self.en_occ = []
        self.en_variance = []
        n = self.dati[0].num
        # find number of states
        nstat = 0
        for i in range(int(self.nsets)):
            a = self.dati[i]
            a.max_val()
            if int(a.massimo) > int(int(nstat)):
                nstat = a.massimo
            self.nst = nstat
        #find occupations        
        for i in range(n):
            #initialize occupation vector
            occ = []
            for l in range(int(nstat)):
                occ.append(0)
            # find occupation
            for j in range(int(self.nsets)):
                a = self.dati[j]
                for k in range(int(nstat)):
                    if int(float(a.data[i])) == k+1:
                        occ[k] = occ[k] + 1
            tmp = []
            tmp2 = []
            for k in range(int(nstat)):
                tmp.append(float(occ[k])/float(self.nsets))
                tmp2.append(float(tmp[k])*(1.0-float(tmp[k])))
            self.en_occ.append(tmp)
            self.en_variance.append(tmp2)
            
            

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
    single_file = False
    infile = "file.in"
    data_file = "data.ls"
    state = False
    serror = False
    sd_opt = 2
    bin = 2
    do_max = False
    do_min = False
    out_file = "data.mean"
    off = 0

    

    opt_list = []

#  Read command line options
    clo = sys.argv

    j = 1
    while j < len(clo):
        op = clo[j]
        if op == "-f" or op == "--file":
            single_file = True
            j = j + 1
            infile = clo[j]
            j = j + 1
            continue
        elif op == "-l" or op == "--list":
            j = j + 1
            data_file = clo[j]
            j = j + 1
            continue            
        elif op == "-s" or op == "--state":
            state = True
            j = j + 1
            continue
        elif op == "--s-error" or op == "--bin":
            serror = True
            if op == "--bin":
                sd_opt = 1
                j = j + 1
                bin = clo[j]
            else:
                sd_opt = 2
            j = j + 1
            continue
        elif op == "--max":
            do_max = True
            j = j + 1
            continue
        elif op == "--min":
            do_min = True
            j = j + 1
            continue
        elif op == "-o" or op == "--out-file":
            j = j + 1
            out_file = clo[j]
            j = j + 1
            continue
        elif op == "-a" or op == "--add-offset":
            j = j + 1
            off = clo[j]
            j = j + 1
            continue
        elif op == "-h" or op == "--help":
            help()
            sys.exit(0)
        else:
            print "\n%s is not a valid option" % op
            print "Use -h or --help for help\n"
            print
            sys.stderr.write("Abnormal termination in mmean\n")
            sys.exit(1)


    # check if options are meaningfull
    if single_file:
        if state:
            print
            print "The average state occupation can not be"
            print "calculated in the single file mode!"
            print
            sys.stderr.write("Abnormal termination in mmean\n")
            sys.exit(2)
    else:
        if do_max or do_min:
            print
            print "--max and --min options can only be used in"
            print "list mode"
            print
            sys.stderr.write("Abnormal termination in mmean\n")
            sys.exit(2)
    



    opt_list.append(single_file)
    opt_list.append(infile)
    opt_list.append(data_file)    
    opt_list.append(state)
    opt_list.append(serror)
    opt_list.append(sd_opt)
    opt_list.append(bin)
    opt_list.append(do_max)
    opt_list.append(do_min)
    opt_list.append(out_file)
    opt_list.append(off)
    

    return opt_list

#.............................................................#


def help():

    print
    print "  +----------------+"
    print "  |  mmean - HELP  |"
    print "  +----------------+"
    print
    print "mmean is a script to compute average and standard"
    print "deviation on MD files. It can work with single files"
    print "to compute expetation values from a single MD run"
    print "or with multiple files (default) to compute averages"
    print "on several trajectories. In multiple files mode it"
    print "can be used also to compute the average occupation of"
    print "states (-s or --state option) after a surface hopping"
    print "calculation."
    print
    print "USAGE:    mmean.py [options]"
    print "  options:"
    print "   -f or --file <file>      the single file mode is"
    print "                            used and file <file> is"
    print "                            used as source of data."
    print "                            If not specified the multiple"
    print "                            file mode is used (default)."
    print "   -l or --list <file>      Name of the file containing"
    print "                            the list of files to process."
    print "                            (default: data.ls)"
    print "   -s or --state            Average occupation of states"
    print "                            is computed instead of"
    print "                            average value."
    print "                            (default: average value computed)"
    print "   --s-error                The standard error is also"
    print "                            computed. For single file mode"
    print "                            this is done with the iterative"
    print "                            method of JCP 91, 461."
    print "                            (default: not performed)"
    print "   --bin <int>              The standard error is also"
    print "                            computed. For multiple state"
    print "                            mode it is identical to --s-error."
    print "                            For single state mode the binning"
    print "                            method is used with bin dimension"
    print "                            = <int>."
    print "                            (default: not performed)"
    print "   --max                    Find the maximum value of the set."
    print "                            Available only in single file mode."
    print "                            (default: not performed)"
    print "   --min                    Find the minimum value of the set."
    print "                            Available only in single file mode."
    print "                            (default: not performed)"
    print "   -o or --out-file <file>  Output file name. Only for multiple"
    print "                            files mode. In single file mode the"
    print "                            output is directed to standard"
    print "                            output."
    print "                            (default: data.mean)"
    print "   -a or --add-offset <int> Add an offset to the index in the"
    print "                            output file. Only for multiple"
    print "                            files mode"
    print "                            (default: 0)"
    print "   -h or --help             display this help."
    print
    print
    print " INDEX FILE FORMAT"
    print
    print "In multiple files mode the files to be read must be specified"
    print "in a separate file (eventually with the complete path) with"
    print "the following format:"
    print "file1"
    print "file2"
    print "  ."
    print "  ."
    print "  ."
    print
    
    
#-----------------------------------------------------------#
#-----------------------------------------------------------#


#----------------------#
#     MAIN CODE        #
#----------------------#

# Read command line options
# and initialize variables

la = line_arg()

single_file = la[0]
infile = la[1]
data_file = la[2]
state = la[3]
serror = la[4]
sd_opt = la[5]
bin = la[6]
do_max = la[7]
do_min = la[8]
out_file = la[9]
off = la[10]



print single_file
print infile
print serror
print sd_opt
print bin
print do_max
print do_min

# Header

print
print "           +---------------------+"
print "           |        mmean        |"
print "           +---------------------+"
print


# SINGLE FILE

if single_file:
    # read data set
    ds1 = data_set(infile)

    # compute average
    ds1.ave_val()

    # compute variance
    if serror:
        ds1.get_sigma(int(bin),int(sd_opt))
    
    # find maximum
    if do_max:
        ds1.max_val()

    # find minimum
    if do_min:
        ds1.min_val()

    # output
    print
    print "Number of points: %6d" % ds1.num
    print "Average: %13.5f" % ds1.average
    if serror:
        tmp = float(ds1.variance)/float(ds1.num)
        tmp = sqrt(float(tmp))
        print "Standard error: %13.5f" % tmp
    if do_max:
        print "Max: %13.5f" % ds1.massimo
    if do_min:
        print "Min: %13.5f" %ds1.minimo
    

# ENSAMBLE

else:

    # read all files
    e1 = ensamble(data_file)

    # find average (occupation)
    if state:
        e1.ens_occ()
    else:
        if serror:
            i_var = True
        else:
            i_var = False
        e1.ens_aver(i_var)

    # output
    print
    print "Number of sets: %6d" % e1.nsets
    print "Number of points per set: %6d" % e1.dati[0].num

    # prepare output file name
    test_file = out_file
    i = 0
    while os.path.isfile(test_file):
        i = i + 1
        test_file = out_file + str(i)
    out_file = test_file

    print "Output file: %s" % out_file

    # open output file
    try:
        ofile = open(out_file,"w")
    except:
        print
        print "I can not create file %s\n" % out_file
        sys.stderr.write("Abnormal termination in mmean\n")
        sys.exit(1)


    # write output
    if state:
        for i in range(int(e1.nst)):   # loop over states
            j = int(i) + 1 
            ofile.write("#state %d \n" % j)
            for k in range(int(e1.dati[0].num)): # loop over lines
                tmp = e1.en_occ[k]
                if serror:
                    tmp2 = e1.en_variance[k]
                    tmp3 = float(tmp2[i])/float(e1.nsets)
                    tmp3 = sqrt(tmp3)
                    ofile.write("%6d   %13.5f   %13.5f \n" \
                            %(int(k)+1+int(off),float(tmp[i]),tmp3))
                else:
                    ofile.write("%6d   %13.5f \n" \
                                %(int(k)+1+int(off),float(tmp[i])))
            ofile.write("\n")
            
    else:
        for i in range(int(e1.dati[0].num)): # loop over lines
            if serror:
                tmp = e1.en_variance[i]
                tmp = float(tmp)/float(e1.nsets)
                tmp = sqrt(float(tmp))
                ofile.write("%6d   %13.5f   %13.5f \n" \
                            %(int(i)+1+int(off),float(e1.en_average[i]),float(tmp)))
            else:
                ofile.write("%6d   %13.5f \n" \
                            %(int(i)+1+int(off),float(e1.en_average[i])))
        


print




        
