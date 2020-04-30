#! /usr/bin/python

from gau_log_parser import *
from gau_rwf_parser import *


# gaussian parser

class gau_parser():
    def __init__(self, config = {}):
        """
        parser gaussian log or chk or rwf files to extract relevant data.
        """
        self.config = config
        
        self.file_type = "log"
        if 'ci_td_use_file_type' in config.keys():
            self.file_type = self.config['ci_td_use_file_type']    
            
                
        return
        
    
    # is-log-or-chk / 
    # if log & config conflict goto warning and drop config.
    # conflit tda & gaussian version
    def get_td_dat(self):
        """
        parse one tddft calculation result.
        """
        log = gau_log_parser(self.config);
        rwf = gau_rwf_parser(self.config);
        # dimensional info. useless for gaussian interface, 
        # only to be consistent with turbomole
        log.get_basis()
        
        # forces
        log.get_gradient()  
        
        # condition: log/rwf
        # if log the config to control ci coefficients will be drop
        file_type = self.config['ci_td_use_file_type']
            
        # mo.dat, qm_energy.dat, ci_*.dat  
        if file_type == "rwf" or file_type == "chk":
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
            
        # other data.
        log.collect_qm()
        log.get_other()
        
        return
        
    def get_ao(self):
        """
        read ao overlap matrix
        """
        log = gau_log_parser(self.config)
        log.get_ao_overlap()  
        
        return
        
              
        
        
        
