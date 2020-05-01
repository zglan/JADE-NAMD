# python
import shutil
from tur_zero import *
from tur_nonzero import *
from tur_zero_ricc import *
from tur_nonzero_ricc import *
from tur_overlap import *
from tur_nac import *

sys.path.append("../tools/")
import tools


# MAIN PROGRAM

#
# % QM METHOD 
#   11: CIS/TDHF/TDDFT
#   12: RICC2
#

class Turbomole():
    def __init__(self):   
       
        self.data = tools.load_data(filename = "interface.json")
        # interface_converter(filename = qm_interface)
        self.files = {"interface": "interface.json", "dyn": "inp.json"}
        
        # global control variable, not very useful now for the case of turbomole
        self.config = {}
        self.dyn = {}
        
        self.worker()        
        return                
        
    def prepare(self):
        """ load configure file """
        # dynamic info.
        self.dyn  = tools.load_data(self.files['dyn'])

        return     
        
    def run(self):
        """
        raise the calc.
        """
        qm_method = int(self.data['parm']['qm_method'])
        it = int(self.data['parm']['i_time'])
        
        # Start the QC calculations  (CIS, TDHF, TDDFT)
        if qm_method == 11:
        # Do electronic structure calculation at time zero
            shutil.copy("./qm_interface", "./turbomole_interface")
            if it == 0:
                tur_tddft_time_zero()
                
            elif it > 0:
                tur_tddft_time_nonzero()
                tur_double_mole ()
                tur_nac ()
            else:
                print "illegal time, it :", it
                sys.exit(1)
        # Start the Turbomole calculations  (RICC2)
        elif qm_method == 12: 
            shutil.copy("./qm_interface", "./turbomole_interface")
            # Do electronic structure calculation at time zero
            if it == 0:
                tur_time_zero_ricc()
                print "exec at zero time."
            elif it > 0:
                tur_time_nonzero_ricc()
                tur_double_mole ()
                tur_nac ()
            else:
                print "illegal time, it :", it
                sys.exit(1)
        else:
            print "QM method : error: no such QM method", qm_method   
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
    n = Turbomole()







