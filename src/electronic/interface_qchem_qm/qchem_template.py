# python

import copy
import re
import sys

sys.path.append("../tools/")
import tools

# qchem input process for templating.


#
class qchem_template():
    """
    process qchem template & generate qchem input
    """
    def __init__(self, config={}):
        """ initialize several internal variable """
        # content of the template.
        self.template = {}
        self.template_cmp = {
            'routine': {},
            'title': '',
            'mol': {},
            'tail': '{}'
        }
        # i/o pointer
        self.pointer = {"content": [], "i_line": 0}
        self.files = {
            'qchem': './QCHEM_EXAM/qchem_template.inp',
            'template': 'template.json',
            'interfce': 'interface.json'
        }

        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files']
            qchem_file = root_dir + "/" + dirs['template'] + "/" + files[
                'qchem_template']
            interface_file = root_dir + "/" + "interface.json"
            tpl_file = root_dir + '/template.json'
            self.files = {'qchem': qchem_file, 'template': tpl_file, 'interface':interface_file}

            # load gjf & write json
            self.interface = tools.load_data(self.files['interface'])

            self.n_atom = self.interface['parm']['n_atom']

        self.dump()

        return

    # ------------------------------------------------------------------
    #
    # dump_template() & load_template is the main called subroutine in this section.
    #
    # -------------------------------------------------------------------

    def __rd_qchem_input_routine(self):

        routine = {}
        i_line = 0
        i_start = 0
        i_end = -1
        content = []
        n = len(self.pointer['content'])
        #        print self.pointer['content']
        for i in xrange(n):
            cur_line = self.pointer['content'][i]
            i_find_sharp = re.search('molecule', cur_line)
            if i_find_sharp is not None:
                i_end = i
                break

        for i in xrange(i_start, i_end + 2):
            content.append(self.pointer['content'][i].strip())

        if i_end == -1:
            print "cannot find qchem input routine line"

        self.template['routine'] = {'content': content}

        self.pointer['i_line'] = i_end

        return

    def __rd_qchem_input_mol(self):
        """
        Molecule specification: Specify molecular system to be studied.
        """
        # find the blank line after '#' colum
        line_each = self.pointer['content']
        n_line = len(line_each)
        i_line = self.pointer['i_line']

        # molecular coord. [suppose cart. coordinates].
        i_line += 1
        natom = self.n_atom
        mol = {'natom': natom, 'atoms': []}
        for i in range(i_line, n_line):
            i_line += 1
            cur_line = line_each[i_line]
            if cur_line.split()[0] == "$end":
                break
            # read one line
            record = self.__check_input_frg(cur_line)
            mol['atoms'].append(record)

        self.template['mol'] = mol

        self.pointer['i_line'] = i_line

        return

    def __check_input_frg(self, line):
        """
            check input fragment type, and return records
        """

        myline = line
        items = myline.split()

        atomname = items[0]
        coord = [float(items[1]), float(items[2]), float(items[3])]
        rec = {'name': atomname, 'coord': coord}
        return rec

    def __rd_qchem_input_tail(self):
        """ 
        read template tail information 
        """
        line_each = self.pointer['content']
        n_line = len(line_each)
        i_line = self.pointer['i_line']

        tlist = []
        tail = ""

        for i in range(i_line, n_line):
            line = line_each[i]
            tlist.append(line)
        for str in reversed(tlist):
            if str.strip() == "":
                tlist.pop()
            else:
                break
        for str in tlist:
            tail = tail + str
        self.template['tail'] = tail

        self.pointer['i_line'] = 0

        return

    def rd_qchem_input(self):
        """ read template file """
        # open adn read all
        fp = open(self.files["qchem"], 'r')
        self.pointer['content'] = fp.readlines()
        fp.close()

        # read process
        # link0 section : %
        #        self.__rd_qchem_input_link0()
        # routine section: #
        self.__rd_qchem_input_routine()
        # molecule spec.
        self.__rd_qchem_input_mol()

        # other data
        self.__rd_qchem_input_tail()

        # deep copy it
        self.template_cmp = copy.deepcopy(self.template)

        return

        # % dump/load template.

    def dump(self):
        """
        read input file; dump template in json format.
        """
        self.rd_qchem_input()

        tools.dump_data(self.files['template'], self.template_cmp)

        return

    def load(self, filename="template.json"):
        """
        load template.json
        """
        obj = tools.load_data(filename)

        return obj


# Main Program
if __name__ == "__main__":
    qchem = qchem_template()
