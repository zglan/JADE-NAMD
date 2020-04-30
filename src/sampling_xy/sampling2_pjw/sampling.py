#! /usr/bin/env python

import os
import shutil
from ConfigParser import SafeConfigParser



# this routine prepare the input file for wigner sampling routine.

class gen_input:
    def __init__(self):

        self.files = {'log': "freq.log"}
        self.parser = 0
        self.config = 0
        
        return

    def check(self):
        """
        at first, we should check the existance of the main sampling program &
        some other preconditions
        """


        return

    def prepare(self):
        """
        create a new directory to run the current job &
        generate fortran style file
        """
        work_dir = "sample"
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)
            
        logfile = self.files['log']
        
        return

 
    def read_ini(self):        
        """
        read config file
        """
        line = raw_input("the ini filename: [default: input.ini]\n >")
        if line.strip() == "":
            filename = "input.ini"
        else:
            filename = line.strip()
        parser = SafeConfigParser()            
        parser.read(filename)
        
        self.parser = parser
        return
    
    def write_input(self):
        """
        write the data in format of fortran
        """
        fp = open('main_input', 'w')
        p = self.parser
        section = 'wigner'
        n_atom = p.getint(section, 'n_atom')
        n_mode = p.getint(section, 'n_mode')        
        label_random = p.getint(section, 'label_random')
        nr = p.getint(section, 'nr')
        nbin = p.getint(section, 'nbin')
        label_read_vib = p.getint(section, 'label_read_vib')
        label_es_output = p.getint(section, 'label_es_output')
        filename_es_output = p.get(section, 'filename_es_output')
        label_displacement = p.getint(section, 'label_displacement')
        label_dis_wigner = p.getint(section, 'label_dis_wigner')
        n_geom = p.getint(section, 'n_geom')
        label_method = p.getint(section, 'label_method')
        label_frozen = p.getint(section, 'label_frozen')
        number_frozen = p.getint(section, 'number_frozen')
        list_frozen = p.get(section, 'list_frozen').split()
        

        print >>fp, "%d read (*,*) n_atom" % n_atom
        print >>fp, "%d read (*,*) n_mode" % n_mode
        print >>fp, "read (*,*)"
        print >>fp, "%d read (*,*) label_random" % label_random
        print >>fp, "%d read (*,*) nr" % nr
        print >>fp, "%d read (*,*) nbin" % nbin
        print >>fp, "read (*,*)"
        print >>fp, "%d read (*,*) label_read_vib" % label_read_vib
        print >>fp, "%d read (*,*) label_es_output" % label_es_output
        print >>fp, "%s  read (*,*) filename_es_output" % filename_es_output
        print >>fp, "read (*,*)"
        print >>fp, "%d read (*,*) label_displacement" % label_displacement
        print >>fp, "read (*,*)"
        print >>fp, "%d read (*,*) label_dis_wigner" % label_dis_wigner
        print >>fp, "%d read (*,*) n_geom" % n_geom
        print >>fp, "%d read (*,*) label_method" % label_method
        print >>fp, "read (*,*)"
        print >>fp, "%d read (*,*) label_frozen" % label_frozen
        print >>fp, "%d read (*,*) number_frozen" % number_frozen        
        for i in list_frozen:
            print >>fp, "%s " % i,
        print >>fp, "read (*,*) list_frozen"
        fp.close()

        print ("GENERATE & WRITE DONE INPUT")
 
        return

    def run(self):
        """
        run wigner sampling
        """
        os.system("which sampling.x")
        bin_dir = os.path.split(os.path.realpath(__file__))[0]
        bin_name = bin_dir + "/sampling.x"

        os.system(bin_name + "< main_input > wigner.log")

        return

    def finalize(self):
        """
        may be used to clean the results
        """

        
        return

    def done(self):
        """
        pack
        """

        self.read_ini()
        self.write_input()
       
        self.run()
 

        return

if __name__ == "__main__":
    pp = gen_input()
    #pp.read_ini()
    #pp.write_input()
    pp.done()
 
