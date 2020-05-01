# python
import os
import sys
import re
import math
from operator import itemgetter
import shutil

sys.path.append("../tools/")
import tools


class gau_log_parser():
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
        self.files = {'ao': "ch2nh2.log", 'mo': 'gaussian.log'}
        
        # @check correction & dump dimensional info from log.
      
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
            self.files["ao"] = self.directory['overlap'] + "/" + files['gau_log'] 
            self.files["mo"] = self.directory['work'] + "/" + files['gau_log'] 
        
        self.check_calc()       
        self.get_dim_info()

        # key words detected
        if 'ci_assign_problem' in config.keys():
                self.ci_type = config['ci_assign_problem']   # X+Y or X
        else:
                # default c = X+Y relationship, and then normalize it      
                self.ci_type = "X+Y"    
        
 
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
        ## print line
        n_double_basis = self.dim['n_basis']*2
        n_col = self.dim['n_col']
        i_start = i_block * n_col     
        # print i_start            
        for i in range(i_start, n_double_basis): # i_end eq n_double_basis
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
        # nothing done
        return
        
    def get_dim_info(self):
        """
        obtain dimension data.
        such as number of atoms and et al.
        core orbitals  are frozen in the Gaussian TDDFT implementation
        """   
        logfile = self.files['mo']
        if not os.path.isfile(logfile):
            print "DFT & TD calculation results do not exist!"
            print "Check the DFT calculation!", logfile
            exit(1)
        
        file_in = open(logfile, "r")
        
        for line in file_in:
            # match
            # NAtoms=    6 NActive=    6 NUniq=    6 SFac= 7.50D-01 NAtFMM=   80 NAOKFM=F Big=F
            pat0 = re.compile("NAtoms=(.*)NActive=(.*)NUniq=(.*)SFac=(.*)NAtFMM=(.*)")
            # NBasis=    38 NAE=     8 NBE=     8 NFC=     2 NFV=     0
            pat1 = re.compile("NBasis=(.*)NAE=(.*)NBE=(.*)NFC=(.*)NFV=(.*)")        
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
                self.dim['neleA'] = int(record[3])
                self.dim['neleB'] = int(record[5])
                self.dim['nfixcore'] = int(record[7])
                self.dim['nfixvir'] = int(record[9])                
                # guess occ_all
                self.dim['nocc_allA'] = self.dim['neleA']
                self.dim['nvir_allA'] = self.dim['n_basis'] - self.dim['nocc_allA']
                self.dim['nocc_allB'] = self.dim['neleB']
                self.dim['nvir_allB'] = self.dim['n_basis'] - self.dim['nocc_allB']
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
                
        tools.dump_data('dimension.json', self.dim)                
        
        return

    def get_basis(self):
        """
        write down dimensional info.
        """
        # dimentional info.
        n_basis = self.dim['n_basis']
        n_occ = self.dim['neleA']
        # this key is no use here, only for format consist with turbo interface
        DFT_or_HF = 1
        func = 1
        
        fileout1=open('qm_basis.dat', 'w')
        if  DFT_or_HF == 0:
	        fileout1.write('TD-HF or CIS?  10(TD-HF),  11 (CIS) zhanzuo:   '+str(func)+'  \n' )
        if  DFT_or_HF == 1:	
	        fileout1.write('Functional: 0(pure),  1 (hybrid),  2 (pure+ TDA) , 3 (hybrid + TDA) zhanzuo:  '+str(func)+'  \n' )
	    
        fileout1.write('number of basis functions: '+str(n_basis)+'  \n')
        fileout1.write('number of occupied orbitals: '+str(n_occ)+'  \n')
        fileout1.close()
        
        return

    def collect_qm(self):
        """
        wrt down in one file
        """
        n_state = self.dim['n_state']
        interface = tools.load_data("interface.json")
        index_state = interface['parm']['i_state']
        # wrt files.
        fileout3 = open('qm_results.dat', 'w')
        # header
        fileout3.write('-----------------------------------------  \n')
        fileout3.write('Summary of QM calculations: \n')
        fileout3.write('-----------------------------------------  \n') 
        
        qm_interface = self.directory['root'] + "/" + "qm_interface"
        filein4=open(qm_interface, 'r')
        fileout3.write(filein4.read())
        fileout3.write('-----------------------------------------  \n')  
        filein4.close()

        fileout3.write('The electronic calculations focus on '+str(n_state)+' states: \n')
        for i_state in range(n_state) :
            fileout3.write('S'+str(i_state)+ '   ..  ' )
        fileout3.write('\n')
        fileout3.write('The S'+str(index_state-1)+' gradient should be computed !   \n') 
        fileout3.write('-----------------------------------------  \n')

        fileout3.write('Basis information: \n')
        filein4=open('qm_basis.dat','r') 
        fileout3.write(filein4.read())
        fileout3.write('-----------------------------------------  \n')
        filein4.close()

        fileout3.write('Energy of electronic states: \n')
        filein4=open('qm_energy.dat','r')
        fileout3.write(filein4.read())  
        fileout3.write('-----------------------------------------  \n')
        filein4.close()

        fileout3.write('Gradient on S'+str(index_state-1)+'  \n')
        filein4=open('qm_gradient.dat','r')
        fileout3.write(filein4.read())  
        fileout3.write('-----------------------------------------  \n')
        filein4.close()    
     
        fileout3.write('Nonadiabatic coupling elements  \n') 
        sourceFile = 'qm_nac.dat'
        if os.path.isfile(sourceFile):
            filein4=open('qm_nac.dat','r')
            fileout3.write(filein4.read())
            fileout3.write('-----------------------------------------  \n')
            filein4.close()
        else : 
            for i_state in range(n_state):
                for j_state in range(n_state):
                    fileout3.write('S'+str(i_state)+'    S'+str(j_state)+'   0.00000   \n')

        fileout3.write('-----------------------------------------  \n')               
        fileout3.close()         
            
        return


