# python

import sys
import re
import copy
sys.path.append("../tools/")
import tools

# gaussian input process for templating, for the ONIOM feature.
# in contrast to QM model of gaussian template

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
#   == spin: intx
#   == charge: intx
#   == title ""
#   == tail "" connectivity & others
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
        #self.dump()     

        return
    
    # ------------------------------------------------------------------
    #
    # Section 0: convert necessary data from gjf template to json format.    
    # dump_template() & load_template is the main called subroutine
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
        '#' section define the methods etc.
        #p force ONIOM(b3lyp/6-31g(d,p) td(singlet,nstates=3,root=1):pm6)=(EmbedCharge,inputfiles) nosymm geom=connectivity pop=full
        note: Gaussian support many-lines of routine keywords, so
        """
        routine = {}
        content = ""
        i_line = 0
        # cut the routine string
        i_flag = -1
        for line in self.pointer['content']:
            i_line += 1
            i_find_sharp = re.search("\s*#", line)
            # print line, i_find_sharp
            i_find_blank = line.strip()==""
            if i_find_sharp is not None and i_flag == -1:
                content += line.strip() + " "
                i_flag = 1
                continue
            if i_find_blank is True:
                break
            else:
                if i_flag == 1:
                    content += line.strip() + " "
        if i_flag == -1:
            print "cannot find gaussian input routine '#' line"

        # find if connectivity is there
        i_connect = False
        pat = re.compile("connectivity", re.IGNORECASE)
        m = pat.search(content)
        if m is not None:
            i_connect = True
            print ("internal coordinate connectivity is present...")
        #
        # ONIOM(b3lyp/6-31g(d,p) td(singlet,nstates=3,root=1):pm6)
        #
        pat = re.compile("ONIOM(.*)", re.IGNORECASE)
        m = pat.search(content)
        if m is None:
            print ("e...no ONIOM keyword found??? check the GAUSSIAN template")
            exit(1)
        oniom = m.group()
        mystr = m.group(1)
        record = mystr.split()
        # suppose: the first one in the record is model chemistry for high layer,
        # such as HF/6-31G*
        # search a word contain '/' char.        
        pat = re.compile('(\w+)\/(\S+)')
        m = pat.search(record[0])
        if m is None:
            print ("routine line,such as B3LYP/6-31G*??")
            exit(1)
        theory = m.group(1)
        basis = m.group(2)
        self.template["routine"] = {
            'content': content, 'model': oniom,
            'theory': theory, 'basis': basis,
            'i_connect': i_connect
            }

        self.pointer['i_line'] = i_line
        return

    def __rd_gau_input_title(self):
        """ read in title info """
        title = ""
        line_each = self.pointer['content']
        i_line = self.pointer['i_line']
        t = 0
        # search title line, may be more than one line
        # find next blank-line
        for line in line_each[i_line:-1]:
            t += 1
            i_find_blank = line.strip()==""
            if i_find_blank is True:
                break
            title += line
        self.template['title'] = title
        self.pointer['i_line'] = i_line + t
        return
        
                
    def __rd_gau_input_mol(self):
        """
        Molecule specification: Specify molecular system to be studied
        (blank line terminated).
        charge spin & coordinates.
        for oniom feature, QM and MM only
        """
        # find the blank line after '#' colum
        line_each = self.pointer['content']
        n_line = len(line_each)
        i_line = self.pointer['i_line']
   
        # now we reach charge/spin section.
        cur_line = line_each[i_line]
        cs = cur_line.replace(","," ").split()
        n_cs = len(cs)
        charge = [int(cs[i]) for i in xrange(0, n_cs, 2)]
        spin = [int(cs[i]) for i in xrange(1, n_cs, 2)]
        # finally, add 1 to the geometric line
        i_line += 1
        
        # now, for molecular coord. & related info. [cart. coord. only].
        i_high = i_medium = i_low = 0
        i_atom = 0
        mol = {}
        atoms = []
        high_atoms = []
        low_atoms = []
        medium_atoms = []
        high_atoms_id = []
        low_atoms_id = []
        medium_atoms_id = []
        max_name_length = 0
        for line in line_each[i_line:-1]:
            if line.strip() == "":
                break
            i_atom += 1
            #parse each line ..
            record = self.__parse_gjf_frg(line)
            record['i_atom'] = i_atom
            # check max length of the name line, useful for format output.
            if max_name_length < len(record['type_name']):
                max_name_length = len(record['type_name'])
            # check layer
            if record['layer'] == "L":
                i_low += 1
                low_atoms.append(record)
                low_atoms_id.append(i_atom)
            elif record['layer'] == "M":
                i_medium += 1
                medium_atoms.append(record)
                medium_atoms_id.append(i_atom)
            else:
                i_high += 1
                high_atoms.append(record)
                high_atoms_id.append(i_atom)
            atoms.append(record)
        # summerize the layer info.            
        mol['atoms'] = atoms
        mol['high_atoms'] = high_atoms
        mol['low_atoms'] = low_atoms
        mol['medium_atoms'] = medium_atoms
        mol['high_atoms_id'] = high_atoms_id
        mol['low_atoms_id'] = low_atoms_id
        mol['medium_atoms_id'] = medium_atoms_id        
        n_atom = i_high + i_medium + i_low # eq. i_atom
        mol['n_high'] = i_high
        mol['n_medium'] = i_medium
        mol['n_low'] = i_low
        mol['n_atom'] = n_atom
        mol['max_name_length'] = max_name_length        
        # backup it 
        self.template['mol'] = mol
        # spin&charge
        self.template['charge'] = charge
        self.template['spin'] = spin
        self.template['n_cs'] = n_cs
        self.pointer['i_line'] = i_line + n_atom     

        return  
        
    def __parse_gjf_frg(self, line):
        """
            check gjf fragment type 03 or 09 version, and return records
        """
        record = line.split()
        # first col is atom-name ff-type etc.
        pat = re.compile("(^[a-zA-Z]+)-(\S+)\s*")
        m = pat.search(record[0])
        atom_name = m.group(1)
        ff_type = m.group(2)
        # fix or not, useless in dynamics script
        ifrozen = int(record[1])
        # coordinates cart. x y z
        coord = [float(record[2]), float(record[3]), float(record[4])]        
        # layer info.
        layer = record[5].upper()
        # other info.
        other = " ".join(record[6:])

        mylist = {
            'name': atom_name, 'ff_type': ff_type, 'coord': coord,
            'ifrozen': ifrozen, 'layer': layer, 'other': other,
            'type_name': record[0], 'content': line 
            }
        return mylist

    def __rd_gau_input_connect(self):
        """
        read geometric connectity, if geom=connectivity is required
        """
        line_each = self.pointer['content']
        i_line = self.pointer['i_line']
        # search connectivity line, usuallymore than one line
        # find next blank-line to end this section
        it = 1 # start from 1, since the i_line+0 is blank line
        connect = []
        for line in line_each[i_line+1:-1]:
            it += 1
            i_find_blank = line.strip()==""
            if i_find_blank is True:
                break
            connect.append(line.strip())
        self.template['connect'] = connect
        self.template['n_connect'] = it
        self.pointer['i_line'] = i_line + it
        #print connect
        return
        
    def __rd_gau_input_tail(self):
        """ 
        read template tail information 
        """
        # read in connectivity, if possible
        i_connect = self.template['routine']['i_connect']
        if i_connect is True:
            print ("read geometric connectivity is required, reading...")
            self.__rd_gau_input_connect()          
        #
        # extra info. such as external basis set, mo-guess, pcm parameter etc.
        line_each = self.pointer['content']
        i_line = self.pointer['i_line'] 
        tlist = []
        tail = ""
        for line in line_each[i_line:-1]:
            tlist.append(line)
        for s in reversed(tlist):
            if s.strip() == "":
                tlist.pop()
            else:
                break
        for s in tlist:
            tail = tail + s
        self.template['tail'] = tail        
        self.pointer['i_line'] = 0
        
        return

    def __rd_all(self):
        """ open file and read all """
        fp = open(self.files["gaussian"], 'r')
        self.pointer['content'] = fp.readlines()
        self.template['fcontent'] = self.pointer['content']
        fp.close()
        
        return
    
    def rd_gau_input(self):
        """ read template file """
        # open adn read all
        self.__rd_all()
       
        # read process
        # link0 section : %
        self.__rd_gau_input_link0()

        # routine section: #
        self.__rd_gau_input_routine()

        # read title section
        self.__rd_gau_input_title()
        
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
    gau.rd_gau_input()
    gau.dump()
    
    

    
    


