#! /usr/bin/env python2

from tools.namelist import *
from interface_mndo_qm.mndo import *
from interface_molpro_qm.molpro import *
from interface_bagel_qm.bagel import *
from interface_qchem_qm.qchem import *
from interface_gaussian_qm.gaussian import *
from interface_gaussian_oniom.GauONIOM import *
from interface_turbomole_qm.turbomole import *
from interface_gamess_qm.gamess import *

import os
import shutil


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


#        WORK_DIR = os.environ['WORK_DIR']
#        SUB_DIR   = os.environ['SUB_DIR']
#
#        dyn_file_all = ['current_state.out', 'dynamics.out', 'ele_time.out', 'energy_time.out', 'grad_time.out', 'hop_all_time.out', 'pe_time.out', 'restart_all', 'traj_time.out', 'vel_time.out', 'di_time.out']
#
#        for i_file in dyn_file_all:
#
#           file_path = WORK_DIR + '/' + i_file
#
#           if os.path.isfile(file_path):
#
#               shutil.copy2(file_path, SUB_DIR)


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
        elif qm_package == 106:
            # call bagel
            print "bagel is running"
            Bagel()
        elif qm_package == 107:
            # call qchem
            print "qchem is running"
            Qchem()
        else:
            # not done.
            # exit.
            print "cannot work with this qm package type: ", qm_package
            sys.exit(1)

        return

    def finalize(self):
        """ action after qc. """

        print "ELECTRONIC CALCULATION JOB DONE"

        return


if __name__ == "__main__":
    qc = QuanChem()
    qc.prepare()
    qc.run()
    qc.finalize()
