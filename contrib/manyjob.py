#! /usr/bin/python2

import os
import shutil
# run many jobs.

class manyjobs:
    def __init__(self):
        """ default """
        self.files = {}
        self.dirs = {}
        self.files['xyz'] = "x_Q_au.dat"
        self.files['jobxyz'] = "stru_xyz.in"
        self.dirs['example'] = "MOLPRO_EXAM"
        self.dirs['workspace'] = "workspace"
        self.dim = {}
        self.model = []
        
        return

    def rd_stream(self):

        line1 = raw_input("The name of the template directory. \n> ")
        line2 = raw_input("The name of the dynamics control file. \n> ")
        self.files['example'] = line1.strip()
        self.files['dyn'] = line2.strip()
        
        return



    def __rd_xyz_nmol(self):
        """ read how many mol in the xyz file"""
        filename = self.files['xyz']
        
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
        self.__rd_xyz_nmol()
        n_mol = self.dim['n_mol']
        
        filename = self.files['xyz']        
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

    def write_xyz_single(self, id):
        """ write xyz in angstrom unit """
        filename = "stru_xyz.in"
        
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


    def make_single(self, id):
        """
        create directory & copy files.
        """
        # make directory
        work_dir = str(id+1)
        dir_temp="../" + self.dirs['example']
        work_dir_temp=work_dir+"/"+self.dirs['example']
        dyn_temp="../" + self.files['dyn']
        work_dyn_temp=work_dir+"/"+self.files['dyn']

        if os.path.exists(work_dir):
           shutil.rmtree(work_dir)
        # Create the new HOME working directory for QC
        if not os.path.exists(work_dir):
           os.makedirs(work_dir)

        shutil.copytree(dir_temp,work_dir_temp)
        shutil.copyfile(dyn_temp,work_dyn_temp)

        os.chdir(work_dir)
        # print "work directory: ", os.getcwd()
        self.write_xyz_single(id)

        os.chdir("../")
        
        return
	
    def make(self):
        """
        make up job working directory
        """
        # make directory
        work_dir = self.dirs['workspace']
        if os.path.exists(work_dir):
          shutil.rmtree(work_dir)
        # Create the new HOME working directory for QC
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)
 

        os.chdir(work_dir)
        
        n_mol = self.dim['n_mol']
        
        for i in xrange(n_mol):
            self.make_single(i)

        os.chdir("../")
        
        return
    

if __name__ == "__main__":
    jobs = manyjobs()
    jobs.rd_stream()
    jobs.read_xyz()
    jobs.make()
