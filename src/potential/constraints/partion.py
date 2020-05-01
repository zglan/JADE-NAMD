#! /usr/bin/env python

import sys
import os
import copy
import shutil
import numpy as np

sys.path.append("../tools/")
import tools


#

class manStruct():
    """
    man. an molecular system
    """
    def __init__(self):
        self.files = {'interface': 'interface.json', \
                      'compare': 'compare.json',     \
                      'gradient': 'qm_gradient.dat', \
                      'dimension': 'dimension.json'}
        self.vars = {}
        self.vars['force_constant'] = 1.0e5

        return

    def load_coord(self):
        """
        load two set of coord. of the system
        """
        oldsetfile = self.files['compare']
        
        self.vars['geom'] = tools.load_data(oldsetfile)
        
        return

    def read_struct(self):
        """
        read struct in xyz format
        """
        fp = open("struct_xyz.in", "r")
        line = fp.readline()
        n_atom = int(line.strip())

        return
    
        

    def center(self):
        """ geom. center of the system """
        mol = self.vars['']['mol']
        n_atom = mol['natom']
        atoms = mol['atoms']
        center = np.zeros(3)
        for i in xrange(n_atom):
            coord = np.array(atoms[i]['coord'])
            center += coord / n_atom
        self.vars['center'] = center
        print center
        return
        


if __name__ == "__main__":
    m = manStruct()
    m.load_coord()
    
    m.center()
