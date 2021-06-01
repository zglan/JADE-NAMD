# python

import sys
import re
import copy

sys.path.append("../tools/")
import tools

# gaussian input process for templating.


# % template & template_cmp
#   cmp is static dict. for comparation only.
#   template<_cmp>:
#   ==
#   == link0 {}
#       == 'chk': ''
#       == 'mem': ''
#       == 'nproc': 1
#       == 'nproclinda': 1
#   == routine {}
#   == mol {}
#       == 'atoms': []
#       == 'natom': 0
#   == spin: int
#   == charge: int
#   == title ""
#   == tail ""
#   ==
#
#   template & template_cmp are not necessary in the current version.
#
class gau_template():
    """
    process gaussian template & generate gaussian input
    """
    def __init__(self, config = {}):
        """ initialize several internal variable """
        # content of the template.
        self.template = {} 
        self.template_cmp = {'link0':{}, 'routine': {}, 'spin': 1, 'charge': 0, \
                        'tail':'', 'title':'', 'mol': {} }  
        # i/o pointer                      
        self.pointer = {"content": [], "i_line": 0}
        self.files = {'gaussian': './EXAM/gau_template.gjf', 'template': 'template.json'}
        
        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files']
            gau_file = root_dir + "/" + dirs['template'] + "/" + files['gau_template']
            tpl_file = root_dir + '/template.json'
            self.files = {'gaussian': gau_file, 'template': tpl_file}          

        # load gjf & write json
        self.dump()     

        return
    
    # ------------------------------------------------------------------
    #
    # Section 0: convert necessary data from gjf template to json format.    
    # dump_template() & load_template is the main called subroutine in this section.
    #
    #-------------------------------------------------------------------
    def __set_default_template_value(self):
        """ default value """
        link0 = {'chk': '', 'mem': '', 'nproc': 1, 'nproclinda':1}
        t = {}
        mol = {'atoms': [], 'natom': 0}
        t['charge'] = 0
        t['spin'] = 1
        self.template['link0'] = link0
        return

    def __rd_gau_input_link0(self):
        """
        % section
        """
        link0 = {}
        link0['chk'] = "gaussian.chk"
        link0['mem'] = "1GB"
        link0['nproc'] = "2"
        link0['nproclinda'] = "1"

        i_line = 0
        for cur_line in self.pointer['content']:
            i_find_chk = re.search('%chk', cur_line)
            if i_find_chk is not None:
                items = cur_line.split('=')
                link0['chk'] = items[1][:-1]
            i_find_mem = re.search('%mem', cur_line)    
            if i_find_mem is not None:
                items = cur_line.split('=')
                link0['mem'] = items[1][:-1]
            i_find_nproc = re.search('%nproc', cur_line)    
            if i_find_nproc is not None:
                items = cur_line.split('=')
                link0['nproc'] = items[1][:-1]         
            i_find_nproclinda = re.search('%nproclinda', cur_line)
            if i_find_nproclinda is not None:
                items = cur_line.split('=')
                link0['nproclinda'] = items[1][:-1]

        self.template['link0'] = link0
        
        return         
        
    def __rd_gau_input_routine(self):
        """
        '#' section
        """
        routine = {}
        i_line = 0
        i_start = -1
        i_end = -1
        content = ""
        n = len(self.pointer['content'])
        for i in xrange(n):
            cur_line = self.pointer['content'][i]
            i_find_sharp = re.search('^#', cur_line)
            if i_find_sharp is not None:
                i_start = i
                break

        for i in xrange(i_start+1, n):
            cur_line = self.pointer['content'][i]
            if cur_line.strip() == "":
                i_end = i
                break

        for i in xrange(i_start, i_end):
            content += self.pointer['content'][i].strip() + " "

        if i_start == -1:
            print "cannot find gaussian input routine '#' line"

        # print content
        
        # suppose: the first one in the record is model chemistry,
        # such as HF/6-31G*
        # search a word contain '/' char.
        pattern = re.compile('(\w)+\/[\S]+')
        m = pattern.search(content)
        if m is not None:            
            model = m.group()
        else:
            print "no routine line. such as B3LYP/6-31G*"
            exit(1)
        theory = model.split('/')[0]
        basis = model.split('/')[1]
        self.template['routine'] = {'content': content, 'model': model,
                        'theory': theory, 'basis': basis
                        }
        
        self.pointer['i_line'] = i_end 

        return        
                
    def __rd_gau_input_mol(self):
        """
        Molecule specification: Specify molecular system to be studied
        (blank line terminated).
        charge spin & coordinates.
        """
        # find the blank line after '#' colum
        line_each = self.pointer['content']
        n_line = len(line_each)
        i_line = self.pointer['i_line']
 
        # jump the title line and a blank line
        self.template['title'] = line_each[i_line+1][:-1]
    
        # now we reach charge/spin line.
        i_line = i_line + 3
        cur_line = line_each[i_line]
        cs = cur_line.split()
        charge = int(cs[0])
        spin = int(cs[1])
        
        # molecular coord. [suppose cart. coordinates].
        i_line += 1
        natom = 0
        mol = {'natom': 0, 'atoms':[]}
        for i in range(i_line, n_line):
            i_line += 1
            cur_line = line_each[i]
            if cur_line.strip() == "":
                break
            # read one line  
            record = self.__check_gjf_frg(cur_line)             
            mol['atoms'].append(record)
            
            natom = natom + 1
            mol['natom'] = natom
   
        self.template['mol'] = mol   
        self.template['charge'] = charge
        self.template['spin'] = spin
        
        self.pointer['i_line'] = i_line     

        return  
        
    def __check_gjf_frg(self, line):
        """
            check gjf fragment type 03 or 09 version, and return records
        """
        frg = ""
        if line.find('=') != -1:
            myline = line.replace('(',' ').replace(')',' ').replace('=',' ')
            items = myline.split()
            atomname = items[0]
            frg = int(items[2])
            coord = [ float(items[3]), float(items[4]), float(items[5]) ]
        else:
            myline = line
            items = myline.split()
            if len(items) > 4:
                frg = int(items[4])
            atomname = items[0]
            coord = [ float(items[1]), float(items[2]), float(items[3]) ]
        rec = {'name': atomname, 'coord': coord, 'frg': frg}
        return rec
    
    def __rd_gau_input_tail(self):
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

    def rd_gau_input(self):
        """ read template file """
        # open adn read all
        fp = open(self.files["gaussian"], 'r')
        self.pointer['content'] = fp.readlines()
        fp.close()
       
        # read process
        # link0 section : %
        self.__rd_gau_input_link0()
        # routine section: #
        self.__rd_gau_input_routine()
        # molecule spec.
        self.__rd_gau_input_mol()

        # other data
        self.__rd_gau_input_tail()
        
        # deep copy it
        self.template_cmp = copy.deepcopy(self.template)
        
        return               

    # % dump/load template.    
    def dump(self):
        """
        read gjf file; dump template in json format.
        """
        self.rd_gau_input()
        # self.wrt_gau_input(flag="cmp", jobfile="template.gjf")
        tools.dump_data(self.files['template'], self.template_cmp)
        
        return   
        
         
    def load(self, filename = "template.json"):
        """
        load template.json
        """
        obj = tools.load_data(filename)
        
        return obj
                
# Main Program    
if __name__ == "__main__":    
    gau = gau_template()

    

    
    


