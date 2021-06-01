# python
import sys
import re
import copy
import os
import shutil
from CONSTANT import *

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/../tools/")
import tools

# gaussian input process.
# Based on json template to produce gaussian input.
# modify: dimmer / td / ...
#
# 
# template content
#   details in 'gau_template.py'
#
# note: qm_interface geometry was given in atomic unit by default.
#
class createInp():
    """
    generate gaussian input based on template.json 
    this version only support DFT GROUND STATE  
    """
    def __init__(self, config = {}):
        """ initialize several internal variable """
        # template data. cmp is static one.
        self.template = {} 
        self.template_cmp = {}    
        
        self.filelist = {}
        
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
            self.files["gaussian"] = files['inp']
            self.files['current']  = "interface1.json"
            self.files['previous'] = "interface2.json"  

        self.load()
        
        return
            
    def load(self):
        """ load template.json """
        filename = self.files['template']
        obj = tools.load_data(filename)
        self.template = copy.deepcopy(obj)
        self.template_cmp = copy.deepcopy(obj)        
        return obj

    def wrt_compare(self, filename = "gaussian.gjf"):
        """ 
        cmp, write template compare file
        """
        bohr2ang = AU2ANGSTROM
        print "QM-INTERFACE GIVEN IN ATOMIC UNIT, CONVERSION TO ANGSTROM IN GAUSSIAN DONE"
        t = self.template_cmp
            
        # open file
        jobfile = self.files['gaussian']
        fp = open(jobfile, 'w') 
        # write link0
        link0 = t['link0']
        print >>fp, "%%chk=%s" % link0['chk'] 
        print >>fp, "%%mem=%s" % link0['mem']
        print >>fp, "%%nproc=%s" % link0['nproc']
        # write routine       
        print >>fp, "%s\n" % t['routine']['content']
        print >>fp, "%s\n" % t['title']
        # charge & spin
        print >>fp, "%-4d%-4d" % (t['charge'], t['spin'])  
        # molecular geometry
        geom = t['mol'] 
        atoms = geom['atoms']
        natom = geom['natom']
        print natom, flag
        for i in range(natom):
            record = atoms[i]
            atomname = record['name']
            coord = record['coord']
            coord = [float(coord[0])*bohr2ang, float(coord[1])*bohr2ang, float(coord[2])*bohr2ang]
            if "frg" in record.keys():
                frg = record['frg']
                if frg == "":
                    print >>fp, "%-10s%12.7f%12.7f%12.7f" % (atomname, \
                            float(coord[0]), float(coord[1]), float(coord[2]))
                else:
                    print >>fp, "%-10s%12.7f%12.7f%12.7f%5d" % (atomname, \
                            float(coord[0]), float(coord[1]), float(coord[2]), frg)
            else:
                print >>fp, "%-10s%12.7f%12.7f%12.7f" % (atomname, \
                            float(coord[0]), float(coord[1]), float(coord[2]))                
        print >>fp, "\n",
        if t['tail'] != "":
            print >>fp, "%s" % t['tail']

        print "gau_write:", os.getcwd(), jobfile

        return

        
    def wrt_gjf(self, i_state = 0):
        """ 
        flag:
        default, write modified template file, or
        """
        bohr2ang = AU2ANGSTROM
        print "QM-INTERFACE GIVEN IN ATOMIC UNIT, CONVERSION TO ANGSTROM IN GAUSSIAN DONE"
        t = self.template[i_state]
            
        # open file
        jobfile = str(i_state) + ".gjf"
        fp = open(jobfile, 'w') 
        # write link0
        link0 = t['link0']
        print >>fp, "%%chk=%s" % link0['chk'] 
        print >>fp, "%%mem=%s" % link0['mem']
        print >>fp, "%%nproc=%s" % link0['nproc']
        # write routine       
        print >>fp, "%s\n" % t['routine']['content']
        print >>fp, "%s\n" % t['title']
        # charge & spin
        print >>fp, "%-4d%-4d" % (t['charge'], t['spin'])  
        # molecular geometry
        geom = t['mol'] 
        atoms = geom['atoms']
        natom = geom['natom']
        for i in range(natom):
            record = atoms[i]
            atomname = record['name']
            coord = record['coord']
            coord = [float(coord[0])*bohr2ang, float(coord[1])*bohr2ang, float(coord[2])*bohr2ang]
            if "frg" in record.keys():
                frg = record['frg']
                if frg == "":
                    print >>fp, "%-10s%12.7f%12.7f%12.7f" % (atomname, \
                            float(coord[0]), float(coord[1]), float(coord[2]))
                else:
                    print >>fp, "%-10s%12.7f%12.7f%12.7f%5d" % (atomname, \
                            float(coord[0]), float(coord[1]), float(coord[2]), frg)
            else:
                print >>fp, "%-10s%12.7f%12.7f%12.7f" % (atomname, \
                            float(coord[0]), float(coord[1]), float(coord[2]))                
        print >>fp, "\n",
        if t['tail'] != "":
            print >>fp, "%s" % t['tail']

        print "gau_write:", os.getcwd(), jobfile

        return jobfile
    
    
    
    def build_input(self):
        """
        base on the input parameter to build a series of files
        """
        # current interface file data.
        model = tools.load_data(self.files['interface'])
        # %charge are kept. and spin varied.
        n_state = model['parm']['n_state']
        i_state = model['parm']['i_state']
        
        filelist = []
        for i in xrange(n_state):
            filename = self.wrt_gjf(i)
            filelist.append(filename)
        filelist.reverse()
        
        tools.dump_data("filelist.dat", filelist)
        
        return filelist
        
        
    def modify_spins(self):
        """
        dft input, spin state would be updated
        """
        # current interface file data.
        model = tools.load_data(self.files['interface'])
        
        # %charge are kept. and spin is varied.
        n_state = model['parm']['n_state']
        # i_low_spin = model['parm']['i_low_spin']
        i_low_spin = 1
        i_state = model['parm']['i_state']
        
        self.template = [{} for i in xrange(n_state)]
        #
        for i in xrange(n_state):
            t = copy.deepcopy(self.template_cmp)
            # %molecular spec.     
            t['spin'] = 2 * i + i_low_spin
            t['mol'] = model['mol']  
            # routine section
            content = t['routine']['content']
            pat = re.compile("force", re.IGNORECASE)
            # delete force, if present.
            sp_content = re.sub(pat, "", content)
            # current state requires force, or you may change i_state to -1
            # and calculate force for each state.
            if i == i_state:    
                sp_content += "force"
            # read check or ?
            # suppose the first occurance of */* is like b3lyp/6-31G* style
            pat = re.compile("\/[\S]+")
            if i != n_state - 1:
                sp_content = re.sub(pat, "/ChkBasis", sp_content, count=1)
            # assign value
            t['routine']['content'] =  sp_content +  " geom=AllCheck Guess=Read "        
            
            self.template[i] = t
        return

    def modify(self):
        """
        modify template
        """
        self.modify_spins()
        
        return
                
# Main Program    
if __name__ == "__main__":      
    gau = InpCreate()    
    gau.modify()
    gau.build_input()
    
    
    
    
    


