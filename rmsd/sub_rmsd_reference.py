import os
import numpy as np
import shutil
import math

class got_refer():
    def __init__ (self) :
        self.savefile = 'split.dat'
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.xnum = 1
        self.ynum = 1

    def two_pot_distance(self,x1=0,y1=0,x2=1,y2=1):
        val = (x1-x2)**2 + (y1-y2)**2
        distance = math.sqrt(val)
        return distance
     
    def read_para(self):

        workfile = self.savefile
        if os.path.exists(workfile):
            fp = open(workfile,"r")
            line = fp.readline()
            line = fp.readline()
            xmin,xmax,ymin,ymax,xnum,ynum = line.split()
#            print "%10s%10s%10s%10s%10s%10s" % ('xmin','xmax','ymin','ymax','xnum','ynum')
#            print "%10.2f%10.2f%10.2f%10.2f%10d%10d" % (float(xmin),float(xmax),float(ymin),float(ymax),int(xnum),int(ynum))
        else:
            print "Error: There is not a file named split.dat \n\tMaybe you should run plot_mds.py first"
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.xnum = xnum
        self.ynum = ynum
        return
    
    def mds_got_reference (self,file_result = 'isomap_dimen_traj_time_cluster.dat',xnu=7,ynu=2):

        xmin = float(self.xmin) 
        xmax = float(self.xmax) 
        ymin = float(self.ymin)
        ymax = float(self.ymax) 
        xnum = int(self.xnum) 
        ynum = int(self.ynum) 
        
        xx = np.loadtxt(file_result)
        rmsd = xx[:,0:2]
        grou = xx[:,-3]
        nu = np.shape(xx)
        num = nu[0]

        x_range = xmax - xmin 
        y_range = ymax - ymin
        d_x = float(x_range)/xnum
        d_y = float(y_range)/ynum
  
        i_dim1 = xnu
        i_dim2 = ynu
        x_low  = xmin + i_dim1 * d_x
        x_high = xmin + (i_dim1+1) * d_x
        x_between= (x_low + x_high) / 2          
        y_low  = ymin + i_dim2 * d_y
        y_high = ymin + (i_dim2+1) * d_y
        y_between = (y_low + y_high)/2
      #  distance_mina = self.two_pot_distance(x_between,y_between,x_low,y_low)
        distance_mina = 100000000
        reference = 1
        number = 0
        for i in range(num):
#            print i_dim1,i_dim2,i
            if xx[i,-2] == (i_dim1+1) and xx[i,-1] == (i_dim2+1):
                number = number+1
                distan = self.two_pot_distance(x_between,y_between,rmsd[i,0],rmsd[i,1])
#                print distance_mina,distan
                if distan < distance_mina:
#                    print 'HA'
                    distance_mina = distan
                    reference = number
#                    print reference
#        print 'end:'
#        print i_dim1+1,i_dim2+1,reference                      

        return int(reference)

def make(filename,i,j) :
    jobs = got_refer()
    jobs.read_para()
    ref = jobs.mds_got_reference(filename,i,j)
    return ref

if __name__ == '__main__' :
    jobs = got_refer()
    a = jobs.two_pot_distance() 
    print a
    os.chdir('all')
    jobs.read_para()
    jobs.mds_group_lim()
