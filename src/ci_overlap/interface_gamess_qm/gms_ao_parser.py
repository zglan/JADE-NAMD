# python
import os
import sys
import re
import math
from operator import itemgetter
import shutil
sys.path.append("../tools/")
import tools



class gms_ao_parser:
    """
    parse gau. log file
    """
    def __init__(self, config = {}):
        """ init """
        self.dim = {'n_col': 5}
        self.ao_overlap = []
        self.mo = {"coeffs": [], "energy": [], "alpha": [], "beta": [], \
                "alpha_energy": [], "beta_energy": [], 'spin': 0} 
                # 0 for close shell case, 1 for open shell case
        self.ci = {}        
        self.files = {"log": 'gamess.log'}
        
        # @check correction & dump dimensional info from log.
        self.check_calc()       
        self.get_dim_info()
        
        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files'] 
            
            # working directory & files >>>
            self.directory = {}
            self.directory['root'] = root_dir
            self.directory['home'] = root_dir + "/" + dirs['home']
            self.directory['work'] = self.directory['home'] + "/" + dirs['work']
            self.directory['overlap'] = self.directory['home'] + "/" + dirs['overlap']
            
            self.files = {}
            self.files["log"] = self.directory['overlap'] + "/" + files['job_log'] 
                
            # run the job directly
        return


    def get_dim_info(self):
        """
        obtain dimension data.
        such as number of atoms and et al.
        parser gamess-us log file.
        """   
        logfile = self.files['log']
        fp = open(logfile, "r")

        line = "STARTER"
        pat = re.compile("TOTAL NUMBER OF BASIS SET SHELLS")
        
        while line != "":
            line = fp.readline()
            m = pat.search(line)
            if m is not None:
                break
        # shell num.
        t_line = line
        # print t_line
        val = t_line.split("=")[1]
        n_shell = int(val)     
        
        # READ THE FOLLOWING LINES
        # 9 lines
        # TOTAL NUMBER OF BASIS SET SHELLS             =   10
        # NUMBER OF CARTESIAN GAUSSIAN BASIS FUNCTIONS =   38
        # NUMBER OF ELECTRONS                          =   14
        # CHARGE OF MOLECULE                           =    0
        # SPIN MULTIPLICITY                            =    1
        # NUMBER OF OCCUPIED ORBITALS (ALPHA)          =    7
        # NUMBER OF OCCUPIED ORBITALS (BETA )          =    7
        # TOTAL NUMBER OF ATOMS                        =    2
        # THE NUCLEAR REPULSION ENERGY IS       22.5117346394
        #
       
        # number of cart gaussian basis functions
        t_line = fp.readline()
        val = t_line.split("=")[1]
        self.dim['n_basis'] = int(val)
        #print t_line
        # number of electrons
        t_line = fp.readline()
        val = t_line.split("=")[1]
        self.dim['n_elec'] = int(val)

        # mol. charge
        t_line = fp.readline()
        val = t_line.split("=")[1]
        charge = int(val)

        # spin-mult
        t_line = fp.readline()
        val = t_line.split("=")[1]
        spin = int(val)

        # number-occupied-orbitals-alpha
        t_line = fp.readline()
        val = t_line.split("=")[1]
        self.dim['neleA'] = int(val)        

        # number-occupied-orbitals-beta
        t_line = fp.readline()
        val = t_line.split("=")[1]
        self.dim['neleB'] = int(val)                
        # print line
        # number-of-atoms
        t_line = fp.readline()
        val = t_line.split("=")[1]
        self.dim['n_atom'] = int(val)
        

        # TDDFT INPUT PARAMETERS
        pat = re.compile("TDDFT INPUT PARAMETERS")
        line = "starter"
        while line != "":
            line = fp.readline()
            m = pat.search(line)
            if m is not None:
                break
        line = fp.readline()
        # reading...
        #   NSTATE=       3  IROOT=       1   MULT=       1
        t_line = fp.readline()
        pat0 = re.compile("NSTATE=(.*)IROOT=(.*)MULT=(.*)")
        m = pat0.search(t_line)
        if m is not None:
            self.dim['n_state'] = int(m.group(1))
            self.dim['i_state'] = int(m.group(2))
        else:
            print "CANNOT FIND TD-DFT INPUT PARAMETERS SETTING in OVERLAP CALCULATION.[IGNORE]"
                            
        fp.close()
                
        tools.dump_data('dimension.json', self.dim)                

        return


