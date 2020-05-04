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



def _c(ca,i,j,dis_matrix):
    if ca[i,j] > -1:
        return ca[i,j]
    elif i == 0 and j == 0:
        ca[i,j] = dis_matrix[0,0]
    elif i > 0 and j == 0:
        ca[i,j] = max(_c(ca,i-1,0,dis_matrix),dis_matrix[i,0])
    elif i == 0 and j > 0:
        ca[i,j] = max(_c(ca,0,j-1,dis_matrix),dis_matrix[0,j])
    elif i > 0 and j > 0:
        ca[i,j] = max(min(_c(ca,i-1,j,dis_matrix),_c(ca,i-1,j-1,dis_matrix),_c(ca,i,j-1,dis_matrix)),dis_matrix[i,j])
    else:
        ca[i,j] = float("inf")
    return ca[i,j]

def frechetDist(dis_matrix):
    len_p = np.shape(dis_matrix)[0]
    len_q = np.shape(dis_matrix)[1]
    ca = np.ones((len_p,len_q))
    ca = np.multiply(ca,-1)
    return _c(ca,len_p-1,len_q-1,dis_matrix)

def read_single(filename):
    fp=open(filename,'r')
    n_atom = int(fp.readline().strip().split()[0])
    line=fp.readline()
    coord = np.zeros((n_atom,3))
    
    for i in range(n_atom):
        line=fp.readline().strip()
        atom,coord[i][0],coord[i][1],coord[i][2] = line.split()
    return coord
def read_all(path):
    coords = []
    curr_path = os.getcwd()
    work_path = curr_path + '/' + str(path)
    tmp = 0
    for parentdir,dirname,filenames in os.walk(work_path):
        for filename in filenames:
             if os.path.splitext(filename)[0]=='sample':  
                 tmp = tmp +1
    for i in range(tmp):
        filename = work_path + '/sample.xyz_' + str(i+1)
        coords.append(read_single(filename))
    return coords

def  rmsd_two_coord (coord1, coord2):
     rmsd,coord_mina = rms.make(coord1,coord2)     
     return rmsd,coord_mina
def disparate_two_coord(coord1,coord2):
    disp = 0
    natom = np.shape(coord1)[0]
    for i in range(natom):
        dis = ( (coord1[i][0]-coord2[i][0])**2 + (coord1[i][1]-coord2[i][1])**2 + (coord1[i][2]-coord2[i][2])**2 ) ** 0.5
        disp = disp + dis
    disparate = disp/natom
    return disparate    
def rmsd_many (path1,path2,npro) : 
    coords0 = read_all('0')
    coords1 = read_all(path1)
    coords2 = read_all(path2)
    coord1_new = []
    coord2_new = []
#   rotate with the same reference
    for coord in coords1:
        tmp,co = rmsd_two_coord(coords0[0],coord)
        coord1_new.append(co)
    for coord in coords2:
        tmp,co = rmsd_two_coord(coords0[0],coord)
        coord2_new.append(co)
    n_geom1 = np.shape(coords1)[0]
    n_geom2 = np.shape(coords2)[0]
    main_dir = os.getcwd()
    rmsd = np.arange(n_geom1 * n_geom2).reshape(n_geom1,n_geom2)
    rmsd = rmsd.astype(float)
    rmsd[:,:] = 0.0
    result = []
    pool = multiprocessing.Pool(processes = npro)
    for i in range(n_geom1):
        for j in range(n_geom2):
             result.append(pool.apply_async(disparate_two_coord, (coord1_new[i], coord2_new[j], ) ) )
#             result.append(rmsd_two_coord(coords[lis[i][0]], coords[lis[i][1]]) )
    pool.close()
    pool.join()
    
    for i_geom in range(n_geom1):
        for j_geom in range(n_geom2) :
            res = result.pop(0)
            rmsd[i_geom, j_geom] = res.get()

# get freched distance
    frech = frechetDist(rmsd)


    return frech


def make_first():
     inp = json.load_json('inp.json')
     npro = int(inp['n_pro'])
     ntraj = int(inp['n_traj'])
     dis = np.arange(ntraj * ntraj).reshape(ntraj,ntraj)
     dis = dis.astype(float)
     print dis
     for i in range(ntraj):
        for j in range(ntraj):
            print i,j
            path1 = i + 1
            path2 = j + 1
            curr_path = os.getcwd()
            dis[i,j] = rmsd_many(path1,path2,npro) 
     print dis
     np.savetxt('similarity.dat',dis)
    
if __name__ == "__main__":
    make_first()
    ####
