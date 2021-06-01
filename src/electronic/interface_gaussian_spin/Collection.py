#!/usr/bin/python
import os
import sys
import re
import shutil

sys.path.append("../tools/")
import tools

class gau_nac():
    """
    calc. nac data.
    """
    def __init__(self, config = {}):
        """
        automatic nac calc.
        """
        self.directory = {'work': "./QC_TMP/GAU_TMP", \
                          'work_prev': "./QC_TMP/GAU_TMP", \
                          "overlap": "./QC_TMP/OVERLAP", \
                          "nac": "./QC_TMP/NAC"  \
                          }
        self.files = {'dimension': "dimension.json"}
        
        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files']            
            
            # working directory & files >>>
            self.directory = {}
            self.directory['root'] = root_dir
            self.directory['home'] = root_dir + "/" + dirs['home']
            
            self.directory['work'] = self.directory['home'] + "/" + dirs['work']
            self.directory['work_prev'] = self.directory['home'] + "/" + dirs['work_prev']
            self.directory['overlap'] = self.directory['home'] + "/" + dirs['overlap']
            self.directory['nac'] = self.directory['home'] + "/" + dirs['nac']
            self.files = {}
            self.files["dimension"] = files['dimension']
            
            # run the job directly
            self.worker()
                        
        return
        

    def prepare(self):
        """
        first, prepare work dir; then, the necessary files.
        """
        # 
        
        return

    def run(self):
        """
        call another standalone program to deal with nac.
        """
        
        return
        
    def dump(self):
        """
            dump necessary data of nac
        """
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
        fp = open('wavefuction_overlap.dat','r') 
        ci_overlap = fp.readlines()        
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

        return

    def finilize(self):
        """
        finish the current step & prepare for the following step
        """
        # file man. & back up
        shutil.copyfile("./qm_result_update.dat", "./qm_results.dat")
        shutil.copyfile("./qm_results.dat", "../../qm_results.dat")          
        #   Go back to directory of dynamics work
        os.chdir("../../")     
           
        return
        
    def worker(self):
        """
        prepare; run; dump; finilize
        """
        self.prepare()
        self.run()
        self.dump()
        self.finilize()
        
        return
        

# main program.
if __name__ == "__main__":    
    n = gau_nac() 
    n.worker()

   
     
     
      
