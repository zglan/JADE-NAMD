#! /usr/bin/env python

import os
import time
import subprocess
import shutil

# exec g09 or g03 

class gau_run():
    """
    gamess runner setting..
    """
    def __init__(self, config = {}):
        """
        parameter set.
        """
        self.config = config
        self.files = {"template": "template.json"}
        self.vars = {}
        self.vars['exec'] = "g09"
        self.vars['print_freq'] = 1000
                
        if config != {}:
            self.vars['exec'] = self.config['command']['exec']
            if 'print_delta_time' in self.config.keys():
                self.vars['print_delta_time'] = self.config['quantum']['print_delta_time']
        
        return

    def check(self):
        """
        check variable
        """
        if self.config == {}:
            return
        # check & use env variable.
        if 'g09root' in os.environ:
            path = os.environ.get('g09root')
            print "the path of g09root<env>: path: ", path
        elif 'g03root' in os.environ:
            path = os.environ.get('g03root')
            print "the path of g03root<env>: path: ", path
        else:
            print "gaussian env path cannot be found ???"
        self.vars['path'] = path
        
        if 'GAUSS_SCRDIR' in os.environ:
            scrdir = os.environ.get('GAUSS_SCRDIR')
            print "use GAUSS_SCRDIR  value<env>: ", scrdir
        else:
            print "GAUSS_SCRDIR cannot be found ???"
        self.vars['scrdir'] = scrdir
        
        return

    
    def run(self, jobfile):
        """
        call the gamess runner
        """
        # check config-ini variable
        # default variables: g09
        exec_name = self.vars['exec']
        # jobfile = self.files['job_inp']
        mycmd = "%s %s" % (exec_name, jobfile)
        print "RUNNING..", mycmd, "@", os.getcwd()
        
        #rcode = subprocess.call(mycmd, shell=True)
        proc = subprocess.Popen([exec_name, jobfile])
        start_time = time.time()
        print_freq = self.vars['print_freq']
        #proc.wait()
        min_time = 0.25 # second
        i_time = 0
        while proc.poll() == None:
            # e.., maybe python can do something meaningful, while it wait for QC code
            # i guess, ..., haha
            i_time += 1
            time.sleep(min_time)
            if i_time % print_freq == 0:
                mid_time = time.time()
                interval = mid_time - start_time
                print "%s seconds passed, continuing.. [%s]" % (min_time*i_time, mycmd)
        end_time = time.time()
        print "##print check## QC exec. time interval: %10.2f seconds" % (end_time - start_time)
        if proc.poll() == None:
            if float(sys.version[:3]) >= 2.6:
                stdout,stderr = proc.terminate()
                print "return info:", stdout, stderr
        return


    def caller(self, filename = ""):
        """
        define external variable and run
        """
        # variable useful.
        self.check()

        if isinstance(filename, list):
            for jobfile in filename:
                self.run(jobfile)
        else:
            self.run(filename)

        return


# main program
if __name__ == "__main__":
    g = gau_run()
    g.caller(filename = "highmodel.gjf")

    


