# python
import os
import sys
import re
import copy
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
    # add or minus of oniom layer
    factor = {'high-model': 1.0, 'med-mid': 1.0, 'low-real': 1.0, \
              'low-mid': -1.0, 'med-model': -1.0, 'low-model': -1.0 }
    template = {}
    ci = {}
    gradient = []
    energy = []
  
    def __init__(self, config = {}):
        """ init """
        self.dim = {'n_col': 5}
        self.mo = {"coeffs": [], "energy": [], "alpha": [], "beta": [], \
                   "alpha_energy": [], "beta_energy": [], 'spin': 0} 
        # 0 for close shell case, 1 for open shell case, 1 is not used now
        self.files = {'high-model': "high-model.log", 'template': "layer.json", \
                      'mo': 'high-model.log'}
        
        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files'] 
            # working directory & files >>>
            self.directory = {}
            self.directory['root'] = root_dir
            self.directory['home'] = root_dir + "/" + dirs['home']
            self.directory['work'] = self.directory['home'] + "/" + dirs['work']
                        
            self.files = {}
            self.files["mo"] = self.directory['work'] + "/" + files['high-model-log'] 

        # @check correction & dump dimensional info from log.
        self.load()
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
    #   %%% Read the gradient
    #   the output file are:
    #   qm_gradient.dat
    #   Attention:
    #   gaussian only give force on the atoms, and gradient = - force
    # -------------------------------------------------------------------------
    def get_gradient(self):
        """
        get gradient energy for each layer
        """
        n_atom = self.dim['n_atom']
        grad = [[0.0 for j in xrange(3)] for i in xrange(n_atom)]
        for name in self.template.keys():
            self.get_gradient_layer(name)
            g = self.template[name]['gradient']
            f_mul = self.factor[name]
            for i in xrange(n_atom):
                grad[i][0] += g[i][0] * f_mul
                grad[i][1] += g[i][1] * f_mul
                grad[i][2] += g[i][2] * f_mul
        fp = open("qm_gradient.dat", "w")
        for gi in grad:
            print >>fp, "%20.12f%20.12f%20.12f" % (gi[0], gi[1], gi[2])
        fp.close()
        return
    
    def get_gradient_layer(self, name):
        """ read gradient and punch out """
        logfile = name + ".log"
        file_in = open(logfile, "r")
        # locate data.
        pattern = re.compile("Forces \(Hartrees\/Bohr\)") 
        # print pattern 
        line = "NOT EMPTY LINE"
        while line != "":
            line = file_in.readline()
            m = pattern.search(line)
            if m is not None:    
                # jump two useless line
                line = file_in.readline()
                line = file_in.readline()
                break
        # dump the data
        g = []
        file_out = open(name + "-gradient.dat", "w")
        while line != "": 
            line = file_in.readline()           
            pattern = re.compile("-"*20)
            m = pattern.search(line)
            if m is not None:
                break
            record = line.split()
            # atomid = int(record[0])
            # atom_charge = int(record[1])
            grad_x = -float(record[2])
            grad_y = -float(record[3])
            grad_z = -float(record[4])
            g.append([grad_x, grad_y, grad_z])
            file_out.write(''+str( grad_x )+'   '+ \
                            str( grad_y )+'   '+str( grad_z )+'  \n')
            
        if m is None:
            print "GRIDENT READ FAILED"
        file_in.close() 
        file_out.close()
        self.template[name]['gradient'] = g
        return        


    # -------------------------------------------------------------------------
    #   %%% Read all other important information of QM output
    #   gaussian.log file is required.
    #   For example: Transition dipole moment and so on 
    # ---------------------------------------------------------------------------
    def get_other(self):
        """ extra oniom info. """
        oniom_info = []
        patin = re.compile("Nuclear repulsion from inactive atom pairs")
        logfile = self.files['mo']
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
        
    # -------------------------------------------------------------------------
    #   %%% Read the CI excited state energy
    #   the output file is 
    #   qm_energy.dat
    # -------------------------------------------------------------------------
    def get_energy_highmodel(self):
        """
        read energy from high-model-energy.dat
        generated by wf_parser of highmodel
        """
        filename = "high-model-energy.dat"
        fp = open(filename, "r")
        energy = []
        while True:
            line = fp.readline()
            if line.strip() == "":
                break
            record = line.split()
            energy.append({'name': record[0], 'energy': float(record[1])})
        self.energy = energy
               
        return


    def __get_es_energy_highmodel(self):
        """ excited state energy """
        logfile = self.files['mo']
        fp = open(logfile, 'r')
        block = []
        es_energy = [0.0] # note 0.0 is for gs  
        pat = re.compile("Excited State\s+\d+")
        float_number = '[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
        while True:
            line = fp.readline()
            if line == "":
                break
            m = pat.search(line)
            if m is not None:
                block.append(line)
        pat = re.compile("(" + float_number + ")\s+eV", re.IGNORECASE)
        for line in block:
            m = pat.search(line)
            if m is None:
                print ("something is wrong in reading excited energy...")
                exit(1)
            s = float(m.group(1))
            es_energy.append(s)
        
        return es_energy

    def __get_gs_energy_highmodel(self):
        """ excited state energy of gs. """
        # open file to read
        logfile = self.files['mo']
        file_in = open(logfile, "r")
               
        # ground state energy.
        pat = re.compile("SCF Done")
        while True:
            line = file_in.readline()
            if line == "":
                break
            m = pat.search(line)
            if m is not None:
                break
            else:
                continue
       
        gs_energy = float(line.split()[4])

        return gs_energy
        
            
    def get_energy_highmodel(self):
        """
        read in energy of high model
        """
        n_state = self.dim['n_state']
        energy = [0.0 for i in xrange(n_state)]
        
        gs_energy = self.__get_gs_energy_highmodel()
        es_energy_list = self.__get_es_energy_highmodel()

        energy[0] += gs_energy
        
        for i in xrange(1, n_state):
            energy[i] = gs_energy + es_energy_list[i]
       
        fp=open('high-model-energy.dat', 'w')
        for i in range(n_state) :
            state_name = 'S'+str(i)
            self.energy.append({'name': state_name, 'energy': energy[i]})
            
            fp.write(state_name + '   ' + str(energy[i]) + '  \n')
        fp.close()
        
        return
    
 
    def get_energy_layer(self, name):
        """
        read energy of each layer, except high-model
        """
        logfile = name + ".log"
        file_in = open(logfile, "r")
        # locate data.
        float_number = '[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
        pat = re.compile("HF=(" + float_number + ")")
        # print pattern 
        while True:
            line = file_in.readline()
            if line == "":
                break
            m = pat.search(line)
            if m is not None:
                ene = float(m.group(1))
                break
        if m is None:
            print ("cannot find HF=energy term in log file")
            exit(0)
        fp = open(name + "-energy.dat", "w")
        print >>fp, "%20.12f" % ene
        fp.close()
        return ene
    
    def get_energy(self):
        """
        read energy of other model
        """
        ene = 0.0
        self.get_energy_highmodel()
        for name in self.template.keys():
            f_mul = self.factor[name] 
            if name != "high-model":
                ene += self.get_energy_layer(name) * f_mul
        fp = open("qm_energy.dat", "w")                
        for x in self.energy:
            x['energy'] += ene
            print >>fp, "%-10s%20.12f" % (x['name'], x['energy'])
        fp.close()
        return
                               
   
### main program
if __name__ == "__main__":
    eandg = gau_log_eandg_parser()
    eandg.check_calc()       
    eandg.get_dim_info()
    
    eandg.get_gradient()
    eandg.get_energy()
    eandg.get_other()



