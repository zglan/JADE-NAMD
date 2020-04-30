#! /usr/bin/python

import os
import shutil
from gau_template import *
from gau_create import *
from gau_parser import *

class gau_zero:
    """
    one step at zero time. electronic structure calc.
    """
    def __init__(self, config = {}):
        """
        common data block, cannot be inherted by subclass automatically
        """
        self.directory = {"qc": "./QC_TMP", "work": "./QC_TMP/GAU_TMP", "home": "./QC_TMP" }
        self.files = {"template": "template.json", "interface": "interface.json"}
        self.config = config
        
        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files']            
            
            # working directory & files >>>
            self.directory = {}
            self.directory['root'] = root_dir
            self.directory['home'] = root_dir + "/" + dirs['home']
            self.directory['work'] = self.directory['home'] + "/" + dirs['work']
            self.files = {}
            self.files["template"] = files['template']
            self.files["interface"] = files['interface']
            
            # run the job directly
            self.worker()
        
        return
 
    def initilize(self):
        """
        check interface & determine the implimented module to be called.
        """
        # make directory
        # @ Check & Remove the old working directory for QC calc. 
        qc_dir = self.directory['home']
        if os.path.exists(qc_dir):
          shutil.rmtree(qc_dir)          
        # Create the new HOME working directory for QC
        if not os.path.exists(qc_dir):
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

    def prepare(self):
        """
        generate gaussian input file
        based on template (user) or parameter (auto)
        """
        # read template & create input gaussian file   
        gau = gau_create(self.config)            
        
        gau.modify(jobtype = "td")
        
        gau.wrt_gau_input()
 
        return
        
    def run(self):
        """
        call the QC code & confirm the running is ok. if not throw error messages.
        """
        #   Run gaussian
        g09 = self.config['command']['gaussian']
        os.system(g09 + " gaussian.gjf" )

        return

    def analyze(self):
        """
        extract data used for surface hopping dynamics., 
        the required QC information was extraced.
        """
        gau = gau_parser(self.config)        
        # @check correction first
        gau.get_td_dat()
     
        return
        
    def finalize(self):
        """
        simply clean up the tmp dat. and so on.
        """
        #   Go back to directory of dynamics work
        #   Copy results of QM calculations
        
        #   Go back to directory of dynamics work
        os.chdir(self.directory['root'])
                            
        #   Copy results of QM calculations 
        sourcePath = self.directory['work']
        sourceFile = sourcePath + '/' + 'qm_results.dat'
        destPath = './'
        shutil.copy2(sourceFile, destPath)

        sourceFile = sourcePath + '/' + 'qm_other.dat'
        destPath = './'
        shutil.copy2(sourceFile, destPath)

        print 'Finish QC calculation'          
        
        return
        
    def worker(self):
        """
        wrap the whole process
        """
        self.initilize()
        self.prepare()
        self.run()
        self.analyze()
        self.finalize()        
        return        



# Main Program
if __name__ == "__main__":
    gz = gau_zero()
    gz.worker()


    