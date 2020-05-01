#! /usr/bin/env python

#
# collect each trajectory data into one file
#

import os

class bCollection():
    def __init__(self):


        return


    def readfile(self, filename = "1.dat", n_jump = 0): 
        fin = open(filename)
        for i in xrange(n_jump):
            line = fin.readline()
        strinfo = fin.read() 
        fin.close()
        return strinfo
    

    def combine(self, n_traj, n_jump = 0):
        """
        combine $i.dat files together
        """
        combfile = "collection.dat"
        fp = open(combfile, "w")
        for i in xrange(1, n_traj+1):
            filename = str(i) + ".dat"
            if not os.path.isfile(filename):
                continue
            print "JOB ID %d" % i
            strinfo = self.readfile(filename, n_jump)
            print >>fp, "%s" % strinfo,
        fp.close()
        return


if __name__ == "__main__":
    c = bCollection()
    n_traj = 100

    line = raw_input("enter the directory:[default:.] \n > ")
    mydir = line.strip()
    if mydir == "":
        mydir = './'
    line = raw_input("number of line to jump:[default:0] \n > ")
    if line.strip() == "":
        n_jump = 0
    n_jump = int(line)
    
    os.chdir(mydir)
    print os.getcwd()

    
    
    c.combine(n_traj, n_jump)





    
