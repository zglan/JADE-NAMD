#! /usr/bin/env python

import os
import numpy as np
import sys

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/btools/")

# my module
from xyzStruct import xyzStruct
from xyzTraj import xyzTraj
from bMolShape import bMolShape

#
#

def get_dihe(flag = 1):
    """
    process traj of xyz file
    """
    line = raw_input("enter the index range  <i.e. 1-5,9,11>: \n >")
    frg_ndx1 = line.strip()
    line = raw_input("enter the index range <i.e. 20-37, 39, 41, 42-48>: \n >")
    frg_ndx2 = line.strip()
    
    line = raw_input("enter the filename (xyz format): \n > ")
    fname = line.strip()

    # traj. info
    traj = xyzTraj()
    traj.read_it(filename = fname)
    # det. shape    
    shape = bMolShape()
    dihe = []
    while True:
        frg1 = traj.fragment(frg_ndx1, flag)
        frg2 = traj.fragment(frg_ndx2, flag)
        t = shape.plane_angle(frg1, frg2)
        dihe.append(t)
        if traj.next_model() == 0:
            break
    return dihe


def __get_radius(self, flag = 1):
    """
    calculate the radius of a ball like mole/frag.
    """
    # vars
    line = raw_input("enter the index range  <i.e. 1-5,9,11>: \n >")
    frg_ndx1 = line.strip()

    line = raw_input("enter the filename (xyz format) [default: traj_time.out]: \n > ")
    if line.strip() != "":
        fname = line.strip()
    else:
        fname = "traj_time.out"
     
    # traj. info
    traj = xyzTraj()
    traj.read_it(filename = fname)
    # det. shape    
    shape = bMolShape()
    rad = []
    while True:
        frg1 = traj.fragment(frg_ndx1, flag)
        t = shape.getSphereRadius(frg1)
        rad.append(t)
        if traj.next_model() == 0:
            break
    #
    jobfilename = "mytmp.dat"
    fp = open(jobfilename, "w")
    print >>fp, "# ball radius e-ratio"
    print >>fp, "#", frg_ndx1
    print >>fp, "#"
    i = 0
    for d in rad:
        i += 1
        print >>fp, "%10d%12.3f%12.3f" % (i, d[0], d[1])
    fp.close()          

    return

    
    
    
def get_struct(flag = 1):
    """
    process on structure of xyz file
    """
    line = raw_input("enter the filename (xyz format): \n > ")
    fname = line.strip()
    line = raw_input("enter the index range (from zero) <i.e. 1-5,9,11>: \n >")
    frg_ndx1 = line.strip()
    line = raw_input("enter the index range (from zero) <i.e. 20-37, 39, 41, 42-48>: \n >")
    frg_ndx2 = line.strip()
    
    # mol. info.
    mol = xyzStruct()

    if 'gjf' in fname:
        mol.read_gjf(filename = fname)
    else:
        mol.read_it(filename = fname)

    frg1 = mol.fragment(frg_ndx1, flag)
    frg2 = mol.fragment(frg_ndx2, flag)
    
    # det. shape    
    shape = bMolShape()
    t = shape.plane_angle(frg1, frg2)

    return t
        

        
# Main Program 
if __name__ == "__main__":
    print "\n"
    print "------------------- versin 1.0a -------------------"
    print "Calculate complex molecule geometric parameters."
    print ""
    print "----------------------------------------------------"
    ndx_flag = 1
    file_type = 1
    line = raw_input("Atom index start from 0 or 1 [default: 1]: \n > ")
    if line.strip() != "":
        ndx_flag = int(line)
    line = raw_input("Select 1: traj or 2: struct [default: 1]: \n > ")
    if line.strip() != "":
        file_type = int(line)
    
    fp = open("dihe.dat", "w")
    print >>fp, "# ID  RAD DEG"
    if file_type == 1:  # traj
        t = get_dihe(flag = ndx_flag)
        i = 0
        for d in t:
            i += 1
            print "%10d%12.3f%12.3f" % (i, d[1], d[0])
            print >>fp, "%10d%12.3f%12.3f" % (i, d[1], d[0])
            
    elif file_type == 2:    # struct
        t = get_struct(flag = ndx_flag)
        print "%10d%12.3f%12.3f" % (0, t[1], t[0])
        print >>fp, "%10d%12.3f%12.3f" % (0, t[1], t[0])
    else:
        print "NOTHING DONE. NO SUCH OPTION."
        exit(1)
    
    fp.close()
    
    
    
# 20-38,40,42-49
# 1-18,39,41,50-57

