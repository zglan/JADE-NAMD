#! /usr/bin/env python

import numpy as np
import re
# my module
from xyzStruct import xyzStruct

#
# this script will man. a fragment of the molecule.
# based on energy concept, i.e. kinetic, momentum, etc.
#


class bMolEnergy():
    dataset = {
         'H':  1.00790000 , 'HE':  4.00260000 , 'LI':  6.94100000 , 
         'BE':  9.01220000 , 'B':  10.81100000 , 'C':  12.01070000 , 
         'N':  14.00670000 , 'O':  15.99940000 , 'F':  18.99840000 , 
         'NE':  20.17970000 , 'NA':  22.98970000 , 'MG':  24.30500000 , 
         'AL':  26.98150000 , 'SI':  28.08550000 , 'P':  30.97380000 , 
         'S':  32.06500000 , 'CL':  35.45300000 , 'AR':  39.94800000 , 
         'K':  39.09830000 , 'CA':  40.07800000 , 'SC':  44.95590000 , 
         'TI':  47.86700000 , 'V':  50.94150000 , 'CR':  51.99610000 , 
         'MN':  54.93800000 , 'FE':  55.84500000 , 'CO':  58.93320000 , 
         'NI':  58.69340000 , 'CU':  63.54600000 , 'ZN':  65.39000000 , 
         'GA':  69.72300000 , 'GE':  72.64000000 , 'AS':  74.92160000 , 
         'SE':  78.96000000 , 'BR':  79.90400000 , 'KR':  83.80000000 , 
         'RB':  85.46780000 , 'SR':  87.62000000 , 'Y':  88.90590000 , 
         'ZR':  91.22400000 , 'NB':  92.90640000 , 'MO':  95.94000000 , 
         'TC':  98.00000000 , 'RU':  101.07000000 , 'RH':  102.90550000 , 
         'PD':  106.42000000 , 'AG':  107.86820000 , 'CD':  112.41100000 , 
         'IN':  114.81800000 , 'SN':  118.71000000 , 'SB':  121.76000000 , 
         'TE':  127.60000000 , 'I':  126.90450000 , 'XE':  131.29300000 , 
         'CS':  132.90550000 , 'BA':  137.32700000 , 'LA':  138.90550000 , 
         'CE':  140.11600000 , 'PR':  140.90770000 , 'ND':  144.24000000 , 
         'PM':  145.00000000 , 'SM':  150.36000000 , 'EU':  151.96400000 , 
         'GD':  157.25000000 , 'TB':  158.92530000 , 'DY':  162.50000000 , 
         'HO':  164.93030000 , 'ER':  167.25900000 , 'TM':  168.93420000 , 
         'YB':  173.04000000 , 'LU':  174.96700000 , 'HF':  178.49000000 , 
         'TA':  180.94790000 , 'W':  183.84000000 , 'RE':  186.20700000 , 
         'OS':  190.23000000 , 'IR':  192.21700000 , 'PT':  195.07800000 , 
         'AU':  196.96650000 , 'HG':  200.59000000 , 'TL':  204.38330000 , 
         'PB':  207.20000000 , 'BI':  208.98040000 , 'PO':  209.00000000 , 
         'AT':  210.00000000 , 'RN':  222.00000000 , 'FR':  223.00000000 , 
         'RA':  226.00000000 , 'AC':  227.00000000 , 'TH':  232.03810000 , 
         'PA':  231.03590000 , 'U':  238.02890000 , 'NP':  237.00000000 , 
         'PU':  244.00000000 , 'AM':  243.00000000 , 'CM':  247.00000000 , 
         'BK':  247.00000000 , 'CF':  251.00000000 , 'ES':  252.00000000 , 
         'FM':  257.00000000 , 'MD':  258.00000000 , 'NO':  259.00000000 , 
         'LR':  262.00000000 , 'RF':  261.00000000 , 'DB':  262.00000000 , 
         'SG':  266.00000000 , 'BH':  264.00000000 , 'HS':  277.00000000 , 
         'MT':  268.00000000
         }
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


   
    def get_mass(self, name='H'):
        """
        dump atomic mass
        """
        tname = name.upper()
        mass = self.dataset[tname]
        return mass



    def get_ekin(self, mol):
        """
        calculate kinetic energy of a fragment.
        here, mol. include
        """
        geom = mol['geom']
        name = mol['name']
        n_atom = mol['n_atom']

        ekin = 0.0
        for i in xrange(n_atom):
            tname = name[i]
            mass = self.get_mass(tname)
            vel = geom[i]
            v2 = np.dot(vel, vel)
            ekin += mass * v2 * 0.5
            
        return ekin


    def get_mom(self, mol):
        """
        kinetic momentum.
        here, mol. include
        """
        geom = mol['geom']
        name = mol['name']
        n_atom = mol['n_atom']

        mom = np.zeros(3)
        for i in xrange(n_atom):
            tname = name[i]
            mass = self.get_mass(tname)
            vel = np.array(geom[i])
            mom += mass * vel
            
        return mom
        

 



# Main         
if __name__ == "__main__":
    shape = bMolEnergy()
    
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
