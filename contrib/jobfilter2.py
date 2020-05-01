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
                         'ratio': float(rec[3])
            }
        self.status = {'n_step': n_step, 'n_traj': n_traj,
                       'traj': traj        
        }
        return
        
        
    def getcmd(self):
        """
        read in control parameters
        """
        n_step = self.params['n_step']
        self.params['mode'] = "normal"
        line = raw_input("the filter mode: <normal/greedy> [default: normal] \n > ")
        if line.strip() != "":
            self.params['model'] = line.strip()
            
        line = raw_input("conditions (maybe integer or float) [default: 1.0] \n > ")
        mystring = line.strip()
        if  mystring == "":
            self.params['ratio0'] = 1.0
            self.params['n_step0'] = n_step
        elif "." in mystring:
            self.params['ratio0'] = float(mystring)
            self.params['n_step0'] = int(n_step * float(mystring))
        else:
            self.params['n_step0'] = int(mystring)
        if self.params['n_step0'] > n_step:
            print "invalid value..."
            exit(1)
            
        return
        
        
    def select(self):
        """
        select ...
        """
        n_step0 = self.params['n_step0']
        n_traj = self.status['n_traj']
        traj = self.status['traj']
        traj2 = []
        for i in xrange(n_traj):
            n_step = traj[i]['n_step']
            if n_step >= n_step0:
                traj2.append(traj[i])
            else:
                continue
        n_traj2 = len(traj2)
        steps = [n_traj2 for i in xrange(n_step0)]
        
        self.filter = {'n_step': n_step0, 'n_step_t': self.params['n_step']
                       'n_traj': n_traj2, 'traj': traj2, 'steps': steps      
        }
        
        return
        
    def greedy(self):
        """
        sum ... greedy case..
        """
        n_step_t = self.filter['n_step_t']
        n_traj = self.filter['n_traj']
        traj   = self.filter['traj']
        steps = [0 for i in xrange(n_step_t)]
        for i in xrange(n_traj):
            n_step = traj[i]['n_step']
            for j in xrange(n_step):
                steps[j] += 1
        self.filter['steps'] = steps
            
        return
            
    
    def filter(self):
        """
        do the main jobs..
        """
        self.getcmd()
        self.get_status()
        self.select()
        if self.params['mode'] == 'greedy':
            self.greedy()
            
        return
        
    def dump(self):
        """
        write the report..
        """
        fp = open("prepare.dat", "w")
        n_step = self.filter['n_step']
        n_traj = len(self.params['mylist'])
        print >>fp, "%10d %10d" % (n_traj, n_step)
        print >>fp, ""
        res = self.results
        for sid in res:
            val = res[sid]
            print >>fp, "%10s %5d %10d %12.6f" % \
            (sid, val['complete'], val['n_step'], val['ratio'])
        fp.close()

if __name__ == "__main__":
    job = jobfilter()
    job.filter()
    
    
    # generate filter.dat to describe each traj
    # generate prepare.dat for summary: total number of each step
    # traj list, n_step
