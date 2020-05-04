#! /usr/bin/env python
import os
from os import system
#import pybel
import numpy as np
#import coord_lan
import shutil
import matplotlib.pyplot as plt
import matplotlib.colors as color
import time
import subprocess
import multiprocessing




def plot_time (n_step) :

    
#    color.Colormap(color_set, N=n_step)

    fig, ax = plt.subplots()
    for i_select in range(n_step):
        file_each_time = 'traj_each_time.dat_'+str(i_select+1)
        xx = np.loadtxt (file_each_time)
#        print xx
        ax.scatter(xx[:,0], xx[:,1]  )
#        print xx[:,0] 
#        raise IOError
    plt.show()
    

    return


def plot_time_color ( file_all_time) :

    xx = np.loadtxt (file_all_time)
    x = xx[:, 0:2]
    y = xx[:, -2]
    target_names = [0, 1, 2, 3, 4, 5, 6, 7]
    print x
    print y
    colors = "bgrcwmyk"

    plt.figure()
    for c, i, target_name in zip(colors, target_names, target_names ):
        plt.scatter(x[y == i, 0], x[y == i, 1], c=c, s=50, label=target_name)
    plt.legend()
    plt.title('ISOMAP')
    plt.show()
    raise IOError

    return

def plot_gnuplot (n_step) :
    return

if __name__ == "__main__":



   n_step  =  20
   working_dir = "./all/"
   file_all_time = "mds_analys_result.dat"
#isomap_dimen.dat_dim_8_cutoff_2
   os.chdir(working_dir)
   plot_time_color ( file_all_time)    

#   plot_time (n_step)
 
