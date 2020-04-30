#! /usr/bin/env python
import sys
import numpy as np

sys.path.append('./')

# my module
from xyzStruct import xyzStruct
from xyzTraj import xyzTraj
from bMolShape import bMolShape


def process_traj():
    """
    process traj of xyz file
    """
    line = raw_input("enter the filename (xyz format): \n > ")
    fname = line.strip()
    line = raw_input("enter the index range (from zero) <i.e. 1-5,9,11>: \n >")
    frg_ndx1 = line.strip()
    line = raw_input("enter the index range (from zero) <i.e. 20-37, 39, 41, 42-48>: \n >")
    frg_ndx2 = line.strip()
    
    # traj. info
    traj = xyzTraj()
    traj.read_it(filename = fname)
    # det. shape    
    shape = bMolShape()
    while True:
        frg1 = traj.fragment(frg_ndx1)
        frg2 = traj.fragment(frg_ndx2)
        t = shape.plane_angle(frg1, frg2)
        print t
        if traj.next_model() == 0:
            break
    return t
    
def process_struct():
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
    mol.read_it(filename = fname)
    frg1 = mol.fragment(frg_ndx1)
    frg2 = mol.fragment(frg_ndx2)
    
    # det. shape    
    shape = bMolShape()
    t = shape.plane_angle(frg1, frg2)

    return t
        
                
if __name__ == "__main__":
    # t = process_struct()
    t = process_traj()
    print t[1]
    
    