# -------------------------------------------------------------------------
#   %%%Read the AO overlap matrix
#   for tda case, only -> were printed in gaussian log.
# ------------------------------------------------------------------------
    def __read_ao_overlap_nbasis(self):
        """ get number of basis for dimer """
        # n_double_basis ncol 
        n_double_basis = 0
        logfile = self.files['log']
        fp = open(logfile, "r")
        
        pat = re.compile("NUMBER OF CARTESIAN GAUSSIAN BASIS FUNCTIONS\s+=\s+([0-9]+)")
        
        for line in fp:
            m = pat.search(line)
            if m is not None:
                val = m.group(1)
                n_double_basis = int(val)
        fp.close()
        if n_double_basis == 0 :
            print "Check the calculation of AO overlap!"
             
        self.dim['n_double_basis'] = n_double_basis        
        self.dim['n_basis'] = n_double_basis/2
        # print n_double_basis
        return    

    def __init_ao_overlap_matrix(self):
        """ init. """  
        n_double_basis = self.dim['n_double_basis']    
        ao_overlap =[]
        for i in range(n_double_basis):
            ao_overlap.append([])
            for j in range(n_double_basis):
                ao_overlap[i].append(0.0)
        self.ao_overlap = ao_overlap   
        return        
            
    def __read_ao_overlap_matrix_block(self, fp, i_block):
        """ 
        read one block of the ao overlap matrix 
        NOTE: IT IS A lower Triangular_matrix
        """
        # read column id & blank lines; useless
        line = fp.readline()
        line = fp.readline()
        line = fp.readline()
        ## print line
        n_double_basis = self.dim['n_basis']*2
        n_col = self.dim['n_col']
        i_start = i_block * n_col     
                
        for i in range(i_start, n_double_basis): # i_end eq n_double_basis
            line = fp.readline()
            row_record = line.split()
            row_id = row_record[0]
            n_col_tmp = (i - i_start < 5) and (i - i_start + 1) or (n_col) 
            # if i_block == 15:
            # print i_start, i, n_col_tmp
            
            for j in range(i_start, i_start + n_col_tmp):  
                j_col = j - i_start + 4 # first 4 column is useless, jump by add 4
                # print row_record[j_col],i,j
                self.ao_overlap[i][j] = row_record[j_col].upper()
                # fill the square overlap matrix                
                self.ao_overlap[j][i] = self.ao_overlap[i][j]              
        return     
 
    def __read_ao_overlap_matrix(self):
        """ read ao overlap matrix S"""
        # initilize matrix dimension info in log file
        n_double_basis = self.dim['n_double_basis']
        n_col = self.dim['n_col']        
 
        i_block_add = (n_double_basis % n_col != 0) and 1 or 0   
        n_block = n_double_basis / n_col + i_block_add
        
        # read log file and locate ao overlap matrix
        logfile = self.files['log']
        fp = open(logfile, "r")
        pat = re.compile("OVERLAP MATRIX")
        line = "I-AM-START-MARKER"
        while line != "":
            line = fp.readline()
            m = pat.search(line)
            if m is not None:
                break
            else:
                continue            
        # start to process the matrix data.                 
        for i_block in range(n_block):
            self.__read_ao_overlap_matrix_block(fp, i_block)          
    
        return        

    def __wrt_ao_overlap_matrix(self):
        """ wrt done ao overlap matrix in one format """
        n_basis = self.dim['n_basis']
        ao_overlap = self.ao_overlap
        # write done all.
        file_out = open('overlap_all.dat', 'w')
        file_out.write('#  All Overlap: i_MO, j_MO, S_ij  \n')
        for i_mo_1 in range(2*n_basis) :
            for i_mo_2 in range(2*n_basis) :
                file_out.write(''+str(i_mo_1+1)+'    '+str(i_mo_2+1)+'    '+ \
                                str(ao_overlap[i_mo_1][i_mo_2])+' \n')
        file_out.close()    
        # write the Overlap between R and R+dR
        file_out = open('ao_overlap.dat', 'w')  
        file_out.write('#  Overlap between R and R+dR : i_MO_R, j_MO_R+dR, S_ij  \n') 
        for i_mo_1 in range(n_basis) :
            for i_mo_2 in range(n_basis) :  
                file_out.write(''+str(i_mo_1+1)+'    '+str(i_mo_2+1)+'    '+ \
                                str(ao_overlap[i_mo_1][i_mo_2+n_basis])+' \n')            
        file_out.close()
        
        return             
                
    def get_ao_overlap(self):
        """
        read ao overlap
        #  Read the DFT calculations of double-molecule calculation 
        #  Read the overlap matrix between Geom R and Geom R+dR
        for the case of gamess: require  NPRINT=3 in 'contrl' block
        to punch out ao overlap matrix & EXETYP=CHECK in 'contrl' block
        to avoid scf step. only ao overlap is required.
        the gms code was slightly modified to avoid the error arised
        when r and r+dr maybe too close geometries
        says: Do not abort the run regardless of 0 distances.
        @ note. in gamess a initial guess <EXETYP=CHECK> is ok to
        get ao overlap matrix.
        @ so. the scf procedure is not required.
        """
        self.__read_ao_overlap_nbasis()
        # initial matrix for overlap
        self.__init_ao_overlap_matrix()   
        # i/o man. 
        self.__read_ao_overlap_matrix()
        self.__wrt_ao_overlap_matrix()
        
        return

# =========================================================================
# GET_AO_OVERLAP <<
# ========================================================================


# -------------------------------------------------------------------------
#   %%% check & prepare for reading data.
#   gamess.log file is required.
# ---------------------------------------------------------------------------

#   Check the DFT and TDDFT output    
    def check_calc(self):
        """
        check and confirm the calc. is ok
        """
        logfile = self.files['log']
        print logfile
        if not os.path.isfile(logfile):
            print "gamess results do not exist!"
            print "Check the ATOMIC OVERLAP calculation!"
            raise IOerror
    
        fp = open(logfile, "r")
        pat = re.compile("OVERLAP MATRIX")
        line_all = fp.read()
        m = pat.search(line_all)
        if m is None:
            print "NO OVERLAP MATRIX FOUND???.", os.path.realpath(__file__)
            raise IOerror
                	          
        return
        


    
### main program
if __name__ == "__main__":
    ao = gms_log_parser()
    ao.get_ao_overlap()
    ao.get_dim_info()




