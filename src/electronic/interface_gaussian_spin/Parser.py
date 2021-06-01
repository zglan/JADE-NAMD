#! /usr/bin/python

from logParser import *

# gaussian parser

class Parser():
    def __init__(self, config = {}):
        """
        parser gaussian log or chk or rwf files to extract relevant data.
        """
        self.config = config
        
        self.file_type = "log"
                
        return
        
    def get(self):
        """ parser gaussian output """
        log = logParser(self.config)
        log.check_calc()       
        log.get_dim_info()
        log.get_energy()
        log.get_gradient()
        log.get_geom()
        log.get_other()
        return

# main program       
if __name__ == "__main__":
    par = Parser()
    par.get()
    
    
    
        
