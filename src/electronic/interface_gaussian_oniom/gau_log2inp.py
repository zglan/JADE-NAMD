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
# split the oniom=onlyinputfiles log into a few new gjf files
#
# run g09 for onlyinputfiles
# then this script.
#
# note: this script can be used as
# 1. alone, to extract onlyinputfiles
# 2. combine with other script, automatic this process.
#
class gau_log2inp():
    """
    process gaussian oniom log. & generate gaussian input
    """
    oniom = {}
    fcontent = []
    template = {}
    pointer = {}
    params = {
        "BOHR2ANG": 0.52917720859E+00,
        "ANG2BOHR": 1.8897261328856432E+00
        }

    def __init__(self, config = {}):
        """ initialize several internal variable """
       
        # test case        
        self.files = {'template': 'template.json', 'interface': 'interface.json', \
                      'gaussian': 'gaussian.gjf', 'onlyinputfiles': 'onlyinputfiles.log'  \
                     }             

        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files']  
            
            # working directory & files >>>

        return
            
    def load(self):
        """
        load layer.json
        """
        filename = self.files['template']
        obj = tools.load_data(filename)
        self.template = copy.deepcopy(obj)
        self.template_cmp = copy.deepcopy(obj)        
        return obj

        
    def read_all(self):
        """
        read in oniom layer input
        """
        filename = self.files['onlyinputfiles']
        fp = open(filename, "r")
        while True:
            line = fp.readline()
            if line == "":
                break
            self.fcontent.append(line)
        fp.close()
        return

    def read_link0(self):
        """
        read in % section
        """
        link0 = {}
        link0['chk'] = "gaussian.chk"
        link0['mem'] = "1GB"
        link0['nproc'] = "2"
        link0['nproclinda'] = "1"

        for cur_line in self.fcontent:
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
        
    def read_info(self):
        """
        read about which atom belong to which model
        """
        pat = re.compile("Symbolic Z-matrix:")
        i = 0
        for line in self.fcontent:
            # print line
            i += 1
            m = pat.search(line)
            if m is not None:
                break
        if m is None:
            print ("cannot find layer info")
            exit(1)
        pat = re.compile("Charge =\s+(\d+) Multiplicity =\s+(\d+)\s+for\s+(\w+)\s+level calculation on\s+(\w+)\s+system")  
        j = 0
        for line in self.fcontent[i:]:
            m = pat.search(line)
            if m is None:
                break
            j += 1
        k = 0
        high_atoms_id = []
        low_atoms_id = []
        medium_atoms_id = []
        region = {}
        for line in self.fcontent[i+j:]:
            #print line
            if line.strip() == "":
                break
            record = line.split()
            layer = record[5]
            if layer.upper() == "H":
                high_atoms_id.append(k)
            elif layer.upper() == "M":
                medium_atoms_id.append(k)
            elif layer.upper() == "L":
                low_atoms_id.append(k)
            else:
                print ("no such layer id ???")
                exit(1)
            k += 1
                            
        region['high_atoms_id'] = high_atoms_id
        region['low_atoms_id'] = low_atoms_id
        region['medium_atoms_id'] = medium_atoms_id
        self.template['region'] = region
        return
        
    def find_layer(self):
        """
        suppose file content in self.fcontent
        """
        pat = re.compile("ONIOM: generating point\s+(\d+) -- (\w+) level on (\w+) system")
        i_line = 0
        oniom = {}
        for line in self.fcontent:
            i_line += 1
            m = pat.search(line)
            if m is not None:
                point = m.group(1)
                level = m.group(2)
                system = m.group(3)
                name = str(level) + "-" + str(system) 
                layer = {'point': point, 'level': level, 'system': system,
                         'name': name, 'i_line': i_line}  
                oniom[name] = layer
        self.oniom = oniom    
        return


    def __parse_routine(self, job):
        """
        '#' section define the methods etc.
        note: Gaussian support many-lines of routine keywords, so so
        """
        routine = {}; content = ""; i_line = 0
        # cut the routine string, note the first line is routine line #
        for line in job:
            i_line += 1
            if line.strip() == "":
                break
            content += line.strip() + " "
        if i_line < 1:
            print "cannot find gaussian input routine '#' line"
        pat = re.compile("Test", re.IGNORECASE)
        m = pat.search(content)
        if m is not None:
            content = re.sub(pat, "force", content)
        else:
            content += " force"
        self.template["routine"] = {
            'content': content
            }

        self.pointer['i_line'] = i_line

        return

    def __parse_title(self, job):
        title = "" 
        i_line = self.pointer['i_line']
        t = 0
        # search title line, may be more than one line
        # find next blank-line
        for line in job[i_line:]:
            t += 1
            i_find_blank = line.strip()==""
            if i_find_blank is True:
                break
            title += line
        self.template['title'] = title
        self.pointer['i_line'] = i_line + t

        return

    def __parse_molspec(self, job):
        """
        mol. spec.
        """
        # find the blank line after '#' column
        i_line = self.pointer['i_line']
        # now we reach charge/spin section.
        cur_line = job[i_line]
        cs = cur_line.replace(","," ").split()
        charge = cs[0]; spin = cs[1]
        # finally, add 1 for the geometric line
        i_line += 1
        # now, for molecular coord. & related info. [cart. coord. only].
        i_atom = 0
        mol = {}
        atoms = []
        max_name_length = 0
        for line in job[i_line:]:
            if line.strip() == "":
                break
            i_atom += 1
            #parse each line ..
            record = self.__parse_gjf_cart(line)
            record['i_atom'] = i_atom
            #print record['type_name']
            # check max length of the name line, useful for format output.
            if max_name_length < len(record['type_name']):
                max_name_length = len(record['type_name'])
            atoms.append(record)
        # summerize the info.            
        mol['atoms'] = atoms
        mol['n_atom'] = i_atom
        mol['max_name_length'] = max_name_length
        
        # backup it 
        self.template['mol'] = mol
        # spin&charge
        self.template['charge'] = charge
        self.template['spin'] = spin
        self.pointer['i_line'] = i_line + i_atom     
       
        return

       
    def __parse_gjf_cart(self, line):
        """
        check gjf coord line, and return records
        """
        record = line.split()
        # first col is atom-name ff-type etc.
        pat = re.compile("(^[a-zA-Z]+)-(\S+)\s*")
        m = pat.search(record[0])
        atom_name = m.group(1)
        ff_type = m.group(2)
        # coordinates cart. x y z
        coord = [float(record[1]), float(record[2]), float(record[3])]
        # other info.
        other = " ".join(record[4:])
        # summerized
        mylist = {
            'name': atom_name, 'ff_type': ff_type, 'coord': coord,
            'other': other, 'type_name': record[0], 'content': line 
            }
        return mylist

    def __parse_connect(self, job):
        """
        connection info, a must for oniom
        """
        i_line = self.pointer['i_line']
        it = 0
        connect = ""
        for line in job[i_line+1:]:
            it += 1
            if line.strip() == "":
                break
            connect += line
        self.template['connect'] = connect
        self.pointer['i_line'] = i_line + it
        return

    def __parse_tail(self, job):
        """
        read other info
        """
        i_line = self.pointer['i_line']
        other = job[i_line:]
        self.template['tail'] = "".join(other)

        return


    def parse_job(self, job):
        """
        parse one layer for input
        """
        self.__parse_routine(job)
        self.__parse_title(job)
        self.__parse_molspec(job)
        self.__parse_connect(job)
        self.__parse_tail(job)
        
        return
    
    def patch_highmodel(self):
        """
        detail routine for high model
        """
        # suppose: the model chemistry for high layer is here
        # such as HF/6-31G*
        # search a word contain '/' char.        
        content = self.template['routine']['content']
        # first store iop info, which may be confilict with theory/basis string
        pat = re.compile("IOP\(.*?\)", re.IGNORECASE)
        m = pat.search(content)
        iop = " "
        if m is not None:
            iop += m.group()
        else:
            iop = " "
        x_content = re.sub(pat, "", content, count=10)
        #
        # then search theory/basis
        pat = re.compile('(\w+)\/(\S+)\s+')
        m = pat.search(x_content)
        if m is None:
            print ("routine line,such as B3LYP/6-31G*??")
            exit(1)
        theory = m.group(1)
        basis = m.group(2)
        self.template["routine"] = {
            'content': content, 
            'theory': theory, 'basis': basis,
            }
        return
    
    def read_layer(self):
        """
        read in job input
        ONIOM: generating point  3 -- low level on real system.
        """
        oniom = self.oniom
        
        for name in oniom.keys():
            self.template = {}
            layer = oniom[name]
            i_line = layer['i_line']
            # so eat up several line and continue to --- line
            i_jump = 0
            for line in self.fcontent[i_line:]:
                i_jump += 1
                if line.count("-"*20) > 0:
                    break                
            content = self.fcontent[i_line + i_jump:]
            job = []
            for line in content:
                if line.count("-"*20) > 0:
                    break
                job.append(line)
            
            layer['job'] = job
            self.parse_job(job)
            self.read_link0()
            self.read_info()
            if name == "high-model":
                self.patch_highmodel()
            layer['template'] = self.template
            #print self.template

        return
       
    def dump_layer(self):
        """
        write down oniom input for each layer
        require additional info.
        """
        oniom = self.oniom
        for name in oniom.keys():
            layer = oniom[name]
            fname = layer['name'] + "-check.gjf"
            job = layer['job']
            fp = open(fname, "w")
            for line in job:
                print >>fp, "%s" % line,
            fp.close()
        tools.dump_data('layer.json', self.oniom) 
        return    
                

    def layer(self):
        """
        read in onlyinputfiles
        """
        self.read_all()
        self.find_layer()
        self.read_layer()
        self.dump_layer()
        return        
 

# Main Program    
if __name__ == "__main__":
    parser = gau_log2inp()
    parser.layer()
    

    


