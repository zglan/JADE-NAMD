#! /usr/bin/python

from gms_ao_parser import *
from gms_log_parser import *


# gaussian parser

class gms_parser():
    def __init__(self, config = {}):
        """
        parser gaussian log or chk or rwf files to extract relevant data.
        """
        self.config = config
        self.dim = {}
        self.dim['i_state'] = config['interface']['parm']['i_state']
        
        self.file_type = "log"
        if 'ci_td_use_file_type' in config.keys():
            self.file_type = self.config['ci_td_use_file_type']    
                            
        return
        
    
    # is-log-or-chk / if log & config conflict goto warning and drop config.
    # conflit tda & gaussian version
    def get_td_dat(self):
        """
        parse one tddft calculation result.
        """
        log = gms_log_parser(self.config)
        # rwf = gau_rwf_parser(self.config);
        # dimensional info. useless for gaussian interface, 
        # only to be consistent with turbomole
        log.get_basis()
        
        # forces
        log.get_gradient()  

        # for ground state..
        
        # mo.dat, qm_energy.dat, ci_*.dat  
        log.get_mo()      
        log.get_ci_td()        
            
        # other data.
        log.collect_qm()
        log.get_other()
        
        return
        
    def get_ao(self):
        """
        read ao overlap matrix
        """
        log = gms_ao_parser(self.config)
        log.get_ao_overlap()  
        
        return
        
              
        
        
        
