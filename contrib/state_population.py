#! /usr/bin/env python

import os
import shutil
#
# =============================
# @dulikai @qibebt
# 2014.4.12
# ver. 1a
# ===============================
#

class state_population():
    def __init__(self):
        """
        some pre-defined parameters
        """
        self.results = {}
        self.status = {}
        self.params = {}
        self.params['filename'] = "pop"
        self.params['resfilename'] = "pop_aver.dat"
        self.params['mydir'] = "tmpdirs"
        return


    def getcmd(self):
        """
        parameters
        """
        self.params['n_state'] = 3
        line = raw_input("number of states [default: 3]\n > ")
        if line.strip() != "":
            self.params['n_state'] = int(line)           
        
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
        
        filename = "hop_all_time.out"
        os.system("grep population " + filename + " > pop")
        fp = open("pop", "r")
        for i_step in xrange(n_step):            
            line = fp.readline()
            rec = line.split()            
            mystep = int(rec[0])
            i_time = float(rec[1])
            
            self.results[i_step][0] = mystep
            self.results[i_step][1] = i_time
            i = 2
            for val in rec[3:]:
                self.results[i_step][i] += float(val)
                i += 1
        # os.system("rm pop")
        return


    def read_traj(self):
        """
        read all traj...
        """
        traj = self.status['traj']
        n_step = self.status['n_step']
        n_state = self.params['n_state']
        
        self.results = [[] for i in xrange(n_step)]
        for i_step in xrange(n_step):
            self.results[i_step] = [0 for i in xrange(n_state+2)]
        
        for sid in traj:
            os.chdir(sid)
            self.__one_traj(sid)
            print "the directory <%s> is done.." % sid
            os.chdir("../")
            
        return


    def prep_traj(self):
        """
        deal & copy et al.  all traj...
        """
        filename = "hop_all_time.out"
        traj = self.status['traj']
        # backup mygeom.dat in one-directory
        mydir = self.params['mydir']
        if os.path.exists(mydir):
            shutil.rmtree(mydir)
        os.mkdir(mydir)
        jobfilename = self.params['filename']
        for sid in traj:
            os.chdir(sid)
            os.system("grep population " + filename + " > pop")
            print "running <%s> job.." % sid
            shutil.copy2(jobfilename, "../"+mydir+"/"+sid+".dat")
            os.chdir("../")

        return




    def aver_traj(self):
        """
        add values
        """
        n_step = self.status['n_step']
        steps = self.status['steps']
        n_state = self.params['n_state']
        
        for i_step in xrange(n_step):
            for i in xrange(2,n_state+2):
                self.results[i_step][i] /= steps[i_step]

        return



    def dump(self):
        """
        dump pe results
        """
        res = self.results
        n_state = self.params['n_state']
        filename = self.params['resfilename']
        mydir = self.params['mydir']
        fp = open(filename, "w")
        for mystep in res:
            print >>fp, "%10d %12.6f" % (mystep[0], mystep[1]),
            for val in mystep[2:]:
                print >>fp, "%15.8f" % (val),
            print >>fp, ""
        fp.close()
        shutil.copy2(filename, mydir)
        
        return


if __name__ == "__main__":
    pop = state_population()
    pop.getcmd()
    pop.get_status()
    pop.prep_traj()
    pop.read_traj()
    pop.aver_traj()
    pop.dump()
        

        
