#! /usr/bin/env python

import os
import math
import shutil

# 
# notes:
# in pe_time.out file
# i_step&i_time&pe_all(1:n)&pe_index
# time in fs. & pe in a.u.
#
#

class dipole_time():
    def __init__(self):
        """
        some pre-defined parameters
        """
        self.results = {}
        self.status = {}
        self.params = {}
        self.params['filename'] = "di_time.out"
        self.params['resfilename'] = "di_aver.dat"
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


    def prep_traj(self):
        """
        deal & copy et al.  all traj...
        """
        traj = self.status['traj']
        # backup mygeom.dat in one-directory
        mydir = self.params['mydir']
        if os.path.exists(mydir):
            shutil.rmtree(mydir)
        os.mkdir(mydir)
        filename = self.params['filename']
        jobfilename = "dp"
        for sid in traj:
            os.chdir(sid)
            #print "grep -A1 \"Dipole moment\" " + filename + \
            #          "| grep \"X=\"" + "| awk '{print $2,$4,$6}'" + " > dp"
            os.system("grep -A1 \"Dipole moment\" " + filename + \
                      "| grep \"X=\"" + "| awk '{print $2,$4,$6}'" + \
                      "| nl -v 0" + " > dp")
            print "running <%s> job.." % sid
            shutil.copy2(jobfilename, "../"+mydir+"/"+sid+".dat")
            os.chdir("../")

        return

    

    def __one_traj(self, sid):
        """
        read in one traj.
        """
        this_traj = self.status['traj'][sid]
        n_step = this_traj['n_active']
 
        fp = open("dp", "r")
        for i_step in xrange(n_step):            
            line = fp.readline()
            val = line.split()         
        
            self.results[i_step][0] = int(val[0])          
            self.results[i_step][1] += float(val[1])
            self.results[i_step][2] += float(val[2])
            self.results[i_step][3] += float(val[3])
            self.results[i_step][4] += math.sqrt(float(val[1])*float(val[1]) +
                                                 float(val[2])*float(val[2]) +
                                                 float(val[3])*float(val[3]) 
                                                 )
        fp.close()       
      
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
            # i_step d_x d_y d_z d
            self.results[i_step] = [0 for i in xrange(1+3+1)]
        
        for sid in traj:
            os.chdir(sid)
            self.__one_traj(sid)
            print "the directory <%s> is done.." % sid
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
            for i in xrange(1,5):
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
        print >>fp, "# i_step i_time state(1-n_state) state(index)"        
        for mystep in res:
            print >>fp, "%10d" % (mystep[0]),
            for val in mystep[1:]:
                print >>fp, "%15.8f" % (val),
            print >>fp, ""
        fp.close()
        shutil.copy2(filename, mydir)
        return


if __name__ == "__main__":
    pe = dipole_time()
    pe.getcmd()
    pe.get_status()
    pe.prep_traj()
    pe.read_traj()
    pe.aver_traj()
    pe.dump()
        
