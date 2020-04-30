#! /usr/bin/env python

#
# linear interpolation within two or several geometries.
#

import os
import numpy as np


class bInterpolation():
    """
    modified Shepard Interpolation 
    """
    def __init__(self):
        self.dataset = {}

        self.params = {}

        self.params['n_state'] = 3
        return


    def normal_weight(self, q, qklist, i):
        """
        normalized weight..
        """
        # $ w_i(\xi_i) = \frac{v_i(\xi)}{\Sum_j{v_j(\xi)}} $
        # w = \Sum_j{v_j(\xi)}
        # w_i = v_i / w
        #
        # v_i
        qi = qklist[i]
        vi = self.free_weight(q, qi)
        # w sum
        w = 0
        for qj in qklist:
            w += self.free_weight(q, qj)
        # w_i
        wi = vi / w
 
        return wi

        
    def general_dist(self, q, qk):
        """
        general distance, between q and q(k)
        may be you can see JCP, 112, 2718 (2000); 
        doi: 10.1063/1.480846
        http://scitation.aip.org/content/aip/journal/jcp/112/6/10.1063/1.480846
        $ d_k(q) = \Sum_i^N{(q_i-q_i^k)^2} $
        """
        vq = (q - qk)  # * np.array([1,1,1,1,40])
        dq = np.linalg.norm(vq)
        
        return dq

        
    def free_weight(self, q, qk):
        """
        un-normalized weight function
        """
        dn = self.general_dist(q, qk)

        v = 1.0 / (dn*dn*dn*dn*dn)

        return v


    def read_vars(self, filename = "vars.dat"):
        """ read variable """
        # suppose the first line is the total group of internal coord.
        fp = open(filename, "r")
        space = []
        while True:
            line = fp.readline()
            if line.strip() == "":
                break
            coord = [float(x) for x in line.split()]
            n_coord = len(coord)
            space.append(coord)

        n_space = len(space)
        
        self.dataset['space'] = space
        self.dataset['n_space'] = n_space

        return

    def read_potential(self, filename = "potential.dat"):
        """ read in energy data """
        n_state = self.params['n_state']
        
        fp = open(filename, "r")
        potential = []
        while True:
            line = fp.readline()
            if line.strip() == "":
                break
            ene = [float(x) for x in line.split()]
            n_ene = len(ene)
            potential.append(ene)

        n_potential = len(potential)
        self.dataset['potential'] = potential
        self.dataset['n_potential'] = n_potential

        return

    def dump_it(self, filename = "dump.dat"):
        """ dump data for temp use """
        #
        space = self.dataset['space']
        n_space = self.dataset['n_space']
        potential = self.dataset['potential']
        n_potential = self.dataset['n_potential']
        # vars
        n_vars = n_space
        if n_vars > n_potential:
            n_vars = n_potential

        n_coord = len(space[0])
        n_ene = len(potential[0])

        #
        fp = open(filename, "w")
        print >>fp, "%12d%12d%12d" % (n_vars, n_coord, n_ene)
        print >>fp, "# UNITS DEGREE ANGSTROM HARTREE"
        for i in xrange(n_vars):

            for x in space[i]:
                print >>fp, "%15.8f" % x,
            for p in potential[i]:
                print >>fp, "%20.12f" % p,
            print >>fp, ""
        fp.close()

        self.dataset['n_vars'] = n_vars

        return

    def build_eMat(self):
        """
        build up eMat..
        row: each state; column: each data-point
        """
        #
        pot = self.dataset['potential']
        n_vars = self.dataset['n_vars']
        n_state = len(pot[0])

        eMat = np.zeros((n_vars, n_state))

        for i in xrange(n_vars):
            for j in xrange(n_state):
                eMat[i][j] = pot[i][j]

        return eMat

    def build_wVec(self, point):
        """
        a point in space, to estimate weight function.
        point : usually presented by a series of internal coord.
        """
        space = self.dataset['space']
        n_vars = self.dataset['n_vars']

        wVec = np.zeros(n_vars)
        
        # w sum
        wsum = 0
        for i in xrange(n_vars):
            wVec[i] = self.free_weight(point, space[i])
            wsum += wVec[i]
            
        # v_i
        for i in xrange(n_vars):
            wVec[i] /= wsum
            #if wVec[i] > 0.01:
            #    print wVec[i]

        return wVec


    def get_energy(self, point):
        """
        calc. energy of a point
        """
        eMat = self.build_eMat()
        wVec = self.build_wVec(point)
        #print eMat
        energy = np.dot(wVec, eMat)

        #print energy

        return energy


    def get_pes(self):
        """
        map out pes
        """
        b_min = 1.9; b_max = 2.0; b_delta = 0.1
        b_bin = int((b_max - b_min) / b_delta)
        d_min = 60.0; d_max = 120.0; d_delta = 5.0
        d_bin = int((d_max - d_min) / d_delta)
        
        pes = []
        
        for i in xrange(b_bin):
            for j in xrange(d_bin):
                b = b_min + b_delta * i
                d = (d_min + d_delta * j) / 180.0 * np.pi
                q = np.array([b, b, b, b, d])

                ene = self.get_energy(q)
                pes.append([b, q, ene])
                
                print b, d/np.pi*180.0, ene[0], ene[1], ene[2], ene[3]
                              
        return pes

    
       
# Main Program
if __name__ == "__main__":
    worker = bInterpolation()

    worker.read_vars(filename = "vars.dat")
    worker.read_potential(filename = "potential.dat")
    worker.dump_it()
    worker.build_eMat()

    #q = np.array([2.0, 2.0, 2.0, 2.0, 1.57])

    
    #worker.build_wVec(q)

    #worker.get_energy(q)

    worker.get_pes()


