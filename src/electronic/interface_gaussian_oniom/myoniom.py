# python
import os
import sys
import re
import math
from operator import itemgetter
import shutil

sys.path.append("../tools/")
import tools


class gau_log_eandg_parser():
    """
    parse gau. log of each layer to obtain energy and force
    especially the lower model
    """
    template = {}
    ci = {}
    def __init__(self, config = {}):
        """ init """
        self.dim = {'n_col': 5}
        self.mo = {"coeffs": [], "energy": [], "alpha": [], "beta": [], \
                   "alpha_energy": [], "beta_energy": [], 'spin': 0} 
        # 0 for close shell case, 1 for open shell case, 1 is not used now
        self.files = {'high-model': "high-model.log", 'template': "layer.json"}
        
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

        # @check correction & dump dimensional info from log.
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
    #   %%% check & prepare for reading data.
    #   gaussian.log file is required.
    #   core orbitals  are frozen in the Gaussian TDDFT implementation
    #   These quantities are read from the log file in t=0  
    # ---------------------------------------------------------------------------
    #
    # Check the DFT and TDDFT output    
    def check_calc(self):
        """
        check and confirm the calc. is ok
        """
        # nothing done
        return

    def load(self):
        """
        load layer.json
        """
        filename = self.files['template']
        obj = tools.load_data(filename)
        self.template = copy.deepcopy(obj)
        return
        
    def get_dim_info(self):
        """
        obtain dimension data.
        such as number of atoms and et al.
        core orbitals  are frozen in the Gaussian TDDFT implementation
        """
        # if old dimension.json is there, ok, simply read it, and return
        if os.path.isfile("dimension.json"):
            self.dim = tools.load_data("dimension.json")
            return
        
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
            # root=3
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
                self.dim['n_state'] = int(m3.group(1)) + 1    # add 1, because of the ground state
            elif m4 is not None:
                self.dim['i_state'] = int(m4.group(1)) + 1
            else:
                continue
        
        file_in.close()
                
        tools.dump_data('dimension.json', self.dim)                
        
        return

    # -------------------------------------------------------------------------
    #   %%% Read all other important information of QM output
    #   gaussian.log file is required.
    #   For example: Transition dipole moment and so on 
    # ---------------------------------------------------------------------------
    def get_oniom_other(self):
        """ extra oniom info. """
        oniom_info = []
        patin = re.compile("Nuclear repulsion from inactive atom pairs")
        logfile = self.files['real']
        fp = open(logfile, "r")
        while True:
            line = fp.readline()
            if line == "":
                break
            m = patin.search(line)
            if m is not None:
                oniom_info.append(line)
        fileout = open('oniom_other.dat', 'w')  
        for line in oniom_info:
            fileout.write(line)
        fileout.write("---------------------------------------------\n")
        fileout.close()        
        return 
        
    def get_excit_other(self):
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
        file_energy = self.files['real']
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
        
        fileout = open('excit_other.dat', 'w')  
        for line in gs:
            fileout.write(line)
        fileout.write("--------------------------------------------------\n")
        for line in es:
            fileout.write(line)
        fileout.write("--------------------------------------------------\n")
        fileout.close()

        return


    def get_other(self):
        """ other QC info """
        self.get_excit_other()
        self.get_oniom_other()
        fileout = open('qm_other.dat', 'w')
        filein1 = open("excit_other.dat","r")
        filein2 = open("oniom_other.dat", "r")
        fileout.write(filein1.read())
        fileout.write(filein2.read())
        filein1.close()
        filein2.close()
        fileout.close()
        return

    # -------------------------------------------------------------------------
    #   %%% Read the gradient
    #   for tda case, only '->' were printed in gaussian log.
    #   the output file are:
    #   qm_gradient.dat
    #   Attention:
    #   gaussian only give force on the atoms, and gradient = - force
    # -------------------------------------------------------------------------   
    def get_gradient(self):
        """ read gradient and punch out """
        logfile = self.files['real']
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
    #   %%% Read the CI excited state energy
    #   the output file is 
    #   qm_energy.dat
    # -------------------------------------------------------------------------
    def __read_excit_energy_block(self, file_in, i_state):
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
        return
    
    def __read_excit_energy(self):
        """
        read only the excited state energy..
        """
        n_state = self.dim['n_state']
        self.ci['state']=[{} for i in xrange(n_state)]
        # open file to read
        logfile = self.files['real']
        file_in = open(logfile, "r")
        # dimensional info.
        print 'Begin to read the CI excit energy from log file' 
        
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
        # note: no ci info for groud state, so start from state 1.      
        for i_block in range(1, n_state):
            self.__read_excit_energy_block(file_in, i_block)                  
        
        return

            
    # -------------------------------------------------------------------------
    # %%% read and dump the real system energy..
    # for different layer
    # oniom energy
    # -------------------------------------------------------------------------
    #
    def __read_total_energy(self):
        """ read oniom energy of the system, for i_state """
        logfile = self.files['real']
        fp = open(logfile, "r")        
        pattern = re.compile("extrapolated energy")
        while True:
            line = fp.readline()
            if line == "":
                break
            m = pattern.search(line)
            if m is not None:
                break
        fp.close()
        if m is not None:
            rec = line.split("=")
            self.ci['this_energy'] = float(rec[1])
        return

    # --------------------------------------------------------------
    # summerized and dump energy
    # --------------------------------------------------------------
    def __summerized_energy(self):
        state = self.ci['state']
        n_state = self.dim['n_state']
        i_state = self.dim['i_state'] - 1
        self.ci['oniom'] = [0.0 for i in xrange(n_state)]
        for i_energy in xrange(n_state):
            self.ci['oniom'][i_energy] = self.ci['this_energy'] - self.ci['state'][i_state]['energy'] + self.ci['state'][i_energy]['energy']
            print "ONIOM A: ", self.ci['oniom'][i_energy]
           
        return

    def __wrt_energy(self):
        """
        wrt down energy for each excited state.
        """
        state = self.ci['state']
        n_state = self.dim['n_state']             
        fileout1=open('qm_energy.dat', 'w')
        for i_energy in xrange(n_state):
            energy = self.ci['oniom'][i_energy]
            fileout1.write('S'+str(i_energy)+'   '+str( energy)+'  \n')
        fileout1.close()
        return
    
    def get_energy(self):
        """ obtain the energy of the system """
        self.__read_excit_energy()
        self.__read_total_energy()
        self.__summerized_energy()
        self.__wrt_energy()
        return        

    
### main program
if __name__ == "__main__":
    eandg = gau_log_eandg_parser()
    eandg.check_calc()       
    eandg.get_dim_info()
    
    eandg.get_gradient()
    eandg.get_energy()
    eandg.get_other()



