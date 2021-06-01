# python
from qchem_run import *
from qchem_template import *

sys.path.append("../tools/")
import tools

# MAIN PROGRAM

#
# % QM METHOD
#   1 : Semi-Emperical
#   2 : CASSCF/CASPT2
#   11: CIS/TDHF/TDDFT
#   12: RICC2
#   13: Spin-Flip TDDFT


class Qchem():
    def __init__(self):

        # interface_converter(filename = qm_interface)
        self.files = {"interface": "interface.json", "dyn": "inp.json"}

        # run

        WORK_DIR = os.environ['WORK_DIR']
        SUB_DIR   = os.environ['SUB_DIR']

        dyn_file_all = ['current_state.out', 'dynamics.out', 'ele_time.out', 'energy_time.out', 'grad_time.out', 'hop_all_time.out', 'pe_time.out', 'restart_all', 'traj_time.out', 'vel_time.out', 'di_time.out']

        for i_file in dyn_file_all:

           file_path = WORK_DIR + '/' + i_file

           if os.path.isfile(file_path):

               shutil.copy2(file_path, SUB_DIR)


        self.worker()

        return

    def prepare(self):
        """ load configure file """
        # dynamic info.
        self.dyn = tools.load_data(self.files['dyn'])

        # qchem directory structure info.
        script_dir = os.path.split(os.path.realpath(__file__))[0]
        self.config = tools.load_data(script_dir + "/config.in")
        self.config['root'] = os.getcwd()
        self.config.update(self.dyn['quantum'])

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

        # Start the QC calculations

        if qm_method == 2 or qm_method == 3 or qm_method == 11:

            qchem_template(config)
            qchem_run(config)

        else:
            print "QM method : error: no such method", qm_method
            sys.exit(1)

        return

    def worker(self):
        self.prepare()
        self.run()
        return


# main program.
if __name__ == "__main__":
    n = Qchem()
