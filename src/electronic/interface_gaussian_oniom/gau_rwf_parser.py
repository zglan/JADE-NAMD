# python
import os
import sys
import re
import copy
import math
from operator import itemgetter

sys.path.append("../tools/")
import tools


    ### =============== collect QC data for dynamics ===================== ###
    # ci vector & mo eigen-value/vector
    #  ---------------------------------------------------------------------
    #  
    #  This subrountine is used to read the TDDFT output of QC code
    # 
    #  'gaussian.chk & gaussian.log is required.
    #  
    #  Two output files are:
    #      (1) mo.dat      The MO coefficient
    #      (2) ci.dat       Important CI vector
    #----------------------------------------------------------------------------------------- 
# suppose the rwf file is obtained.

class gau_rwf_parser():
    """ parse rwf file of gaussian """
    def __init__(self, config = {}):
        """ 
        basic variables
        """
        self.config = config
        self.files = {'chk': "gaussian.chk", 'mo': 'gaussian.log'}
        self.dim = {}  
        self.ci = {}
        self.mo = {}     
                              
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
            self.files["mo"] = self.directory['work'] + "/" + files['gau_log'] 
            self.files["chk"] = self.directory['work'] + "/" + files['gau_chk'] 


        # check & dump dimensional dat. 
        self.__get_dim_info()
        self.prepare_chk() 
        # key words detected
        if 'ci_assign_problem' in config.keys():
                self.ci_type = config['ci_assign_problem']   # X+Y or X
        else:
                # default c = X+Y relationship, and then normalize it      
                self.ci_type = "X+Y"    
        
        self.is_do_cis_casida = "no"   # default: do not do cis-casida
        if 'is_do_cis_casida' in config.keys():
            self.is_do_cis_casida = config['is_do_cis_casida']
               

                    
        return        


# -------------------------------------------------------------------------
#   gaussian.log file is required.
#   this would only be called if this file is the main program
#   These quantities are read from the log file in t=0 
# ---------------------------------------------------------------------------    
    def __get_dim_info(self):
        """
        obtain dimension data.
        such as number of atoms and et al.
        core orbitals  are frozen in the Gaussian TDDFT implementation
        """   
        logfile = self.files['mo']
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
            pat4 = re.compile("root=(\d)+", re.IGNORECASE)
            # ..
            m0 = pat0.search(line)           
            m1 = pat1.search(line)
            m2 = pat2.search(line)
            m3 = pat3.search(line)
            m4 = pat4.search(line)
            
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
            elif m4 is not None:
                string = m4.group()
                record = string.split("=")
                self.dim['i_state'] = int(record[1]) + 1    
            else:
                continue
        
        file_in.close()
        print "DIMENSIONAL INFO DONE"
        tools.dump_data('dimension.json', self.dim)                

        return
        
# ----------------------------------------------------------------
# check the required input for this parser.
    def __check_calc(self):
        """
        require the existence of log & chk in the current directory
        """
        # nothing done
        return        

# ----------------------------------------------------------------
# to generate Record files from Gaussian chk file
    def prepare_chk(self):
        """
        run rwfdump to obtain Record file, such as ci vector eigen-mo et al.
        """        
        if not os.path.isfile(self.files['chk']):
            print "DFT & TD calculation results do not exist!"
            print self.files['chk']
            exit(1)
            
        chkfile = self.files['chk']       
        # eigenvalues: file containing  KS energies 
        os.system("rwfdump " + chkfile + " 522R.dat 522R")
        # MO_coefs: file containing MO coeficients of alpha orbital
        # MO coefficients, real beta. is 526R; this is not used in closed shell case
        os.system("rwfdump " + chkfile + " 524R.dat 524R")          
        # excited state energy & transition moments
        os.system("rwfdump " + chkfile + " 770R.dat 770R")      
        # file containing TDDFT vectors X+Y> and X-Y>
        os.system("rwfdump " + chkfile + " 635R.dat 635R")                
        print "chk file converted to Record files"
        return        
