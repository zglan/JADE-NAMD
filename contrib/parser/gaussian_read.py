#! /usr/bin/env python

import os
import sys
import re
import math
#from operator import itemgetter
#import shutil
#sys.path.append("./tools/")
#from tools import tools



class gau_log_parser():
    """
    parse gau. log file
    """
    def __init__(self, config = {}):
        """ init """
        self.dim = {'n_col': 5}
        self.ao_overlap = []
        self.fock = []
        self.mo = {"coeffs": [], "energy": [], "alpha": [], "beta": [], \
                "alpha_energy": [], "beta_energy": [], 'spin': 0} 
                # 0 for close shell case, 1 for open shell case
        self.ci = {}        
        self.files = {'gaussian': "gaussian.log"}

        self.files["gaussian"] = "test/gaussian.log"
        
        # @check correction & dump dimensional info from log.
        self.check_calc()       
        #self.get_dim_info()
 
        return

# -------------------------------------------------------------------------
#   %%%Read the AO overlap matrix
#   for tda case, only -> were printed in gaussian log.
# --------------------------------------------------------------------------------------------------
 
    def __init_ao_overlap_matrix(self):
        """ init. """  
        n_basis = self.dim['n_basis']    
        ao_overlap =[[0.0 for j in xrange(n_basis)] for i in xrange(n_basis)]
        self.ao_overlap = ao_overlap   
        return        
            
    def __read_ao_overlap_matrix_block(self, fp, i_block):
        """ 
        read one block of the ao overlap matrix 
        NOTE: IT IS A lower Triangular_matrix
        """
        # read column
        line = fp.readline()
        ## print line
        n_basis = self.dim['n_basis']
        n_col = self.dim['n_col']
        i_start = i_block * n_col     
        # print i_start            
        for i in range(i_start, n_basis):
            line = fp.readline()
            row_record = line.split()
            row_id = row_record[0]
            n_col_tmp = (i - i_start < 5) and (i - i_start + 1) or (n_col) 
            # if i_block == 15:
            #    print i_start, i, n_col_tmp
            for j in range(i_start, i_start + n_col_tmp):  
                j_col = j -i_start + 1 # first column is basis id, jump it by add 1                 
                self.ao_overlap[i][j] = row_record[j_col].upper().replace("D", "E")
                # fill the square overlap matrix
                self.ao_overlap[j][i] = self.ao_overlap[i][j]              
        return     
 
    def __read_ao_overlap_matrix(self):
        """ read ao overlap matrix S"""
        # initilize matrix dimension info in log file
        n_basis = self.dim['n_basis']
        n_col = self.dim['n_col']        
 
        i_block_add = (n_basis % n_col != 0) and 1 or 0   
        n_block = n_basis / n_col + i_block_add
        
        # read log file and locate ao overlap matrix
        logfile = self.files['gaussian']
        file_in = open(logfile, "r")
        pattern = re.compile("\*\*\* Overlap \*\*\*")
        line = "I-AM-START-MARKER"
        while line != "":
            line = file_in.readline()
            m = pattern.search(line)
            if m is not None:
                break
            else:
                continue            
        # start to process the matrix data.                 
        for i_block in range(n_block):
            self.__read_ao_overlap_matrix_block(file_in, i_block)          
    
        return        

    def __wrt_ao_overlap_matrix(self):
        """ wrt done ao overlap matrix in one format """
        n_basis = self.dim['n_basis']
        ao_overlap = self.ao_overlap
        # write done all.
        file_out = open('overlap_all.dat', 'w')
        file_out.write('#  All Overlap: i_MO, j_MO, S_ij  \n')
        for i_mo_1 in range(n_basis) :
            for i_mo_2 in range(n_basis) :
                file_out.write(''+str(i_mo_1+1)+'    '+str(i_mo_2+1)+'    '+ \
                                str(ao_overlap[i_mo_1][i_mo_2])+' \n')         
        file_out.close()
     
        return             
                
    def get_ao_overlap(self):
        """
        read ao overlap
        #  Read the DFT calculations  
        for the case of gaussian: require  iop(3/33=1) to output ao overlap matrix
        and iop(2/12=3,3/33=1) is required, since r and r+dr maybe too close geometries
        2/12=3 says: Do not abort the run regardless of 0 distances.
        @ note. in gaussian a initial guess <guess=only> is ok to get ao overlap matrix.
        @ so. the scf procedure is not required.
        """
        # initial matrix for overlap
        self.__init_ao_overlap_matrix()   
        # i/o man. 
        self.__read_ao_overlap_matrix()
        self.__wrt_ao_overlap_matrix()
        
        return
    

    # read in Fock information. at the end of SCF Iteration.
    def __init_fock_matrix(self):
        """ init. """  
        n_basis = self.dim['n_basis']    
        fock =[[0.0 for j in xrange(n_basis)] for i in xrange(n_basis)]
        self.fock = fock
        return        
            
    def __read_fock_matrix_block(self, fp, i_block):
        """ 
        read one block of the fock matrix 
        NOTE: IT IS A lower Triangular_matrix
        """
        # read column
        line = fp.readline()
        ## print line
        n_basis = self.dim['n_basis']
        n_col = self.dim['n_col']
        i_start = i_block * n_col     
        # print i_start            
        for i in range(i_start, n_basis): # i_end eq n_basis
            line = fp.readline()
            row_record = line.split()
            row_id = row_record[0]
            n_col_tmp = (i - i_start < 5) and (i - i_start + 1) or (n_col) 
            # if i_block == 15:
            #    print i_start, i, n_col_tmp
            for j in range(i_start, i_start + n_col_tmp):  
                j_col = j -i_start + 1 # first column is basis id, jump it by add 1                 
                self.fock[i][j] = row_record[j_col].upper().replace("D", "E")
                # fill the square overlap matrix
                self.fock[j][i] = self.fock[i][j]              
        return     
 
    def __read_fock_matrix(self):
        """ read fock matrix F"""
        # initilize matrix dimension info in log file
        n_basis = self.dim['n_basis']
        n_col = self.dim['n_col']        
 
        i_block_add = (n_basis % n_col != 0) and 1 or 0   
        n_block = n_basis / n_col + i_block_add
        
        # read log file and locate ao overlap matrix
        logfile = self.files['gaussian']
        file_in = open(logfile, "r")
        pattern = re.compile("Fock matrix \(alpha\)")
        m0 = None
        while True:
            line = file_in.readline()
            if line == "":
                break
            m = pattern.search(line)
            if m is not None:
                m0 = m
                fock_pos = file_in.tell()            
        if m0 is not None:
            print "Find the Fock matrix"
        else:
            print "Cannot find Fock matrix, check gaussian log file.."
            exit(0)

        file_in.seek(fock_pos)
        # start to process the Fock matrix data.                 
        for i_block in range(n_block):
            self.__read_fock_matrix_block(file_in, i_block)          
    
        return        

    def __wrt_fock_matrix(self):
        """ wrt done ao overlap matrix in one format """
        n_basis = self.dim['n_basis']
        fock = self.fock
        # write done all.
        file_out = open('fock_all.dat', 'w')
        file_out.write('#  Fock: i_MO, j_MO, S_ij  \n')
        for i_mo_1 in range(n_basis) :
            for i_mo_2 in range(n_basis) :
                file_out.write(''+str(i_mo_1+1)+'    '+str(i_mo_2+1)+'    '+ \
                               str(fock[i_mo_1][i_mo_2])+' \n')
        file_out.close()
        
        return             
                
    def get_fock(self):
        """
        read fock
        #  the last Fock matrix alpha only
        # iop(5/33=3) is required, this usually dump fock matrix at each inter.
        """
        # initial matrix for overlap
        self.__init_fock_matrix()   
        # i/o man. 
        self.__read_fock_matrix()
        self.__wrt_fock_matrix()
        
        return
    

    
