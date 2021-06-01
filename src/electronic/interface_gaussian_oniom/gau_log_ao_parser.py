#! /usr/bin/env  python
import os
import re


class gau_log_ao_parser():
    """
    parse gau. log file
    """
    def __init__(self, config = {}):
        """ init """
        self.dim = {'n_col': 5}
        self.ao_overlap = []
        self.files = {'ao': "high-model-overlap.log"}        
      
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
            self.files["ao"] = self.directory['overlap'] + "/" + files['ao-overlap-log'] 
        
        return

# -------------------------------------------------------------------------
#   %%%Read the AO overlap matrix
#   for tda case, only -> were printed in gaussian log.
# --------------------------------------------------------------------------------------------------
    def __read_ao_overlap_nbasis(self):
        """ get number of basis for dimer """
        # n_double_basis ncol 
        n_double_basis = 0
        logfile = self.files['ao']
        file_in = open(logfile, "r")
        pattern = re.compile("([0-9]+)(\s)(basis functions,)")  # 76 basis functions
        for line in file_in:
            m = pattern.search(line)
            if m is not None:
                string = m.group()
                n_double_basis = int(string.split()[0])
        file_in.close()
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
        # read column
        line = fp.readline()
        #print line
        n_double_basis = self.dim['n_basis']*2
        n_col = self.dim['n_col']
        i_start = i_block * n_col     
        # print i_start            
        for i in range(i_start, n_double_basis): # i_end eq n_double_basis
            line = fp.readline()
            #print line
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
        n_double_basis = self.dim['n_double_basis']
        n_col = self.dim['n_col']        
 
        i_block_add = (n_double_basis % n_col != 0) and 1 or 0   
        n_block = n_double_basis / n_col + i_block_add
        
        # read log file and locate ao overlap matrix
        logfile = self.files['ao']
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
        if m is None:
            print ("Error: AO matrix in gaussian log is missing.. exit..")
            exit(0)
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
        for the case of gaussian: require  iop(3/33=1) to output ao overlap matrix
        and iop(2/12=3,3/33=1) is required, since r and r+dr maybe too close geometries
        2/12=3 says: Do not abort the run regardless of 0 distances.
        @ note. in gaussian a initial guess <guess=only> is ok to get ao overlap matrix.
        @ so. the scf procedure is not required.
        """
        self.__read_ao_overlap_nbasis()
        # initial matrix for overlap
        self.__init_ao_overlap_matrix()   
        # i/o man. 
        self.__read_ao_overlap_matrix()
        self.__wrt_ao_overlap_matrix()
        
        return
    
    
### main program
if __name__ == "__main__":
    ao = gau_log_ao_parser()       
    ao.get_ao_overlap()
 



