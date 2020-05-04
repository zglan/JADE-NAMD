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



def plot_time_color ( file_all_time) :

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
    fp = open('./all/split.dat',"r")
    line = fp.readline()
    line = fp.readline()
    xmin,xmax,ymin,ymax,xnum,ynum = line.split()
    
    plt.rcParams['xtick.direction'] = 'out'
    plt.rcParams['ytick.direction'] = 'out'
    fig, ax = plt.subplots( squeeze=True)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    xticklines = ax.xaxis.get_ticklines()
    xticklabels = ax.xaxis.get_ticklabels() 
    for tickline in xticklines:
        tickline.set_markersize(5)
        tickline.set_markeredgewidth(3)
    for ticklabel in xticklabels:
        ticklabel.set_fontsize(24)
    
    yticklines = ax.yaxis.get_ticklines() 
    yticklabels = ax.yaxis.get_ticklabels() 
    for tickline in yticklines:
        tickline.set_markersize(5)
        tickline.set_markeredgewidth(3)
    for ticklabel in yticklabels:
        ticklabel.set_fontsize(24)
    ax.spines['bottom'].set_linewidth(3)
    ax.spines['right'].set_linewidth(3)
    ax.spines['left'].set_linewidth(3)
    ax.spines['top'].set_linewidth(3)
         
    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)
    ax.set_xticks([-1,-0.6,-0.2,0.2,0.6,1])
    ax.set_yticks([-1,-0.6,-0.2,0.2,0.6,1])
        
    for tick in ax.xaxis.get_major_ticks():  
        tick.label1.set_family('Bold')
    for tick in ax.yaxis.get_major_ticks():  
        tick.label1.set_family('Bold')

    sample = range(len(target_names))
    num = 1
    num2 = 1
    for i in range(np.shape(z)[0]):
        if z[i] == 0:
            plt.scatter(x[i, 0], x[i, 1], c='r',marker='o',s=70, label='S0')
        if y[i] == 1:
            if num ==1 :
                plt.scatter(x[i, 0], x[i, 1], c='w',marker='o',s=50, label='Initial sampling')
                num = num+1
            else:
                plt.scatter(x[i, 0], x[i, 1], c='w',marker='o',s=50)

        if z[i] == -1:
            if num2 ==1 :
                plt.scatter(x[i, 0], x[i, 1], c='b',marker='o',s=50, label='Hopping geom')
                num2 = num2+1
            else:
                plt.scatter(x[i, 0], x[i, 1], c='b',marker='o',s=50)
    for i in range(np.shape(z)[0]):
        if z[i] == 0:
            plt.scatter(x[i, 0], x[i, 1], c='r',marker='o',s=70)

#    plt.xlim(float(xmin),float(xmax))
#    plt.ylim(float(ymin),float(ymax))         
#    plt.legend(loc=1)
    plt.savefig('../s0.png')
    plt.show()
#        plot_name = str(key) + '.svg'
#        fig.savefig(plot_name)
#        command = "convert " + plot_name + " " + str(key) + ".jpg"
#        os.system(command)
    return
def make():
    file_all_time = "./all/mds_analys_result.dat"
    plot_time_color ( file_all_time)    
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
 
