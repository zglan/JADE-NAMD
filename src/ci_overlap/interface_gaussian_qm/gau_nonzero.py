# python

import os
import sys
import re
import shutil
import time
import subprocess
from gau_create import *
from gau_parser import *


class gau_nonzero():
    """
    one step at zero time. electronic structure calc.
    """
    def __init__(self, config = {}):
        """
        common data block
        """
        self.directory = {"work": "./QC_TMP/GAU_TMP", \
                          "work_prev": "./QC_TMP/GAU_TMP_PREV"}
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
        # @ Check & Remove the old backup working directory 
        prev_dir = self.directory['work_prev']
        if os.path.exists(prev_dir):
          shutil.rmtree(prev_dir)          
        # Create the new backup directory
        if not os.path.exists(prev_dir):
            os.makedirs(prev_dir)          
                
        # Copy the old output to other directory
        sourcePath = self.directory['work']
        destPath   = self.directory['work_prev']        
        sourcePath_files = os.listdir(sourcePath)
        for file_name in sourcePath_files:
            full_file_name = os.path.join(sourcePath, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, destPath)

        # Copy new interface & copy template
        sourceFile = self.files['template']
        shutil.copy2(sourceFile, destPath)         
        interface_File =self.files['interface']
        if os.path.isfile(interface_File):
            shutil.copy2(interface_File, sourcePath)

        # Remove *.dat file
        qm_resultfile = 'qm_results.dat'
        if os.path.isfile(qm_resultfile):
            os.remove(qm_resultfile)

        # Enter the Turbomole working directory
        os.chdir(self.directory['work'])
        
        #   Delete some old files 
        files = os.listdir("./")
        for filename in files:
            pos= re.search('(.*).chk|(.*).dat|(.*).log', filename)      
            if pos is not None:
                os.remove(filename)         

        return

    def prepare(self):
        """
        prepare gaussian input data
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
        for surface hopping like calc., the required QC information was extraced.
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
        sourceFile = self.directory['work'] + '/qm_results.dat'
        destPath = './'
        shutil.copy2(sourceFile, destPath)

        sourceFile = self.directory['work'] + '/qm_other.dat'
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
        

if __name__ == "__main__":
    gau = gau_nonzero()
    gau.worker()


    