# -------------------------------------------------------------------------
#   %%% Read all other important information of QM output
#   gaussian.log file is required.
#   For example: Transition dipole moment and so on 
# ---------------------------------------------------------------------------

    def get_other(self):
        """
        Write other important information in QM output 
        """
        es = []
        gs = []
        pat1e = re.compile("Excited states from <AA,BB:AA,BB> singles matrix")
        pat2e = re.compile("Excitation energies and oscillator strengths")
        float_number = '[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
        pat1g = re.compile("Charge=(\s)+" + float_number + "(\s)+electrons")
        pat2g = re.compile("XXYZ=(.*)YYXZ=(.*)ZZXY=(.*)")
                
        # read all
        file_energy = self.files['mo']
        filein = open(file_energy,'r')        
        
        line = "empty"
        # Excited states from <AA,BB:AA,BB> singles matrix
        while line != "":
            line = filein.readline()
            m1 = pat1e.search(line)
            if m1 is not None:
                break            
        line = filein.readline()
        line = filein.readline() 

        while line != "":
            line = filein.readline()   
            m2 = pat2e.search(line)
            if m2 is not None:
                break
            es.append(line)             

        # ground state.
        while line != "":
            line = filein.readline()
            m1 = pat1g.search(line)
            if m1 is not None:
                break            
        gs.append(line)
        while line != "":
            line = filein.readline()   
            gs.append(line) 
            m2 = pat2g.search(line)
            if m2 is not None:
                break
        filein.close()
        
        fileout = open('qm_other.dat', 'w')  
        for line in gs:
            fileout.write(line)
        fileout.write('------------------------------------------------------------- \n')           
        for line in es:
            fileout.write(line) 
        fileout.write('------------------------------------------------------------- \n')       
        fileout.close()

        return

# -------------------------------------------------------------------------
#   %%% Read the gradient
#   for tda case, only '->' were printed in gaussian log.
#   the output file are:
#   qm_gradient.dat
#   Attention:
#   gaussian only give force on the atoms, and gradient = - force
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
            m = pattern.search(line)
            if m is not None:
                break
            record = line.split()
            # atomid = int(record[0])
            # atom_charge = int(record[1])
            grad_x = -float(record[2])
            grad_y = -float(record[3])
            grad_z = -float(record[4])
            file_out.write(''+str( grad_x )+'   '+ \
                            str( grad_y )+'   '+str( grad_z )+'  \n')            
        if m is None:
            print "GRIDENT READ FAILED"
        file_in.close() 
        file_out.close()       
        
        return
        
