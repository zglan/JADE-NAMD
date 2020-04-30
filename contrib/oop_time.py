#! /usr/bin/env python

import os
import shutil
import optparse
import sys

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/btools/")

# my module
from xyzStruct import xyzStruct
from xyzTraj import xyzTraj
from bMolShape import bMolShape

# 
# notes:
# Analysis of kinetic energy
#
#

class oop_time():
    def __init__(self):
        """
        some pre-defined parameters
        """
        self.results = {}
        self.status = {}
        self.params = {}
        self.params['filename'] = "myoop.dat"
        self.params['resfilename'] = "oop_aver.dat"
        self.params['mydir'] = "tmpdirs"
        self.params['job_type'] = 1
        self.params['n_col'] = 2
        self.params['trajfile'] = 'traj_time.out'
        
        return


    def getcmd(self):
        """
        parameters setup
        """
        line = raw_input("enter the index range  <i.e. 1-5,9,11>: \n >")
        frg_ndx1 = line.strip()
        self.params['frg_ndx1'] = frg_ndx1
            
        line = raw_input("enter the filename (xyz format) [default: vel_time.out]: \n > ")
        if line.strip() != "":
            fname = line.strip()
            
        ndx_flag = 1
        line = raw_input("Atom index start from 0 or 1 [default: 1]: \n > ")
        if line.strip() != "":
            ndx_flag = int(line)
                
        self.params['ndx_flag'] = ndx_flag
        
        return


    def get_status(self):
        """
        read in prepare.dat
        """
        filename = "prepare.dat"
        fp = open(filename, "r")
        line = fp.readline()
        rec = line.split()
        n_traj = int(rec[0]); n_step = int(rec[1])
        line = fp.readline()
        traj = {}
        for i in xrange(n_traj):
            line = fp.readline()
            rec = line.split()
            key = rec[0]
            traj[key] = {'complete': int(rec[1]), 'n_step': int(rec[2]),
                         'n_active': int(rec[3]), 'ratio': float(rec[4])
            }

        line = fp.readline()
        line = fp.readline()
        line = fp.readline()
        steps = [0 for i in xrange(n_step)]
        for i in xrange(n_step):
            line = fp.readline()
            rec = line.split()
            steps[i] = int(rec[1])
        self.status = {'n_step': n_step, 'n_traj': n_traj,
                       'traj': traj, 'steps': steps  
        }
        return        


    def __one_traj(self, sid):
        """
        read in one traj.
        """
        this_traj = self.status['traj'][sid]
        n_step = this_traj['n_active']
        n_col = self.params['n_col']
        
        filename = self.params['filename']
        fp = open(filename, "r")
        line = fp.readline()
        line = fp.readline()
        line = fp.readline()
        for i_step in xrange(n_step):            
            line = fp.readline()
            rec = line.split()            
            mystep = int(rec[0])            
            self.results[i_step][0] = mystep
            for i_col in xrange(1,n_col):
                val = float(rec[i_col])
                self.results[i_step][i_col] += val
        fp.close()

        return


    def read_traj(self):
        """
        read all traj...
        """
        traj = self.status['traj']
        n_step = self.status['n_step']
        n_col = self.params['n_col']
         
        self.results = [[] for i in xrange(n_step)]
        for i_step in xrange(n_step):
            self.results[i_step] = [0 for i in xrange(n_col)]
        
        for sid in traj:
            os.chdir(sid)
            self.__one_traj(sid)            
            os.chdir("../")
            
        return


    def get_dist(self, flag = 1):
        """
        process traj of xyz format
        """
        fname = self.params['trajfile']
        frg_ndx1 = self.params['frg_ndx1']
        
        # traj. info
        traj = xyzTraj()
        traj.read_it(filename = fname)
        # det. shape    
        shape = bMolShape()
        dist = []; i = 0;
        while True:
            frg1 = traj.fragment(frg_ndx1, flag)
            t = shape.outofplane_dist(frg1)
            i += 1
            dist.append([i, t])
            if traj.next_model() == 0:
                break

        filename = self.params['filename']
        fp = open(filename, "w")
        print >>fp, "# ID out of plane dist"
        print >>fp, "#"
        print >>fp, "#"
        for d in dist:
            print >>fp, "%10d%15.8f" % (d[0], d[1])
        
        fp.close()   
        
        return dist

  
    def prep_traj(self):
        """
        read all traj...
        """
        traj = self.status['traj']
        filename = "myplot.plt"
        fp = open(filename, "w")
        print >>fp, "plot ",
        # backup mygeom.dat in one-directory
        mydir = self.params['mydir']
        if os.path.exists(mydir):
            shutil.rmtree(mydir)
        os.mkdir(mydir)
        jobfilename = self.params['filename']
        for sid in traj:
            os.chdir(sid)
            print "running <%s> job.." % sid
            self.get_dist(flag = self.params['ndx_flag'])
            
            shutil.copy2(jobfilename, "../"+mydir+"/"+sid+".dat")
            os.chdir("../")
            print >>fp, "'./" + sid+ ".dat" +  "'" + " u 1:2,",
        fp.close()

        return

    def aver_traj(self):
        """
        add values
        """
        n_step = self.status['n_step']
        steps = self.status['steps']
        n_col = self.params['n_col']
        
        for i_step in xrange(n_step):
            for i_col in xrange(1,n_col):
                self.results[i_step][i_col] /= steps[i_step]

        return



    def dump(self):
        """
        dump pe results
        """
        res = self.results
        filename = self.params['resfilename']
        mydir = self.params['mydir']
        fp = open(filename, "w")
        for mystep in res:
            print >>fp, "%10d " % (mystep[0]),
            for val in mystep[1:]:
                print >>fp, "%15.8f" % (val),
            print >>fp, ""
        fp.close()
        
        shutil.copy2(filename, mydir)

        return

    
if __name__ == "__main__":
    pe = oop_time()
    pe.getcmd()
    pe.get_status()
    pe.prep_traj()
    pe.read_traj()
    pe.aver_traj()
    pe.dump()
        
