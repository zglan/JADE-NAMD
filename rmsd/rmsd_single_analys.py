import os
from os import system
import pybel
import numpy as np
import shutil
import time
import rmsd_traj_xsli_xy3 as rmsd
#import mds_result_group_rmds as md
'''
To run this script, you should install openbabel and its python library firstly. 
In linux, the installation command is:
apt-get (or yum) install openbabel (or openbabel.x86_64)
apt-get (or yum) install python-openbabel (or python-openbabel.x86_64)
'''

class split_coord() :
    def __init__(self):
        self.dim = {}
        self.model = []
        self.num = 0
        self.index = 0

    def __rd_xyz_nmol(self,filename):
        """ read how many mol in the xyz file"""
        filename 

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


    def read_xyz(self,filename):
        """ read in xyz format in ang """
        n_mol = self.dim['n_mol']

        filename 
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


    def write_xyz(self,id):
        """ write xyz in angstrom unit """
        filename = "all_sample.xyz_" + str(id+1)
        self.num = self.num +1
        fp = open(filename, "w")
        mol = self.model[id]
        molinfo = mol['info']
        atoms = mol['atoms']
        n_atom = molinfo['n_atom']
        title = molinfo['title']
        print >>fp, "%d" % (n_atom)
        print >>fp, "%s" % title
        for rec in atoms:
            coord = rec['coord']
            atom_name = rec['name']
            print >>fp, "%s%15.8f%15.8f%15.8f" % (atom_name,
                                                      coord[0],
                                                      coord[1],
                                                      coord[2])
        fp.close()

        return

    def write_all_samples(self,filename):
        curr_dir = os.getcwd()
        work_dir = curr_dir + '/all'
        os.chdir(work_dir)
        self.__rd_xyz_nmol(filename)
        self.read_xyz(filename)
        job_dir = work_dir + '/job_dir'
        command1 = 'rm -rf ' + job_dir
        command2 = 'mkdir ' + job_dir
        os.system(command1)
        os.system(command2)
        os.chdir(job_dir)
        for i in range(self.dim['n_mol']):
            self.write_xyz(i)
        os.chdir(curr_dir)
    def get_rmsd(self):
        nu = self.dim['n_mol']
        curr_dir = os.getcwd()
        work_dir = curr_dir + '/all'
        job_dir = work_dir + '/job_dir'
        rmsd.make_second(nu,job_dir)
        os.chdir(curr_dir)
    def get_min_idex(self):
        nu = self.dim['n_mol']
        curr_dir = os.getcwd()
        work_dir = curr_dir + '/all'
        job_dir = work_dir + '/job_dir'
        os.chdir(job_dir)
        xx = np.loadtxt('rmsd_all.dat')
        sumlist = []
        for i in range(nu):
            sumlist.append(sum(xx[i,:]))
        print sumlist
        mina = min(sumlist)
        print mina
        index = sumlist.index(mina) + 1
        print index
        self.index = index
        os.chdir(curr_dir)
        return index #    def group_rmsd(self):
#        index = self.index
#        jobs = md.rmsd_group()
#        jobs.read_num(index)
    def make():
        
        jobs = split_coord()
        jobs.write_all_samples()
        jobs.get_rmsd()
        jobs.get_min_idex()
            
        

        
"""if __name__ == "__main__":

    jobs = split_coord()
    jobs.write_all_samples()
    jobs.get_rmsd()
    jobs.get_min_idex()
#    jobs.group_rmsd()
"""
          
def make(filename):
        
    jobs = split_coord()
    jobs.write_all_samples(filename)
    jobs.get_rmsd()
    a = jobs.get_min_idex()
    return a


if     __name__ == "__main__":
    file_name = 'geom_rmsd_5_7.xyz'
    a=make(file_name)
    print a





















