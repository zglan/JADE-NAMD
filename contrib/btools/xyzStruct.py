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
class xyzStruct:
    """ the xyz format, only one model """
    def __init__(self, config = {}):
        """ common variable """
        #print "##WARNING : atom index starting from 0 !!!"

        self.mol = {}
        self.frg = {}

        return
        
    def set_it(self, mol):
        """ reset """
        self.mol = mol
        return
        
    def read_it(self, filename = "cu.xyz"):
        """
        read in xyz format structure in angstrom unit
        """
        fp = open(filename, "r")
        # read number of atom
        line = fp.readline().strip()  
        # check the end of file
        if line == "":
            print("Fail to read xyz file!!!")
            exit(1)
        n_atom = int(line.split()[0])        
        title = fp.readline().strip()
        geom = []
        atom_name = []
        # read a mole
        for i in xrange(n_atom):
            line = fp.readline()
            name, x, y, z= line.split()[0:4]            
            coord = [float(x),float(y),float(z)]
            atom_name.append(name)
            geom.append(coord)
        mol = {'title':title, 'n_atom': n_atom, 'geom':geom, 'name': atom_name}
        self.mol = mol
        return mol
       
    def read_gjf(self, filename = "gau.gjf"):
        """
        gaussian gjf file cart. coordinate
        Molecule specification: Specify molecular system to be studied
        """
        fp = open(filename, "r")
        
        while True:
            line = fp.readline()
            if line == "":
                break
            i_find_sharp = re.search('^#', line)
            if i_find_sharp is not None:
                break
        while True:
            line = fp.readline()
            if line == "":
                break
            if line.strip() == "":
                break
        line = fp.readline()
        title = line.strip()
        line = fp.readline()
        line = fp.readline()

        # molecular coord. [suppose cart. coordinates].
        geom = []
        atom_name = []
        n_atom = 0
        while True:
            line = fp.readline()
            if line == "":
                break
            if line.strip() == "":
                break
            a, c, f = self.__check_gjf_frg(line) 
            atom_name.append(a)
            geom.append(c)
            n_atom += 1
        mol = {'title':title, 'n_atom': n_atom, 'geom':geom, 'name': atom_name}
        self.mol = mol
        return mol
            
    def __check_gjf_frg(self, line):
        """
        check gjf fragment type 03 or 09 version, and return records
        """
        frg = ""
        if line.find('=') != -1:
            myline = line.replace('(',' ').replace(')',' ').replace('=',' ')
            items = myline.split()
            atom_name = items[0]
            frg = int(items[2])
            coord = [ float(items[3]), float(items[4]), float(items[5]) ]
        else:
            myline = line
            items = myline.split()
            if len(items) > 4:
                frg = int(items[4])
            atom_name = items[0]
            coord = [ float(items[1]), float(items[2]), float(items[3]) ]
        return atom_name, coord, frg
    
    
    def dump_it(self, filename="dump.xyz"):
        """ write xyz format in angstrom unit """    
        if os.path.isfile(filename):
            print "OVERWRITE this FILE: %s !!!" % filename
        fp = open(filename, "w")
        # variables
        title = self.mol['title']
        n_atom = self.mol['n_atom']
        geom = self.mol['geom']
        name = self.mol['name']
        # write down
        print >>fp, "%-10d" % (n_atom)
        print >>fp, title
        for i in xrange(n_atom):
            pos = geom[i]
            atom_name = name[i]
            print >>fp, "%-10s%12.6f%12.6f%12.6f" % (atom_name, pos[0], pos[1], pos[2])
        fp.close()    
        return
 
    def print_it(self):
        """ print mol into string & in the screen """
        mystr = ""
        # variable
        title = self.mol['title']
        n_atom = self.mol['n_atom']
        geom = self.mol['geom']
        name = self.mol['name']
        # print to var.
        mystr += "%-10d\n" % n_atom
        mystr += title + "\n"
        for i in xrange(n_atom):
            pos = geom[i]
            atom_name = name[i]
            mystr += "%-10s%12.6f%12.6f%12.6f\n" % (atom_name, pos[0], pos[1], pos[2])
        print mystr
        return
  

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
        frg_list = self.ext_frg_ndx(frg_ndx, flag)
        n_atom = len(frg_list)
        title = str(frg_list)
        mol = self.mol
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
        return theta, theta * 180.0/np.pi

        
if __name__ == "__main__":
    # read in mole & dump
    xyz = xyzStruct()
    xyz.read_it(filename = "./cu.xyz")
    xyz.read_gjf(filename = "dmphen.gjf")
    xyz.print_it()
    xyz.dump_it()
    
    frg_ndx = "0-17, 38, 40"
    xyz.fragment(frg_ndx)
    xyz.print_frg()
    # a = xyz.fit_plane()

    frg_ndx = "20-37, 39, 41, 42-48"
    xyz.fragment(frg_ndx, flag = 1)
    xyz.print_frg()
    # b = xyz.fit_plane()
    
    # t = xyz.get_angle(a, b)
    
    # print t
    
    
    