# -------------------------------------------------------------------------
#   %%% Read the mo coefficients
#   the output file are:
#   mo.dat      The MO coefficient
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
        logfile = self.files['mo']
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
        # init. matrix for mo.
        self.__init_mo_matrix()
        
        # first, check open or close shell imp. later
        # self.__check_spin()
        # i/o man.
        self.__read_mo_matrix()
        self.__wrt_mo_matrix()
        
        return
        

# -------------------------------------------------------------------------
#   %%% Read the CI vector
#   for tda case, only -> were printed in gaussian log.
#   the output file is 
#   ci.dat       Important CI vector
# --------------------------------------------------------------------------------------------------

    def __assign_ci_parm(self, line):
        """
        assign
        3 ->  9        -0.00703  
        to 
        [3][9] = -0.00703  
        or 
        for alpha/beta open shell; will implemented later.
        3A -> 9A       -0.00703
        to
        [3][9] = ...   
        """        
        # dimentional info.
        neleA = self.dim['neleA']

        # check if open shell case
        pat = re.compile("[AB]+")
        m = pat.search(line)
        if m is not None:
            print "find open shell calculations: orbital %s", m.group()
            print "cannot deal with it currently."
            sys.exit(1)
        else:
            arrow_str = line[9:11]
            i = int(line[0:9]) - 1
            j = int(line[11:20]) - neleA - 1      # virtual orbital assign 
            ci = float(line[20:])
            if arrow_str == "->":
               flag = "ia"
            elif arrow_str == "<-":
               flag = "ai"
            else:
                print "ERROR: -> or <- cannot find???"
                sys.exit()

        return i, j, ci, flag
        
                    
    def __init_ci_matrix(self, n_state):
        """
        init ci data mat.
        """
        # dimensional info.
        n_basis = self.dim['n_basis']
        nocc_all = self.dim['neleA']
        nvir_all = n_basis - nocc_all
        # 
        # init.
        self.ci['n_state'] = n_state
        self.ci['state'] = []   # n_state

        # make suitable memory space.
        for i in range(n_state):            # i: state, j: occ; k: vir
            trans_ia = []
            trans_ai = []
            trans = []
            for j in range(nocc_all):  # for trans[nocc][nvir]
                trans_ia.append([])                
                trans_ai.append([])                
                trans.append([])
                for k in range(nvir_all):
                    trans_ia[j].append(0.0)
                    trans_ai[j].append(0.0)
                    trans[j].append(0.0)
            one_state = {'energy': 0.0, 'trans_ia': trans_ia, 'trans_ai': trans_ai, 'trans': trans}
            self.ci['state'].append(one_state)
            
        return        
        
    def __read_ci_block(self, file_in, i_state):
        """
        read one section of ci coeffs in log file of gau.
        """
        # go to 'Excited State   no.' line
        pat = re.compile("Excited State(\s)+(\d)+")
        line = "HAHA-not empty line"
        while line != "":
            m = pat.search(line)
            if m is not None:
                break
            line = file_in.readline()            
            
        # read this line, energy et al.
        pat = re.compile("[\d.]+(\s)+eV")    # catch string like "1.2 eV"
        m = pat.search(line)
        grp = m.group()
        record = grp.split()
        self.ci['state'][i_state]['energy'] = float(record[0]) / 27.21138386
        
        # read the coefficient and others.
        pat = re.compile("[<>]+")
        while 1 :
            line = file_in.readline()
            m = pat.search(line)
            if m is None:
                break
                            
            i_ci_1, i_ci_2, value, flag = self.__assign_ci_parm(line)
            # print i_ci_1, i_ci_2
            # the other trans ci vector was zero by default
            if flag == "ia":
                self.ci['state'][i_state]['trans_ia'][i_ci_1][i_ci_2] = value
                self.ci['state'][i_state]['trans'][i_ci_1][i_ci_2] = value
            elif flag == "ai":
                self.ci['state'][i_state]['trans_ai'][i_ci_1][i_ci_2] = value
            else:
                print "ERROR: unexpected value ??? ci coefficients"
     
        return
        

    def __read_ci_td(self, n_state):
        """
        read ci paramters
        """
        # open file to read
        logfile = self.files['mo']
        file_in = open(logfile, "r")
        # dimensional info.
        print 'Begin to read the CI vector from log file. ' 
        
        # ground state energy.
        pat = re.compile("SCF Done")
        line = "I-AM-START-MARKER"
        while line != "":
            line = file_in.readline()
            m = pat.search(line)
            if m is not None:
                break
            else:
                continue  
        self.ci['gs_energy'] = float(line.split()[4])
        self.ci['state'][0]['energy'] = 0.0
        
        # excited state section.       
        pat = re.compile("Excitation energies and oscillator strengths")
        while line != "":
            line = file_in.readline()
            m = pat.search(line)
            if m is not None:
                break
            else:
                continue         
        # go on one line.   
        
        line = file_in.readline()
        # start to process the matrix data.   
        # no ci vector for groud state.              
        for i_block in range(1, n_state):
            self.__read_ci_block(file_in, i_block)                  
        
        return


    def __distrib_ci_matrix(self):
        """
        contruct ci vector; only close shell is supported
        """
        # dimensional info.
        dim = self.dim
        n_occ = dim['nocc_allA']
        n_vir = dim['nvir_allA']
        n_state = dim['n_state']     
        # determine the ci assign problem                
        ci_type = self.ci_type
        print "current CI type:", ci_type
        
        for i_state in range(1, n_state):
            print "get X+Y> VECTOR:", i_state
            one_state1 = self.ci['state'][i_state]['trans_ia']
            one_state2 = self.ci['state'][i_state]['trans_ai']
            add_alpha = [[0.0 for i in xrange(n_vir)] for j in xrange(n_occ)] 
            if ci_type == "X+Y":
                for i_ci_1 in range(n_occ):
                    for i_ci_2 in range(n_vir):
                        add_alpha[i_ci_1][i_ci_2]  =  one_state1[i_ci_1][i_ci_2] + one_state2[i_ci_1][i_ci_2]                 
    
                self.ci['state'][i_state]['trans'] = add_alpha     
                
        print "|X+Y> & |X-Y> DONE"
        return       


    def __norm_ci_td(self):
        """
        normalization test and so on.
        """
        # dimensional info.
        n_state = self.dim['n_state']
        n_occ = self.dim['nocc_allA']
        n_vir = self.dim['nvir_allA']
        
        for i_state in range(1, n_state):
            print "Check normalization for State:", i_state
            norm = 0.0
            one_state = self.ci['state'][i_state]['trans']
            for i_ci_1 in range(n_occ):
                for i_ci_2 in range(n_vir):
                    norm  =   norm + one_state[i_ci_1][i_ci_2] * one_state[i_ci_1][i_ci_2]
            print "Norm before Normailzation: ", norm

            for i_ci_1 in range(n_occ) :
                for i_ci_2 in range(n_vir) :
                    one_state[i_ci_1][i_ci_2] = one_state[i_ci_1][i_ci_2] / (math.sqrt(norm))
            norm = 0.0
            for i_ci_1 in range(n_occ) :
                for i_ci_2 in range(n_vir) :
                    norm  =   norm + one_state[i_ci_1][i_ci_2] * one_state[i_ci_1][i_ci_2]
            print "Norm after Normalization:", norm              
            self.ci['state'][i_state]['trans'] = one_state
        return

    def __mip_ci_td(self):
        """
        Find the most important (mip) CI vector and dump it.
        """
        # dimensional info.
        n_occ = self.dim['nocc_allA']
        n_vir = self.dim['nvir_allA']
        n_state = self.dim['n_state']        
        n_index = n_occ*n_vir < 20 and n_occ*n_vir or 20    # max. 20 ci vectors
        self.ci['n_index'] = n_index    # mip value
        

        print "CI vector"
        ci_info_state = []
        for i_all in range(n_occ*n_vir) :
            ci_info_state.append([])     
               
        # open file for wrt.
        file_out=open('ci.dat', 'w')        
        file_out.write('#  State, CI vector, i_occ, j_vir,  |Coeff^2|)    \n')
        
        # no ci vector for ground state, start from 1.
        for i_state in range(1,n_state) :
            i_all=0
            one_state = self.ci['state'][i_state]['trans']
            for i_ci_1 in range(n_occ) :
                for i_ci_2 in range(n_vir) :
                    ci_dict= {}         
                    ci_dict['state'] = i_state
                    ci_dict['index'] = i_ci_1 * n_vir + i_ci_2+1
                    ci_dict['civector'] = one_state[i_ci_1][i_ci_2]
                    ci_dict['prob'] = math.pow(one_state[i_ci_1][i_ci_2] ,2)
                    ci_dict['index_vir'] = i_ci_2 + 1 + n_occ
                    ci_dict['index_occ'] = i_ci_1 + 1                    
                    ci_info_state[i_all]=ci_dict
