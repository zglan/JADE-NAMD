#! /usr/bin/env python

import os
import numpy as np
import sys

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/btools/")

# my module
from xyzStruct import xyzStruct
from xyzTraj import xyzTraj
from bMolShape import bMolShape

# suppose a planar molecular 
# and calc. out of plane degree.
#

class oop_worker():
    def __init__(self):
        """ """
        self.params = {}
        # command line
        line = raw_input("enter the index range  <i.e. 1-5,9,11>: \n >")
        self.params['frg_ndx1'] = line.strip()
        
        self.params['trajfile'] = 'traj_time.out'
        line = raw_input("enter the filename (xyz format) \
        [default: traj_time.out]: \n > ")
        if line.strip() != "":
            self.params['trajfile'] = line.strip()
    
        return

        
    def get_traj(self, flag = 1):
        """
        process traj of xyz format
        """
        fname = self.params['trajfile']
        frg_ndx1 = self.params['frg_ndx1']
        
        # traj. info
        traj = xyzTraj()
        traj.read_it(filename = fname)
        # det. shape    
        shape = bMolShape()
        dist = []; i = 0;
        while True:
            frg1 = traj.fragment(frg_ndx1, flag)
            t = shape.outofplane_dist(frg1)
            i += 1
            dist.append([i, t])
            if traj.next_model() == 0:
                break
        return dist


# Main Program 
if __name__ == "__main__":
    worker = oop_worker()
    print "\n"
    print "------------------- versin 1.0a -------------------"
    print "Calculate complex molecule geometric parameters."
    print ""
    print "----------------------------------------------------"
    ndx_flag = 1
 
    line = raw_input("Atom index start from 0 or 1 [default: 1]: \n > ")
    if line.strip() != "":
        ndx_flag = int(line)
    
    fp = open("outofplane.dat", "w")
    print >>fp, "# ID  RAD DEG"
    t = worker.get_traj(flag = ndx_flag)
    for d in t:
        print "%10d%12.3f" % (d[0], d[1])
        print >>fp, "%10d%12.3f" % (d[0], d[1])
 
    fp.close()
    


    



        
