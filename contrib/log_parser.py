#! /usr/bin/env python

import os




class LogParser():
    def __init__(self):

        return

    def state_pop(self):
        """
        open log file and read current state
        """
        mystr = "100ps  1ps  1ps-gms  50ps  cam  ch2nh2  guanine  pbe  population_ana  wigne"
        nstep = 600

        traj = mystr.split()
        s1 = [0 for i in xrange(nstep)]
        s2 = [0 for i in xrange(nstep)]
        s3 = [0 for i in xrange(nstep)]
        for itraj in traj:
            os.chdir(itraj)
            os.system("grep 'current state' hop_all_time.out | awk '{print $2,$5}' > t0")
            fp = open("t0", "r")
            for j in xrange(step):
                line = fp.readline()
                if line.strip() == "":
                    continue
                print i, j, line
                i_state = int(line.strip())
                if i_state == 3:
                    s3[j] += 1.0/traj
                if i_state == 2:
                    s2[j] += 1.0/traj
                if i_state == 1:
                    s1[j] += 1.0/traj

            os.chdir("../")

        fp = open("rs.dat", "w")
        time_step = 0.0
        for a, b, c in zip(s1,s2,s3):
            time_step += 0.5
            print >>fp, "%10.2lf%10.2lf%10.2lf%10.2lf" % (time_step, a, b, c)
        fp.close()

        return
        
        
### main program
if __name__ == "__main__":
    log = LogParser()
    log.state_pop()




