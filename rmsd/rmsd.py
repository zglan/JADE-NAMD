#! /usr/bin/env python
import sub_rmsd_two_coord as rms
import sub_inp_json as json
import os 
from os import system
#import pybel
import numpy as np
#import coord_lan
import shutil
#import matplotlib.pyplot as plt
import time
import subprocess 
import multiprocessing
import time
import itertools
import sys
sys.path.append('lRMSD')
import lrmsd

# 2016.09.09, Yu Xie
# Remove directories created for calculation each rmsd.
# 2016.10.25 ,lixs 




def read_single(filename):
    fp=open(filename,'r')
    n_atom = int(fp.readline().strip().split()[0])
    line=fp.readline()
    coord = np.zeros((n_atom,3))
    
    for i in range(n_atom):
        line=fp.readline().strip()
        atom,coord[i][0],coord[i][1],coord[i][2] = line.split()
    return coord
def read_all(n_geom):
    coords = []
    curr_path = os.getcwd()
    work_path = curr_path + '/all'
    for i in range(n_geom):
        filename = work_path + '/all_sample.xyz_' + str(i+1)
        coords.append(read_single(filename))
    return coords

def  rmsd_two_coord (coord1, coord2):
     rmsd,coord_mina = rms.make(coord1,coord2)     
     return rmsd

def rmsd_many (n_geom,n_atom,npro) : 
    coords = read_all(n_geom)
    main_dir = os.getcwd()
    rmsd = np.arange(n_geom * n_geom).reshape(n_geom,n_geom)
    rmsd = rmsd.astype(float)
    rmsd[:,:] = 0.0
    result = []
    lis = []
    for i_geom in range(n_geom):
        for j_geom in range(i_geom):
            lis.append([i_geom,j_geom])
    pool = multiprocessing.Pool(processes = npro)
    for i in range(n_geom*(n_geom-1)/2):
             print lis[i][0],lis[i][1]
             result.append(pool.apply_async(rmsd_two_coord, (coords[lis[i][0]], coords[lis[i][1]], ) ) )
#             result.append(rmsd_two_coord(coords[lis[i][0]], coords[lis[i][1]]) )
    pool.close()
    pool.join()
    print "Sub-process(es) done."
    
    for i_geom in range(n_geom):
        for j_geom in range(i_geom) :
            res = result.pop(0)
            print res.get()
            rmsd[i_geom, j_geom] = res.get()
#            rmsd[i_geom, j_geom] = res
            rmsd[j_geom, i_geom] = rmsd[i_geom, j_geom]  
    file_rmsd_all = main_dir + '/all/rmsd_all.dat'
    np.savetxt(file_rmsd_all, rmsd)
    os.chdir(main_dir)
#    plot_rmsd ()
    
    return

def plot_rmsd () :
     data = np.loadtxt('rmsd_all.dat') 
     plt.imshow(data, cmap=plt.cm.spectral)
     plt.show()
     return   
 

def make_first():
     inp = json.load_json('inp.json')
     n_geom = int(inp['n_geom'])
     n_atom = int(inp['n_atom'])
     npro = int(inp['n_pro'])
     curr_path = os.getcwd()
     dir_path = curr_path + '/all/'
     command = 'cp inp.json ' + dir_path
     os.system(command)   
     rmsd_many(n_geom,n_atom,npro) 

  
def make_second(id,workdir): 
    n_geom = id
    inp = json.load_json('inp.json')
    n_atom = int(inp['n_atom'])
    npro = int(inp['n_pro'])
    dir_path = workdir   
    command = 'cp inp.json ' + dir_path
    os.system(command)   
    os.chdir(dir_path)
    rmsd_many ( n_geom, n_atom, npro) 
   
    
if __name__ == "__main__":
    make_first()
