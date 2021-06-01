# python
from molpro_run import *
from molpro_template import *

sys.path.append("../tools/")
import tools

# MAIN PROGRAM

#
# % QM METHOD
#   1 : Semi-Emperical
#   2 : CASSCF/CASPT2
#   11: CIS/TDHF/TDDFT
#   12: RICC2
#


class Molpro():
    def __init__(self):

        # interface_converter(filename = qm_interface)
        self.files = {"interface": "interface.json", "dyn": "inp.json", \
                      "molpro_template": "./MOLPRO_EXAM/molpro_template.inp"}

        self.config = {}
        self.dyn = {}

        # run
        self.worker()

        return

    def prepare(self):
        """ load configure file """
        # dynamic info.
        self.dyn = tools.load_data(self.files['dyn'])

        # molpro directory structure info.
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

        if qm_method == 2 or qm_method == 3:

            molpro_template(config)
            molpro_run(config)

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
    n = Molpro()
