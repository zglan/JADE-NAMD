#! /usr/bin/env python

import os
import sys
import shutil
import numpy as np

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/btools/")

# my module
from xyzTraj import xyzTraj
from bMolShape import bMolShape
from bRotation import bRotation
from general_time import general_time

#
# @ 2015-07-29 pm
# @ dulikai
# @ qibebt
#
# #
#

#
## 
# notes:
# calculate rmsd value in comparision with the ref. geom.
# normally, the first frame
#
#
# Based on general_time
# you only need to define init. and prep_once.
class rmsd_time(general_time):
    def __init__(self):
        """
        some pre-defined parameters
        """
        self.results = {}
        self.status = {}
        self.params = {}
        self.params['filename'] = "myrmsd.dat"
        self.params['resfilename'] = "rmsd_aver.dat"
        self.params['mydir'] = "tmpdirs"

        self.params['n_col'] = 2
        self.params['trajfile'] = 'traj_time.out'
        
        self.params['ndx_flag'] = 1
        return


    def get_cmd(self):
        """
        obtain parameter from command line
        """
        # fragment index
        line = raw_input("enter the index range  <i.e. 1-5,9,11>: \n >")
        self.params['frg_ndx1'] = line.strip()

        print "default column of dataset: ", self.params['n_col']
        print "@ Press Enter to use default value. ^_&"
        line = raw_input("column of the dataset:  \n > ")
        if line.strip() != "":
            self.params['n_col'] = int(line)   
        
        line = raw_input("atom index start from: [default: 1] \n > ")
        if line.strip() != "":
            self.params['ndx_flag'] = int(line)

        print "enter the filename (xyz format): "
        line = raw_input(" [default: traj_time.out]: \n >")
        if line.strip() != "":
            self.params['trajfile'] = line.strip()

        return


    def prep_once(self, flag = 1):
        """
        rmsd
        """
        frg_ndx1 = self.params['frg_ndx1']
        fname = self.params['trajfile']
        
        traj = xyzTraj()
        traj.read_it(filename = fname)

        # shape obj.
        shape = bMolShape()

        # traj. frg.
        # reset model to the first frame
        traj.reset_model()
        frg1 = traj.fragment(frg_ndx1, flag)

        # reset model to the first frame
        traj.reset_model()
        # start analysis
        i = 0; angle = []
        while True:
            # for each frame
            frg2 = traj.fragment(frg_ndx1, flag)
            d = shape.get_rmsd(frg1, frg2)
            i += 1; 
            angle.append([i, d])

            if traj.next_model() == 0:
                break

        filename = self.params['filename']
        fp = open(filename, "w")
        print >>fp, "# ID RMSD"
        print >>fp, "# unit: Angstrom"
        print >>fp, "#", frg_ndx1
        for d in angle:
            print >>fp, "%10d%15.8f" % \
                  (d[0], d[1])
        
        fp.close()
            
        return angle            

             
if __name__ == "__main__":
    print "\n"
    print "------------------- versin 1.0a -------------------"
    print "Calculate complex geometric parameters of one fragment."
    print ""
    print "----------------------------------------------------"
    
    pe = rmsd_time()
    pe.get_cmd()
    pe.get_status()
    pe.prep_traj()
    pe.read_traj()
    pe.aver_traj()
    pe.dump()
        

