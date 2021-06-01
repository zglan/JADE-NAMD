# python
import sys
import re
import copy
import os
import shutil

sys.path.append("../tools/")
import tools

# mndo input process.
# Based on json template to produce mndo input.
#


# template content
#   details in 'mndo_template.py'
#
# note: qm_interface geometry was given in atomic unit by default.
#
class mndo_create():
    """
    process mndo template & generate mndo input
    """
    def __init__(self, config={}):
        """ initialize several internal variable """
        # template data. cmp is static one.
        self.template = {}
        self.template_cmp = {}
        self.interface = {}

        # test case
        self.files = {'template': 'template.json', 'interface': 'interface.json', \
                      'mndo': 'mndo.inp' }
        self.files['current'] = "./MNDO_TMP/" + self.files['interface']

        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files']

            # working directory & files >>>
            self.directory = {}
            self.directory['root'] = root_dir
            self.directory['home'] = root_dir + "/" + dirs['home']
            self.directory[
                'work'] = self.directory['home'] + "/" + dirs['work']
            self.files = {}
            self.files["template"] = root_dir + "/" + files['template']
            self.files["interface"] = files['interface']
            self.files["mndo"] = files['mndo_input']
            self.files['current'] = "interface1.json"
            self.files['previous'] = "interface2.json"

        self.load()

        return

    def load(self):
        """
        load template.json and interface.json
        """
        filename1 = self.files['template']
        filename2 = self.files['interface']
        obj_1 = tools.load_data(filename1)
        obj_2 = tools.load_data(filename2)
        self.template = copy.deepcopy(obj_1)
        self.template_cmp = copy.deepcopy(obj_1)
        self.interface = copy.deepcopy(obj_2)

    def wrt_mndo_input(self, flag="default"):
        """ 
        wrt template file 
        cmp for template_cmp
        """
        bohr2ang = 0.529177
        print "QM-INTERFACE GIVEN IN ATOMIC UNIT, CONVERSION TO ANGSTROM IN Mndo DONE"
        if flag == "cmp":
            t = self.template_cmp
        elif flag == "default":
            t = self.template
        else:
            print "only cmp/default is possible option: wrt_mndo_input"
            sys.exit(1)

        # open file
        jobfile = self.files['mndo']
        fp = open(jobfile, 'w')

        # write routine
        for i in t['routine']['content']:
            print >> fp, "%s" % i
        print >> fp, "%s\n" % t['title']
        geom_t = t['mol']
        atoms_t = geom_t['atoms']
        natom_t = geom_t['natom']

        i = self.interface
        geom_i = i['mol']
        atoms_i = geom_i['atoms']
        natom_i = geom_i['natom']

        #        print natom_i, flag

        for i in range(natom_t):
            record_t = atoms_t[i]
            atomname = record_t['name']
            fix = record_t['fix']

            record_i = atoms_i[i]
            coord = record_i['coord']
            coord = [
                float(coord[0]) * bohr2ang,
                float(coord[1]) * bohr2ang,
                float(coord[2]) * bohr2ang
            ]

            print >>fp, "%-10s%24.14f %s %24.14f %s %24.14f %s" % (atomname, \
                        float(coord[0]), fix[0], float(coord[1]), fix[1], float(coord[2]), fix[2])

        print >> fp, "0            0.0000000 0    0.0000000 0    0.0000000 0"
        print >> fp, "\n",
        if t['tail'] != "":
            print >> fp, "%s" % t['tail']

        print "mndo_write:", os.getcwd(), jobfile

        return

    def wrt_internal(self):
        """ internal exchange dat """
        dump_data('template.json', self.template_cmp)
        return


# Main Program
if __name__ == "__main__":

    mndo = mndo_create()
    mndo.wrt_mndo_input()
