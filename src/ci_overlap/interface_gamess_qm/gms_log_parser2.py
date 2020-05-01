# python
import os
import sys
import re
import math
import copy
from operator import itemgetter
import shutil
sys.path.append("../tools/")
import tools

# deal with EFP model

class gms_log_parser2:
    """
    parse gau. log file
    """
    def __init__(self, config = {}):
        """ init """
        self.dim = {'n_col': 5, 'i_state': 1}
        self.ao_overlap = []
        self.mo = {"coeffs": [], "energy": [], "alpha": [], "beta": [], \
                "alpha_energy": [], "beta_energy": [], 'spin': 0} 
                # 0 for close shell case, 1 for open shell case
        self.ci = {}        
        self.files = {'dat': 'gamess.dat', 'log': 'gamess.log', 'interface': 'interface.json',
                      'log2': 'gamess2.log', 'dat2': 'gamess2.dat'}
        
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
            self.files["log"] = self.directory['work'] + "/" + files['job_log'] 
            self.files["dat"] = self.directory['work'] + "/" + files['job_dat']
            self.files["log2"] = self.directory['work'] + "/" + files['job_log2'] 
            self.files["dat2"] = self.directory['work'] + "/" + files['job_dat2'] 
            self.files["interface"] = self.directory['work'] + "/" + files['interface'] 

            self.dim['i_state'] = config['interface']['parm']['i_state']
            
        # key words detected
        if 'ci_assign_problem' in config.keys():
                self.ci_type = config['ci_assign_problem']   # X+Y or X
        else:
                self.ci_type = "X+Y"     # default c = X+Y relationship, and then normalize it      
        
        self.is_do_cis_casida = "no"   # default: do not do cis-casida
        if 'is_do_cis_casida' in config.keys():
            self.is_do_cis_casida = config['is_do_cis_casida']
            
               
        # run the job directly
        
        return


    def get_dim_info(self):
        """
        obtain dimension data.
        such as number of atoms and et al.
        parser gamess-us log file.
        """
        # default setting
        myobj = tools.load_data(self.files['interface'])
        self.dim['n_state'] = myobj['parm']['n_state']
        self.dim['i_state'] = myobj['parm']['i_state']
        # read 
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
        #print line
        # number-of-atoms
        t_line = fp.readline()
        val = t_line.split("=")[1]
        self.dim['n_atom'] = int(val)

        # other
        self.dim['noccA'] = self.dim['neleA']
        self.dim['nvirA'] = self.dim['n_basis'] - self.dim['neleA']
        self.dim['nvir_allA'] = self.dim['nvirA']
        self.dim['nocc_allA'] = self.dim['noccA']
                 
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
            self.dim['n_state'] = int(m.group(1)) + 1 # because of the ground state.
            self.dim['i_state'] = int(m.group(2))
        else:
            print "<^WARNING> CANNOT FIND TD-DFT INPUT PARAMETERS SETTING: [suppose it to be ground state]"
         
        fp.close()
                
        tools.dump_data('dimension.json', self.dim)                

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
        logfile = self.files['log']
        file_in = open(logfile, "r")
        
        if not os.path.isfile(logfile):
            print "DFT & TD calculation results do not exist!"
            print "Check the DFT calculation!"
            raise IOerror  
	    
	    pat_ter = re.compile("EXECUTION OF GAMESS TERMINATED NORMALLY")
	    line_all = file_in.read()
	    m = pat_ter.search(line)

	    if m is None:
	        print "calculation was not terminated normally"
	        raise IOerror	           
     	          
        return
        
    # copy gms data file.
    def prepare_dat(self):
        """
        prepare dat file. copy et al.
        """
        datfile = self.files['dat']       
        sourceFile = "./scr/" + datfile
        targetFile = "./" + datfile
        shutil.copy2(sourceFile, targetFile)
        print "copying data file.."
        
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
        pat1e = re.compile("SUMMARY OF TDDFT RESULTS")
        pat2e = re.compile("RWF  633")
        float_number = '[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
        pat1g = re.compile("ELECTROSTATIC MOMENTS")
        pat2g = re.compile("END OF PROPERTY EVALUATION")
                
        # read all
        i_state = self.dim['i_state']
        if i_state > 1:
            file_energy = self.files['log']
        else:
            file_energy = self.files['log2']
            
        filein = open(file_energy,'r')        
        
        line = "empty"
        # SUMMARY OF TDDFT RESULTS
        while line != "":
            line = filein.readline()
            m1 = pat1e.search(line)
            if m1 is not None:
                break            
        line = filein.readline()
        line = filein.readline()
        
        line = "WWW"
        while line.strip() != "":
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
#   
#   the output file are:
#   qm_gradient.dat
# ---------------------------------------------------------------------------    
    def get_gradient(self):
        """ read gradient and punch out """
        logfile = self.files['dat']
        # logfile = "td.log"
        file_in = open(logfile, "r")
        # locate data.
        pat = re.compile("\$GRAD") 
        # print pattern 
        line = "NOT EMPTY LINE"
        while line != "":
            line = file_in.readline()
            # print line
            m = pat.search(line)
            if m is not None:    
                # jump one line
                line = file_in.readline()
                break
        
        file_out = open("qm_gradient.dat", "w")
        line = "blank line"
        while line != "": 
            line = file_in.readline()
            # print line
            if line.strip() == "$END":
                break
            record = line.split()
            # atomid = int(record[0])
            # atom_charge = int(record[1])
            grad_x = float(record[2])
            grad_y = float(record[3])
            grad_z = float(record[4])
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
        record = line.split()
        
        n_col_tmp = len(record) 
        for i in range(i_start, i_start + n_col_tmp):
            self.mo['energy'][i] = record[i-i_start]
        # jump symbols line
        line = fp.readline()
        # later, the mo coeffs.         
        for i in range(0, n_basis): # i_end eq n_double_basis
            line = fp.readline()
            record = line[17:].split()
            for j in range(i_start, i_start + n_col_tmp):  
                j_col = j -i_start  #                  

                self.mo['coeffs'][j][i] = record[j_col]
                # print record[j_col]
        return        
            

    def __read_mo_matrix(self):
        """ read ao overlap matrix S"""
        # initilize matrix dimension info in log file
        n_basis = self.dim['n_basis']
        n_col = self.dim['n_col']        
 
        i_block_add = (n_basis % n_col != 0) and 1 or 0   
        n_block = n_basis / n_col + i_block_add
        
        # read log file and locate ao overlap matrix
        logfile = self.files['log']
        file_in = open(logfile, "r")
        # locate mo coeffs.
        pat = re.compile("EIGENVECTORS") 
        line = "I-AM-START-MARKER"
        while line != "":
            line = file_in.readline()
            m = pat.search(line)
            # print m, line
            if m is not None:
                line = file_in.readline()
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
        #print mo_energy
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
        