# -------------------------------------------------------------------------
#   %%% check & prepare for reading data.
#   gaussian.log file is required.
#   core orbitals  are frozen in the Gaussian TDDFT implementation
#   These quantities are read from the log file in t=0  
# ---------------------------------------------------------------------------

#   Check the DFT and TDDFT output    
    def check_calc(self):
        """
        check and confirm the calc. is ok
        """
        logfile = self.files['gaussian']
        file_in = open(logfile, "r")
        
        if not os.path.isfile(logfile):
            print "DFT & TD calculation results do not exist!"
	    print "Check the DFT calculation!"
	    raise IOerror  
	    
	    pat_dft = re.compile("SCF Done")
	    pat_ter = re.compile("Normal termination")
	    line_all = file_in.read()
	    m1 = pat_dft.search(line)
	    m2 = pat_ter.search(line)
	    if m1 is None:
	        print "DFT calculation failed."
	        raise IOerror
	    if m2 is None:
	        print "calculation was not terminated normally"
	        raise IOerror	           
     	          
        return
        
    def get_dim_info(self):
        """
        obtain dimension data.
        such as number of atoms and et al.
        core orbitals  are frozen in the Gaussian TDDFT implementation
        """   
        logfile = self.files['gaussian']
        file_in = open(logfile, "r")
        for line in file_in:
            # match
            # NAtoms=    6 NActive=    6 NUniq=    6 SFac= 7.50D-01 NAtFMM=   80 NAOKFM=F Big=F
            pat0 = re.compile("NAtoms=(.*)NActive=(.*)NUniq=(.*)SFac=(.*)NAtFMM=(.*)")
            # NBasis=    38 NAE=     8 NBE=     8 NFC=     2 NFV=     0
            pat1 = re.compile("NBasis=(.*)NAE=(.*)NBE=(.*)NFC=(.*)NFV=(.*)")
            pat1 = re.compile("NBasis=(.*)")
            # NROrb=     36 NOA=     6 NOB=     6 NVA=    30 NVB=    30
            pat2 = re.compile("NROrb=(.*)NOA=(.*)NOB=(.*)NVA=(.*)NVB=(.*)") 
            # nstates=3
            pat3 = re.compile("nstates=(\d)+", re.IGNORECASE)
            # ..
            m0 = pat0.search(line)           
            m1 = pat1.search(line)
            m2 = pat2.search(line)
            m3 = pat3.search(line)
            
            if m0 is not None:
                string = m0.group()
                record = string.split()
                self.dim['n_atom'] = int(record[1])
                self.dim['n_active'] = int(record[3])
                
            elif m1 is not None:
                string = m1.group()
                record = string.split()
                self.dim['n_basis'] = int(record[1])

                #print self.dim['neleA']

            elif m2 is not None:
                string = m2.group()
                record = string.split()
                #"$NoccA $NoccB $NvirtA $NvirtB";
                self.dim['norb'] = int(record[1]) # number of orbital active
                self.dim['noccA'] = int(record[3])
                self.dim['noccB'] = int(record[5])
                self.dim['nvirA'] = int(record[7])
                self.dim['nvirB'] = int(record[9])
            elif m3 is not None:
                string = m3.group()
                record = string.split("=")
                self.dim['n_state'] = int(record[1]) + 1    # add 1, because of the ground state
            else:
                continue
        
        file_in.close()
                
        #tools.dump_data('dimension.json', self.dim)                

        return


