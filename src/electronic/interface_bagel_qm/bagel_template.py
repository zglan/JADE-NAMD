# python

import copy
import re
import sys

sys.path.append("../tools/")
import tools

# bagel input process for templating.


#
class bagel_template():
    """
    process bagel template & generate bagel input
    """
    def __init__(self, config={}):

        self.pointer = {"content": [], "i_line": 0}

        root_dir = config['root']
        dirs = config['dirs']
        files = config['files']
        bagel_file = root_dir + "/" + dirs['template'] + "/" + files[
            'bagel_template']
        tpl_file = root_dir + '/template.json'
        self.files = {'bagel': bagel_file, 'template': tpl_file}

        # load gjf & write json
        self.dump()

        return

    # ------------------------------------------------------------------
    #
    # dump_template() & load_template is the main called subroutine in this section.
    #
    # -------------------------------------------------------------------

    def rd_bagel_input(self):
        """ read template file """

        self.template = tools.load_data(self.files["bagel"])

        # deep copy it
        self.template_cmp = copy.deepcopy(self.template)

        return

        # % dump/load template.

    def dump(self):
        """
        read input file; dump template in json format.
        """
        self.rd_bagel_input()

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
    bagel = bagel_template()
