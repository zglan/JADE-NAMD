#! /usr/bin/env python2

# ======================
# dulikai @qibebt
# @2014.5.10
# =====================

import os

# check the job status.
# do a report of the job status.
#

class jobstatus():
    def __init__(self):
        self.params = {}
        self.params['n_step'] = 0
        self.params['n_traj'] = 10
        self.params['mylist'] = []
        self.results = {}

        return

    def getcmd(self):
        """
        some parameters..
        """
        line = raw_input("number of steps: [default: 0] \n > ")
        if line.strip() != "":
            self.params['n_step'] = int(line)
        line = raw_input("number of trajectries (mybe a list of number): [default: 10] \n > ")
        if line.strip() != "":
            rec = line.split()
            if len(rec) == 1:
                self.params['n_traj'] = int(rec[0])
            else:
                self.params['n_traj'] = rec
        return


    def set_list(self):
        """
        myid could be a integer or a list
        to descript the name of the working directory
        """
        myid = self.params['n_traj']
        mylist = []
        if isinstance(myid, list):
            mylist = myid
        elif isinstance(myid, int):
            for i in xrange(1, myid+1):
                mylist.append(str(i))
        else:
            print "NO OTHER ID TYPE.. CHECK IT"
            exit(1)
        self.params['mylist'] = mylist        
        # initial results section
        for sid in mylist:
            self.results[sid] = {}
        return
    
    def __check_list_once(self, sid):
        """
        read one sid & check the completeness
        """
        filename = "./" + sid + "/pe_time.out"
        if os.path.isfile(filename) is not True:
            os.system("touch "+filename)
        n_line = len(open(filename).readlines())
        n_step = self.params['n_step']
        complete = 1
        ratio = 1.0
        if n_line < n_step:
            complete = 0
            ratio = float(n_line) / n_step
            print "the job <%s> is NOT complete.." % sid
        else:
            print "the job <%s> is complete.." % sid
            
        self.results[sid] = {'complete': complete, 'n_step': n_line,
                             'n_active': n_step, 'ratio': ratio}
        
        return
        

    def check_list(self):
        """
        check if the traj is complete or something else.
        """
        mylist = self.params['mylist']
        for sid in mylist:
             self.__check_list_once(sid)
            
        return
    
    def dump(self):
        """
        write the report..
        """
        fp = open("status.dat", "w")
        n_step = self.params['n_step']
        n_traj = len(self.params['mylist'])
        print >>fp, "%10d %10d" % (n_traj, n_step)
        print >>fp, ""
        res = self.results
        res = sorted(res.items(),key=lambda d:int(d[0]))
 
        for sid, val in res:
            print >>fp, "%10s %5d %10d %10d %12.6f" % \
            (sid, val['complete'], val['n_step'], val['n_active'], val['ratio'])
        fp.close()

        return


if __name__ == "__main__":
    chk = jobstatus()
    chk.getcmd()
    chk.set_list()
    chk.check_list()
    chk.dump()