# -------------------------------------------------------------------------
#   %%% Read the gradient
#   for tda case, only '->' were printed in gaussian log.
#   the output file are:
#   qm_gradient.dat
# ---------------------------------------------------------------------------    
    def get_gradient(self):
        """ read gradient and punch out """
        logfile = self.files['mo']
        # logfile = "td.log"
        file_in = open(logfile, "r")
        # locate data.
        pattern = re.compile("Forces \(Hartrees\/Bohr\)") 
        # print pattern 
        line = "NOT EMPTY LINE"
        while line != "":
            line = file_in.readline()
            m = pattern.search(line)
            if m is not None:    
                # jump two line
                line = file_in.readline()
                line = file_in.readline()
                break
        
        file_out = open("qm_gradient.dat", "w")
        while line != "": 
            line = file_in.readline()           
            pattern = re.compile("-------------")              
            if pattern.search(line) is not None:
                break
            record = line.split()
            # atomid = int(record[0])
            # atom_charge = int(record[1])
            grad_x = record[2]
            grad_y = record[3]
            grad_z = record[4]
            file_out.write(''+str( grad_x )+'   '+ \
                            str( grad_y )+'   '+str( grad_z )+'  \n')            
            
        file_in.close() 
        file_out.close()       
        
        return
        
# -------------------------------------------------------------------------
#   %%% Read the mo coefficients
#   the output file are:
#   mos.dat      The MO coefficient
# --------------------------------------------------------------------------------------------------
    def __init_mo_matrix(self):
        """ init. """  
        n_basis = self.dim['n_basis']
        
        coeffs = []
        alpha = []
        beta = []
        alpha_energy = []
        beta_energy = []
        energy = []
        for i in range(n_basis):
            energy.append(0.0)
            coeffs.append([])        
            for j in range(n_basis):
                coeffs[i].append(0.0)
        self.mo = {'coeffs': coeffs, 'energy': energy} 
         
        return
        
     
    # for close shell, currently
    def __read_mo_matrix_block(self, fp, i_block):
        """ 
        read one block of the MO matrix 
        """
        # jump first two lines.
        line = fp.readline()
        line = fp.readline()
        ## dimensional info.
        n_basis = self.dim['n_basis']
        n_col = self.dim['n_col']
        i_start = i_block * n_col    
        # the third line: eigenvalue energy of orb.
        line = fp.readline()
        record = line[20:].split()
        n_col_tmp = len(record) 
        for i in range(i_start, i_start + n_col_tmp):
            self.mo['energy'][i] = record[i-i_start]            
        # later, the mo coeffs.         
        for i in range(0, n_basis): # i_end eq n_double_basis
            line = fp.readline()
            record = line[20:].split()
            for j in range(i_start, i_start + n_col_tmp):  
                j_col = j -i_start  #                  

                self.mo['coeffs'][j][i] = record[j_col]
             
        return        
            

    def __read_mo_matrix(self):
        """ read ao overlap matrix S"""
        # initilize matrix dimension info in log file
        n_basis = self.dim['n_basis']
        n_col = self.dim['n_col']        
 
        i_block_add = (n_basis % n_col != 0) and 1 or 0   
        n_block = n_basis / n_col + i_block_add
        
        # read log file and locate ao overlap matrix
        logfile = self.files['gaussian']
        file_in = open(logfile, "r")
        # locate mo coeffs.
        pattern = re.compile("Molecular Orbital Coefficients") 
        line = "I-AM-START-MARKER"
        while line != "":
            line = file_in.readline()
            m = pattern.search(line)
            if m is not None:
                break
            else:
                continue
 
        # start to process the matrix data.                 
        for i_block in range(n_block):
            self.__read_mo_matrix_block(file_in, i_block)          
    
        
        return        
        

    def __wrt_mo_matrix(self):
        """ wrt done mo matrix in specific format """
        # dim. info.
        n_basis = self.dim['n_basis']
        # vars
        coeffs = self.mo['coeffs']
        mo_energy = self.mo['energy']
        
        # now, write done all.
        file_out=open('mo.dat', 'w')
        file_out.write('#  MO coefficient (i_MO, j_AO, M_ij)    \n')
        for i_mo_1 in range(n_basis) :
            file_out.write('MO:'+str(i_mo_1+1)+'   '+str(mo_energy[i_mo_1])+'\n')
            for i_mo_2 in range(n_basis) :  
                file_out.write(''+str(i_mo_1+1)+'    '+str(i_mo_2+1)+'    '+ \
                               str(coeffs[i_mo_1][i_mo_2])+' \n')
 
        file_out.close()
        
        return                       
  
                
    def get_mo(self):
        """
        close shell and open shell.
        """
        # init. matrix for mos.
        self.__init_mo_matrix()
       
        # first, check open or close shell imp. later
        # self.__check_spin()
        # i/o man.
        self.__read_mo_matrix()
        self.__wrt_mo_matrix()
        
        return

    

### main program
if __name__ == "__main__":
    ao = gau_log_parser()
    #ao.get_gradient()
    ao.get_dim_info()
    ao.get_mo()
    ao.get_ao_overlap()
    ao.get_fock()
 
 



