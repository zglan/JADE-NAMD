#! /usr/bin/env python2

from tools.namelist import *
from interface_mndo_qm.mndo import *
from interface_molpro_qm.molpro import *
from interface_gaussian_qm.gaussian import *
from interface_gaussian_oniom.GauONIOM import *
from interface_turbomole_qm.turbomole import *
from interface_gamess_qm.gamess import *


# job wrapper of different quantum-chemistry package.

# % read fortran namelist to get md info. & the target qc package. 
#   convert to json format.
# % call related quantum code
#
# %
#

class QuanChem:
    """
    model for quantum chemistry calculations.
    """

    def __init__(self):

        self.files = {}
        self.files["interface"] = "qm_interface"
        self.files["dyn"] = "dyn.inp"
        self.files['dyn_json'] = "inp.json"
        self.obj = {}

        return

    def prepare(self):
        """
        read md info. & prepare for the qc job
        """
        # interface file
        # generate interface.json
        ic = interface_converter(filename=self.files['interface'])
        i_time = int(ic['parm']['i_time'])

        if i_time == 0:
            # read dynamic in file
            print "zero step"
            nma = namelist(filename=self.files['dyn'])
            self.obj = nma.get()
        else:
            nma = namelist(filename=self.files['dyn'])
            self.obj = nma.get()
#            self.obj = tools.load_data(filename=self.files['dyn_json'])
            print "STEP : ", i_time

        return

    def run(self):
        """ 
        distributing the job
        """
        qm_package = int(self.obj['quantum']['qm_package'])

        if qm_package == 101:
            # call turbomole
            Turbomole()
        elif qm_package == 102:
            # call gaussian
            print "Gaussian is running"
            Gaussian()
        elif qm_package == 1021:
            # call gaussian with oniom feature
            print "CALL GAUSSIAN PACKAGE WITH ONIOM FEATURE"
            GauONIOM()
        elif qm_package == 103:
            # call gamess
            Gamess()
        elif qm_package == 104:
            # call mndo
            print "mndo99 is running"
            Mndo()
        elif qm_package == 105:
            # call molpro
            print "molpro is running"
            Molpro()
        else:
            # not done.
            # exit.
            print "cannot work with this qm package type: ", qm_package
            sys.exit(1)

        return

    def ZN_file_prepare(self):

        ZN_FILE = 'ZN'
        ZN_CAL = 'qm_results.dat'
        ZN_PRE_2 = ZN_FILE + '/' + 'qm_results_pre_2.dat'
        ZN_PRE_1 = ZN_FILE + '/' + 'qm_results_pre_1.dat'
        ZN_CUR = ZN_FILE + '/' + 'qm_results_cur.dat'

        if not os.path.exists(ZN_FILE):
           os.makedirs(ZN_FILE)

        if os.path.exists(ZN_FILE): 
           if os.path.isfile(ZN_PRE_1):
              shutil.copy2(ZN_PRE_1,ZN_PRE_2)
              shutil.copy2(ZN_CUR,ZN_PRE_1)
              shutil.copy2(ZN_CAL,ZN_CUR)

           if not os.path.isfile(ZN_PRE_1):
              if os.path.isfile(ZN_CUR):
                 shutil.copy2(ZN_CUR,ZN_PRE_1)
                 shutil.copy2(ZN_CAL,ZN_CUR)

              if not os.path.isfile(ZN_CUR):
                 shutil.copy2(ZN_CAL,ZN_CUR)
        
        return


    def finalize(self):
        """ action after qc. """

        print "ELECTRONIC CALCULATION JOB DONE"

        return


if __name__ == "__main__":
    qc = QuanChem()
    qc.prepare()
    qc.run()
#    qc.ZN_file_prepare()
    qc.finalize()
