# python
import copy
import os

import tools

# molpro input process.
# Based on json template to produce molpro input.
#


# template content
#   details in 'molpro_template.py'
#
# note: qm_interface geometry was given in atomic unit by default.
#
class molpro_create():
    """
    process molpro template & generate molpro input
    """
    def __init__(self, config={}):
        """ initialize several internal variable """
        # template data. cmp is static one.
        self.template = {}
        self.interface = {}

        # test case
        self.files = {'template': 'template.json', 'interface': 'interface.json', \
                      'molpro': 'molpro.inp'}

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
            self.files["molpro"] = files['molpro_input']

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
        self.interface = copy.deepcopy(obj_2)

    def wrt_molpro_input(self):
        """ 
        wrt template file 
        """
        bohr2ang = 0.529177
        #        print "QM-INTERFACE GIVEN IN ATOMIC UNIT, CONVERSION TO ANGSTROM IN Molpro DONE"

        t = self.template

        # open file
        jobfile = self.files['molpro']
        fp = open(jobfile, 'w')

        # write routine
        for i in t['routine']['content']:
            print >> fp, "%s" % i
        geom_t = t['mol']
        atoms_t = geom_t['atoms']
        natom_t = geom_t['natom']

        i = self.interface
        geom_i = i['mol']
        atoms_i = geom_i['atoms']
        natom_i = geom_i['natom']

        print >> fp, "%s" % natom_i
        print >> fp, ""
        #        print natom_i, flag

        print natom_t
        for i in range(natom_t):
            record_t = atoms_t[i]
            atomname = record_t['name']

            record_i = atoms_i[i]
            coord = record_i['coord']
            coord = [
                float(coord[0]) * bohr2ang,
                float(coord[1]) * bohr2ang,
                float(coord[2]) * bohr2ang
            ]

            print >> fp, "%-10s%12.7f %12.7f %12.7f " % (atomname, \
                                                         float(coord[0]), float(coord[1]), float(coord[2]))

        if t['tail'] != "":
            print >> fp, "%s" % t['tail']

        print "molpro_write:", os.getcwd(), jobfile

        return

    def wrt_internal(self):
        """ internal exchange dat """
        dump_data('template.json', self.template_cmp)
        return


# Main Program
if __name__ == "__main__":
    molpro = molpro_create()
    molpro.wrt_molpro_input()