#                   print "ci_dict", ci_dict
#                   print "ci_all", i_all, ci_info_state[i_all]
#                   if i_all > 0 :
#                       print "ci_all", i_all-1, ci_all[i_all-1] 
                    i_all=i_all+1 

            # dump sorting info. only for debuging.
            # print "Before sort"
            # for i_all in range(n_occ*n_vir) :
                # print i_all, ci_info_state[i_all]
            ci_info_state = sorted(ci_info_state, key=itemgetter('prob'), reverse=True)
            # print "After sort"
            # print ci_info_state[i_all]

            norm = 0.0
            for i_index in range(n_index) :
                norm  =   norm + ci_info_state[i_index]['civector']**2
            print "Norm (Saved CI vector):", norm

            for i_index in range(n_index) :
                file_out.write('S'+str(ci_info_state[i_index]['state'])+'  '+ \
                                str(ci_info_state[i_index]['civector'])+'    '+ \
                                str(ci_info_state[i_index]['index_occ'])+'   '+ \
                                str(ci_info_state[i_index]['index_vir'])+'  '+ \
                                str((ci_info_state[i_index]['prob']))+'    \n')
        file_out.close()  
                        
        return
    
    def __wrt_ci_td(self, filename = "ci_all.dat"):
        """
        wrt ci infomations.
        """
        # vars
        state = self.ci['state']
        n_state = self.ci['n_state']        
        n_occ = self.dim['nocc_allA']
        n_vir = self.dim['nvir_allA']            
        # open file
        file_out = open(filename, "w")
        file_out.write('#  State, CI vector, i_occ, j_vir,  |Coeff^2|)    \n')
        for i_state in range(1, n_state):
            one_state = self.ci['state'][i_state]['trans']
            for i in range(n_occ) :
                for j in range(n_vir) :
                    c = one_state[i][j]
                    print >>file_out, "S%5d%15.6e%10d%10d%15.6e" % (i_state, c, i+1, j+1+n_occ, c*c)  
                    
        file_out.close()         
        return
            
            
    def __wrt_ci_td_energy(self):
        """
        wrt down energy for each excited state.
        """
        state = self.ci['state']
        n_state = self.ci['n_state']             
        fileout1=open('qm_energy.dat', 'w')
        for i_energy in range(n_state) :
            energy = self.ci['state'][i_energy]['energy'] + self.ci['gs_energy']
            fileout1.write('S'+str(i_energy)+'   '+str( energy)+'  \n')
        fileout1.close()
        return

    def get_ci_td(self):
        """
        wrapper
        get ci vector for hybrid functional et al.

        """
        n_state = self.dim['n_state']
        self.__init_ci_matrix(n_state)
        self.__read_ci_td(n_state)
        self.__wrt_ci_td(filename = "ci_all.dat")
        self.__distrib_ci_matrix()
        self.__norm_ci_td()
        self.__wrt_ci_td(filename = "ci_all_norm.dat") 
        self.__mip_ci_td()    
        self.__wrt_ci_td_energy()
        
        return
        
    
### main program
if __name__ == "__main__":
    ao = gau_log_parser()
    ao.check_calc()       
    ao.get_dim_info()
    
    ao.get_ao_overlap()
    #ao.get_gradient()
    ao.get_dim_info()
    #ao.get_mo()
    ao.get_ci_td()
    ao.get_other()



