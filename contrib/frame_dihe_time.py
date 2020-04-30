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
# @ 2015-07-22 pm
# @ dulikai
# @ qibebt
#
#
#
#
#
# Based on general_time
# you only need to define init. and prep_once.
class frame_dihe_time(general_time):
    def __init__(self):
        """
        some pre-defined parameters
        """
        self.results = {}
        self.status = {}
        self.params = {}
        self.params['filename'] = "mytmp.dat"
        self.params['resfilename'] = "fd_aver.dat"
        self.params['mydir'] = "tmpdirs"

        self.params['n_col'] = 3
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

        #line = raw_input("enter index for original point   <i.e. 1-5,9>: \n >")
        #self.params['frg_ndx2'] = line.strip()

        self.params['frg_ndx2'] = self.params['frg_ndx1']

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


    def get_angle(self, vpx, upx):
        """ vec angle """
        dupx = np.linalg.norm(upx)
        dvpx = np.linalg.norm(vpx)
        dotx = np.dot(vpx, upx)

        val = dotx/dvpx/dupx
        if val > 1.0:
            print "arccos encounter val > 1.0, maybe slightly %20.15e" % (val-1.0)
            val = 1.0
        elif val < -1.0:
            print "arccos encounter val < -1.0, maybe slightly %20.15e" % (val+1.0)
            val = -1.0

        deg = np.arccos(val) * 180 / np.pi
       
        return deg


    def vec_in_plane(self, v1, vn):
        """
        find the projected 3d vector in a plane
        """
        vn = vn[0:3]; v1 = v1[0:3];
        vn0 = vn / np.linalg.norm(vn)
        h = np.dot(vn0, v1)
        vh = h * vn0
        vp = v1 - vh

        return vp


    def prep_once(self, flag = 1):
        """
        obtain coordinate system based on frg list
        see coord. chem. rev. 2008, 252, 2572
        doi:10.1016/j.ccr.2008.03.013
        """
        frg_ndx1 = self.params['frg_ndx1']
        frg_ndx2 = self.params['frg_ndx2']
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
        traj.next_model()
        # start analysis
        i = 0; angle = []
        while True:
            frg2 = traj.fragment(frg_ndx2, flag)
            t = shape.plane_angle(frg1, frg2)

            deg = t[1]; rad = t[0]
            if t[1] > 90.0:
                rad = np.pi - t[0]
                deg = 180.0 - t[1]

            i += 1; 
            angle.append([i, rad, deg])

            if traj.next_model() == 0:
                break

        filename = self.params['filename']
        fp = open(filename, "w")
        print >>fp, "# ID frame dihedral"
        print >>fp, "# unit: degree"
        print >>fp, "#"
        for d in angle:
            print >>fp, "%10d%15.8f%15.8f" % \
                  (d[0], d[1], d[2])
        
        fp.close()
            
        return angle            

             
if __name__ == "__main__":
    print "\n"
    print "------------------- versin 1.0a -------------------"
    print "Calculate complex geometric parameters of one fragment."
    print ""
    print "----------------------------------------------------"
    
    pe = frame_dihe_time()
    pe.get_cmd()
    pe.get_status()
    pe.prep_traj()
    pe.read_traj()
    pe.aver_traj()
    pe.dump()
        

