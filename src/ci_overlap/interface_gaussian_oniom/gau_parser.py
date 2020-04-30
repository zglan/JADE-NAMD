#! /usr/bin/env python

from gau_log_wf_parser import *
from gau_rwf_wf_parser import *
from gau_log_eandg_parser import *
from gau_log_ao_parser import *


# gaussian parser
class gau_parser():
    def __init__(self, config = {}):
        """
        parser gaussian log or chk or rwf files to extract relevant data.
        """
        self.config = config
        
        if 'ci_td_use_file_type' in config.keys():
            self.file_type = self.config['ci_td_use_file_type']    
        else:
            self.file_type = "log"
            
        return
        
    def get_td(self):
        """
        parse one tddft calculation result.
        """
        file_type = self.file_type

        # wave function info
        # condition: log/rwf
        log = gau_log_wf_parser(self.config);
        # dimensional info. useless for gaussian interface, 
        # only to be consistent with turbomole
        log.get_basis()
        # mo.dat, qm_energy.dat, ci_*.dat  
        if file_type == "rwf" or file_type == "chk":
            rwf = gau_rwf_wf_parser(self.config)
            rwf.get_mo()
            rwf.get_ci_td()
        elif file_type == "log": 
            print "WARNING: parameters related to \
            ci coefficients assign problem \
            WILL NOT considered."
            log.get_mo()      
            log.get_ci_td()        
        else:
            raise ValueError, "invalid argument"

        # pes info.
        pes = gau_log_eandg_parser()
        pes.get_gradient()
        pes.get_energy()
        pes.get_other()
    
        # extra data.
        log.collect_qm()
        log.get_other()

        return
        
    def get_ao(self):
        """
        read ao overlap matrix
        """
        log = gau_log_ao_parser(self.config)
        log.get_ao_overlap()  
        
        return
        
if __name__ == "__main__":
    p = gau_parser()
    p.get_mo()
    p.get_ao()
    
        
        
        
