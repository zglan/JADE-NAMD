#! /usr/bin/env python

from gau_ao_create import *
from gau_model_create import *


# gaussian input creator
class gau_create():
    def __init__(self, config = {}):
        """
        create the gaussian input file..
        """
        self.config = config
        self.joblist = []

        return

    def create_model(self):
        """
        create for different layer model
        """
        # model class
        mod = gau_model_create(self.config)
        #
        mod.modify()
        mod.write()
        # additional file name
        self.joblist = mod.joblist

        return 
    

    def create_ao(self):
        """
        create atomic overlap input file
        """
        ao = gau_ao_create(self.config)
        #
        ao.modify()
        ao.write()
        # additional file name
        self.joblist = ao.joblist

        return
    
# main program         
if __name__ == "__main__":
    p = gau_create()
    p.create_model()
    p.create_ao()
    
        
        
        
