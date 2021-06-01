#! /usr/bin/env python

import os
import subprocess
import shutil


class ffRunner():
    """
    gamess runner setting..
    """
    vars = {}
    def __init__(self, config = {}):
        """
        parameter set.
        """
        self.files = {"inp": "gaussian.gjf",
                      "log": "gaussian.log"}
        
        if config != {}:
            files = config['files']
            self.files['inp'] = files['inp']
            self.files['log'] = files['log']
            
        return

    def check(self):
        """
        check variable
        """
        # check & use env variable.
        if 'g09root' in os.environ:
            mycmd = os.environ.get('g09root')
            print "use gaussian value<env>: DIRECTORY: ", verno
        else:
            print "g09root cannot be found ???"
            print "use default value: g09"
        self.vars['exec'] = "g09"
        
        return

    def run(self):
        """
        call the gamess runner
        """
        exec_name = self.vars['exec']
        jobfile = self.files['inp']
        logfile = self.files['log']
        mycmd = "%s %s >& %s;" % (exec_name, jobfile,
                                  logfile)
        mycmd = mycmd.strip()
        print mycmd,"@", os.getcwd()
        # os.system("rungms gamess.inp 06 2 >& gamess.log")
        # subprocess.call(mycmd, shell=True) 
        print "%", mycmd
        return

    def execjob(self):
        """
        define external variable and run
        """
        # variable useful.
        self.check()        
        self.run()
        return

        
if __name__ == "__main__":
    run = ffRunner()
    run.execjob()
    
    



