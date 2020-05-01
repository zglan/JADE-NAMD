# python
import os
import sys
import shutil

from firstStep import *
from nextStep import *
from Template import *
from buildSOC import *
from buildNAC import *

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/../tools/")
import tools

# dulikai
# 2015.08 
# @ qibebt
#
#

class Package():
    def __init__(self):
        """ gaussian interface """
        
        self.files = {"interface": "interface.json", "dyn": "inp.json", \
                      "gau_template": "./GAU_EXAM/gau_template.gjf"}
        # make a full dictionary for the gaussian job
        self.config = {}
        self.dyn = {}
        
        # directly call
        self.worker()
        
        return        
        
    def prepare(self):
        """ load configure file """
        # dynamic info.
        self.dyn  = tools.load_data(self.files['dyn'])
        # gaussian directory structure info.
        #script_dir = os.path.split(os.path.realpath(sys.argv[0]))[0]
        script_dir = os.path.split(os.path.realpath(__file__))[0]
        self.config = tools.load_data(script_dir + "/config.in")
        self.config['root'] = os.getcwd()
        # attach dyn info in config vars
        self.config.update(self.dyn['quantum'])
        return
        
    def run(self):
        """
        raise the calc. code.
        """
        # load interface file
        interface = tools.load_data(self.files['interface'])
        it = int(interface['parm']['i_time'])
 
        qm_method = int(self.dyn['quantum']['qm_method'])
        print "QM_METHOD: ", qm_method
        
        config = self.config
        # 
        # make template
        Template(self.config)
        # Start the QC calculations
        if it == 0:
            firstStep(config)
            buildSOC(config)
            buildNAC(config)
        elif it > 0:
            nextStep(config)
            buildSOC(config)
            buildNAC(config)
        else:
            print "Error: keyword 'it':", it
            sys.exit(0)                
        
        return
        
    def finalize(self):
        """ collect qm out and dump it in standard format. """
        # open file & read data.
        fp = open('qm_results.dat','r')
        qms = fp.readlines()
        fp.close()
        # num. of states
        for cur_line in qms:
            i_find_n_state = re.search ('Number of states', cur_line)
            if i_find_n_state is not None:
                n_state = int (cur_line.split()[-1]) 
          
        # open & read wf-overlap
        fp = open('soc.dat','r') 
        nac = fp.readlines()        
        fp.close()         
          
        # open & read wf-overlap
        fp = open('nac_time.dat','r') 
        nac = fp.readlines()        
        fp.close()         
        
        # dump data.
        n_line = len(qms)
        fp = open('qm_result_update.dat','w')
        for i_line in range(n_line - n_state*n_state - 2): # n_state^2 + 2 is wf data.
            fp.write(''+str(qms[i_line][:-1]) + '  \n')
            
            
            
        fp.write('Wave-function overlap between R and R+dR \n')          
        i_line=1 
        
        for i_state in range(n_state):
            for j_state in range(n_state):    
                fp.write('S'+str(i_state)+'   S'+str(j_state)+'    '+ str(ci_overlap[i_line].split()[-1])+'  \n')
 
                i_line = i_line + 1
        fp.write('----------------------------------------------')
        fp.close()           
        
        # file man. & back up
        shutil.copyfile("./qm_result_update.dat", "./qm_results.dat")
        shutil.copyfile("./qm_results.dat", "../../qm_results.dat")          
        #   Go back to directory of dynamics work
        os.chdir("../../")     
           
        return

        
    def worker(self):
        self.prepare()
        self.run()
        self.finilize()
        return

# main program.
if __name__ == "__main__":    
    n = Package()
    n.worker()







