#! /usr/bin/env python


import os
import shutil
       
import sys

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/btools/")

import numpy as np
# my module
from xyzStruct import xyzStruct
from xyzTraj import xyzTraj
from bMolEnergy import bMolEnergy

#
# @ 2015-07-21
#

class ke_worker():
    def __init__(self):
        """
        params
        """
        self.params = {}
        # command line parameters
        self.params['filename'] = "vel_time.out"
        self.params['frg_ndx1'] = ""
        line = raw_input("enter the filename (xyz format) [default: vel_time.out]: \n > ")
        if line.strip() != "":
            self.params['filename'] = line.strip()
        line = raw_input("enter the index range  <i.e. 1-5,9,11>: \n >")
        if line.strip() != "":
            self.params['frg_ndx1'] = line.strip()
        else:
            print "cannot be empty for index range"
            exit(1)

        return

         
    def get_kinc(self, flag = 1):
        """
        process traj of xyz file
        """
        fname = self.params['filename']
        frg_ndx1 = self.params['frg_ndx1']
        
        # traj. info
        traj = xyzTraj()
        traj.read_it(filename = fname)
        #
        kinc = []; i = 0;
        myenergy = bMolEnergy()
        while True:
            frg1 = traj.fragment(frg_ndx1, flag)
            ekin = myenergy.get_ekin(frg1)
            mom = myenergy.get_mom(frg1)
            i += 1; ene = [i, ekin]; ene.extend(mom)
            kinc.append(ene)
            if traj.next_model() == 0:
                break
        return kinc


# Main Program 
if __name__ == "__main__":
    print "\n"
    print "------------------- versin 1.0a -------------------"
    print "Calculate kinetic energy of one fragment."
    print ""
    print "----------------------------------------------------"
    ndx_flag = 1
    line = raw_input("atom index start from: [default: 1] \n > ")
    if line.strip() != "":
        ndx_flag = int(line)
    #...
    ke = ke_worker()
    ene = ke.get_kinc(flag = ndx_flag)
    
    fp = open("ekin.dat", "w")
    print >>fp, "# ID kinetic"
    print >>fp, "#"
    print >>fp, "#"
    for d in ene:
        print "%10d%15.8f%15.8f%15.8f%15.8f" % \
              (d[0], d[1], d[2], d[3], d[4])
        print >>fp, "%10d%15.8f%15.8f%15.8f%15.8f" % \
              (d[0], d[1], d[2], d[3], d[4])
        
    fp.close()
    
    
        
    
