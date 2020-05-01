# python

import os
import sys
from operator import itemgetter
import re
import shutil
import time
import subprocess
from gau_template import *
from gau_create import *
from gau_parser import *

sys.path.append("../tools/")
import tools

# ao overlap from gaussian

class gau_overlap():
    """
    obtain ao overlap from gaussian output
    """
    def __init__(self, config = {}):
        """
        common data block
        """
        self.directory = {"work": "./QC_TMP/GAU_TMP", \
                          "work_prev": "./QC_TMP/GAU_TMP_PREV", \
                          "overlap": "./QC_TMP/OVERLAP"}
        self.files = {"interface": "interface.json", "template": "template.json"}

        self.config = config
        
        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files']  
            
            # working directory >>>
            self.directory = {}
            self.directory['root'] = root_dir
            self.directory['home'] = root_dir + "/" + dirs['home']
            
            self.directory['work'] = self.directory['home'] + "/" + dirs['work']
            self.directory['work_prev'] = self.directory['home'] + "/" + dirs['work_prev']
            self.directory['overlap'] = self.directory['home'] + "/" + dirs['overlap']

            self.files = {}
            self.files["template"] = files['template']
            self.files["interface"] = files['interface']    
    
            # run the job directly
            self.worker()       
    
        return
    
    def initilize(self):
        """
        prepare input file
        """
        # Create the working directory for Turbomole
        work_dir= self.directory['overlap']
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)
        # Copy all input files
        sourceFile = self.directory['work'] + '/interface.json'
        destFile   = self.directory['overlap'] + '/interface1.json'
        shutil.copy2(sourceFile, destFile)  
          
        sourceFile = self.directory['work_prev'] + '/interface.json'
        destFile   = self.directory['overlap'] + '/interface2.json'
        shutil.copy2(sourceFile, destFile)                
        # Enter the Turbomole working directory
        os.chdir(self.directory['overlap'])
                        
        return
        
    def prepare(self):
        # read template & create input gaussian file   
        gau = gau_create(self.config)            
        
        gau.modify(jobtype = "dimer")
        
        gau.wrt_gau_input()     
           
        return
    
    def run(self):
        # Run gaussian Work
        #g09 = self.config['command']['gaussian']
        #os.system(g09 + " gaussian.gjf" )
        #   Run gaussian
        exec_name = self.config['command']['gaussian']
        jobfile = "gaussian.gjf"
        # os.system(g09 + " gaussian.gjf" )
        proc = subprocess.Popen([exec_name, jobfile])
        start_time = time.time()
        print_freq = 1000
        #proc.wait()
        min_time = 1.0 # second
        i_time = 0
        while proc.poll() == None:
            # e.., maybe python can do something meaningful, while it wait for QC code
            # i guess, ..., haha
            i_time += 1
            time.sleep(min_time)
            if i_time % print_freq == 0:
                mid_time = time.time()
                interval = mid_time - start_time
                print "%s seconds passed, continuing.. [%s]" % (min_time*i_time, exec_name)
        end_time = time.time()

        print "##print check## QC exec. time interval: %10.2f seconds" % (end_time - start_time)
        if proc.poll() == None:
            if float(sys.version[:3]) >= 2.6:
                stdout,stderr = proc.terminate()
                print "return info:", stdout, stderr

        return
            
        
    def analyze(self):
        """
        read ao overlap matrix
        """
        gau = gau_log_parser(self.config)
        gau.get_ao_overlap()
        
        return
        
    def finalize(self):
        """ clear up """
        #   Go back to directory of dynamics work
        os.chdir(self.directory['home'])    
        
        return
        
    def worker(self):
        """ packing """
        self.initilize()
        self.prepare()
        self.run()
        self.analyze()
        self.finalize()
        
        return

if __name__ == "__main__":
    go = gau_overlap()
    go.worker()








    
        
