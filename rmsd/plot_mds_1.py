#! /usr/bin/env python
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
import os


"""
This script is used to plot the mds result

you can choose to just plot the map 

or choose setting the limit of the axle and how many grid you want to split

the later will save the xlim ylim and the split number into a file named split.dat  

"""
class plot_mds():

    def __init__(self):
        self.filename = "mds_analys_result.dat"
        self.savefile = "split.dat" 

    def plot_first(self):
        filename = self.filename
    
        curr_path = os.getcwd()
        work_path = curr_path + '/all/'
        os.chdir(work_path)
        
        xx = np.loadtxt (filename)
        fig, ax = plt.subplots()
        ax.scatter(xx[:,0], xx[:,1] ,color='r',marker='*')
            
        plt.show()
        
        
        
    def plot_lim_grid(self):
        filename = self.filename
        tmpfile = self.savefile
        xmin = raw_input("The min value of x axle \n> ")
        xmin = float(xmin)
        xmax = raw_input("The max value of x axle \n> ")
        xmax = float(xmax)
        ymin = raw_input("The min value of y axle \n> ")
        ymin = float(ymin)
        ymax = raw_input("The max value of y axle \n> ")
        ymax = float(ymax)
        xnum = raw_input("How many grid on the x axle \n> ")
        ynum = raw_input("How many grid on the y axle \n> ")
        xnum = float(xnum)+1
        ynum = float(ynum)+1
        #print xmin
        curr_path = os.getcwd()
        work_path = curr_path + '/all/'
        os.chdir(work_path)
        
        xx = np.loadtxt (filename)
        #delete the S0 data and the hop data
        num_delete = 0
        for i in range(np.shape(xx)[0]):
            i = i - num_delete
            if int(xx[i,-3]) == -1 or int(xx[i,-3]) == 0:
                xx = np.delete(xx,i,axis=0)
                num_delete= num_delete+1 
#        colors=['#FF0000','#CC0033','#CC3300','#FF6633','#FF9933','#CC9900','#FFCC00','#FFFF00','#CCCC00','#999900','#666600','#336600','#66CC00','#00FF00','#00CC33','#009933','#33CC66','#33FF99','#66FFCC','#00FFFF','#00CCCC','#009999','#339999','#609999','#99CCFF','#6699CC','#1874CD','#3A5FCD','#0000EE','#0000CD']
        colors=['#FF0000','#CC0033','#CC3300','#FF6633','#FF9933','#CC9900','#FFCC00','#FFFF00','#CCCC00','#999900','#66CC00','#00FF00','#00CC33','#009933','#33CC66','#33FF99','#66FFCC','#00FFFF','#00CCCC','#99CCFF','#6699CC','#1874CD','#3A5FCD','#0000EE','#0000CD','#0000CD','#0000CD','#0000CD','#0000CD','#0000CD']

        plt.rcParams['xtick.direction'] = 'out'
        plt.rcParams['ytick.direction'] = 'out'
        fig, ax = plt.subplots( squeeze=True)
#        ax.set_xlabel('RCI',fontsize=30)
#        ax.set_ylabel('RCII',fontsize=30)
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

        for tick in ax.xaxis.get_major_ticks():  
            tick.label1.set_family('Bold')
        for tick in ax.yaxis.get_major_ticks():  
            tick.label1.set_family('Bold')
          
        
        

        x = xx[:, 0:2]
        y = xx[:, -2]
        target_names = np.arange( 30 , 1, -1 )
        for i in target_names:
            plt.scatter(x[y == i, 0], x[y == i, 1], c=colors[i-1],marker='o',s=25,label=i)
            
        ax.set_ylim(bottom=ymin,top=ymax)
        ax.set_xlim(xmin,xmax)
        ax.set_xticks([-0.8,-0.6,-0.4,-0.2,0,0.2,0.4])
        ax.set_yticks([-0.6,-0.4,-0.2,0,0.2,0.4,0.6])
#        ax.grid()
        fig.tight_layout()
        for tick in ax.yaxis.get_major_ticks():  
            tick.label1.set_fontsize(24)  
            tick.label1.set_family('Bold')  
        for tick in ax.xaxis.get_major_ticks():  
            tick.label1.set_fontsize(24)  
            tick.label1.set_family('Bold')
    
      
        plt.savefig('../mds.png')
        plt.show()

        # creat a file which save the xlim ylim and the split num
        fp = open(tmpfile,"w")
        xnum = xnum - 1
        ynum = ynum - 1
        print >>fp, "%15s%15s%15s%15s%10s%10s" % ('xmin','xmax','ymin','ymax','xnum','ynum')
        print >>fp, "%15.8f%15.8f%15.8f%15.8f%10d%10d" % (xmin,xmax,ymin,ymax,xnum,ynum)
        fp.close()



    def make(self):
        key = raw_input("Do u want to set the limit of the x and y axle and plot the split grid? yes or no(defaut:no)\n>")
        if key=="yes" or key == "YES":
            self.plot_lim_grid()
        else:
            self.plot_first()

if __name__ == "__main__":
    jobs = plot_mds()
    jobs.make()
