# python
import sys
import re
import copy
import os
import shutil
sys.path.append("../tools/")
import tools
from periodictable import periodictable as PT

# gamess input process.
# Based on json template to produce gamess input.
# modify: dimmer / td / ...
#

# template content definition
#   details in 'gms_template.py'
#
# note: qm_interface geometry was given in atomic unit by default.
#
class gms_create():
    """
    process gaussian template & generate gaussian input
    """
    def __init__(self, config = {}):
        """ initialize several internal variable """
        # template data. cmp is static one.
        self.template = {}
        self.template2 = {}
        self.template_cmp = {}    
        
        # test case        
        self.files = {'template': 'template.json', 'interface': 'interface.json', \
                      'job': 'gamess.inp', 'job2': 'gamess2.inp' }             
        self.files['current']  ="./GMS_TMP/" + self.files['interface']
        self.files['previous'] = "./GMS_TMP_PREV/"+ self.files['interface']
        self.constant = {"BOHR2ANGSTROM": 0.529177249}

        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files']  

            self.constant = config['constant']
            # working directory & files >>>
            self.directory = {}
            self.directory['root'] = root_dir
            self.directory['home'] = root_dir + "/" + dirs['home']           
            self.directory['work'] = self.directory['home'] + "/" + dirs['work']
            self.directory['work_prev'] = self.directory['home'] + "/" + dirs['work_prev']            
                        
            self.files = {}
            self.files["template"] = root_dir + "/" + files['template']
            self.files["interface"] = files['interface']            
            self.files["job_inp"] = files['job_inp']
            self.files["job_inp2"] = files['job_inp2']         
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


    def wrt_input_template(self, jobfile="", template={}):
        """
        write gms input template
        """
        bohr2ang = self.constant["BOHR2ANGSTROM"]
        print "QM-INTERFACE (AU) TO GAMESS Angstrom unit. > ", jobfile
        # open file
        fp = open(jobfile, "w")
        # write gms namelist ...
        # suppose it has been modified.
        t = template
        #
        for key in t:
            if key != "DATA" and key[0] != "@":
                print >>fp, "%s" % t[key],

        data = self.template['DATA']
        print >>fp, "%s" % data
        print "gau_write:", os.getcwd(), jobfile
        return

    def wrt_input(self):
        """
        write gms inputs
        """
        inpfile = self.files['job_inp']
        t = self.template
        self.wrt_input_template(jobfile = inpfile, template = t)

        inpfile = self.files['job_inp2']
        t = self.template2
        self.wrt_input_template(jobfile = inpfile, template = t)       

        return

    

    def wrt_internal(self):
        """ internal exchange dat """
        dump_data('template.json', self.template_cmp)        
        return

    # ------------------------------------------------------------------
    #
    # Section I: ao overlap; dimer approach    
    # modify_for_dimer is the main called subroutine in this section.
    #
    #-------------------------------------------------------------------
    def __geom_data(self):
        """
        write down data section in gms.
        """
        mytable = PT()
        # constant
        bohr2ang = float(self.constant['BOHR2ANGSTROM'])
        at_data  = self.template['@DATA']
        title = at_data['title']
        symm = at_data['symm']
        mol = at_data['mol']
        if 'n_atom' in mol:            
            n_atom = mol['n_atom']
        else:
            n_atom = mol['natom']
        atoms = mol['atoms']

        if symm.upper() != "C1":
            symm = symm + '\n'

        data = " $data\n" + title + '\n' + symm + '\n'
        for i in xrange(n_atom):
            record = atoms[i]
            atomname = record['name']
            coord = record['coord']
            charge = mytable.get_charge(label=atomname)
            line = "%-10s%6.1f%12.7f%12.7f%12.7f" % (atomname, charge, \
                            float(coord[0])*bohr2ang, float(coord[1])*bohr2ang, float(coord[2])*bohr2ang)
            data = data + line + "\n"
                                                   
        data += "$end"

        self.template['DATA'] = data
        
        return data

    
    def __merge_mols(self, mols):
        """
        merge a few mols in to one mol in data format.
        """
        natom = 0
        atoms = []
        for imol in mols:
            if 'n_atom' in imol:
                natom += imol['n_atom']
            else:
                natom += imol['natom']
            for record in imol['atoms']:
                record['frg'] = ""
                atoms.append(record) 
        mol = {'n_atom': natom, 'atoms': atoms}        
        return mol
    
    def modify_dimer(self):
        """
        setup ao overlap calc.
        """
        # load interface data from previous and current step
        filename = self.files
        i_pre = tools.load_data(filename['previous'])
        i_cur = tools.load_data(filename['current'])
        t = copy.deepcopy(self.template_cmp)
        
        # $data section in gms.
        # molecular spec.
        mol = self.__merge_mols([i_cur['mol'], i_pre['mol']])
        t['@DATA']['mol'] = mol
        t['@DATA']['title'] = "ONLY CHECK CALC, IGNORE WARINING.."
        # re-build $data section.
                
        # modify charge & spin (kept)
        #
        at_contrl = t['@CONTRL']
        if 'MULT' in at_contrl:
            mol_spin = int(at_contrl['MULT'])
        else:
            mol_spin = 1

        if "ICHARG" in at_contrl:
            mol_chrg = int(at_contrl['ICHARG']) * 2
        else:
            mol_chrg = 0

        t['CONTRL'] = " $contrl scftyp=rhf runtyp=energy exetyp=check\n \
        NPRINT=3 MULT=%d ICHARG=%d NPRINT=3 $end\n" % (mol_spin, mol_chrg)

        # tddft is not necessary, so...
        if 'TDDFT' in at_contrl:
            del t['TDDFT']

        # recover template
        self.template = t
        self.__geom_data()
        
        return

    def build_list(self, at_list):
        """
        change dict. vars to string
        """
        mystring = ""
        i = 1
        for mykey in at_list:
            # print at_list[mykey],mykey
            
            mystring += mykey + "=" + str(at_list[mykey]) + " "
            i += 1
            if i % 4 == 0:
                mystring += "\n         "
        mystring += " $END\n"
        return mystring
