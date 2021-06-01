# python
import os
import shutil

from goStep import *

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/../tools/")
import tools

# dulikai
# 2015.07
# @qibebt
#
#

class GauSpin():
    def __init__(self):
        """ gaussian interface """
        
        self.files = {"interface": "interface.json", "dyn": "inp.json", \
                      "gau_template": "./GAU_EXAM/gau_template.gjf"}
        # make a full dictionary for the gaussian job
        self.config = {}
        self.dyn = {}
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
        return
        
    def run(self):
        """
        raise the calc. code.
        """
        # load interface file
        interface = tools.load_data(self.files['interface'])
        it = int(interface['parm']['i_time'])
        # Start the QC calculations  
        # Do electronic structure calculation at time zero
        g = goStep(self.config)
        g.step()
        
        return
        
    def finalize(self):
        pass
        return
        
        
    def go(self):
        self.prepare()
        self.run()
        self.finilize()
        return

# main program.
if __name__ == "__main__":    
    n = Gaussian()
    n.go()







