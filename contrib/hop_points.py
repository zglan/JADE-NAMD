#! /usr/bin/env python2

import os
import shutil
import mndotools

#
# =============================
# @dulikai @qibebt
# 2014.4.12
# ver. 1a
# ===============================
#

class hop_points():
    def __init__(self):
        """
        some pre-defined parameters
        """
        self.results = {}
        self.status = {}
        self.params = {}
        self.params['filename'] = "hop_points.dat"
        self.params['resfilename'] = "hop_record.dat"
        self.params['mydir'] = "tmpdirs"
        return


    def getcmd(self):
        """
        parameters
        """
        self.params['mode'] = "first"
        line = raw_input("the mode to extract hop points: <first/greedy/2to1> [default: first]\n > ")
        if line.strip() != "":
            self.params['mode'] = line.strip()       
        
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
        shell_txt = """
        grep 'The current state' ele_time.out > tmp1;
        grep 'The new state' ele_time.out > tmp2;
        awk '{print $1, $2, $6}' tmp1 > tmp10;
        awk '{print $6}' tmp2 > tmp20;
        paste tmp10 tmp20 > states_report.dat;
        rm -rf tmp1 tmp2 tmp10 tmp20;
        """
        for sid in traj:
            os.chdir(sid)
            os.system(shell_txt)
            print "running <%s> job.." % sid
            shutil.copy2("states_report.dat", "../"+mydir+"/states_"+sid+".dat")
            shutil.copy2("traj_time.out",  "../"+mydir+"/traj_"+sid+".xyz")
            os.chdir("../")
        return


    def __hop_one_traj(self, sid):
        """
        read in one hop point
        """
        filename = "states_"+sid+".dat"
        hop_filename = "hop_"+sid+".dat"
        #print os.getcwd()
        fp = open(filename, "r")
        any_points = []
        while True:
            line = fp.readline()
            if line.strip() == "":
                break
            rec = line.split()
            i_step = int(rec[0])
            i_time = float(rec[1])
            x_state = int(rec[2])
            n_state = int(rec[3])
            hop_flag = x_state - n_state
            mydict = {'i_step': i_step, 'i_time': i_time,
                         'x_state': x_state, 'n_state': n_state,
                         'hop_flag': hop_flag}
            any_points.append(mydict)
        fp.close()
        
        # dump new states_sid.dat
        # dump hop_sid.dat
        fp = open(filename, "w")
        fp_hop = open(hop_filename, "w")
        print >>fp, "%10s%12s%10s%10s%10s" % ("# I_STEP", "I_TIME", "I_STATE", "NEW_STATE", "HOP_FLAG")
        print >>fp_hop, "%10s%12s%10s%10s%10s" % ("# I_STEP", "I_TIME", "I_STATE", "NEW_STATE", "HOP_FLAG")
        for mydict in any_points:
            i_step = mydict['i_step']
            i_time = mydict['i_time']
            x_state = mydict['x_state']
            n_state = mydict['n_state']
            hop_flag = mydict['hop_flag']
            print >>fp, "%10d%12.6f%10d%10d%10d" % (i_step, i_time, x_state, n_state, hop_flag)
            if hop_flag != 0:
                print >>fp_hop, "%10d%12.6f%10d%10d%10d" % (i_step, i_time, x_state, n_state, hop_flag)
        fp.close()
        fp_hop.close()       
        return

    def __one_greedy_traj(self, sid):
        """
        out-put-first-structure
        """
        hop_filename = "hop_"+sid+".dat"
        traj_filename = "traj_"+sid+".xyz"
        greedy_filename = "greedy_"+sid+".xyz"
        first_filename = "first_"+sid+".xyz"
        t2o_filename = "2to1_"+sid+".xyz"
        fp = open(hop_filename, "r")
        snapshots = []
        snapshots_2_1 = []
        line = fp.readline()
        while True:
            line = fp.readline()
            if line.strip() == "":
                break
            rec = line.split()
            i_step = int(rec[0])
            snapshots.append(i_step-1)
            if (int(rec[2]) == 2 and int(rec[3]) == 1):
              snapshots_2_1.append(i_step-1)

        xyz = mndotools.XYZFile(traj_filename)
        if self.params['mode'] == "greedy":
            xyz.writeSnapshots(snapshots, greedy_filename)
        elif self.params['mode'] == "first":
            xyz.writeSnapshots(snapshots[0:1], first_filename)
        elif self.params['mode'] == "2to1":
               xyz.writeSnapshots(snapshots_2_1, t2o_filename)
        else:
            print "NO SUCH MODE.."
            exit(1)
        return
        
    def hop_traj(self):
        """
        read hop point
        """
        traj = self.status['traj']
        n_step = self.status['n_step']      
        
        os.chdir("tmpdirs")
        for sid in traj:
            print "check hopping condition  <%s> job.." % sid
            self.__hop_one_traj(sid)
            self.__one_greedy_traj(sid)
        os.chdir("../")
        return


    ###
    ###
    ### useless ...
    ##
    #
    def __one_traj(self, sid):
        """
        read in one traj.
        """
        this_traj = self.status['traj'][sid]
        n_step = this_traj['n_active']
        
        filename = "states_"+sid+".dat"
        fp = open(filename, "r")
        hop_flag = 0
        for i_step in xrange(n_step):            
            line = fp.readline()
            rec = line.split()            
            i_step = int(rec[0])
            i_time = float(rec[1])
            x_state = int(rec[2])
            n_state = int(rec[3])
            hop_flag += int(rec[4])
            this_step = {'i_step': mystep, 'i_time': i_time, 'hop_flag': hop_flag}
            self.results[i_step] = this_step
            
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
    pop = hop_points()
    pop.getcmd()
    pop.get_status()
    pop.prep_traj()
    pop.hop_traj()
#    pop.read_traj()
#    pop.aver_traj()
#    pop.dump()
        

        
