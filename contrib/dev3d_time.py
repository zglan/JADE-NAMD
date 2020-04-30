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
# #
#
# originally, designed for
# deviations from the ideal tetrahedral geometry of copper complex
# purpose:
# suppose a planar molecule or fragment or ligand, we want to measure
# its derivation from
# a specific direction x, y, z
# i.e. wagging, rocking and flattening motion
# see the definition in  A. Lavie-Cambot et. al. Coord. Chem. Rev. 2008, 252, 2572
#
# the overall distortion from the ideal tetrahedral geometry (zeta) is considered as
# the contribution from x y z plane (theta),
# that is
# $\zeta = \frac{90+\theta_x)(90+\theta_y)(90+\theta_z)}{180^3}
#
## 
# notes:
# 3d deviations from the ideal tetrahedral geometry of copper complex
#
#
# Based on general_time
# you only need to define init. and prep_once.
class dev3d_time(general_time):
    def __init__(self):
        """
        some pre-defined parameters
        """
        self.results = {}
        self.status = {}
        self.params = {}
        self.params['filename'] = "mydev3d.dat"
        self.params['resfilename'] = "dev3d_aver.dat"
        self.params['mydir'] = "tmpdirs"

        self.params['n_col'] = 5
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

        line = raw_input("enter index for original point   <i.e. 1-5,9>: \n >")
        self.params['frg_ndx2'] = line.strip()

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
        cog1 = shape.get_cog(frg1)
        frg2 = traj.fragment(frg_ndx2, flag)
        cog2 = shape.get_cog(frg2)
        vx0 = cog1 - cog2
        # norm vector
        vz = shape.fit_plane(frg1)
        
        vx_z = (-vz[3] - vz[0] * vx0[0] - vz[1] * vx0[1]) / vz[2]
        vx = np.array([vx0[0], vx0[1], vx_z])

        # build three plane, namely, xy, xz, yz.
        vy = np.cross(vx[0:3], vz[0:3])

        # define first case of xy projection
        vpz = self.vec_in_plane(vx0, vz)
        # define first case of xz projection
        vpy = self.vec_in_plane(vx0, vy)
        # define first case of yz projection
        vpx = self.vec_in_plane(vx0, vx)
        #
        # reset model to the first frame
        traj.reset_model()
        # start analysis
        i = 0; angle = []
        while True:
            frg1 = traj.fragment(frg_ndx1, flag)
            cog1 = shape.get_cog(frg1)
            frg2 = traj.fragment(frg_ndx2, flag)
            cog2 = shape.get_cog(frg2)
            ux0 = cog1 - cog2            
            # print vx, ux
            # norm vector
            uz = shape.fit_plane(frg1)
            # build three plane, namely, xy, xz, yz.
            uy = np.cross(vx[0:3], vz[0:3])
            # project on to specific plane
            upz = self.vec_in_plane(ux0, vz)
            upy = self.vec_in_plane(ux0, vy)
            upx = self.vec_in_plane(ux0, vx)
            # measure and compare with the first frame
            # see coord. chem. rev. 2008, 252, 2572
            degx = self.get_angle(vpx, upx) # flattening
            degy = self.get_angle(vpy, upy) # rolling
            degz = self.get_angle(vpz, upz) # rocking
 
            degs = (90.+degx) * (90.+degy) * (90.+degz) / (180*180*180);
            i += 1; 
            angle.append([i, degs, degx, degy, degz])

            if traj.next_model() == 0:
                break

        filename = self.params['filename']
        fp = open(filename, "w")
        print >>fp, "# ID sum flattening rolling rocking"
        print >>fp, "# unit: degree"
        print >>fp, "#"
        for d in angle:
            print >>fp, "%10d%15.8f%15.8f%15.8f%15.8f" % \
                  (d[0], d[1], d[2], d[3], d[4])
        
        fp.close()
            
        return angle            

             
if __name__ == "__main__":
    print "\n"
    print "------------------- versin 1.0a -------------------"
    print "Calculate complex geometric parameters of one fragment."
    print ""
    print "----------------------------------------------------"
    
    pe = dev3d_time()
    pe.get_cmd()
    pe.get_status()
    pe.prep_traj()
    pe.read_traj()
    pe.aver_traj()
    pe.dump()
        