# ---------------------------------------------------------------- 
# -------------------------------------------------------------------------
#   %%% read mo eigenvalue/vector
#   522R.dat & 524R.dat file is required.
#   called routine: get_mo()
# ---------------------------------------------------------------------------  

    def __read_mo_energy(self):
        """ 
            mo engenvalue
            522R Eigenvalues, alpha and if necessary, beta. 
            522R contain alpha & beta ks energies with dimensiton of 2*n_basis
        """
        n_basis = self.dim['n_basis']
        
        filename = "522R.dat"        
        fp = open(filename, "r")   
             
        pat = re.compile("Dump of file   522")
        line = "empty line"
        while line != "":
            line = fp.readline()          
            m = pat.search(line)
            if m is not None:
                break 
        data = []
        while line != "":
            line = fp.readline()
            record = line.split()
            n_rec = len(record)
            for i in range(n_rec):
                data.append( record[i].replace('D', 'E') )
        # the alpha is used with dimension of n_basis for close shell case
        alpha = data[0:n_basis]
        # only alpha is used, for the case of close shell only
        self.mo['energy'] = {'alpha': alpha, 'n_alpha': n_basis}         
        print "READ MO ENERGY"
        return       
    def __read_mo(self):
        """
        mo vector
        524R for MO coefficients, real alpha.
        526R for MO coefficients, real beta. not considered here
        """
        n_basis = self.dim['n_basis']
        
        filename = "524R.dat"        
        fp = open(filename, "r")
        
        pat = re.compile("Dump of file   524")
        line = "empty line"
        while line != "":
            line = fp.readline()
            m = pat.search(line)
            if m is not None:
                break 
        data = []
        while line != "":
            line = fp.readline()
            record = line.split()
            n_rec = len(record)
            for i in range(n_rec):
                data.append( record[i].replace('D', 'E') )
                
        # alpha for closed shell. dimension: n_basis*n_basis        
        alpha = [[data[i*n_basis+j] for j in xrange(n_basis)] for i in xrange(n_basis)]
        # only alpha is used, for the case of close shell only
        self.mo['vector'] = {'alpha': alpha, 'n_alpha': n_basis}                            
        print "READ MO vector"        
        return
                
    def __wrt_mo(self):
        """ wrt done mo matrix in specific format """
        # dim. info.
        n_basis = self.dim['n_basis']
        # vars
        coeffs = self.mo['vector']['alpha']
        mo_energy = self.mo['energy']['alpha']
        
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
        read/write mo vector
        """
        if not os.path.isfile(self.files['mo']):
            print "DFT & TD calculation results do not exist!"
            print self.files['mo']
            exit(1)
        
        self.__read_mo()
        self.__read_mo_energy()
        self.__wrt_mo()
        print "MO SECTION DONE"
        return
                     
# -------------------------------------------------------------------------
#   %%% ci vector related routine
#   gaussian.chk file is required.
#   core orbitals  are frozen in the Gaussian TDDFT implementation
#   These quantities are read from the log file in t=0  
# ---------------------------------------------------------------------------                
    def __read_ci_td_energy(self):
        """
        read excited energy
        770R Saved ground-to-excited state energies and transition moments
        770R format:
        energy(1) + transition moments(15)
        the first 10 + 2 * number-of-excited-state record is useless
        jump_num = 10 + 2 * (n_state-1)  numbers should be ignored.
        energy(1) is the excited energy (+ ground state energy)
        They are: 
        Ground to excited state transition electric dipole moments (Au): three per state
            state          X           Y           Z  

        Ground to excited state transition velocity dipole moments (Au): three per state
            state          X           Y           Z 

        Ground to excited state transition magnetic dipole moments (Au): three per state
            state          X           Y           Z

        Ground to excited state transition velocity quadrupole moments (Au): six per state
            state          XX          YY          ZZ          XY          XZ          YZ
        """
        n_state = self.dim['n_state']
        
        filename = "770R.dat"
        fp = open(filename, "r")
        pat = re.compile("Dump of file   770")
        line = "empty line"
        while line != "":
            line = fp.readline()
            m = pat.search(line)
            if m is not None:
                break         
        data = []
        while line != "":
            line = fp.readline()
            record = line.split()
            n_rec = len(record)
            for i in range(n_rec):
                data.append( record[i].replace('D', 'E') )

        # the previous 10 + 2 * number-of-excited-state record is useless
        jump_num = 10 + 2 * (n_state-1)
        data = data[jump_num:]
        
        self.ci['energy'] = [0 for i in xrange(0, n_state)]
        self.ci['moments'] = [[0 for i in xrange(15)] for j in xrange(0, n_state)]
        for i_state in xrange(1,n_state):
            energy = data[(i_state-1)*16]
            moments = data[(i_state-1)*16+1: (i_state)*16]
            self.ci['energy'][i_state] = float(energy)
            self.ci['moments'][i_state] = moments   
        return      
    def __wrt_ci_td_energy(self):
        """
        wrt down energy for each excited state. unit (au)
        """
        n_state = self.dim['n_state']
        # get the ground state energy
        logfile = self.files['mo']
        fp = open(logfile, "r")
        pat = re.compile("SCF Done")
        line = "I-AM-START-MARKER"
        while line != "":
            line = fp.readline()
            m = pat.search(line)
            if m is not None:
                break
            else:
                continue  
        fp.close()
        self.ci['gs_energy'] = float(line.split()[4])
        self.ci['energy'][0] = self.ci['gs_energy']      
                  
        fileout1=open('qm_energy.dat', 'w')
        for i_energy in range(n_state) :
            energy = self.ci['energy'][i_energy] 
            fileout1.write('S'+str(i_energy)+'   '+str(energy)+'  \n')
        fileout1.close()
        return        
                    

    # CI vector
    def __read_ci_635R(self):
        """
        read ci from rwf dump 635R
        """
        #open rwf to read X+Y> and X-Y> 
        dim = self.dim
        # dimensional info.
        noccA = dim['noccA']
        nvirA = dim['nvirA']
        noccB = dim['noccB']
        nvirB = dim['nvirB']      
        n_state = dim['n_state']
        
        # number of elements per state to be readed.
        # exclued ground state so n_state - 1
        n_emts = (noccA*nvirA + noccB*nvirB) * (n_state-1) * 2 + 12

        filename = "635R.dat"
        fp = open(filename, "r")
        pat = re.compile("Dump of file   635")
        line = "empty line"
        while line != "":
            line = fp.readline()
            m = pat.search(line)
            if m is not None:
                break 
        data = []
        while line != "":
            line = fp.readline()
            record = line.split()
            n_rec = len(record)
            for i in range(n_rec):
                data.append( record[i].replace('D', 'E') )

       # only alpha is valid in current case                 
        self.ci['raw635R'] = data[12:n_emts]
                          
        return 
        
    def __distrib_ci_matrix(self):
        """
        obtain one ci state X+Y & X-Y
        """
        data = self.ci['raw635R']      

        # dimensional info.
        dim = self.dim
        nocc_allA = dim['nocc_allA']
        nvir_allA = dim['nvir_allA']
        nocc_allB = dim['nocc_allB']
        nvir_allB = dim['nvir_allB'] 
        nfix_core = dim['nfixcore'] 
              
        noccA = dim['noccA']
        nvirA = dim['nvirA']
        noccB = dim['noccB']
        nvirB = dim['nvirB']
        n_state = dim['n_state']        
        
        n_alpha_size = noccA * nvirA
        n_beta_size  = noccB * nvirB
        n_ab_size = n_alpha_size + n_beta_size
        n_add_size = n_ab_size * (n_state - 1)
                    
        self.ci['state'] = [{} for i in xrange(n_state)]  
        self.ci['n_state'] = n_state    
             
        # four condition, X OR X+Y; \EPSION OR NOT
             
        for i_state in range(1, n_state):
            add_alpha = [[0.0 for i in xrange(nvir_allA)] for j in xrange(nocc_allA)] 
            sub_alpha = copy.deepcopy(add_alpha)
            add_beta  = [[0.0 for i in xrange(nvir_allB)] for j in xrange(nocc_allB)]
            sub_beta  = copy.deepcopy(add_beta)
  
            one_state = {}
            ip = (i_state - 1) * n_ab_size
            # add-alpha add-beta sub-alpha sub-beta
            # only use alpha section now.
            # state x:
            # <\alpha X+Y \beta X+Y>
            # state y:
            # ......  
            # Then state x:
            # <\alpha X-Y \beta X-Y>                   
            for i in range(noccA):
                for j in range(nvirA):
                    add_alpha[i+nfix_core][j] = float(data[ip + i*nvirA+j])
                    sub_alpha[i+nfix_core][j] = float(data[ip + n_add_size + i*nvirA+j])
            for i in range(noccB):
                for j in range(nvirB):
                    add_beta[i+nfix_core][j] = float(data[ip + n_alpha_size + i*nvirB+j])
                    sub_beta[i+nfix_core][j] = float(data[ip + n_alpha_size + n_add_size + i*nvirB+j])
            # determine the ci assign problem                
            ci_type = self.ci_type
            print "current CI type:", ci_type
            # determine the ci coefficients
            if ci_type == "X+Y":
                alpha_coeffs = copy.deepcopy(add_alpha)
                beta_coeffs  = copy.deepcopy(add_beta)       
            elif ci_type == "X":
                alpha_coeffs = [[(add_alpha[i][j]+sub_alpha[i][j]) for j in xrange(nvir_allA)] for i in xrange(nocc_allA)]
                beta_coeffs = [[(add_beta[i][j]+sub_beta[i][j]) for j in xrange(nvir_allB)] for i in xrange(nocc_allB)]
            else:
                print "only 'X+Y' & 'X' is avaiable now. td -ci_type"
                exit(1)

            # back up data.
            one_state = {'add_alpha': add_alpha, 'add_beta': add_beta, \
                         'sub_alpha': sub_alpha, 'sub_beta': sub_beta, \
                         'alpha_coeffs': alpha_coeffs, 'beta_coeffs': beta_coeffs, \
                         'nocc_allA': nocc_allA, 'nvir_allA': nvir_allA, \
                         'nocc_allB': nocc_allB, 'nvir_allB': nvir_allB}
            self.ci['state'][i_state] = one_state
        print "|X+Y> & |X-Y> DONE"
        return       
   
    def __do_cis_casida(self):
        """ cis casida propose for ci coefficients """
        
        # relation: $ c_{ia} = (\epsilon_a-\epsilon_i)^{-1/2}(X_{ia}+Y_{ia}) $
        if self.is_do_cis_casida != "yes":
             return
        
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
                    orb = self.mo['energy']['alpha']
                    de = float(orb[j+noccA]) - float(orb[i])
                    # page: 76; 
                    # Nonadiabatic Dynamics of Cis-trans Photoisomerization --- A First Principles ...
                    # Benjamin G. Levine
                    # \Omega \bf F = \omega \bf F
                    # F = (A-B)^(-1/2) |X+Y>
                    # the solved equation in gaussian is F not |X+Y>, so sqrt(de/omega)
                    alpha_coeffs[i][j] = alpha_coeffs[i][j]  * math.sqrt(de/omega)
                  
            one_state['alpha_coeffs'] = alpha_coeffs
            self.ci['state'][i_state] = one_state
                
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
        
    def __wrt_ci_td(self, filename = "ci_all.dat"):
        """
        wrt ci infomations.
        """
        # vars
        dim = self.dim
        
        state = self.ci['state']
        n_state = self.dim['n_state']        
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
        
              
    def get_ci_td(self):
        """ 
        read ci from rwf 
        file 635R containing TDDFT vectors X+Y> and X-Y>
        """        
        # td excited state energy
        self.__read_ci_td_energy()
        self.__wrt_ci_td_energy()
        # ci coefficient X+Y & X-Y
        self.__read_ci_635R()
        self.__distrib_ci_matrix()  
        self.__wrt_ci_td(filename = "ci_all.dat") 
        
        # relation: $ c_{ia} = (\epsilon_a-\epsilon_i)^{-1/2}(X_{ia}+Y_{ia}) $

        self.__do_cis_casida()
        
        # normalization and et al.
        self.__norm_ci_td() 
        self.__wrt_ci_td(filename = "ci_all_norm.dat") 
        self.__mip_ci_td()  
         # per state per spin
         # in each state, there is X+Y and X-Y
         # the data in rwf 635 is
         # state 1:
         # <\alpha X+Y \beta X+Y>
         # state 2:
         # ......  
         # <\alpha X-Y \beta X-Y>
        return


    
# main program.
if __name__ == "__main__":      
    gau = gau_rwf_parser()
    gau.prepare_chk()        
    gau.get_mo()    
    gau.get_ci_td()
    



    
    
