# python
import copy
import os
import re
import sys

sys.path.append("../tools/")
import tools

class qchem_create():
    """
    process qchem template & generate qchem input
    """
    def __init__(self, config={}):
        """ initialize several internal variable """
        # template data. cmp is static one.
        self.template = {}
        self.interface = {}

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
        self.files["qchem"] = files['qchem_input']

        self.qm_interface = tools.load_data(self.files["interface"])
        self.n_state = self.qm_interface['parm']['n_state']
        self.i_state = self.qm_interface['parm']['i_state']

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

    def wrt_qchem_input(self):
        """ 
        wrt template file 
        """
        bohr2ang = 0.529177
        #        print "QM-INTERFACE GIVEN IN ATOMIC UNIT, CONVERSION TO ANGSTROM IN Qchem DONE"

        t = self.template

        # open file
        jobfile = self.files['qchem']
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

#        print >> fp, "%s" % natom_i
#        print >> fp, ""
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


        self.tail = t['tail']

        self.tail_split()


        print >> fp, "%s" % self.tail_split_dict["head"]


        print >> fp, "%s" % '$rem\n'

        print >> fp, "%s" % self.tail_split_dict[self.i_state-1]

        print >> fp, "%s" % '$rem\n'
        print >> fp, "%s" % self.tail_split_dict["nac"]
        


        print "qchem_write:", os.getcwd(), jobfile

        return

    def tail_split(self):


        tail_split_dict = {}

        tail_split_all = self.tail.split('$rem')

        for i_content in tail_split_all:

           if i_content.find('force') != -1:

              flag = 0

              for i_state in range(self.n_state):

                 pattern_state = 'CIS_STATE_DERIV    ' + str(i_state)

                 if i_content.find(pattern_state) != -1:
#              if re.match(pattern, i_content) != None:
                    tail_split_dict[i_state] = i_content
                    flag = 1

              if flag == 0:
                    tail_split_dict[0] = i_content

           elif i_content.find("SP") != -1:
                 tail_split_dict["nac"] = i_content

           else:
                 tail_split_dict["head"] = i_content


           self.tail_split_dict = tail_split_dict
 

    def wrt_internal(self):
        """ internal exchange dat """
        dump_data('template.json', self.template_cmp)
        return


# Main Program
if __name__ == "__main__":
    qchem = qchem_create()
    qchem.wrt_qchem_input()
