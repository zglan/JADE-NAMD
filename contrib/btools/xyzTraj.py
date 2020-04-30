#! /usr/bin/env python

import os
import copy
import re
import shutil
import numpy as np

#
# xyz format 
#
# Key Data Structure
# mol = {'title':title, 'n_atom': n_atom, 'geom':geom, 'name': atom_name}
#
#

class xyzTraj:
    """ the xyz format, trajectory """
    def __init__(self, config = {}):
        """ common variable """
        print "note: the atom index (0 or 1)"

        self.traj = {}
        self.frg = {}
        self.sid = 0
        
        return
        
    def read_stru(self, fpin):
        """ read in xyz format in angstrom unit """    
        # read number of atom
        line = fpin.readline().strip() 
        # check the end of file
        if line == "":
            return 0
        n_atom = int(line.split()[0])        
        title = fpin.readline().strip()
        geom = []
        atom_name = []
        # read a mole
        for i in xrange(n_atom):
            line = fpin.readline()
            rec = line.split()
            name, x, y, z= rec[0:4]            
            coord = [float(x),float(y),float(z)]
            atom_name.append(name)
            geom.append(coord)
        mol = {'title':title, 'n_atom': n_atom, 'geom':geom, 'name': atom_name}
        return mol        
    
    def read_it(self, filename="traj.xyz"):
        """ read in a list of xyz """
        fp = open(filename, "r")
        model = []
        n_model = 0
        while True:
            mol = self.read_stru(fp)
            if mol == 0:
                print("End of xyz traj. file. ^_^")
                break
            model.append(mol)
            n_model += 1
        fp.close()   
        traj = {'model': model, 'n_model': n_model}
        self.traj = traj
        return
       
    def print_mol(self, mol):
        """ puts mol into string """
        mystr = ""
        title = mol['title']
        n_atom = mol['n_atom']
        geom = mol['geom']
        name = mol['name']
        mystr += "%-10d\n" % n_atom
        mystr += title + "\n"
        for i in xrange(n_atom):
            pos = geom[i]
            atom_name = name[i]
            mystr += "%-10s%12.6f%12.6f%12.6f\n" % (atom_name, pos[0], pos[1], pos[2])
        return mystr

    def dump_it(self, filename="ptraj.xyz"):
        """ write down all xyz traj files """
        fp = open(filename, "w")
        for mol in self.traj['model']:
            mystr = self.print_mol(mol)
            print >>fp, "%s" % mystr,
        fp.close()    
        return    

    # 
    # split the trajectory file
    #
    def dump_once(self, mol, filename="punch.xyz"):
        """ write xyz format in angstrom unit """    
        if os.path.isfile(filename):
            print "OVERWRITE: %s" % filename
        fp = open(filename, "w")
        title = mol['title']
        n_atom = mol['n_atom']
        geom = mol['geom']
        name = mol['name']
        print >>fp, "%-10d" % (n_atom)
        print >>fp, title
        for i in xrange(n_atom):
            pos = geom[i]
            atom_name = name[i]
            print >>fp, "%-10s%12.6f%12.6f%12.6f" % (atom_name, pos[0], pos[1], pos[2])
        fp.close()    
        return

    
    def dump_many(self, filename="punch.xyz"):
        """ write all xyz files """
        mydir = self.config['mydir']
        if os.path.isdir(mydir):
            shutil.rmtree(mydir)
        os.mkdir(mydir)
        os.chdir(mydir)
        mystr = filename.split(".")
        prefix = mystr[0]
        model = self.model
        for i in xrange(len(model)):
            mol = model[i]
            myfile = filename + "." + str(i)
            self.dump_once(mol, myfile)
            print "MOL %d done" % i
        os.chdir("../")    
        return    
    #    
    # ---------------------------------------------
    #
    def ext_frg_ndx(self, frg_ndx, flag = 0):
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
        
        
    def fragment(self, frg_ndx, flag = 0):
        """
        find atom index to fragment
        """
        #
        frg_list = self.ext_frg_ndx(frg_ndx, flag)
        n_atom = len(frg_list)
        title = str(frg_list)
        #
        model = self.traj['model']
        sid = self.sid
        mol = model[sid]
        geom = mol['geom']
        aname = mol['name']
        frg_geom = []
        frg_aname = []
        for i in frg_list:
            frg_geom.append(geom[i])
            frg_aname.append(aname[i])
        frg = {'title':title, 'n_atom': n_atom, 'geom': frg_geom, 'name': frg_aname, 'ndx': frg_list} 
        self.frg = frg
        return frg

    def next_model(self):
        """ next struct """
        n_model = self.traj['n_model']
        flag = 1
        if self.sid < n_model - 1:
            self.sid += 1
        else:
            self.sid = 0
            flag = 0
            print "END OF TRAJ."
 
        return flag

    def get_model(self, sid = 0):
        """
        get the sid-th model
        """
        n_model = self.traj['n_model']
        
        if sid > n_model - 1:
            self.sid = sid
            print "sid larger than n_model, reset to 0"
        elif sid < 0:
            self.sid = 0
            print "sid smaller than 0, reset to 0"
        else:
            self.sid = sid
        return


    def reset_model(self):
        """
        get the sid-th model
        """
        print "sid model reset to 0"
        self.sid = 0
        return    
        
  
    def print_frg(self):
        """ print mol into string & in the screen """
        mystr = ""
        # variable
        mol = self.frg
        title = mol['title']
        n_atom = mol['n_atom']
        geom = mol['geom']
        name = mol['name']
        # print to var.
        mystr += "%-10d\n" % n_atom
        mystr += title + "\n"
        for i in xrange(n_atom):
            pos = geom[i]
            atom_name = name[i]
            mystr += "%-10s%12.6f%12.6f%12.6f\n" % (atom_name, pos[0], pos[1], pos[2])
        print mystr
        return  

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
        return theta, theta*180.0/np.pi

       

# Main        
if __name__ == "__main__":
    # read in mole & dump
    xyz = xyzTraj()
    xyz.read_it(filename="./traj.xyz")
    xyz.dump_it()
    
    frg_ndx = "0-17, 38, 40"
    xyz.fragment(frg_ndx)
    xyz.print_frg()
    
    frg_ndx = "20-37, 39, 41, 42-48"
    xyz.fragment(frg_ndx)
    xyz.print_frg()
    
    xyz.next()
    xyz.fragment(frg_ndx)
    xyz.print_frg()
    
    
    
    
