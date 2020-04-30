#! /usr/bin/env python

import os
import shutil
from gms_zero import *
from gms_nonzero import *
from gms_overlap import *
from gms_nac import *

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/../tools/")
import tools

# MAIN PROGRAM

#
# % QM METHOD 
#   11: CIS/TDHF/TDDFT
#   12: *
#

class Gamess():
    def __init__(self):
    
        # interface_converter(filename = qm_interface)
        self.files = {"interface": "interface.json", "dyn": "inp.json", \
                      "template": "./GMS_EXAM/gms_template.inp"}
        
        # make a full dictionary for the gamess job
        self.config = {}
        self.dyn = {}
        
        self.worker()
                
        return        
        
    def prepare(self):
        """ load configure file """
        # dynamic info.
        self.dyn  = tools.load_data(self.files['dyn'])
        # gaussian directory structure info.
        #script_dir = os.path.split(os.path.realpath(sys.argv[0]))[0]
        script_dir = os.path.split(os.path.realpath(__file__))[0]
        self.config = tools.load_data(script_dir + "/config.in")
        self.config['root'] = os.getcwd()
        # attach dyn info in config vars
        self.config.update(self.dyn['quantum'])
        # attch interface info in config vars.
        interface = tools.load_data(self.files['interface'])
        self.config['interface'] = interface

        return

    def run(self):
        """
        raise the calc. code.
        """
        # load interface file
        interface = tools.load_data(self.files['interface'])
        it = int(interface['parm']['i_time'])
 
        qm_method = int(self.dyn['control']['qm_method'])
    
        config = self.config
        # Start the QC calculations  (CIS, TDHF, TDDFT)
        if qm_method == 11:
        # Do electronic structure calculation at time zero
            if it == 0:
                # call zero time     
                # % make template: dump gjf in json format
                gms_template(config)                 
                # % call gaussian
                gms_zero(config)
                
            elif it > 0:
                gms_nonzero(config)
                print "now work dir:", os.getcwd()
                gms_overlap(config)
                gms_nac(config)        
            else:
                print "Error: keyword 'it':", it
                sys.exit(0)                
        else:
            print "QM method : error: no such method" , qm_method  
            sys.exit(1)
            
        return

        
    def finilize(self):
        """
        dump exchange info. with dynamic code.
        may be useful in the future version.
        """
        filename = "qm.dump"
        fp = open(filename, "w")
        print >>fp, "Noting done now. hahaha"
        fp.close()
        
        return
        
    def worker(self):
        self.prepare()
        self.run()
        self.finilize()
        return

# main program.
if __name__ == "__main__":    
    n = Gamess()








