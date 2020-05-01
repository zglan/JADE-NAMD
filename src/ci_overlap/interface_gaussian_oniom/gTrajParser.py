# python
import os
import sys
import re
import math
from operator import itemgetter
import shutil

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/../tools/")
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/tools/")
#print sys.path
import tools
import elements

class gTrajParser():
    """
    parse gau. log file
    """
    def __init__(self, config = {}):
        """ init """
        self.dim = {'n_col': 5}
        self.files = {'log': 'gaussian.log'}
        self.traj = {}
        
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

    def get_geom(self):
        """ read gaussian geom data """      
        filename = self.files['log']
        fp = open(filename, "r")
        n_atom = self.dim['n_atom']
        
        pat1 = re.compile("Input orientation:")
        pat2 = re.compile("Standard orientation:")
        pat3 = re.compile("Z-Matrix orientation:")
    
        std_pos = 0
        ipt_pos = 0
        z_pos = 0
        geom = [{} for i in xrange(n_atom)]
        while True:
            line = fp.readline()
            if line == "":
                break
            m = pat1.search(line)
            if m is not None:
                ipt_pos = fp.tell()
            m = pat2.search(line)
            if m is not None:
                std_pos = fp.tell()
            m = pat3.search(line)
            if m is not None:
                z_pos = fp.tell()
                
        # read geom
        if std_pos != 0:
            print "Read Standard orientation: Find Geometry"
            fp.seek(std_pos)
        elif ipt_pos != 0:
            print "Read Input orientation: Find Geometry"
            fp.seek(ipt_pos)
        elif z_pos != 0:
            print "Z-matrix orientation: Find Geometry.. Jujar"
            fp.seek(z_pos)
        else:
            print "FAILED TO READ GAUSSIAN FREQ. CHECK LOG FILE"
            exit(1)
        # start to read geom
        # jump four lines  
        for i in xrange(4):
            line = fp.readline()
        # read coord.
        m = elements.elements()
        for i in xrange(n_atom):
            coord = [0.0 for j in xrange(3)]
            line = fp.readline() 
            record = line.split()
            atom_number = int(record[1])
            coord[0] = float(record[3])
            coord[1] = float(record[4])
            coord[2] = float(record[5])
            atom = {'atom_number': atom_number, 'coord': coord}
            atom['atom_label'] = m.number2label(atom['atom_number'])
            geom[i] = atom
        fp.close()
        self.traj['mol'] = geom
        # dump xyz file for check
        file_xyz = open("check.xyz", "w")
        n_atom = self.dim['n_atom']
        print >>file_xyz, "%10d\n" % n_atom
        for atom in geom:
            print >>file_xyz, "%10s%15.8f%15.8f%15.8f" % (atom['atom_label'],
                                                          atom['coord'][0],
                                                          atom['coord'][1],
                                                          atom['coord'][2])
        file_xyz.close()
        
        return


    def read_vel(self):
        """ read in velocity """
        
        return


    def pygrep(filename, mystr):
        mygrp = []
        for line in open(f).readlines():
            if re.match(mystr, line):
                mygrp.append(line)
            else:
                mygrp = None
        return mygrp
        
    def get_traj_num(self, mystr):
        f = self.files['log']
        mystr = ""
        mygrp = []
        pat = re.compile("Cartesian coordinates:")
        for line in open(f).readlines():
            if pat.search(line):
                mygrp.append(line)
        return len(mygrp)

    def dump_geom(self, file_xyz, i_geom):
        # dump xyz file for check
        BOHR = 0.529177
        n_atom = self.dim['n_atom']
        mol = self.traj['mol']
        geom = self.traj['traj'][i_geom]
        print >>file_xyz, "%10d\n" % n_atom
        for i_atom in xrange(n_atom):
            atom = geom[i_atom]            
            print >>file_xyz, "%10s%15.8f%15.8f%15.8f" % (mol[i_atom]['atom_label'],
                                                          atom['coord'][0]*BOHR,
                                                          atom['coord'][1]*BOHR,
                                                          atom['coord'][2]*BOHR)
        return
        
    def dump_traj(self):
        """ dump trajectory """
        file_xyz = open("dump.xyz", "w")
        n_geom = self.traj['n_geom']
        for i_geom in xrange(n_geom):
            self.dump_geom(file_xyz, i_geom)
        file_xyz.close()
        return

            
    def many_traj(self):
        """ dump many trajectory """
        mol = self.get_geom()
        traj = self.get_ntraj()
        self.dump_traj()
        return
    
            
    def get_ntraj(self):
        """ read many traj geom """
        filename = self.files['log']
        fp = open(filename, "r")
        mystr = "Cartesian coordinates:"
        n_geom = self.get_traj_num(mystr)
        print "max geom number: ", n_geom
        traj = []
        for i_geom in xrange(n_geom):
            geom = self.get_itraj(fp)
            traj.append(geom)
        fp.close()    
        
        self.traj['traj'] = traj
        self.traj['n_geom'] = n_geom
        return
        
    def get_itraj(self, fp):
        """ read gaussian geom data """      
        n_atom = self.dim['n_atom']
        pat1 = re.compile("Cartesian coordinates:")
        geom = [{} for i in xrange(n_atom)]
        ipt_pos = None
        while True:
            line = fp.readline()
            if line == "":
                break
            m = pat1.search(line)
            if m is not None:
                ipt_pos = fp.tell()
                break
        if ipt_pos is None:
            print "READ DONE"
        # start to read geom
        for i in xrange(n_atom):
            coord = [0.0 for j in xrange(3)]
            line = fp.readline().replace("D", "E")
            record = line.split()
            atom_id = int(record[1])
            coord[0] = float(record[3])
            coord[1] = float(record[5])
            coord[2] = float(record[7])
            atom = {'atom_id': atom_id, 'coord': coord}
            geom[i] = atom
        return geom     


    
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


        
    def get_other(self):
        pass
        return



    def __read_velocity_block(self):
        """
        read up velocity from admp calc.
        """


        return

    def read_velocity(self):
        """
        velocity from admp log..
        """
        filename = "admp.log"
        fp = open(filename, "r")
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

   
# main program
if __name__ == "__main__":
    
    
    log = gTrajParser()
    
    line = raw_input("the filename: \n > ")
    log.files['log'] = line.strip()
    
    log.check_calc()       
    log.get_dim_info()
    
    log.many_traj()
    
    # log.get_energy()
    # log.get_gradient()
    # log.get_geom()
    


