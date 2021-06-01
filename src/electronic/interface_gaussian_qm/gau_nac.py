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
        very ok nac
        """
        self.directory = {'work': "./QC_TMP/GAU_TMP", \
                          'work_prev': "./QC_TMP/GAU_TMP", \
                          "overlap": "OVERLAP", \
                          "nac": "NAC"  \
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
        work_dir = self.directory['nac']
        if os.path.exists(work_dir):
	    shutil.rmtree(work_dir)
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)
   
        sourceFile = self.directory['work_prev'] + '/mo.dat'
        destFile = self.directory['nac'] + '/mo_1.dat'
        shutil.copy2(sourceFile, destFile)
 
        sourceFile = self.directory['work_prev'] + '/ci.dat'
        destFile   = self.directory['nac'] + '/ci_1.dat'
        shutil.copy2(sourceFile, destFile)
 
        sourceFile = self.directory['work'] + '/mo.dat'
        destFile =   self.directory['nac'] + '/mo_2.dat'
        shutil.copy2(sourceFile, destFile)

        sourceFile = self.directory['work'] + '/ci.dat'
        destFile =   self.directory['nac'] + '/ci_2.dat'
        shutil.copy2(sourceFile, destFile)

        sourceFile = self.directory['work'] + '/qm_results.dat'
        destFile   = self.directory['nac']  + '/qm_results.dat'
        shutil.copy2(sourceFile, destFile)
        
        sourceFile = self.directory['work'] + '/' + self.files['dimension']
        destFile   = self.directory['nac']  + '/' + self.files['dimension']
        shutil.copy2(sourceFile, destFile)
        
        sourceFile = self.directory['overlap'] + '/ao_overlap.dat'
        destFile =   self.directory['nac']  + '/ao_overlap.dat'
        shutil.copy2(sourceFile, destFile)

        os.chdir(work_dir)
        
        # load internal data.
        filename = self.files['dimension']
        dim = tools.load_data(filename)
        
        n_atom = dim['n_atom']      # Number of atom
        n_state = dim['n_state']    # Number of states
        n_ao = dim['n_basis']       # number of basis functions
        n_occ = dim['nocc_allA']    # number of occupied orbitals        

        fileout1=open('main_overlap_slater_input','w')
        fileout1.write('                        read (*,*)  \n')
        fileout1.write(''+str(n_atom)+'               read (*,*) n_atom \n')
        fileout1.write(''+str(n_ao)+'                 read (*,*) n_ao \n')
        fileout1.write(''+str(n_occ)+'               read (*,*) n_ele_alpha \n')
        fileout1.write(''+str(n_occ)+'               read (*,*) n_ele_beta \n')
        fileout1.write('                        read (*,*)  \n')
        fileout1.write(''+str(n_state)+'               read (*,*) n_state \n')
        fileout1.write('                        read (*,*)  \n')
        fileout1.write('1                       read (*,*)  type_input  \n')
        fileout1.write('ci_1.dat                read (*,*)  filename_input1  \n')
        fileout1.write('ci_2.dat                read (*,*)  filename_input2  \n')
        fileout1.write('overlap.dat             read (*,*)  filename_input2  \n')
        fileout1.write('                        read (*,*)  \n')
        fileout1.write('0                       read (*,*) output_level  \n')
        fileout1.write('ci_overlap.dat          read (*,*) filename_output  \n')
        fileout1.close()

        print "NAC PREPARED"
        
        return
###

    def run(self):
        """
        call another standalone program to deal with nac.
        """
        os.system("main_overlap_slater.exe  < main_overlap_slater_input")
        
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
    n = NAC() 
    n.worker()

   
     
     
      
