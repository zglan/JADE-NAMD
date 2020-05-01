#! /usr/bin/env python

import os
import optparse
import geoman

# 
# notes:
# in pe_time.out file
# i_step&i_time&pe_all(1:n)&pe_index
# time in fs. & pe in a.u.
#
#


class geom_collect():
    def __init__(self):
        """
        some pre-defined parameters
        """
        self.results = {}
        self.status = {}
        self.params = {}

        
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
        
        filename = "mygeom.tmp"
        fp = open(filename, "r")
        line = fp.readline()
        line = fp.readline()
        line = fp.readline()
        for i_step in xrange(n_step):            
            line = fp.readline()
            rec = line.split()            
            mystep = int(rec[0])
            val = float(rec[1])
            
            self.results[i_step][0] = mystep
            self.results[i_step][1] += val

        return


    def read_traj(self):
        """
        read all traj...
        """
        traj = self.status['traj']
        n_step = self.status['n_step']
         
        self.results = [[] for i in xrange(n_step)]
        for i_step in xrange(n_step):
            self.results[i_step] = [0 for i in xrange(2)]

        
        for sid in traj:
            os.chdir(sid)
            self.__one_traj(sid)            
            os.chdir("../")
            
        return




    def aver_traj(self):
        """
        add values
        """
        n_step = self.status['n_step']
        steps = self.status['steps']
         
        for i_step in xrange(n_step):
            self.results[i_step][1] /= steps[i_step]

        return



    def dump(self):
        """
        dump pe results
        """
        res = self.results
        filename = "geom_aver.dat"
        fp = open(filename, "w")
        for mystep in res:
            print >>fp, "%10d %12.6f" % (mystep[0], mystep[1]),
            for val in mystep[2:]:
                print >>fp, "%15.8f" % (val),
            print >>fp, ""
        fp.close()

        return

    
if __name__ == "__main__":
    pe = geom_collect()
    pe.get_status()
 
    pe.read_traj()
    pe.aver_traj()
    pe.dump()
        
