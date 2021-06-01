# python
import sys
import re
import copy
import os
import shutil
sys.path.append("../tools/")
import tools

# gaussian input process, for oniom feature in gaussian
# g09 is tested, maybe g03 is also suitable..
# Based on json template to produce gaussian input.
# modify: dimmer / td / ...
#
# 1. onlyinputfiles
# 2. high model
# 3. real 
# 4. AO
# 5. wf
#

# template variable definition 
# see details in 'gau_template.py'
#
# note: qm_interface geometry was given in atomic unit by default!!!
#
class gau_create():
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
        
        # test case        
        self.files = {'template': 'template.json', 'interface': 'interface.json', \
                      'gaussian': 'gaussian.gjf' }             
        self.files['current']  ="./GAU_TMP/" + self.files['interface']
        self.files['previous'] = "./GAU_TMP_PREV/"+ self.files['interface']

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
            self.files["template"] = root_dir + "/" + files['template']
            self.files["interface"] = files['interface']            
            self.files["gaussian"] = files['gau_input']
            self.files['current']  = "interface1.json"
            self.files['previous'] = "interface2.json"  

        #self.load()
        
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


    def wrt_gau_input_wf(self, flag="default"):
        """ 
        wrt gaussian gjf file with the info. in template.json
        cmp for template_cmp
        """
        # 
        print "QM-INTERFACE GIVEN IN ATOMIC UNIT (AU)"
        print "So, CONVERSION TO ANGSTROM IN GAUSSIAN input"
        BOHR2ANG = self.params['BOHR2ANG']
        #
        # which data set is used.
        # cmp or default version
        if flag == "cmp":
            t = self.template_cmp
        elif flag == "default":
            t = self.template
        else:
            print "only cmp/default is possible option: wrt_gau_input"
            sys.exit(1)
            
        # open file
        jobfile = self.files['gaussian']
        fp = open(jobfile, 'w')
 
        # write link0
        link0 = t['link0']
        print >>fp, "%%chk=%s" % link0['chk'] 
        print >>fp, "%%mem=%s" % link0['mem']
        print >>fp, "%%nproc=%s" % link0['nproc']
        print >>fp, "%%nproclinda=%s" % link0['nproclinda']
        # write routine       
        print >>fp, "%s\n" % t['routine']['content']
        print >>fp, "%s\n" % t['title']

        # molecular spec. i.e. geometry spin charge
        mol = t['mol']        
        # charge & spin
        charge = mol['charge']; spin = mol['spin']
        for c, s in zip(charge, spin):
            print >>fp, "-%4d%-4d" % (c, s)
        #geometry
        atoms = mol['atoms']
        n_atom = mol['n_atom']
        max_name_length = mol['max_name_length']
        # print natom, flag
        for i in xrange(n_atom):
            record = atoms[i]
            type_name = record['type_name']
            ifrozen = record['ifrozen']
            coord = record['coord']
            other = record['other']
            coord = [float(coord[0])*BOHR2ANG,
                     float(coord[1])*BOHR2ANG, float(coord[2])*BOHR2ANG]
            # by Dr. Yanfang Liu
            fmt = "%"+str(max_name_length+2)+"s"+"%3d%15.8f%15.8f%15.8f" + \
            "%"+str(len(other)+2)+"s"
            print >>fp, fmt % (type_name, ifrozen, \
                               coord[0], coord[1], coord[2], \
                               other)
        print >>fp, "\n"
        # wrt. connectivity info.
        if "connect" in t.keys():
            print >>fp, "%s" % "\n".join(t['connect'])                
        # wrt. other info. at the end of gaussian gjf file
        if t['tail'] != "":
            print >>fp, "%s" % t['tail']        

        # write extra job
        if 'force_content' in t['routine'].keys():
            force_content = t['routine']['force_content']
            print >>fp, "--LINK1--"
            link0 = t['link0']
            print >>fp, "%%chk=%s" % link0['chk']
            print >>fp, "%%mem=%s" % link0['mem']
            print >>fp, "%%nproc=%s" % link0['nproc']
            print >>fp, "%%nproclinda=%s" % link0['nproclinda']
            # write routine
            print >>fp, "%s\n" % force_content
        
        if 'es_content' in t['routine'].keys():
            es_content = t['routine']['es_content']
            print >>fp, "--LINK1--"
            link0 = t['link0']
            print >>fp, "%%chk=%s" % link0['chk']
            print >>fp, "%%mem=%s" % link0['mem']
            print >>fp, "%%nproc=%s" % link0['nproc']
            print >>fp, "%%nproclinda=%s" % link0['nproclinda']
            # write routine
            print >>fp, "%s\n" % es_content
        print "gau_write:", os.getcwd(), jobfile
        print "GENERATE GJF SUCCESS."
        
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
    def __merge_mols(self, mols):
        """
        merge a few mols in to one mol in data format.
        mols is a list
        load in atomic geometries in high model
        """
        n_atom = 0
        atoms = []
        for imol in mols:
            high_atoms_id = imol['high_atoms_id']
            for i_atom in high_atoms_id:
                record = imol['atoms'][i_atom]
                atoms.append(record) 
                n_atom += 1
        mol['n_atom'] = n_atom
        mol['atoms'] = atoms
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
        # only the high model is required to calc. ao     
        # modify charge & spin (kept)
        charge = []
        for c in t['charge']:
            charge.append(c*2)
        t['charge'] = charge
        # molecular spec.
        mol = self.__merge_mols([i_cur['mol'], i_pre['mol']])        
        t['mol'] = mol

        # routine
        routine = t['routine']
        theory = "HF"
        basis = routine['basis']
        model = theory + "/" + basis
        other = "nosymm iop(2/12=3,3/33=1) guess=only pop=full"
        t['routine']['content'] = "#" + model + " " + other
        # delete connect
        if 'connect' in t.keys():
            del t['connect']
 
        # recover template
        self.template = t
        
        return
        
        
    # -----------------------------------------------------------------
    #
    # update excited state calculations
    #
    # section II: mo ci vector ...
    # ----------------------------------------------------------------
    def modify_td(self):
        """
        tddft input, nstates & root would be updated.
        for oniom feature
        """
        # current interface file data.
        i_cur = tools.load_data(self.files['interface'])
 
        t = copy.deepcopy(self.template_cmp)
        
        # %charge & spin was kept. none was requred.
        # %molecular spec.     
        t['mol'] = i_cur['mol']        
        # %routine
        # in dyn. interface, gs was 1, the first-es is 2, et al.
        # so there are n_es + 1 states
        # but gaussian, root=1 is first es.
        # so, x - 1 is ok
        n_state = int(i_cur['parm']['n_state']) - 1
        i_state = (i_cur['parm']['i_state']) - 1
        routine = t['routine']
        content = routine['content']
        pat = re.compile("nstates=(\d+)", re.IGNORECASE)
        content = re.sub(pat, "nstates="+str(n_state), content)
        pat = re.compile("root=(\d+)", re.IGNORECASE)
        content = re.sub(pat, "root="+str(i_state), content)

        # calc force routine of gs if required
        pat = re.compile("(td\(.+?\))|(tda\(.+?\))|(cis\(.+?\))", re.IGNORECASE)
        force_content = re.sub(pat, "", content)
        # gs single point calc.
        pat = re.compile("force", re.IGNORECASE)
        sp_content = re.sub(pat, "", force_content)
        # new content routine for es
        pat = re.compile("force", re.IGNORECASE)
        es_content = re.sub(pat, " ", content)

        # suppose the first occurance of */* is like b3lyp/6-31G* style
        pat = re.compile("\/[\S]+")
        es_content = re.sub(pat, "/ChkBasis", es_content, count=1)
        pat = re.compile("\/[\S]+")
        force_content = re.sub(pat, "/ChkBasis", force_content, count=1)
        # assign value
        t['routine']['content'] = sp_content
        t['routine']['es_content'] =  content +  " geom=AllCheck Guess=Read "        
        if i_state == 0:
            t['routine']['force_content'] = force_content + " geom=AllCheck Guess=Read "       
            t['routine']['es_content'] =  es_content +  " geom=AllCheck Guess=Read " 
        # recover template
        self.template = t
        
        return

    def setup_high_model(self):
        """ 
        for oniom calc.
        and setup the information for high model
        """

        
        filename = "only.log"
        pat = re.compile("ONIOM: generating point\s+\d+ -- high level on model system")
        fp = open(filename, "r")
        while True:
            line = fp.readline()
            if line == "":
                break
            m = pat.search(line)
            if m is not None:
                break
        if m is None:
            print "fail, cannot find oniom high model input file.."
            exit(1)
        i = 0
        while i < 4: # number of line to jump 
            i += 1
            fp.readline() 
        # read input file
        content = ""
        while True:
            line = fp.readline()
            if line.count("-"*20) > 0:
                break
            if line == "":
                print "onlyinputfiles content error.."
                exit(1)
            content += line 
        fp.close()
        fp = open("highmodel.gjf", "w")
        print >>fp, "%s" % content
        fp.close()

        return

        
         


    def modify(self, jobtype = "td"):
        """
        optional input: td / dimer
        """
        if jobtype == "td":
            self.modify_td()
        elif jobtype == "dimer":
            self.modify_dimer()
        else:
            print "Error: gau_input; no other type."
            sys.exit(1)
        return
                
# Main Program    
if __name__ == "__main__":
      
    gau = gau_create()    
    # gau.modify(jobtype = "dimer")    
    # gau.wrt_gau_input()    
    gau.modify(jobtype = "td")
    gau.wrt_gau_input()
    
    
    
    
    


