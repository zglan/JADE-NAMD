#! /usr/bin/env python
import os
import shutil
import numpy as np




class cut_coord():
    def __init__(self,filename,cutlist,cut_atom):
        self.filename = filename
        self.cutlist = cutlist
        self.cutatom = cut_atom
        self.dim = {}
        self.model = []
    def __rd_xyz_nmol(self):
         """ read how many mol in the xyz file"""
         filename = self.filename

         fpin = open(filename, "r")
         nmol = 0
         # read number of atom
         line = fpin.readline()
         while line.strip() != "":
             natom = int(line.split()[0])
             line = fpin.readline()
             # read a mol
             for i in range(natom):
                 line = fpin.readline()
             nmol = nmol + 1

             line = fpin.readline()
         fpin.close()

         self.dim['n_mol'] = nmol

         return

    def read_xyz(self):
        """ read in xyz format in ang """
        n_mol = self.dim['n_mol']

        filename = self.filename
        fpin = open(filename, "r")

        model = []
        for i in xrange(n_mol):
            # number of atom, 
            line = fpin.readline()
            natom = int(line)
            line = fpin.readline()[0:-1]
            molinfo = {'n_atom': natom, 'title':line}

            atom = []
            for j in range(natom):
                line = fpin.readline()
                rec = line.split()
                atomname, x, y, z= rec[0:4]
                record = {'name': atomname, 'coord': [float(x),float(y),float(z)]}
                atom.append(record)
            mol = {'info':molinfo, 'atoms':atom}
            model.append(mol)
        fpin.close()

        self.model = model
        return
    def write_xyz(self):
        self.__rd_xyz_nmol()
        self.read_xyz()
        nmol = self.dim['n_mol']
        model = self.model
        savefile = self.filename + '_aftercut'
        if os.path.isfile(savefile):
            os.remove(savefile)

        """get the a_num after cut"""
        mol = model[0]
        molinfo = mol['info']
        atom = mol['atoms']
        natom = int(molinfo['n_atom'])
        n_atom_new = natom
        for i in range(natom):
            if i+1 in self.cutlist or atom[i]['name'] in self.cutatom:
                n_atom_new = n_atom_new -1

        """write the coord afercut  into a new file named filename_aftercut """ 
        fp = open(savefile,'a')
        for i in range(nmol):
            mol=model[i]
            molinfo = mol['info']
            atom = mol['atoms']
            print >> fp, n_atom_new
            print >> fp, molinfo['title']
            natom = int(molinfo['n_atom'])
            for i in range(natom):
                if i+1 in self.cutlist:
                    continue
                name = atom[i]['name']
                if name in self.cutatom:
                    continue
                coord = atom[i]['coord']
                print >> fp,  "%s%15.8f%15.8f%15.8f" % (name,
                                                      coord[0],
                                                      coord[1],
                                                      coord[2])
        fp.close() 
       



if __name__ == '__main__':
    filename = 'input.xyz'
    cut_list = []
    cut_atom = ['H','h']
    jobs = cut_coord(filename,cut_list,cut_atom)
    jobs.write_xyz()
