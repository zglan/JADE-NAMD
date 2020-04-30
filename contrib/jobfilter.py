#! /usr/bin/env python2

# =====================
# dulikai @qibebt
# @2014.5.10
# =====================

import os

# read the job status reports
# filter the undesired trajectory
# conditions:
# 1. >= n_step or
# 2. >= ratio  or
# 3. greedy
# 4. 1 & 2 & 3 is also ok
#
# then,
# generate a file to understand the job status
#

class jobfilter():
    def __init__(self):
        self.status = {}
        self.filter = {}
        self.params = {}

        return

    def get_status(self):
        """
        read in status.dat
        """
        filename = "status.dat"
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
        self.status = {'n_step': n_step, 'n_traj': n_traj,
                       'traj': traj        
        }
        return
        
        
    def getcmd(self):
        """
        read in control parameters
        """
        n_step = self.status['n_step']
        line = raw_input("conditions (maybe integer or float) [default: 1.0] \n > ")
        mystring = line.strip()
        if  mystring == "":
            self.status['ratio0'] = 1.0
            self.status['n_step0'] = n_step
        elif "." in mystring:
            self.status['ratio0'] = float(mystring)
            self.status['n_step0'] = int(n_step * float(mystring))
        else:
            self.status['n_step0'] = int(mystring)
        if self.status['n_step0'] > n_step:
            print "invalid value..."
            exit(1)
            
        return
        
        
    def select(self):
        """
        select ...
        """
        n_step0 = self.status['n_step0']
        n_traj = self.status['n_traj']
        traj = self.status['traj']
        traj2 = {}
        for key in traj:
            n_step = traj[key]['n_step']
            if n_step >= n_step0:
                traj[key]['n_active'] = n_step0
                traj2[key] = traj[key]
            else:
                continue
        n_traj2 = len(traj2)
        steps = [n_traj2 for i in xrange(n_step0)]
        self.filter = {'n_step': n_step0, 
                       'n_traj': n_traj2, 'traj': traj2, 'steps': steps      
        }
        
        return               
    
        
    def dump(self):
        """
        write the report..
        """
        fp = open("prepare.dat", "w")
        n_step = self.filter['n_step']
        n_traj = self.filter['n_traj']
        print >>fp, "%10d %10d" % (n_traj, n_step)
        print >>fp, ""
        res = self.filter['traj']
        res = sorted(res.items(),key=lambda d:int(d[0]))
        for sid, val in res:
            print >>fp, "%10s %5d %10d %10d %12.6f" % \
            (sid, val['complete'], val['n_step'], val['n_active'], val['ratio'])

        steps = self.filter['steps']
        print >>fp, ""
        print >>fp, "%10d" % n_step
        print >>fp, ""
        for i in xrange(n_step):
            print >>fp, "%10d %10d" % (i+1, steps[i])
        fp.close()
        return
        
if __name__ == "__main__":
    job = jobfilter()
    job.get_status()
    job.getcmd()
    job.select()
    job.dump()
    
    # generate filter.dat to describe each traj
    # generate prepare.dat for summary: total number of each step
    # traj list, n_step
