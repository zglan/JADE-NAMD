# python
import os
import sys
import re
import math
from operator import itemgetter
import shutil

sys.path.append("../tools/")
import tools
import FileMan


class gau_log_parser():
    """
    parse gau. log file
    """
    def __init__(self, config = {}):
        """ init """
        self.dim = {'n_col': 5}
        self.files = {'log': 'gaussian.log'}
        
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
            self.files["log"] = self.directory['work'] + "/" + files['gau_log'] 
        
        return

#
# -------------------------------------------------------------------------
#   %%% check & prepare for reading data.
#   gaussian.log file is required.
# ---------------------------------------------------------------------------
#
#   Check the DFT output   
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
        logfile = self.files['log']
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

# ------------------------------------------------
# read energy of the system. g.s.
# qm_energy.dat
# ------------------------------------------------        
    def get_energy(self):
        """ read energy from log file and punch out """
        logfile = self.files['log']
        # logfile = "td.log"
        file_in = open(logfile, "r")
        # locate data.
        pattern = re.compile("SCF Done") 
        # print pattern 
        line = "NOT EMPTY LINE"
        while line != "":
            line = file_in.readline()
            m = pattern.search(line)
            if m is not None:    
                # jump two line
                break
        file_in.close() 
        if m is None:
            print "SCF ERROR; CHECK IT..."
            exit(0)
        file_out = open("qm_energy.dat", "w")        
        record = line.split()
        gs_ene = "%20.12f\n" % float(record[4])
        file_out.write("# energy (a.u.)\n")
        file_out.write(gs_ene)
        file_out.close()       
        return
        
# -------------------------------------------------------------------------
#   %%% Read the gradient
#   the output file are:
#   qm_gradient.dat
#   Attention:
#   gaussian only give force on the atoms, so gradient = - force
# ---------------------------------------------------------------------------    
    def get_gradient(self):
        """ read gradient and punch out """
        logfile = self.files['log']
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
        file_out.write("# Forces (Hartrees/Bohr)\n")
        while line != "": 
            line = file_in.readline()           
            pattern = re.compile("-------------")
            m = pattern.search(line)
            if m is not None:
                break
            record = line.split()
            # atomid = int(record[0])
            # atom_charge = int(record[1])
            grad_x = "%20.12f" % -float(record[2])
            grad_y = "%20.12f" % -float(record[3])
            grad_z = "%20.12f\n" % -float(record[4])
            file_out.write(grad_x +grad_y + grad_z)
                                        
        if m is None:
            print "GRIDENT READ FAILED"
        file_in.close() 
        file_out.close()       
        return
        
   
# main program
if __name__ == "__main__":
    log = gau_log_parser()
    log.check_calc()       
    log.get_dim_info()
    log.get_energy()
    log.get_gradient()

    


