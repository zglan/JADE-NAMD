#! /usr/bin/env python

import os
import sys
from operator import itemgetter
import re
import shutil
from gms_template import *
from gms_create import *
from gms_parser import *
from gms_run import *

sys.path.append("../tools/")
import tools


# ao overlap from quantum chemistry calc.

class gms_overlap():
    """
    obtain ao overlap by a QC calculation.
    """
    def __init__(self, config = {}):
        """
        common data block
        """
        self.directory = {"work": "./QC_TMP/GMS_TMP", \
                          "work_prev": "./QC_TMP/GMS_TMP_PREV", \
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
        # Create the working directory
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
        # read template & create input gamess file
        myjob = gms_create(self.config)            
        
        myjob.modify(jobtype = "dimer")
        
        myjob.wrt_input()     
           
        return
    
    def run(self):
        """
        Run gamess
        """
        myjob = gms_run(self.config)
        myjob.caller()
        
        return
            
        
    def analyze(self):
        """
        read ao overlap matrix
        """
        myjob = gms_parser(self.config)
        myjob.get_ao()
        
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
    go = gms_overlap()
    go.worker()








    
        


