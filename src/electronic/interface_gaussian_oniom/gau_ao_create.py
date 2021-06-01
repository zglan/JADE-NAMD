# python
import sys
import re
import copy
import os
import shutil
sys.path.append("../tools/")
import tools

# gaussian input process, for oniom feature in gaussian
# only require the high layer model
# g09 is tested, maybe g03 is also suitable..
# Based on json template to produce gaussian input.
# calculate AO overlap 
#
# 1. onlyinputfiles
# 2. high model
# 4. AO
#

# template variable definition 
#   see gau_log_layer_parser.py
#
# note: qm_interface geometry was given in atomic unit by default!!!
#
class gau_ao_create():
    """
    process gaussian template & generate gaussian input
    """
    params = {
        "BOHR2ANG": 0.52917720859E+00,
        "ANG2BOHR": 1.8897261328856432E+00
        }
    def __init__(self, config = {}):
        """ initialize several internal variable """
        # template data. cmp is static one.
        self.template = {} 
        self.template_cmp = {}    
        self.joblist = ["high-model-overlap"]
        
        # test case        
        self.files = {'template': 'layer.json', 'interface': 'interface.json', \
                      'gaussian': 'high-model-overlap.gjf' }             
        self.files['current']  = "interface1.json"
        self.files['previous'] = "interface2.json"

        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files']  
            
            # working directory & files >>>
            self.directory = {}
            self.directory['root'] = root_dir
            self.directory['home'] = root_dir + "/" + dirs['home']           
            self.directory['work'] = self.directory['home'] + "/" + dirs['work']
            self.directory['work_prev'] = self.directory['home'] + "/" + dirs['work_prev']            
                        
            self.files = {}
            self.files["template"] = root_dir + "/" + files['layer']
            self.files["gaussian"] = files['ao-overlap-inp']
            self.files['current']  = "interface1.json"
            self.files['previous'] = "interface2.json"  

        self.load()
        
        return
            
    def load(self):
        """
        load template.json
        """
        filename = self.files['template']
        obj = tools.load_data(filename)
        self.template = copy.deepcopy(obj)
        self.template_cmp = copy.deepcopy(obj)        
        return obj

    def write(self):
        """ 
        wrt gaussian gjf file with the info. in template.json
        cmp for template_cmp
        """
        # 
        print "QM-INTERFACE GIVEN IN ATOMIC UNIT (AU)"
        print "So, CONVERSION TO ANGSTROM IN GAUSSIAN input"
        BOHR2ANG = self.params['BOHR2ANG']
        #
        t = self.template['high-model']['template']   
        # open file
        jobfile = self.files['gaussian']
        fp = open(jobfile, 'w')
 
        # write link0
        link0 = t['link0']
        #print >>fp, "%%chk=%s" % link0['chk'] 
        print >>fp, "%%mem=%s" % link0['mem']
        print >>fp, "%%nproc=%s" % link0['nproc']
        print >>fp, "%%nproclinda=%s" % link0['nproclinda']
        # write routine       
        print >>fp, "%s\n" % t['routine']['content']
        print >>fp, "%s" % t['title']

        # molecular spec. i.e. geometry spin charge
        # charge & spin
        charge = int(t['charge']); spin = int(t['spin'])
        print >>fp, "%-4d%-4d" % (charge, spin)
        #geometry
        mol = t['mol']        
        atoms = mol['atoms']
        n_atom = mol['n_atom']
        # print natom, flag
        for i in xrange(n_atom):
            record = atoms[i]
            name = record['name']
            coord = record['coord']
            coord = [float(coord[0])*BOHR2ANG,
                     float(coord[1])*BOHR2ANG, float(coord[2])*BOHR2ANG]
            # by Dr. Yanfang Liu
            fmt = "%-5s%15.8f%15.8f%15.8f"
            print >>fp, fmt % (name, coord[0], coord[1], coord[2])

        # wrt. other info. at the end of gaussian gjf file
        if t['tail'] != "":
            print >>fp, "%s" % t['tail']        

        print "gau_write:", os.getcwd(), jobfile
        print "GENERATE GJF SUCCESS."
        
        return

    # ------------------------------------------------------------------
    #
    # Section I: ao overlap; dimer approach    
    # modify_for_dimer is the main called subroutine in this section.
    #
    #-------------------------------------------------------------------
    def merge_mol(self, mols, region):
        """
        merge a few mols in to one mol in data format.
        load in atomic geometries in high model
        """
        n_atom = 0
        atoms = []
        mol = {}
        high_atoms_id = region['high_atoms_id']
        for imol in mols:
            for i_atom in high_atoms_id:
                record = imol['atoms'][i_atom]
                atoms.append(record) 
                n_atom += 1
        mol['n_atom'] = n_atom
        mol['atoms'] = atoms
        return mol

    def modify(self):
        """
        setup ao overlap calc.
        """
        print "AO the Working Directory is:\n", os.getcwd()

        # load interface data from previous and current step
        i_pre = tools.load_data(self.files['previous'])
        i_cur = tools.load_data(self.files['current'])        
        t = copy.deepcopy(self.template_cmp['high-model']['template'])        
        # only the high model is required to calc. ao     
        # modify charge & spin (kept)
        t['charge'] *= 2
        # molecular spec.
        t['mol'] = self.merge_mol([i_cur['mol'], i_pre['mol']], t['region'])

        # routine
        routine = t['routine']
        theory = "HF"
        basis = routine['basis']
        print basis
        model = theory + "/" + basis
        other = "nosymm iop(2/12=3,3/33=1) guess=only pop=full"
        t['routine']['content'] = "# " + model + " " + other
        # delete connect
        if 'connect' in t.keys():
            del t['connect']
        # recover template
        self.template['high-model']['template'] = t
        
        return

                
# Main Program    
if __name__ == "__main__":
    gau = gau_ao_create()    
    gau.modify()
    gau.write()
    
    
    
    
    


