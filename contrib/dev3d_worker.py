#! /usr/bin/env python

import os
import sys
import numpy as np

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/btools/")

# my module
from xyzTraj import xyzTraj
from bMolShape import bMolShape
from bRotation import bRotation

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
#

class dev3d_worker():
    def __init__(self):
        self.params = {}
        self.params['trajfile'] = 'traj_time.out'

        self.get_cmd()
        
        return

    def get_cmd(self):
        """
        obtain parameter from command line
        """
        line = raw_input("enter the filename (xyz format): \n \
        [default: traj_time.out]: \n > ")
        if line.strip() != "":
            self.params['trajfile'] = line.strip()
        line = raw_input("enter the index range  <i.e. 1-5,9,11>: \n >")
        self.params['frg_ndx1'] = line.strip()

        line = raw_input("enter index for original center  <i.e. 1-5,9>: \n >")
        self.params['frg_ndx2'] = line.strip()
 
        return

    def vec_in_plane(self, v1, vn):
        """
        find the projected vector in a plane
        """
        vn = vn[0:3]; v1 = v1[0:3];
        vn0 = vn / np.linalg.norm(vn)
        h = np.dot(vn0, v1)
        vh = h * vn0
        vp = v1 - vh

        return vp


    def get_traj(self, flag = 1):
        """
        obtain coordinate system based on frg list
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
            degx = self.get_angle(vpx, upx) # flattening
            degy = self.get_angle(vpy, upy) # rolling
            degz = self.get_angle(vpz, upz) # rocking
 
            degs = (90+degx) * (90+degy) * (90+degz) / (180*180*180);
            i += 1; 
            angle.append([i, degs, degx, degy, degz])

            if traj.next_model() == 0:
                break
            
        return angle            

    def get_angle(self, vpx, upx):
        """ vec angle """
        dupx = np.linalg.norm(upx)
        dvpx = np.linalg.norm(vpx)
        dotx = np.dot(vpx, upx)

        deg = np.arccos(dotx/dvpx/dupx) * 180 / np.pi
        
        return deg

        
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
    worker = dev3d_worker()
    angle = worker.get_traj(flag = ndx_flag)
    
    fp = open("distorsion.dat", "w")
    print >>fp, "# ID sum flattening rolling rocking"
    print >>fp, "#"
    print >>fp, "#"
    for d in angle:
        print "%10d%15.8f%15.8f%15.8f%15.8f" % \
              (d[0], d[1], d[2], d[3], d[4])
        print >>fp, "%10d%15.8f%15.8f%15.8f%15.8f" % \
              (d[0], d[1], d[2], d[3], d[4])
        
    fp.close()
    

