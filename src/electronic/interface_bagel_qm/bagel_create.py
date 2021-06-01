# python
import copy
import os
import re

import tools

# bagel input process.
# Based on json template to produce bagel input.
#


# template content
#   details in 'bagel_template.py'
#
# note: qm_interface geometry was given in atomic unit by default.
#
class bagel_create():
    """
    process bagel template & generate bagel input
    """
    def __init__(self, config={}):
        """ initialize several internal variable """
        # template data. cmp is static one.

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
        self.files["bagel"] = files['bagel_input']
        self.files["dyn"] =  self.directory['root'] + '/' + files['dyn']

        self.load()

        return

    def load(self):
        """
        load template.json and interface.json
        """
        filename1 = self.files['template']
        filename2 = self.files['interface']
        filename3 = self.files['dyn']
        obj_1 = tools.load_data(filename1)
        obj_2 = tools.load_data(filename2)
        obj_3 = tools.load_data(filename3)


        self.template = copy.deepcopy(obj_1)
        self.interface = copy.deepcopy(obj_2)
        self.dyn = copy.deepcopy(obj_3)
        self.label_ZN = int(self.dyn['control']['label_ZN'])
        self.n_atom = self.interface['parm']['n_atom']

    def wrt_bagel_input(self):
        """ 
        wrt template file 
        """
        ANSTOBOHR = 1.8897261328856432

        current_state = self.interface['parm']['i_state']
        n_state = self.interface['parm']['n_state']

        self.template['bagel'][2]['grads'] = []

        current_state_force = {"title" : "force", "target" : current_state -1}

#        print "self.label_ZN", self.label_ZN

        if self.label_ZN == 0:

            print "self.label_ZN", self.label_ZN

            self.template['bagel'][2]['grads'].append(current_state_force)

        elif self.label_ZN == 1:

           for i_state in range(n_state):

               self.template['bagel'][2]['grads'].append(i_state)


        for i_state in range(n_state):

           if i_state < current_state - 1:
               
               nacm =  { "title" : "nacme", "target" : i_state, "target2" : current_state -1, "nacmtype" : "interstate" }
               self.template['bagel'][2]['grads'].append(nacm)

           elif i_state > current_state - 1:

               nacm =  { "title" : "nacme", "target" : current_state -1, "target2" : i_state, "nacmtype" : "interstate" }
               self.template['bagel'][2]['grads'].append(nacm)

#        for i_state in range(n_state):
#
#           for j_state in range(n_state):
#
#               if i_state < j_state:
#               
#                   nacm =  { "title" : "nacme", "target" : i_state, "target2" : j_state, "nacmtype" : "interstate" }
#                   self.template['bagel'][2]['grads'].append(nacm)


        for i_atom in range(self.n_atom):
           coord = self.interface['mol']['atoms'][i_atom]['coord']
           coord = list(map(eval,coord))
           coord = [i / ANSTOBOHR for i in coord]
           self.template['bagel'][0]['geometry'][i_atom]['xyz'] = coord

        tools.dump_data(self.files['bagel'], self.template)

# Main Program
if __name__ == "__main__":
    bagel = bagel_create()
    bagel.wrt_bagel_input()
