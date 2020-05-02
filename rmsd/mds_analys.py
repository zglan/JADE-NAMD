#! /usr/bin/env python
import os
from os import system
#import pybel
import numpy as np
import shutil

import subprocess
import multiprocessing
import sub_inp_json as json


'''
To run this script, you should install openbabel and its python library firstly. 
In linux, the installation command is:
apt-get (or yum) install openbabel (or openbabel.x86_64)
apt-get (or yum) install python-openbabel (or python-openbabel.x86_64)
'''


def  analy_result (i_dimension, i_cutoff,job) : 
    file_result =  job + '_dim_'+str(i_dimension) + '.dat'
    xx= np.loadtxt(file_result)
    zz = np.loadtxt('list_file_save.dat')
    yy = np.hstack ((xx,zz))
    filename = 'mds_analys_result.dat'
    np.savetxt (filename, yy)

#   this code is just to create a file include the old list after rmsd cutoff  which the group work need
    kk = np.loadtxt('list_file_save_aftercut.dat')
    dd = np.hstack ((xx,kk))
    filename = 'mds_analys_result_tmp.dat'
    np.savetxt (filename, dd)
    os.remove('list_file_save_aftercut.dat')
     
  
    return
def make():
    curr_path = os.getcwd()
    work_path = curr_path + "/all"
    inp = json.load_json('inp.json')
    distance_cutoff = float(inp['rmsd_cutoff'].encode('utf-8')) 
    n_dimension = int(inp['mds_dimension'].encode('utf-8'))
    job = inp['job_select']
    os.chdir(work_path) 
    analy_result(n_dimension,distance_cutoff,job)    
    os.chdir(curr_path)
if __name__ == "__main__":
    make()


    
