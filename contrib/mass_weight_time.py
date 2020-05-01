#! /usr/bin/env python2.6

import os
import sys
import shutil

# you only need to define init. and prep_once.

class mass_weight_time():
    def __init__(self):
        """
        some pre-defined parameters
        """
        self.params = {}
        self.params['filename'] = "mass_weight_time.dat"

        self.params['trajfile'] = 'all.xyz'
        
        self.params['atom_number'] = 1
        self.params['geom_number'] = 1
        self.params['structure'] = {}
        self.params['mass_weighted'] = []
        return


    def get_cmd(self):
        """
        obtain parameter from command line
        """
        print "enter the filename (xyz format): "
        line = raw_input(" [default: all.xyz]: \n >")
        if line.strip() != "":
            self.params['trajfile'] = line.strip()

        print "enter ther number of atoms"
        line = raw_input("number of atoms:\n > ")
        if line.strip() != "":
            self.params['atom_number'] = int(line)

        return


    def read_ngeom(self):

        fname = self.params['trajfile']
        n_atom = self.params['atom_number']

        n_line = 0
        file = open(fname,"r")
        for line in file:
           n_line += 1
        file.close()
       
        n_geom = int (n_line / (n_atom + 2))
        self.params['geom_number'] = n_geom

        return

    def read_first_geom(self):

        fname = self.params['trajfile']
        n_atom = self.params['atom_number']

        file = open(fname,"r")

        line = file.readline()
        line = file.readline()

        structure = {}
 
        for i_line in range(n_atom):
            line =  file.readline()
            structure[i_line] = line.split()

        file.close()
       
        self.params['structure'] = structure  

        mass_total = 0.0
        mass_weighted = []

        for i_atom in range(n_atom):
            mass_weighted.append(0.0)

        for i_atom in range(n_atom):

            if str(structure[i_atom][0]) == 'C':
               structure[i_atom][0] = 6
            if (structure[i_atom][0] == 'N'):
               structure[i_atom][0] = 7
            if (structure[i_atom][0] == 'O'):
               structure[i_atom][0] = 8
            if (structure[i_atom][0] == 'H'):
               structure[i_atom][0] = 1
            if (structure[i_atom][0] == 'S'):
               structure[i_atom][0] = 16

            mass_total = mass_total + float(structure[i_atom][0])


        for i_atom in range(n_atom):
            mass_weighted[i_atom] = float(structure[i_atom][0]) / mass_total

        self.params['mass_weighted'] = mass_weighted

        return

    def read_all_geom(self):
        n_geom = self.params['geom_number']
        fname = self.params['trajfile']

        file = open(fname,"r")

        for i_geom in range(n_geom):

           self.read_once_geom(i_geom,file)

        file.close()
        return

    def read_once_geom(self,i_geom,file):

        n_atom = self.params['atom_number']
        structure_first = self.params['structure']
        mass_weighted = self.params['mass_weighted']

        line = file.readline()
        line = file.readline()

        structure_current = {}
        
        distance_all =  0.0 
        for i_line in range(n_atom):
            line =  file.readline()
            structure_current[i_line] = line.split()

            a = mass_weighted[i_line]
            b=  (float(structure_current[i_line][1])-float(structure_first[i_line][1]))**2 \
                + (float(structure_current[i_line][2])-float(structure_first[i_line][2]))**2 \
                + (float(structure_current[i_line][3])-float(structure_first[i_line][3]))**2

            distance = b*a
            distance_all = distance_all + distance

        distance_all = distance_all**0.5

        print distance_all



        return        

             
if __name__ == "__main__":
    pe = mass_weight_time()
    pe.get_cmd()
    pe.read_ngeom()
    pe.read_first_geom()
    pe.read_all_geom()
