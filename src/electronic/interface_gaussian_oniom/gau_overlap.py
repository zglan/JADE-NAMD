# python

import os
import sys
from operator import itemgetter
import re
import shutil

from gau_create import *
from gau_parser import *
from gau_run import *

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
        joblist = ["high-model-overlap"]
        self.directory = {"work": "./QC_TMP/GAU_TMP", \
                          "work_prev": "./QC_TMP/GAU_TMP_PREV", \
                          "overlap": "./QC_TMP/OVERLAP", \
                          "root": "../../", \
                          "home": "../"}
        self.files = {"interface": "interface.json", "template": "layer.json", \
                      "joblist": joblist}

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

        # copy template & interface
        sourceFile = self.files['template']
        destFile   = self.directory['overlap'] + "/" + self.files['template']
        shutil.copy2(sourceFile, destFile)        
        # Copy all input files
        sourceFile = self.directory['work'] + '/interface.json'
        destFile   = self.directory['overlap'] + '/interface1.json'
        shutil.copy2(sourceFile, destFile)  
        sourceFile = self.directory['work_prev'] + '/interface.json'
        destFile   = self.directory['overlap'] + '/interface2.json'
        shutil.copy2(sourceFile, destFile)                
        # Enter the Turbomole working directory
        os.chdir(self.directory['overlap'])
        print "NOW the Working Directory is:\n", os.getcwd()
                        
        return
        
    def prepare(self):
        # read template & create input gaussian file   
        gau = gau_create(self.config)            

        gau.create_ao()

        self.files['joblist'] = gau.joblist

        return
    
    def run(self):
        """
            Run gaussian Work
        """
        # collect input file list
        filelist = [x+".gjf" for x in self.files['joblist']]
        # Run gaussian
        g = gau_run()
        g.caller(filename = filelist)

        return
            
        
    def analyze(self):
        """
        read ao overlap matrix
        """
        gau = gau_parser(self.config)
        gau.get_ao()
        
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








    
        
