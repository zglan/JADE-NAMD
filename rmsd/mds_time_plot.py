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
import matplotlib.colors



def plot_time_color ( file_all_time,xmin,xmax,ymin,ymax) :

    xx = np.loadtxt (file_all_time)
    x = xx[:, 0:2]
    y = xx[:, -2]
    z = xx[:,-3]
    target_names = np.arange( 0 , 20, 1)
    print target_names
    markers = [
    '.', # point
    ',', # pixel
    'o', # circle
    'v', # triangle down
    '^', # triangle up
    '<', # triangle_left
    '>', # triangle_right
    '1', # tri_down
    '2', # tri_up
    '3', # tri_left
    '4', # tri_right
    '8', # octagon
    's', # square
    'p', # pentagon
    '*', # star
    'h', # hexagon1
    'H', # hexagon2
    '+', # plus
    'x', # x
    'D', # diamond
    'd', # thin_diamond
    '|', # vline
    ]
    colors = ['#FF0000','#FF34B3','#FF6347','#FF7F00','#FFA500','#FFFF00','#EEAD0E','#FFFF00','#EEEE00','#CAFF70','#76EE00',
    '#228B22','#20B2AA','#0000CD','#4169E1','#00688B','#00F5FF','#6959CD','#7D26CD','#616161','#000000']
    
    sample = range(len(target_names))
    for key in range(1,31):   
        fig = plt.figure()
        num = 1
        num2 = 1
        for i in range(np.shape(z)[0]):
            if y[i] == key:
                if num ==1 :
                    plt.scatter(x[i, 0], x[i, 1], c='g',marker='o',s=30, label=key)
                    num = num+1
                else:
                    plt.scatter(x[i, 0], x[i, 1], c='g',marker='o',s=30)

            if z[i] == 0:
                plt.scatter(x[i, 0], x[i, 1], c='r',marker='o',s=70, label='S0')
            if z[i] == -1:
                if num2 ==1 :
                    plt.scatter(x[i, 0], x[i, 1], c='b',marker='x',s=70, label='CI')
                    num2 = num2+1
                else:
                    plt.scatter(x[i, 0], x[i, 1], c='b',marker='x',s=70)

        plt.xlim(float(xmin),float(xmax))
        plt.ylim(float(ymin),float(ymax))         
        plt.legend()
        plot_name = str(key) + '.svg'
        fig.savefig(plot_name)
        command = "convert " + plot_name + " " + str(key) + ".jpg"
        os.system(command)
    return
def make():
    limi_file = "./all/split.dat"
    if os.path.exists(limi_file): 
        fp = open(limi_file,"r")
        line = fp.readline()
        line = fp.readline()
        xmin,xmax,ymin,ymax,xnum,ynum = line.split()
    
    file_all_time = "./all/mds_analys_result.dat"
    plot_time_color ( file_all_time,xmin,xmax,ymin,ymax)    
    save_path = "./plot_times"
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
    os.mkdir(save_path) 
    command = "mv *.jpg " + save_path
    command2 = "rm *.svg"
    os.system(command)
    os.system(command2)
    os.chdir(save_path)
    command3 = "ffmpeg -r 1 -i %d.jpg a.avi"
    os.system(command3)
 
if __name__ == "__main__":
    make()
#   plot_time (n_step)
 