# section II: mo ci vector ...
#
    def modify_td(self):
        """
        tddft input, nstates & root would be updated.
        """
        # current interface file data.
        i_cur = tools.load_data(self.files['interface'])
 
        t = copy.deepcopy(self.template_cmp)


        # %charge & spin was kept. none was requred.
        # %molecular spec.     
        t['@DATA']['mol'] = i_cur['mol']
        t['@DATA']['title'] = "energy & gradient.."    
        # %routine
        # in dyn. interface, gs was 1, the first-es is 2, et al.
        # so there are n_es + 1 states
        # but gaussian, gamess, 'root=1' is first es.
        # so, x - 1 is ok
        n_state = int(i_cur['parm']['n_state']) - 1 
        i_state = int(i_cur['parm']['i_state']) - 1

        # TDDFT SECTION
        at_tddft = t['@TDDFT']
        at_tddft['NSTATE'] = str(n_state)
        at_tddft['IROOT'] = str(i_state)
        mystring = self.build_list(at_tddft)        
        t['TDDFT'] = " $TDDFT " + mystring
        if i_state == 0:
            del t['TDDFT']

        # CONTRL SECTION
        at_contrl = t['@CONTRL']
        if 'MULT' not in at_contrl:
            at_contrl['MULT'] = "1"
        if "ICHARG" not in at_contrl:
            # print at_contrl['ICHARG']
            at_contrl['ICHARG'] = "0"
        if i_state == 0:
            del at_contrl['TDDFT']
        mystring = self.build_list(at_contrl)
        t['CONTRL'] = " $CONTRL " + mystring
 
        # recover template
        self.template = t
        self.__geom_data()
        
        return

    def modify_td_gs(self):
        """
        tddft input, nstates & root would be updated.
        """
        # current interface file data.
        i_cur = tools.load_data(self.files['interface'])
 
        t = copy.deepcopy(self.template_cmp)

        # %charge & spin was kept. none was requred.
        # %molecular spec.     
        t['@DATA']['mol'] = i_cur['mol']
        t['@DATA']['title'] = "energy & gradient.."    
        # %routine
        # in dyn. interface, gs was 1, the first-es is 2, et al.
        # so there are n_es + 1 states
        # but gaussian, gamess, 'root=1' is first es.
        # so, x - 1 is ok
        n_state = int(i_cur['parm']['n_state']) - 1
        i_state = int(i_cur['parm']['i_state']) - 1

        if i_state == 0:
            i_state = 1
        else:
            print "excited state condition [ignored]"

        # TDDFT SECTION
        at_tddft = t['@TDDFT']
        at_tddft['NSTATE'] = str(n_state)
        at_tddft['IROOT'] = str(i_state)
        mystring = self.build_list(at_tddft)        
        t['TDDFT'] = " $TDDFT " + mystring

        # CONTRL SECTION
        at_contrl = t['@CONTRL']
        at_contrl['RUNTYP'] = "ENERGY"
        if 'MULT' not in at_contrl:
            at_contrl['MULT'] = "1"
        if "ICHARG" not in at_contrl:
            # print at_contrl['ICHARG']
            at_contrl['ICHARG'] = "0"

        mystring = self.build_list(at_contrl)
        t['CONTRL'] = " $CONTRL " + mystring
 
        # recover template
        self.template2 = t
 
        self.__geom_data()
        
        return


    def modify(self, jobtype = "td"):
        """
        optional input: td / dimer
        """
        if jobtype == "td":            
            self.modify_td()
            self.modify_td_gs()
        elif jobtype == "dimer":
            self.modify_dimer()
        else:
            print "Error: gau_input; no other type."
            sys.exit(1)
        return

                
# Main Program    
if __name__ == "__main__":
      
    gms = gms_create()    
    gms.modify(jobtype = "dimer")    
    gms.wrt_input()    
    gms.modify(jobtype = "td")
    gms.wrt_input()
    
    
    
    
    


