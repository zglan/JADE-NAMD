#! /usr/bin/env python

import os
import sys
import shutil

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/../tools/")
import tools

class setupEnv:
    """ setup calculation environment """
    def __init__(self, config = {}):
        """
        parameter set.
        """
        self.directory = {"qc": "./QC_TMP", "work": "./QC_TMP/GAU_TMP", \
                          "home": "./QC_TMP" }
        self.files = {"template": "template.json",
                      "inp": "gaussian.gjf",
                      "log": "gaussian.log",
                      "interface": "interface.json"}
        
        if config != {}:
            self.config = config
            #
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files']

            self.directory = {}
            self.files = {}
            #
            self.directory['root'] = root_dir
            self.directory['home'] = root_dir + "/" + dirs['home']
            self.directory['work'] = self.directory['home'] + "/" + dirs['work']

            self.files['template'] = files['template']
            self.files['inp'] = files['inp']
            self.files['log'] = files['log']
            self.files['interface'] = files['interface']
            
        return
    
    def setup(self):
        """
        check interface, make directory,
        setup the job exec. environment
        """
        # make directory
        # @ Check & Remove the old working directory for QC calc. 
        qc_dir = self.directory['home']
        if os.path.exists(qc_dir):
          shutil.rmtree(qc_dir)          
        # Create the new HOME working directory for QC
        else:
            os.makedirs(qc_dir)
 
        # working directory: such as GAU_TMP or TUR_TMP et al.
        destPath = self.directory['work']
        if not os.path.exists(destPath):
            os.makedirs(destPath)            
 
        # copy template & interface
        sourceFile = self.files['template']
        shutil.copy2(sourceFile, destPath)   
 
        sourceFile = self.files['interface']     
        if os.path.isfile(sourceFile):
            shutil.copy2(sourceFile, destPath)
        else :
            print 'Check the interface file generated by dynamics code!'
            exit(1)            
        #   Enter the QC working directory
        os.chdir(destPath)                    
        print "NOW the Working Directory is:\n", os.getcwd()
       
        return         


if __name__ == "__main__":
    config = tools.load_data("config.in")
    s = SetupEnv(config)
    s.setup()
    
    
        