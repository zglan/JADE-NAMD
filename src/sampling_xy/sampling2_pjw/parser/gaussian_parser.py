#! python
import sys
import os
import re
import math


class gaussian_parser():
    """ parser every format of log file """
    def __init__(self, config = {}):
        """
        init. variables
        """
        self.files = {'log': 'freq.log', 'newlog': 'force.dat'}
        self.freq = {}
        self.dim = {}
        self.par = {}
        self.par['ANSTOBOHR'] = 1.8897261328856432
        
        self.dim['n_atom'] = 6
        self.dim['n_mode'] = 12
        
        if config != {}:
            self.files['log'] = config['log']
            self.files['newlog'] = config['newlog']
            self.dim['n_atom'] = config['n_atom']
            self.dim['n_mode'] = config['n_mode']
            #self.read_log()
            
        return


 
    def __read_gaussian_log_dim(self):
        """
        read number of atom in log file
        """        
        pat0 = re.compile("Deg. of freedom\s+(\d+)")
        pat = re.compile("NAtoms=(.*)NActive=(.*)NUniq=(.*)SFac=(.*)NAtFMM=(.*)")
        
        filename = self.files['log']
        fp = open(filename, "r")
        
        for line in fp:
            m = pat.search(line)
            m0 = pat0.search(line)
            if m0 is not None:
                n_mode = int(m0.group(1))
 
            if m is not None:
                string = m.group()
                record = string.split()
                n_atom = int(record[1])
                self.dim['n_active'] = int(record[3])
                break
        fp.close()
        
        if n_atom != self.dim['n_atom']:
            print "number of atom not consist !!! fail."

        if n_mode != self.dim['n_mode']:
            print "number of mode not consist !!! this may be related with symm. if this is, donnot worry"
        
        return
   
    def __read_gaussian_log_geom(self):
        """ read gaussian geom data """
      
        filename = self.files['log']
        fp = open(filename, "r")
        n_atom = self.dim['n_atom']
        ANSTOBOHR = self.par['ANSTOBOHR']
        
        line = "EMPTY"
        pat0 = re.compile("Charge\s* =\s*\d+ Multiplicity\s*=\s*\d+")
        pat1 = re.compile("Input orientation:")
        pat2 = re.compile("Standard orientation:")
    
        std_pos = 0
        ipt_pos = 0
        name_pos = 0
        geom = [{} for i in xrange(n_atom)]
        while line != "":
            line = fp.readline()
            m = pat0.search(line)
            if m is not None:
                name_pos = fp.tell()
            m = pat1.search(line)
            if m is not None:
                ipt_pos = fp.tell()
            m = pat2.search(line)
            if m is not None:
                std_pos = fp.tell()

        # read geom
        if std_pos != 0:
            print "Read Standard orientation: Find Geometry"
            fp.seek(std_pos)
        elif ipt_pos != 0:
            print "Read Input orientation: Find Geometry"
            fp.seek(ipt_pos)
        else:
            print "FAILED TO READ GAUSSIAN FREQ. CHECK LOG FILE"
            exit(1)
        # start to read geom
        # jump four lines  
        for i in xrange(4):
            line = fp.readline()
        # read coord.
        for i in xrange(n_atom):
            coord = [0.0 for j in xrange(3)]
            line = fp.readline()
 
            record = line.split()
            atom_number = int(record[1])
            coord[0] = float(record[3])*ANSTOBOHR
            coord[1] = float(record[4])*ANSTOBOHR
            coord[2] = float(record[5])*ANSTOBOHR
            atom = {'atom_number': atom_number, 'coord': coord}
            geom[i] = atom
            
        fp.seek(name_pos)
        # line = fp.readline()
        for i in xrange(n_atom):
            line = fp.readline()
            record = line.replace(",", " ").split()
            atom_name = record[0]
            geom[i]['atom_label'] = atom_name
  
        self.freq['geom'] = geom
        
        fp.close()

        # dump xyz file for check
        file_xyz = open("check.xyz", "w")
        n_atom = self.dim['n_atom']
        print >>file_xyz, "%10d\n" % n_atom
        b2a = 0.529177
        for atom in geom:
            print >>file_xyz, "%10s%15.8f%15.8f%15.8f" % (atom['atom_label'],
                                                          atom['coord'][0]*b2a,
                                                          atom['coord'][1]*b2a,
                                                          atom['coord'][2]*b2a)
        file_xyz.close()

        
        return

    def __read_gaussian_log_freq_block(self, fp, i_block):
        """
        read in one block and assign variables
        """
        n_atom = self.dim['n_atom']
        n_col = 5
 
        line = fp.readline()
        pat_freq = re.compile("Frequencies ---")
        pat_mass = re.compile("Reduced masses ---")
        pat_value = re.compile("Coord Atom Element:")
        while line != "":
            line = fp.readline()
            m1 = pat_freq.search(line)
            m2 = pat_mass.search(line)
            m3 = pat_value.search(line)                
            if m1 is not None:
                record = line.split("---")[1].split()
                for f in record:
                    self.freq['freq'].append(float(f))                    
            if m2 is not None:
                record = line.split("---")[1].split()
                for mass in record:
                    self.freq['mass'].append(float(mass)) 
            if m3 is not None:
                pos_value = fp.tell()
                break

        # read in normal modes       
        i_start = i_block * n_col 
        fp.seek(pos_value)
 
        for i in xrange(0, n_atom*3):
            line = fp.readline()
            record = line.split()[3:]
            n_col_tmp = len(record)
            for j in xrange(i_start, i_start + n_col_tmp):
                j_col = j - i_start
                self.freq['normal_mode'][j][i] = float(record[j_col])
                # print j, i, j_col, record[j_col]

        return

 
    def __read_gaussian_log_freq(self):
        """ read in every normal mode """
        filename = self.files['log']
        n_atom = self.dim['n_atom']
        fp = open(filename, "r")
        pat1 = re.compile("Harmonic frequencies")
        line = "EMPTY"
        while line != "":
            line = fp.readline()
            m = pat1.search(line)
            if m is not None:
                print "Find the normal modes"
                break
         # jump three lines
        for i in xrange(3):
            line = fp.readline()

        # read data now
        n_mode = self.dim['n_mode']
        n_col = 5
        n_block = n_mode/n_col+1 if n_mode%n_col>0 else n_mode/n_col
        self.freq['n_mode'] = n_mode
        self.freq['n_atom'] = n_atom
        
        self.freq['mass'] = []
        self.freq['freq'] = []
        self.freq['normal_mode'] = [[0.0 for i in xrange(n_atom*3)] for j in xrange(n_mode)]
        self.freq['coor_vib'] = [[0.0 for i in xrange(n_atom*3)] for j in xrange(n_mode)]

        for i in xrange(n_block):
            self.__read_gaussian_log_freq_block(fp, i)

        # Write down the final transfermation matrix S(n_mode, n_atom)
        normal_mode = self.freq['normal_mode']
        mass_mode = self.freq['mass']
        for i in xrange(n_mode):
            for j in xrange(n_atom*3):                
                self.freq['coor_vib'][i][j] = normal_mode[i][j] / math.sqrt(mass_mode[i])

        fp.close()
        
        return

    def dump_gau_log_freq(self):
        """
        write down freq related data in a specific format.
        """
        filename = self.files['newlog']
        fp = open(filename, "w")
        n_atom = self.freq['n_atom']
        n_mode = self.freq['n_mode']
        geom = self.freq['geom']
        print >>fp, "ATOMIC GEOMETRYS(AU)"
        # geometry
        print >>fp, "%10d" % (n_atom)
        for i in xrange(n_atom):
            atom = geom[i]
            print >>fp, "%5s%10d" % (atom['atom_label'], atom['atom_number']),
            print >>fp, "%15.8f%15.8f%15.8f" % (atom['coord'][0], atom['coord'][1], atom['coord'][2])
 
        # normal modes
        print >>fp, "%10d%10d" % (n_mode, n_atom)
        freq = self.freq['freq']
        mass = self.freq['mass']
        coor_vib = self.freq['coor_vib']
        print >>fp, "FREQUENCY(cm**-1)"
        for i in xrange(n_mode):
            print >>fp, "%15.8f" % (freq[i])
                
        print >>fp, "REDUCED MASS(AMU)"        
        for i in xrange(n_mode):
            print >>fp, "%15.8f" % (mass[i])

        print >>fp, "NORMAL MODE"
        for i in xrange(n_mode):
            this_mode = coor_vib[i]
            for j in xrange(n_atom):
                print >>fp, "%15.8f%15.8f%15.8f" \
                % (this_mode[j*3+0], this_mode[j*3+1], this_mode[j*3+2])
        fp.close()
        
        return
    
    def read_log(self):
        """
        read gaussian log file
        """ 
        filename = self.files['log']
        file_out = open(filename, "r")
        # read gaussian geometry
        self.__read_gaussian_log_dim()
        self.__read_gaussian_log_geom()
        self.__read_gaussian_log_freq()
        self.dump_gau_log_freq()

        return
    
### main program
if __name__ == "__main__":
    gau = gaussian_parser()
    gau.read_log()
 


    
