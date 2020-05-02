#! /usr/bin/env python
import sub_chage_coord as change
import sub_inp_json as json 
import sys
import lrmsd
import numpy as np
import shutil
import os
import os.path  
import copy

class rmsd_two_coord():
 
    def __init__(self,coord1,coord2):
     
        inp = json.load_json('inp.json')
        self.charality = inp['charality']
        self.exchange = inp['exchange']
        self.exchnu = None 
        self.atom = inp['n_atom']
        self.coord1 = coord1
        self.coord2 = coord2
        self.mina = None
        self.geom_mina = None
        self.rmsd_list = []
        self.num = 0
    def analy_rmsd(self,xyz1,xyz2):
        r= np.array([0.])
        xyz1_T = xyz1.T
        xyz2_T = xyz2.T
        lrmsd.sub_whole_overlap(xyz1_T,xyz2_T,r)
        if self.num == 0:
            self.mina = r[0]
            self.geom_mina = xyz2_T.T
            self.rmsd_list.append(r[0])
            self.num = 1
        else:
            self.rmsd_list.append(r[0])
            if r[0] < self.mina:
                self.mina = r[0]
                self.geom_mina = xyz2_T.T
        return 
        
        

    def get_rmsd_two(self):
        cha = self.charality
        exch = self.exchange
        xyz1 = copy.deepcopy(self.coord1)
        xyz2 = copy.deepcopy(self.coord2)
#        print xyz2
        self.analy_rmsd(xyz1,xyz2)
        
        if cha == 'yes' and exch != 'yes':
            xyz2 = copy.deepcopy(self.coord2)
            xyz2_chara = change.Chara(xyz2)
#            print xyz2_chara
            self.analy_rmsd(xyz1,xyz2_chara)
            
        if cha != 'yes' and exch == 'yes':
            xyz2 = copy.deepcopy(self.coord2)
            change_coords = change.Exch(xyz2)
            for i in range(np.shape(change_coords)[0]):
#                print change_coords[i]
                self.analy_rmsd(xyz1,change_coords[i]) 

        if cha == 'yes' and exch == 'yes':
            xyz2 = copy.deepcopy(self.coord2)
            change_coords = change.Exch(xyz2)
            for i in range(np.shape(change_coords)[0]):
#                 print change_coords[i]
                self.analy_rmsd(xyz1,change_coords[i])

            xyz2 = copy.deepcopy(self.coord2)
            xyz2_chara = change.Chara(xyz2)
#            print xyz2_chara
            self.analy_rmsd(xyz1,xyz2_chara)

            change_coords = change.Exch(xyz2_chara)
            for i in range(np.shape(change_coords)[0]):
#                print change_coords[i]
                self.analy_rmsd(xyz1,change_coords[i])
        return self.mina,self.geom_mina

        
        

if __name__ == '__main__':
    coord1 = np.loadtxt('inp.xyz')
    coord2 = np.loadtxt('inp2.xyz')
    jobs = rmsd_two_coord(coord1,coord2)
    jobs.get_rmsd_two()

def make(coord1,coord2):
    jobs = rmsd_two_coord(coord1,coord2)
    rmsd,coord_mina = jobs.get_rmsd_two()
    return rmsd,coord_mina
def make_second(coord1,coord2,n_atom,atoms,filename):
    jobs = rmsd_two_coord(coord1,coord2)
    rmsd,coord_mina = jobs.get_rmsd_two()
    fp = open(filename,"a")
    print >> fp, "%d" % n_atom
    print >> fp, ""
    for i in range(int(n_atom)):
        atom = atoms[i]
        coord = coord_mina[i]
        print >> fp, "%s%15.8f%15.8f%15.8f" % (atom,coord[0],coord[1],coord[2])
    fp.close()
    
    
