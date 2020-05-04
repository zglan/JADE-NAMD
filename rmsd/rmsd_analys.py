#! /usr/bin/env python
import numpy as np
import shutil
import os
import sub_inp_json as json
from sklearn.utils import graph

class rmsd_analys():

    def __init__(self):
        self.inp = json.load_json('inp.json')
        self.rmsd_matrix = []
        self.savelist = []
    def classical_analy(self):
        a = self.rmsd_matrix
        b = self.savelist
        lis = []
        n_geom = self.inp['n_geom']
        cut_off = float(self.inp['rmsd_cutoff'].encode('utf-8'))
        
        dele_nu = 0
        for i in range(n_geom):
            i = i - dele_nu
            for j in range(i):
                if a[i,j] == 0 or a[i,j] >= cut_off:
                    if j != 0:
                        a = np.delete(a,j,axis=0)
                        a = np.delete(a,j,axis=1)
                        b = np.delete(b,j,axis=0)
                    else:
                        a = np.delete(a,i,axis=0)
                        a = np.delete(a,i,axis=1)
                        b = np.delete(b,i,axis=0)
                    dele_nu = dele_nu +1
                    break
        n_geom = n_geom - dele_nu
        self.inp['n_geom'] = n_geom
        
        tmp_list = [[i+1]for i in range(n_geom)]
        c = b[:,0:2]
        list_new  = np.hstack ((c,tmp_list))
        np.savetxt('list_file_save_aftercut.dat',b)
        np.savetxt('list_file_save.dat',list_new)
        np.savetxt('rmsd_all.dat',a)
        return 
    
    def isomap_epsilon(self) :
        n_geom = self.inp['n_geom']
        i_cutoff = float(self.inp['mds_cutoff'].encode('utf-8'))
        cut_off = float(self.inp['rmsd_cutoff'].encode('utf-8'))
        xx = self.rmsd_matrix
        b = self.savelist

        dele_nu = 0
        for i in range(n_geom):
            i = i - dele_nu
            for j in range(i):
                if xx[i,j] == 0 or xx[i,j] >= cut_off:
                    if j != 0:
                        xx = np.delete(xx,j,axis=0)
                        xx = np.delete(xx,j,axis=1)
                        b = np.delete(b,j,axis=0)
                    else:
                        xx = np.delete(xx,i,axis=0)
                        xx = np.delete(xx,i,axis=1)
                        b = np.delete(b,i,axis=0)
                    dele_nu = dele_nu +1
                    break
        n_geom = n_geom - dele_nu

        print "rmsd_cut:%d" % n_geom
        x_train_scale = xx
    
        dist_matrix =  np.arange(n_geom * n_geom).reshape(n_geom,n_geom)
        dist_matrix =  dist_matrix.astype(float)
    
        maximum_value = np.amax(x_train_scale)
        INF = maximum_value * n_geom
        for i_dim in range(n_geom) :
            for j_dim in range(n_geom) :
                if xx[i_dim, j_dim] < i_cutoff :
                   dist_matrix [i_dim, j_dim] = xx[i_dim, j_dim]
                else :
                   dist_matrix [i_dim, j_dim] = INF
        a = graph.graph_shortest_path ( dist_matrix )

        dele_nu = 0
        for i in range(n_geom):
            i = i - dele_nu
            for j in range(i):
                if a[i,j] == 0 or a[i,j] == INF:
                    if j != 0:
                        a = np.delete(a,j,axis=0)
                        a = np.delete(a,j,axis=1)
                        b = np.delete(b,j,axis=0)
                    else:
                        a = np.delete(a,i,axis=0)
                        a = np.delete(a,i,axis=1)
                        b = np.delete(b,i,axis=0)
                    dele_nu = dele_nu +1
                    break
        n_geom = n_geom - dele_nu
        self.inp['n_geom'] = n_geom
        print "mds_cut:%d" % n_geom

        tmp_list = [[i+1]for i in range(n_geom)]
        c = b[:,0:2]
        list_new  = np.hstack ((c,tmp_list))
        np.savetxt('list_file_save_aftercut.dat',b)
        np.savetxt('list_file_save.dat',list_new)
        np.savetxt('rmsd_all.dat',a)
        return 
    def make(self):
        curr_path = os.getcwd()
        work_path = curr_path + '/all'
        os.chdir(work_path)
        self.rmsd_matrix = np.loadtxt('rmsd_all.dat')
        self.savelist = np.loadtxt('list_file_save.dat')
        command1 = 'cp rmsd_all.dat rmsd_all.dat_old'
        command2 = 'cp list_file_save.dat list_file_save.dat_old'
        os.system(command1)
        os.system(command2) 
        if self.inp['job_select'] == 'isomap':
            self.isomap_epsilon()
        else:
            self.classical_analy()
        os.chdir(curr_path)
        json.dump_json('inp.json',self.inp)


def make():
    jobs = rmsd_analys()
    jobs.make() 

if __name__ == "__main__":
    jobs = rmsd_analys()
    jobs.make() 
