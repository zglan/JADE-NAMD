# python

import os
import sys
import re
import shutil
from gau_run import *
from gau_log2inp import *


class gau_onlyinp():
    """
    one step at zero time. electronic structure calc.
    """
    def __init__(self, config = {}):
        """
        common data block
        """
        self.directory = {"onlyinput": "./ONLYINPUT", \
                          "work_prev": "./QC_TMP/GAU_TMP_PREV"}
        self.files = {"interface": "interface.json", "template": "template.json",
                      "layer": "layer.json"}

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
            self.directory['onlyinput'] = root_dir + "/" + dirs['onlyinput']
            
            self.files = {}
            self.files["template"] = files['template']
            self.files["interface"] = files['interface']
            self.files["layer"] = files['layer']
            
            # run the job directly
            self.worker()     

        return 

        
    def initilize(self):
        """
        check interface & determine the implimented module to be called.
        """    
        # @ Check & Remove the old backup working directory
        inpdir = self.directory['onlyinput']
        inpfile = "onlyinputfiles.gjf"
        # check directory
        if os.path.isdir(inpdir):
            shutil.rmtree(inpdir)
        if not os.path.isdir(inpdir):
            os.makedirs(inpdir)
                       
        # Copy the template file
        sourceFile = self.files['template']
        destPath = inpdir + "/" + sourceFile
        if os.path.isfile(sourceFile):
            shutil.copy2(sourceFile, destPath)

        # Enter the working directory
        os.chdir(inpdir)

        return


    def prepare(self):
        """
        prepare gaussian input data
        based on template (user) or parameter (auto)
        """
        inpfile = "onlyinputfiles.gjf"
        # read template & create input gaussian file   
        obj = tools.load_data(self.files['template'])
        #
        fp = open(inpfile, "w")
        for line in obj['fcontent']:
            print >>fp, "%s" % line,
        fp.close()
        
        return
        
    def run(self):
        """
        call the QC code & confirm the running is ok. if not throw error messages.
        """
        # Run gaussian
        inpfile = "onlyinputfiles.gjf"
        r = gau_run(self.config)
        r.caller(filename = inpfile)
        
        return

    def analyze(self):
        """
        for surface hopping like calc., the required QC information was extraced.
        """
        gau = gau_log2inp(self.config)        
        # @check correction first
        gau.layer()

        return
        
    def finalize(self):
        """
        simply clean up the tmp dat. and so on.
        """
        #   Go back to directory of dynamics work
        #   Copy some QM calculations        
        #   Go back to directory of dynamics work
        #   Copy results of QM calculations
        sourceFile = self.files['layer']
        destPath = '../' + sourceFile
        shutil.copy2(sourceFile, destPath)
        os.chdir("../")

        print 'Finish QC calculation (ONLYINPUTFILES)'          
        
        return

        
    def worker(self):
        """
        wrap the whole process
        """
        # the working directory etc.
        self.initilize()
        # gen input file
        self.prepare()
        # run & call qc code
        self.run()
        # parser qc log file
        self.analyze()
        # clean & other env. config.
        self.finalize()
        
        return
        

if __name__ == "__main__":
    gau = gau_onlyinp()
    gau.worker()


    
