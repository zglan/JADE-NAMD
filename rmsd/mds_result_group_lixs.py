#! /usr/bin/env python
import os
from os import system
#import pybel
import numpy as np
#import coord_lan
import shutil


'''
To run this script, you should install openbabel and its python library firstly. 
In linux, the installation command is:
apt-get (or yum) install openbabel (or openbabel.x86_64)
apt-get (or yum) install python-openbabel (or python-openbabel.x86_64)
'''
class MDS_group():

    def __init__(self):
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.xnum = 0
        self.ynum = 0
        self.savefile = "split.dat"
        self.distance_cutoff = [2]
        self.n_dimension = [8]
        self.ifplot = 'no'
#        self.ifplot = 'yes'
        return
        

    def read_para(self):

        workfile = self.savefile 
        if os.path.exists(workfile): 
            fp = open(workfile,"r")
            line = fp.readline()
            line = fp.readline()
            xmin,xmax,ymin,ymax,xnum,ynum = line.split()
            print "%10s%10s%10s%10s%10s%10s" % ('xmin','xmax','ymin','ymax','xnum','ynum')
            print "%10.2f%10.2f%10.2f%10.2f%10d%10d" % (float(xmin),float(xmax),float(ymin),float(ymax),int(xnum),int(ynum))
        else:
            print "Error: There is not a file named split.dat \n\tMaybe you should run plot_mds.py first"
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.xnum = xnum
        self.ynum = ynum
        return
    
    def mds_group_lim (self,file_result):

        xmin = float(self.xmin) 
        xmax = float(self.xmax) 
        ymin = float(self.ymin)
        ymax = float(self.ymax) 
        xnum = int(self.xnum) 
        ynum = int(self.ynum) 
        xx= np.loadtxt(file_result)
        n_sample = xx.shape[0]
        n_dim    = xx.shape[1]
        
        x_range = xmax - xmin 
        y_range = ymax - ymin
        d_x = float(x_range)/xnum
        d_y = float(y_range)/ynum
#        print d_x,d_y
  
        zz = np.arange(n_sample * 2).reshape(n_sample,2)
        zz[:,:] = 0
        fileout = []

#        print "%10s%10s" % ('block','number')
        command = 'rm -f block.dat'
        os.system(command) 
        fi = open('block.dat','w')
        for i_dim1 in range(xnum) :
            for i_dim2 in range(ynum) :
                x_low  = xmin + i_dim1 * d_x
                x_high = xmin + (i_dim1+1) * d_x           
                y_low  = ymin + i_dim2 * d_y
                y_high = ymin + (i_dim2+1) * d_y
                file_name= 'geom_'+str(i_dim1+1)+"_"+str(i_dim2+1)+".xyz"
                fileout = open(file_name, 'w') 
                d_num = 0
                for i_sample in range (n_sample) :
                    if (x_low <= xx[i_sample][0] < x_high) and (y_low <=  xx[i_sample][1] < y_high) : 
                                      d_num = d_num +1
                                      zz [i_sample][0] = i_dim1+1
                                      zz [i_sample][1] = i_dim2+1     
                                      file_index = int(xx [i_sample, -1])
                                      traj_file = 'all_sample.xyz_'+str(file_index)
                                      file_input = open (traj_file)
                                      fread = file_input.read()
                                      file_input.close()
                                      fileout.write(fread)
                
                fileout.close()
                print >> fi, "%5d%5d%10d" % (i_dim1+1, i_dim2+1, d_num)
                self.vmd_plot(file_name,i_dim1+1,i_dim2+1)    

        kk =  np.hstack ((xx,zz)) 
        np.savetxt('isomap_dimen_traj_time_cluster.dat', kk)
        fi.close()


        return

    def collect_geometry (self) :
    
         xnum = int(self.xnum) 
         ynum = int(self.ynum) 
         for i_dim1 in range (xnum) :
             file_name1 = 'geom_first_dimension_'+str(i_dim1+1)+".xyz" 
             command1 = "touch " + str(file_name1)
             os.system (command1)
             for i_dim2 in range (ynum) :
                 file_name2 = 'geom_'+str(i_dim1+1)+"_"+str(i_dim2+1)+".xyz"
                 command2 = 'cat  ' + str(file_name2) + ' >>  ' + str(file_name1)  
                 os.system (command2) 
             self.vmd_plot(file_name1,'first',i_dim1+1)    
    
         for i_dim2 in range (ynum) :
             file_name1 = 'geom_second_dimension_'+str(i_dim2+1)+".xyz"
             command1 = "touch " + str(file_name1)
             os.system (command1)
             for i_dim1 in range (ynum) :
                 file_name2 = 'geom_'+str(i_dim1+1)+"_"+str(i_dim2+1)+".xyz"
                 command2 = 'cat  ' + str(file_name2) + ' >>  ' + str(file_name1) 
                 os.system (command2)
             self.vmd_plot(file_name1,'second',i_dim2+1)    
    
    
         return
    def vmd_plot(self,filename,i_dim,j_dim):
        ifplot = self.ifplot
        i_dim = str(i_dim)
        j_dim = str(j_dim)
        workfile ='vmd_plotgroup.tcl'
        if ifplot == 'yes':
            line = open(filename,'r').readline()
            if len(line) != 0:
                if os.path.exists(workfile):
                    print filename
                    command1 = "cp " + filename + " tmp.xyz"
                    os.system(command1)
                    command2 = "vmd -e " + workfile
                    os.system(command2)
                    command3 = "mv tmp.bmp group_plot_" + i_dim + "_" + j_dim + ".bmp" 
                    os.system(command3)
                else:
                    print "A script file named vmd_plotgroup.tcl is required"
                            
            
    def make (self):
        curr_path = os.getcwd()
        work_path = curr_path + '/all/'
        os.chdir(work_path)
        command = "cp " + curr_path +  "/vmd_plotgroup.tcl " + work_path
        os.system(command)
        self.read_para()
        os.system('rm geom*')
        distance_cutoff = self.distance_cutoff
        n_dimension = self.n_dimension

        file_result = 'mds_analys_result_tmp.dat'
        self.mds_group_lim(file_result)
        os.remove(file_result)
        self.collect_geometry()

        """cp the pictures to a file named group_plot"""
            
        if self.ifplot == 'yes':
            print "mv the group pictures to a file named \'group_plot\'....."
            plotfile = 'group_plt_vmd' 
            if os.path.exists(plotfile):
                command = 'rm -r ' + plotfile
                os.system(command)
                os.mkdir(plotfile)
            else:
                os.mkdir(plotfile)
            command1 = "mv group_plot* " + plotfile
            os.system(command1)

        return

if     __name__ == "__main__":
    jobs = MDS_group()
    jobs.make()
