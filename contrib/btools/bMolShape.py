#! /usr/bin/env python

import numpy as np
import re
# my module
from xyzStruct import xyzStruct

#
# this script will man. a fragment of the molecule.
# based on geometric concept, i.e. line, plane, sphere, etc.
#
# routines:
# * get_angle(self, v1, v2)
# - return the angle between two vector. a list with [rad, deg]
# * make_plane(self, pA, pB, pC)
# - return an planar equation (A,B,C,D). suppose known three point pA pB pC
# * fit_plane(self, mol)
# - return an planar equation (A,B,C,D). known a series of point coord.

class bMolShape():
    def __init__(self):
        """ mol shape man. """
        print "note: the atom index (0 or 1)"
        
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
                for i in xrange(a, b+1):
                    frg_list.append(i-flag)
            else:
                frg_list.append(int(ir)-flag)
        return frg_list
        
        
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

    
    def make_plane(self, pA, pB, pC):
        """
        known: A, B, C: three points
        ax+by+cz+d=0
        v_norm = (a,b,c) = AB \cross AC
        d = -v_n \cdot A
        make plane require three points only
        return (A B C D) of the plane equation.
        note: i cannot remember anything, haha, so see this explanation
        http://keisan.casio.com/exec/system/1223596129
        """
        AB = pB - pA
        AC = pC - pA
        norm = np.cross(AB, AC) # (a,b,c)
        d = - np.dot(norm, pA)
        return np.append(norm, d)

    def fit_plane(self, mol):
        """
        best fit plane from a list of atoms position
        useful for planar molecular fragments
        Av = 0 
        note:
        matrix A can be obtain by outer product of (x, y, z, 1)
        and v = (A, B, C, D)
        http://www.ilovematlab.cn/thread-220252-1-1.html        
        """
        geom = mol['geom']
        n_atom = mol['n_atom']
        G = np.zeros((4,4))
        for i in xrange(n_atom):
            g = geom[i][0:3];
            g.append(1.0)
            c = np.array(g)
            G = G + np.outer(c, c)
        u, s, v = np.linalg.svd(G)
        # print v[-1]
        return v[-1]
        

    
    def plane_angle(self, frg1, frg2):
        """
        angle between two fragment plane..
        """
        v1 = self.fit_plane(frg1)

        v2 = self.fit_plane(frg2)
    
        t = self.get_angle(v1, v2)
        
        return t
 

    def outofplane_dist(self, frg1):
        """
        measure the degree of out-of-plane
        in contrast to Ax+By+Cz+D = 0 planar equation.
        Der = \Sigma{Ax_i+By_i+Cz_i+D}
        """
        v1 = self.fit_plane(frg1)
        # V M ?
        geom = frg1['geom']
        n_atom = frg1['n_atom']
        der = 0.0
        for coord in geom:
            c = np.array([coord[0], coord[1], coord[2], 1.0])
            der += abs(np.dot(v1, c))
        der /= n_atom

        return der 


    # cog
    def get_cog(self, mol):
        """
        geometric center of a fragment
        """
        #
        geom = mol['geom']
        n_atom = mol['n_atom']
        
        cog = np.zeros(3)
        for g in geom:
            cog += np.array(g)
        cog = cog / n_atom

        return cog

    def get_rmsd(self, frg1, frg2):
        """ calculate rmsd val. """
        v1 = self.fit_plane(frg1)
        # V M ?
        geom1 = frg1['geom']
        geom2 = frg2['geom']
        n_atom = frg1['n_atom']
        n_atom2 = frg2['n_atom']
        if n_atom != n_atom2:
            print "get_rmsd : unequal n_atom. Error"
            sys.exit(1)
            
        der = 0.0
        for i in xrange(n_atom):
            c1 = np.array(geom1[i][0:3])
            c2 = np.array(geom2[i][0:3])
            xc = c1 - c2
            der += np.dot(xc, xc)
        d = np.sqrt(der/n_atom)

        return d

    #
    # routine: get radius or diameter
    def getSphereRadius(self, mol):
        """Return the radius of fullerene-like molecules and et al..
        may be a fragment
        """
        n_atom = mol['n_atom']
        geom = mol['geom']
        # geometric center
        averCoord = np.zeros(3)
        for i in xrange(n_atom):
            averCoord += geom[i] 
        averCoord /= n_atom

        # rad
        radius = 0.0
        dist = [0.0 for i in xrange(n_atom)]
        for i in xrange(n_atom):
            vdiff = geom[i] - averCoord
            dist[i] = np.linalg.norm(vdiff)
            radius += dist[i]
        radius /= n_atom

        min_dist = min(dist)
        max_dist = max(dist)
        c = np.sqrt(max_dist*max_dist - min_dist*min_dist)
        e_ratio = c / max_dist
        # print "%12.6f%12.6f%12.6f" % (min_dist, max_dist, e_ratio)
        return radius, e_ratio

# Main         
if __name__ == "__main__":
    shape = bMolShape()
    
    xyz = xyzMole()
    xyz.read_it(filename="./cu.xyz")
    # xyz.print_it()
    # xyz.dump_it()
    
    frg_ndx = "0-17, 38, 40"
    frg1 = xyz.fragment(frg_ndx)
    # xyz.print_frg()
    
    frg_ndx = "20-37, 39, 41, 42-48"
    frg2 = xyz.fragment(frg_ndx)
    # xyz.print_frg()
    
    shape.plane_angle(frg1, frg2)


    # m = molPlane()
    # pA = np.array([-2.758366107940674, -0.511352002620697, -0.511256992816925])
    # pB = np.array([-1.5573660135269165, -0.9552469849586487, -0.9550809860229492])
    # pC = np.array([-1.557610034942627, 0.955062985420227, 0.9552770256996155])
    # x = m.make_plane(pA, pB, pC)

    # pA = np.array([2.7585020065307617, -0.5111259818077087, 0.5111380219459534])
    # pB = np.array([1.5573569536209106, 0.9553229808807373, -0.9550409913063049])
    # pC = np.array([1.5576189756393433, -0.9550920128822327, 0.9552119970321655])
    # y = m.make_plane(pA, pB, pC)
    # t = m.get_angle(x, y)
    # print t