# -------------------------------------------------------------------------
#   %%% Read the CI vector
#   for tda case, only -> were printed in gaussian log.
#   the output file is 
#   ci.dat       Important CI vector
# -------------------------------------------------------------------------
#


    def __read_ci_td_energy(self):
        """
        read in energy of gs & es state.
        """
        n_state = self.dim['n_state']
        i_state = self.dim['i_state']
        # open file to read
        if i_state > 1:
            logfile = self.files['log']
        else:
            logfile = self.files['log2']
            
        file_in = open(logfile, "r")        
        
        print 'Begin to read energy from log file. '         
        # find position.
        pat = re.compile("SUMMARY OF TDDFT RESULTS")
        line = "I-AM-START-MARKER"
        while line != "":
            line = file_in.readline()
            m = pat.search(line)
            if m is not None:
                break
            else:
                continue
        if m is None:
            print "TDDFT RESULTS CANNOT BE FOUND???"
            exit()
            
        line = file_in.readline()
        line = file_in.readline()
        line = file_in.readline()

        self.ci['energy'] = [0 for i in xrange(0, n_state)]
        self.ci['moments'] = [[0 for i in xrange(3)] for j in xrange(0, n_state)]

        line = file_in.readline()
        rec = line.split()
        self.ci['gs_energy'] = float(rec[2])
        self.ci['energy'][0] = self.ci['gs_energy']
        
        for i_state in xrange(1,n_state):
            line = file_in.readline()
            rec = line.split()
            energy = float(rec[2])
            moments = [float(rec[4]), float(rec[5]), float(rec[6])]
            self.ci['energy'][i_state] = energy
            self.ci['moments'][i_state] = moments
               
        return

    def __wrt_ci_td_energy(self, n_state = -1):
        """
        wrt down energy for each excited state. unit (au)
        """
        if n_state < 0:
            n_state = self.dim['n_state']
         
        fileout1=open('qm_energy.dat', 'w')
        
        for i_energy in range(n_state) :
            energy = self.ci['energy'][i_energy] 
            fileout1.write('S'+str(i_energy)+'   '+str(energy)+'  \n')
        fileout1.close()
        return        
                    
 
    def __read_ci_block(self, file_in, i_state):
        """
        read one section of ci coeffs in gms dat file.
        only alpha orbital is considered here.
        """
        #open dat to read X+Y> and X-Y> 
        dim = self.dim
        # dimensional info.
        nocc_allA = dim['nocc_allA']
        nvir_allA = dim['nvir_allA']
        add_alpha = [[0.0 for i in xrange(nvir_allA)] for j in xrange(nocc_allA)] 
        sub_alpha = copy.deepcopy(add_alpha)
        x_alpha = copy.deepcopy(add_alpha)
        y_alpha = copy.deepcopy(add_alpha)
        # jump a few lines 
        for i in xrange(6):
            line = file_in.readline()
            # print line
        
        # read the coefficient and others.
        # first loop occupied, then virtual ones.
        for i in range(nvir_allA):
            for j in range(nocc_allA):
                line = file_in.readline()
                rec = line.split()
                add_alpha[j][i] = float(rec[4])
                sub_alpha[j][i] = float(rec[5])
                x_alpha[j][i] = float(rec[2])
                y_alpha[j][i] = float(rec[3])
                
        # determine the ci assign problem                
        ci_type = self.ci_type
        print "current CI type:", ci_type
        # determine the ci coefficients
        if ci_type == "X+Y":
            alpha_coeffs = copy.deepcopy(add_alpha)
        elif ci_type == "X":
            alpha_coeffs = copy.deepcopy(x_alpha)
        else:
            print "only 'X+Y' & 'X' is avaiable now. td -ci_type"
            exit(1)

        # back up data.
        one_state = {'add_alpha': add_alpha,  \
                         'sub_alpha': sub_alpha,  \
                         'alpha_coeffs': alpha_coeffs, \
                         'nocc_allA': nocc_allA, 'nvir_allA': nvir_allA, \
                         }
        self.ci['state'][i_state] = one_state
            
        print "|X+Y> & |X-Y> DONE"

        return
    

    def __read_ci_td(self):
        """
        read ci paramters
        """
        n_state = self.dim['n_state']
        i_state = self.dim['i_state']
        
        self.ci['state'] = [{} for i in xrange(n_state)]  
        self.ci['n_state'] = n_state
        
        # open file to read
        if i_state > 1:
            logfile = self.files['dat']
        else:
            logfile = self.files['dat2']
        file_in = open(logfile, "r")
        # dimensional info.
        print 'Begin to read the CI vector from log file. ' 
        
        # ground state energy.
        pat = re.compile("\$TDVECS")
        line = "I-AM-START-MARKER"
        while line != "":
            line = file_in.readline()
            m = pat.search(line)
            if m is not None:
                break
            else:
                continue  
 
        # start to process the matrix data.   
        # no ci vector for groud state.              
        for i_block in range(1, n_state):
            self.__read_ci_block(file_in, i_block)                  
        
        return



    def __do_cis_casida(self):
        """ cis casida propose for ci coefficients """
        n_state = self.ci['n_state']

        for i_state in range(1, n_state):                    
            one_state = self.ci['state'][i_state]
            noccA = one_state['nocc_allA']
            nvirA = one_state['nvir_allA']
            # add-alpha add-beta sub-alpha sub-beta
            # only use alpha section now.           
            alpha_coeffs = one_state['alpha_coeffs']
            omega = self.ci['energy'][i_state] - self.ci['gs_energy']    
                    
            for i in range(noccA):
                for j in range(nvirA):
                    orb = self.mo['energy']
                    de = float(orb[j+noccA]) - float(orb[i])
                    # page: 76; 
                    # Nonadiabatic Dynamics of Cis-trans Photoisomerization --- A First Principles ...
                    # Benjamin G. Levine
                    # \Omega \bf F = \omega \bf F
                    # F = (A-B)^(-1/2) |X+Y>
                    # the solved equation in gaussian is F not |X+Y>, so sqrt(de/omega)
                    alpha_coeffs[i][j] = alpha_coeffs[i][j]  * math.sqrt(de/omega)
                  
        # we use $c_{ia} = \sqrt{\frac{\Omega_a}{\epsilon_a - \epsilon_i}} |X+Y>$                                
            one_state['alpha_coeffs'] = alpha_coeffs
            self.ci['state'][i_state] = one_state
                
        return     


    def __norm_ci_td(self):
        """
        normalization test and so on.
        """
        # dimensional info.
        n_state = self.dim['n_state']
        n_occ = self.dim['noccA']
        n_vir = self.dim['nvirA']
        
        for i_state in range(1, n_state):
            print "Check normalization for State:", i_state
            norm = 0.0
            one_state = self.ci['state'][i_state]
            alpha_coeffs = one_state['alpha_coeffs']
            for i_ci_1 in range(n_occ):
                for i_ci_2 in range(n_vir):
                    norm  =   norm + alpha_coeffs[i_ci_1][i_ci_2] * alpha_coeffs[i_ci_1][i_ci_2]
            print "Norm before Normailzation: ", norm

            for i_ci_1 in range(n_occ) :
                for i_ci_2 in range(n_vir) :
                    alpha_coeffs[i_ci_1][i_ci_2] = alpha_coeffs[i_ci_1][i_ci_2] / (math.sqrt(norm))
            norm = 0.0
            for i_ci_1 in range(n_occ) :
                for i_ci_2 in range(n_vir) :
                    norm  =   norm + alpha_coeffs[i_ci_1][i_ci_2] * alpha_coeffs[i_ci_1][i_ci_2]
            print "Norm after Normalization:", norm    
            one_state['alpha_coeffs'] = alpha_coeffs         
            self.ci['state'][i_state] = one_state
        return

    def __mip_ci_td(self, n_state = -1):
        """
        Find the most important (mip) CI vector and dump it.
        """
        if n_state < 0:
            n_state = self.dim['n_state']  
        # dimensional info.
        n_occ = self.dim['nocc_allA']
        n_vir = self.dim['nvir_allA']      
        n_index = n_occ*n_vir < 20 and n_occ*n_vir or 20    # max. 20 ci vectors
        self.ci['n_index'] = n_index    # mip value
        
        print "CI vector"        
         
        # open file for wrt.
        file_out=open('ci.dat', 'w')        
        file_out.write('#  State, CI vector, i_occ, j_vir,  |Coeff^2|)    \n')
        
        # no ci vector for ground state, start from 1.
        for i_state in range(1,n_state):
            i_all=0
            ci_info_state = [{} for i in xrange(n_occ*n_vir)]
            one_state = self.ci['state'][i_state]
            alpha_coeffs = one_state['alpha_coeffs']
            for i_ci_1 in range(n_occ) :
                for i_ci_2 in range(n_vir) :
                    ci_dict= {}         
                    ci_dict['state'] = i_state
                    ci_dict['index'] = i_ci_1 * n_vir + i_ci_2+1
                    ci_dict['civector'] = alpha_coeffs[i_ci_1][i_ci_2]
                    ci_dict['prob'] = alpha_coeffs[i_ci_1][i_ci_2] * alpha_coeffs[i_ci_1][i_ci_2]
                    ci_dict['index_vir'] = i_ci_2 + 1 + n_occ
                    ci_dict['index_occ'] = i_ci_1 + 1                    
                    ci_info_state[i_all]=ci_dict

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
            del ci_info_state                    
        file_out.close()  
                        
        return
        

    def __wrt_ci_td(self, filename = "ci_all.dat", n_state = -1):
        """
        wrt ci infomations.
        """
        # vars
        dim = self.dim
        if n_state < 0:
            n_state = self.dim['n_state']
            
        state = self.ci['state']   
        n_occ = self.dim['nocc_allA']
        n_vir = self.dim['nvir_allA']  

        # open file
        file_out = open(filename, "w")
        file_out.write('#  State, CI vector, i_occ, j_vir,  |Coeff^2|)    \n')
        for i_state in range(1, n_state):
            coeffs = self.ci['state'][i_state]['alpha_coeffs']
            for i in range(n_occ) :
                for j in range(n_vir) :
                    c = coeffs[i][j]
                    print >>file_out, "S%5d%15.6e%10d%10d%15.6e" % (i_state, c, i+1, j+1+n_occ, c*c)  
                    
        file_out.close()   
              
        return

    
    def get_ci_td_es(self):
        """ 
        read ci vector in td.
        """        
        # td excited state energy
        self.__read_ci_td_energy()
        
        self.__wrt_ci_td_energy()
        # ci coefficient X+Y & X-Y
        self.__read_ci_td() 
        self.__wrt_ci_td(filename = "ci_all.dat") 
        
        # relation: $ c_{ia} = (\epsilon_a-\epsilon_i)^{-1/2}(X_{ia}+Y_{ia}) $
        if self.is_do_cis_casida == "yes":
            self.__do_cis_casida()
        
        # normalization and et al.
        self.__norm_ci_td() 
        self.__wrt_ci_td(filename = "ci_all_norm.dat") 
        self.__mip_ci_td()  
 
        return

    # ground state case.
    def __read_ground_state_energy(self, n_state = -1):
        """
        read in gs energy, that is the case,
        when, no excitation is on
        """
        if n_state < 0:
            n_state = self.dim['n_state']
        logfile = self.files['log']
        file_in = open(logfile, "r")

        print "Begin to read energy from log file"
        # find position
        pat = re.compile("ENERGY COMPONENTS")
        line = "not-empty-line"
        while line != "":
            line = file_in.readline()
            m = pat.search(line)
            if m is not None:
                break
            else:
                continue
        pat = re.compile("TOTAL ENERGY")
        while line != "":
            line = file_in.readline()
            m = pat.search(line)
            if m is not None:
                break
            else:
                continue
            
        self.ci['energy'] = [0 for i in xrange(0, n_state)]
        self.ci['moments'] = [[0 for i in xrange(3)] for j in xrange(0, n_state)]
        rec = line.split("=")
        gs_energy = float(rec[1])
        self.ci['gs_energy'] = gs_energy
        self.ci['energy'][0] = self.ci['gs_energy']
        
        for i_state in xrange(1,n_state):
            energy = 999999
            moments = [999999, 999999, 999999]
            self.ci['energy'][i_state] = energy
            self.ci['moments'][i_state] = moments
                
        return


 
    def __set_ci_block_gs(self, i_state):
        """
        read one section of ci coeffs in gms dat file.
        only alpha orbital is considered here.
        """
        #open dat to read X+Y> and X-Y> 
        dim = self.dim
        # dimensional info.
        nocc_allA = dim['nocc_allA']
        nvir_allA = dim['nvir_allA']
        add_alpha = [[0.0 for i in xrange(nvir_allA)] for j in xrange(nocc_allA)] 
        sub_alpha = copy.deepcopy(add_alpha)
        x_alpha = copy.deepcopy(add_alpha)
        y_alpha = copy.deepcopy(add_alpha)
        # jump a few lines 

        # read the coefficient and others.
        # first loop occupied, then virtual ones.
        for i in range(nvir_allA):
            for j in range(nocc_allA):
                add_alpha[j][i] = 0.0
                sub_alpha[j][i] = 0.0
                x_alpha[j][i] = 0.0
                y_alpha[j][i] = 0.0
                
        # determine the ci assign problem                
        ci_type = self.ci_type
        print "current CI type:", ci_type
        # determine the ci coefficients
        if ci_type == "X+Y":
            alpha_coeffs = copy.deepcopy(add_alpha)
        elif ci_type == "X":
            alpha_coeffs = copy.deepcopy(x_alpha)
        else:
            print "only 'X+Y' & 'X' is avaiable now. td -ci_type"
            exit(1)

        # back up data.
        one_state = {'add_alpha': add_alpha,  \
                         'sub_alpha': sub_alpha,  \
                         'alpha_coeffs': alpha_coeffs, \
                         'nocc_allA': nocc_allA, 'nvir_allA': nvir_allA, \
                         }
        self.ci['state'][i_state] = one_state
            
        print "|X+Y> & |X-Y> DONE"

        return
    

    def __set_ci_td_gs(self, n_state):
        """
        read ci paramters
        """
       
        self.ci['state'] = [{} for i in xrange(n_state)]  
        self.ci['n_state'] = n_state              

        # start to process the matrix data.   
        # no ci vector for groud state.              
        for i_block in range(1, n_state):
            self.__set_ci_block_gs(i_block)                  
        
        return


    def get_ci_td_gs(self):
        """
        read information in td for gs condition
        """
        # myobj = tools.load_data(self.files['interface'])
        # n_state = myobj['parm']['n_state']
        # energy
        # self.__read_ground_state_energy(n_state)
        # self.__wrt_ci_td_energy(n_state)
        # ci coefficients
        # self.__set_ci_td_gs(n_state)
        # punch out
        # self.__wrt_ci_td(filename = "ci_all.dat", n_state = n_state)
        # punch out more as es. condition
        # self.__wrt_ci_td(filename = "ci_all_norm.dat", n_state = n_state) 
        # self.__mip_ci_td(n_state)
        
        return
    

    def get_ci_td(self):
        """
        read in ci info.
        """
        i_state = self.dim['i_state']
        
        if i_state > -1:
            self.get_ci_td_es()
        else:
            # self.get_ci_td_gs()
            print "GROUND STATE CASE.."

        return
    
    
### main program
if __name__ == "__main__":
    ao = gms_log_parser()
 
    ao.get_gradient()
    ao.get_dim_info()
    ao.get_mo()
    ao.get_ci_td()
    #ao.get_other()



