#! /usr/bin/env python
import sub_split_coord  as spl
import  sub_rmsd_reference as got_ref
import  sub_rmsd_two_coord as rmsd
import numpy as np
import os
import shutil

# lixs 2016.10.26
# This script is used to rotate geom_*_*.xyz to geom_rmsd_*_*.xyz which has been overlap in case of the rmsd value


class mds_group_overlap():
    def __init__ (self) :
        self.savefile = 'split.dat'
        self.xnum = 1
        self.ynum = 1
        self.ifplot = 'yes'
        self.n_atom = None
        self.atoms = []
    def get_para(self,savefile): 
        if os.path.exists(savefile):
            fp = open(savefile,"r")
            line = fp.readline()
            line = fp.readline()
            xmin,xmax,ymin,ymax,xnum,ynum = line.split()
        else:
            print "Error: There is not a file named split.dat \n\tMaybe you should run plot_mds.py first"
        self.xnum = xnum
        self.ynum = ynum
        print xnum,ynum

        return
    def get_sample_num(self,name):
        m=0  
        dir=os.getcwd()
        for parentdir,dirname,filenames in os.walk(dir):
            for filename in filenames:  
                 if name in filename :
                      m=m+1  
        return(m)
    def read_single(self,filename):
        fp=open(filename,'r')
        n_atom = int(fp.readline().strip().split()[0])
        line=fp.readline()
        coord = np.zeros((n_atom,3))
        self.atoms = []
        self.n_atom = n_atom
        for i in range(n_atom):
            line=fp.readline().strip()
            atom,coord[i][0],coord[i][1],coord[i][2] = line.split()
            print atom
            (self.atoms).append(atom)
        return coord

    def make_single(self,reference = 1,filenameold='geom.xyz',filenamenew='../geom_rmsd.xyz'):
        curr_dir = os.getcwd()
        work_dir = curr_dir + '/all'
        job_dir =  work_dir + '/job_dir'
        filenameold = filenameold
        filenamenew = filenamenew
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)
        command0 = 'mkdir ' + job_dir
        os.system(command0)
        command = 'cp inp.json ' + job_dir
        os.system(command)
        os.chdir(job_dir)
        command1 = 'cp ' + work_dir + '/' +  filenameold + ' ' + job_dir + '/input.xyz'
        os.system(command1)
        spl.make()
        num = self.get_sample_num('all_sample.xyz_')
        if num == 1:
            shutil.copyfile('all_sample.xyz_1',filenamenew)
        if num > 1:
            refer = reference
            print refer
            if refer <= num: 
                file1 = job_dir + '/all_sample.xyz_' + str(refer)
                coord1 = self.read_single(file1)
                for i in range(num):
                    file2 = job_dir + '/all_sample.xyz_' + str(i+1)
                    coord2 = self.read_single(file2)
                    rmsd.make_second(coord1,coord2,self.n_atom,self.atoms,filenamenew)
            if refer > num:
                print "The reference is too large" 
        os.chdir(curr_dir)
        command1 = 'rm -r ' + job_dir
        os.system(command1)    
        
        
    def make_all_group(self):
        curr_dir = os.getcwd()
        work_dir = curr_dir + '/all'
        savefile = work_dir + '/' + self.savefile
        self.get_para(savefile) 
        xnum = int(self.xnum) 
        ynum = int(self.ynum)
        command = "cp " + curr_dir +  "/vmd_plotgroup.tcl " + work_dir
        os.system(command)
        os.chdir(work_dir) 
        num = self.get_sample_num('geom_rmsd_')
        if num > 0:
            command = 'rm geom_rmsd_*'
            os.system(command)
        os.chdir(curr_dir)
        for i in range(xnum):
            for j in range(ynum):
                filenameold = 'geom_' + str(i+1) + '_' +  str(j+1) + '.xyz'
                filenamenew = work_dir +'/geom_rmsd_' + str(i+1) + '_'+ str(j+1) + '.xyz'
                os.chdir(work_dir) 
                reference = got_ref.make('isomap_dimen_traj_time_cluster.dat',i,j)
                os.chdir(curr_dir)
                print "%15s job is doing......." % filenameold
                print "   the reference is %i" % reference
                self.make_single(reference,filenameold,filenamenew) 
                self.vmd_plot(filenamenew,i+1,j+1)    
        self.MvPlot()

    def vmd_plot(self,filename,i_dim,j_dim):
        ifplot = self.ifplot
        i_dim = str(i_dim)
        j_dim = str(j_dim)
        workfile ='vmd_plotgroup.tcl'
        if ifplot == 'yes':
            if os.path.exists(filename):
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

    def MvPlot(self):
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


       

if __name__ == '__main__':
    jobs = mds_group_overlap()
    jobs.make_all_group()

