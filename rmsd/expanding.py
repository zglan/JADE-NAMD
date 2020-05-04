#! /usr/bin/env python
from sklearn.metrics.pairwise import euclidean_distances
import os
import shutil
import numpy as np
import math

def get_one(dimention=1):
    rmsd_filename = 'rmsd_all.dat'
#    mds_filename = 'isomap_dim_10.dat'
    mds_filename = 'isomap_dimen_traj_time_cluster.dat'
    curr_path = os.getcwd()
    work_path = curr_path + '/all'
    rmsd_file = work_path + '/' +  rmsd_filename
    mds_file = work_path + '/' + mds_filename
    rmsd_distance = np.loadtxt(rmsd_file)
    mds_value = np.loadtxt(mds_file)
    X = mds_value[:,0:dimention]
    print X
    mds_distance = euclidean_distances(X,X)
    print np.shape(mds_distance)
    print type(mds_distance)
    matrix = rmsd_distance - mds_distance
    print np.shape(matrix)
    result = 0
    deno = 0
    num = 0
    for i in range(np.shape(matrix)[0]):
        for j in range(i):
            result = result + matrix[i][j]**2
            deno = deno + mds_distance[i][j]**2
            num = num + 1
    erro = math.sqrt(result/deno)
    return erro
    
   
if __name__ == '__main__':
    dimentions = np.linspace(1,20,20)
    save_list = []
    for dimention in dimentions:
        save_list.append(get_one(dimention))
    fp = open('expanding_erro.dat','w')
    for dimention in dimentions:
#        print >> fp, "%12.8f" % save_list[dimention]
        print save_list[int(dimention-1)]
    for dimention in dimentions:
        print >> fp, "%12.8f" % float(save_list[int(dimention-1)])
    fp.close()
#    np.savetxt('expanding_erro.dat',save_list)
    
 
