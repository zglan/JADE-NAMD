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
# for each layer
#
# require layer.json, interface.json
#
#
# template variable definition 
# see gau_log_layer_parser.py
#
# note: qm_interface geometry was given in atomic unit by default!!!
#
class gau_model_create():
    """
    process gaussian template & generate gaussian input
    for gaussian oniom feature
    """
    params = {
        "BOHR2ANG": 0.52917720859E+00,
        "ANG2BOHR": 1.8897261328856432E+00
        }
    # template data. cmp is static one.
    template = {}
    template_cmp = {}

    def __init__(self, config = {}):
        """ initialize several internal variable """
        self.joblist = []
        self.config = config
        # for test case        
        self.files = {'template': 'layer.json', 'interface': 'interface.json'}             
        # by calling
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
            self.files["interface"] = files['interface']            

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

  
    def wrt_gau_input(self, template):
        """
        write gaussian gjf format input file
        base on self.template info.
        t is the template data structure
        """
        print "QM-INTERFACE GIVEN IN ATOMIC UNIT (AU)"
        print "So, CONVERSION TO ANGSTROM IN GAUSSIAN input"
        BOHR2ANG = self.params['BOHR2ANG']
        #
        jobfile = template['name'] + ".gjf"
        fp = open(jobfile, "w")
        t = template['template']
        # write link0
        link0 = t['link0']
        print >>fp, "%%chk=%s" % link0['chk'] 
        print >>fp, "%%mem=%s" % link0['mem']
        print >>fp, "%%nproc=%s" % link0['nproc']
        print >>fp, "%%nproclinda=%s" % link0['nproclinda']
        # write routine       
        print >>fp, "%s\n" % t['routine']['content']
        print >>fp, "%s" % t['title']
        # print t['routine']['content']

        # molecular spec. i.e. geometry spin charge
        # charge & spin
        charge = int(t['charge']); spin = int(t['spin'])
        #print charge, spin
        print >>fp, "%-4d%-4d" % (charge, spin)
        
        #geometry
        mol = t['mol']        
        atoms = mol['atoms']
        n_atom = mol['n_atom']
        max_name_length = mol['max_name_length']
        # print natom, flag
        for i in xrange(n_atom):
            record = atoms[i]
            type_name = record['type_name']
            coord = record['coord']
            other = record['other']
            coord = [float(coord[0])*BOHR2ANG,
                     float(coord[1])*BOHR2ANG, float(coord[2])*BOHR2ANG]
            # by Dr. Yanfang Liu
            fmt = "%-"+str(max_name_length+2)+"s"+"%15.8f%15.8f%15.8f" + \
                  "%"+str(len(other)+2)+"s"
            print >>fp, fmt % (type_name, \
                               coord[0], coord[1], coord[2], \
                               other)
        print >>fp, "\n",
        # wrt. connectivity info.
        if "connect" in t.keys():
            print >>fp, "%s" % t['connect'],
        # wrt. other info. at the end of gaussian gjf file
        # print t['tail']
        if t['tail'] != "":
            print >>fp, "%s" % t['tail'],      
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


    # -----------------------------------------------------------------
    #
    # update excited state calculations
    #
    # ----------------------------------------------------------------
    def copy_mol(self, target, src):
        """
        copy mol info of src to target
        """
        n_atom = target['n_atom']
        n_atom_src = src['natom']
        if n_atom != n_atom_src:
            print "fail!!! no consistent atomic number ??"
            exit(1)
        for i in xrange(n_atom):
            target['atoms'][i]['coord'] = src['atoms'][i]['coord']
        return
                
    def modify_highmodel(self):
        """
        tddft input, nstates & root would be updated.
        """
        t = copy.deepcopy(self.template_cmp['high-model']['template'])
        i_cur = tools.load_data(self.files['interface'])
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
        if i_state == 0:
            content = re.sub(pat, "root="+str(i_state+1), content)
        else:
            content = re.sub(pat, "root="+str(i_state), content)
        # calc force routine of gs if required
        pat = re.compile("(td\(.+?\))|(tda\(.+?\))|(cis\(.+?\))", re.IGNORECASE)
        force_content = re.sub(pat, "", content)
        # gs single point calc.
        pat = re.compile("force", re.IGNORECASE)
        sp_content = re.sub(pat, "", force_content)
        print sp_content
        # new content routine for es
        pat = re.compile("force", re.IGNORECASE)
        es_content = re.sub(pat, " ", content)

        # suppose the first occurance of */* is like b3lyp/6-31G* style
        # 
        # first store iop info, which may be confilict with theory/basis string
        pat = re.compile("IOP\(.*?\)", re.IGNORECASE)
        m = pat.search(content)
        iop = " "
        if m is not None:            
            iop += m.group() 
        else:
            iop = " "
        es_content = re.sub(pat, "", es_content, count=1)
        force_content = re.sub(pat, "", force_content, count=1)
        #
        # then replace theory/basis
        pat = re.compile('\/(\S+)')
        es_content = re.sub(pat, "/ChkBasis", es_content, count=1)
        es_content += iop
        pat = re.compile('\/(\S+)')
        force_content = re.sub(pat, "/ChkBasis", force_content, count=1)
        force_content += iop
        # assign value
        # print i_state
        t['routine']['content'] = sp_content + " pop=full"
        pat = re.compile("IOP\(.*?\)", re.IGNORECASE)
        alter_content = re.sub(pat, "", content, count=1)

        t['routine']['es_content'] =  alter_content + iop +  " geom=AllCheck Guess=Read " + \
                                     " iop(9/40=20) pop=full"       
        if i_state == 0:
            t['routine']['force_content'] = force_content + " geom=AllCheck Guess=Read "       
            t['routine']['es_content'] =  es_content +  " geom=AllCheck Guess=Read " +  " iop(9/40=20) pop=full" 
                                      
        # recover template
        self.template['high-model']['template'] = t
        
        return

    def modify_coord(self):
        """
        change the coord. of template to interface by dynamics
        """
        # %charge & spin was kept. none was required.
        #
        # %molecular spec.    
        # current interface file data.
        i_cur = tools.load_data(self.files['interface'])
        # loop for each layer
        for name in self.template_cmp.keys():
            #print self.template[name]
            t = copy.deepcopy(self.template_cmp[name]['template'])
            # print t
            self.copy_mol(t['mol'], i_cur['mol'])
            self.template[name]['template'] = t
        return        
    
    def modify(self):
        """
        energy and gradient 
        """
        self.modify_coord()
        self.modify_highmodel()
        
        return

    def write(self):
        """
        write each layer to an gaussian gjf format file
        """
        joblist = []
        for name in self.template.keys():
            t = copy.deepcopy(self.template[name])
            t['template']['link0']['chk'] = name + ".chk"
            self.wrt_gau_input(t)
            joblist.append(name)
        self.joblist = joblist
        return
  
    
# Main Program    
if __name__ == "__main__":
    gau = gau_model_create()    
    gau.modify()
    gau.write()
    print gau.joblist
    
    
