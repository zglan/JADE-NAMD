#! /usr/bin/env python

import numpy as np
import re

from xyzMole import xyzMole


# http://stackoverflow.com/questions/10900141/fast-plane-fitting-to-many-points
class molPlane():
    def __init__(self):
        """ mol plane """
        print "note: the atom index 0 or 1"
        
        return

    def ext_frg_ndx(frg_ndx, flag = 0):
        """
        extend it in to actual list
        [0-17, 38, 40]
        """
        frg_list = []
        pat = re.compile("([0-9]+)-([0-9]+)")
        r = frg_ndx.split(',')
        for ir in r:
            m = pat.search(ir)
            if m is not None:
                a, b = [int(x) for x in m.group(1,2)]
                for i in xrange(a, b+1)
                    frg_list.append(i-flag)
            else:
                frg_list.append(int(ir)-flag)
        return frg_list
        
        
    def groups(self, frg_tbl):
        """
        group fraction of the molecule into different fragments
        """
        # for frg_ndx in frg_tbl:
        return

        
        
    def read_xyz(self, filename = "cu.xyz"):
        """
        read in xyz format structure in angstrom unit
        """
        fp = open("cu.xyz", "r")
        # read number of atom
        line = fpin.readline().strip()  
        # check the end of file
        if line == "":
            print("Fail to read xyz file!!")
            exit(1)
        n_atom = int(line.split()[0])        
        title = fpin.readline().strip()
        geom = []
        atom_name = []
        # read a mole
        for i in xrange(n_atom):
            line = fpin.readline()
            name, x, y, z= line.split()[0:4]            
            coord = [float(x),float(y),float(z)]
            atom_name.append(name)
            geom.append(coord)
        mol = {'title':title, 'n_atom': n_atom, 'geom':geom, 'name': atom_name}
        return mol            


    def make_plane(self, pA, pB, pC):
        """
        http://keisan.casio.com/exec/system/1223596129
        known: A, B, C: three points
        ax+by+cz+d=0
        v_norm = (a,b,c) = AB \cross AC
        d = -v_n \cdot A
        """
        AB = pB - pA
        AC = pC - pA
        norm = np.cross(AB, AC) # (a,b,c)
        d = - np.dot(norm, pA)
        return np.append(norm, d)

    def get_angle(self, v1, v2):
        """
        angle between two vector
        x = v1*v2/|v1||v2|)
        """
        vi = v1[0:3]; vj = v2[0:3]
        vi = vi / np.linalg.norm(vi)
        vj = vj / np.linalg.norm(vj)
        axis = np.cross(vi, vj)
        if np.linalg.norm(axis) < 1.0e-15:
            print "vector i \cross j is zero !!!", vi, vj
            axis = np.array([0., 0., 1.])
            theta = 0.0
        else:
            costheta = np.dot(vi, vj)
            theta = np.arccos(costheta)
        return theta, theta * 180.0/np.pi

    
#plane = bRotation.make_plane(vertices[0], vertices[1], vertices[2])





if __name__ == "__main__":
    m = molPlane()
    pA = np.array([-2.758366107940674, -0.511352002620697, -0.511256992816925])
    pB = np.array([-1.5573660135269165, -0.9552469849586487, -0.9550809860229492])
    pC = np.array([-1.557610034942627, 0.955062985420227, 0.9552770256996155])
    x = m.make_plane(pA, pB, pC)
    #print x

    pA = np.array([2.7585020065307617, -0.5111259818077087, 0.5111380219459534])
    pB = np.array([1.5573569536209106, 0.9553229808807373, -0.9550409913063049])
    pC = np.array([1.5576189756393433, -0.9550920128822327, 0.9552119970321655])
    y = m.make_plane(pA, pB, pC)
    #print x
    t = m.get_angle(x, y)
    print t
