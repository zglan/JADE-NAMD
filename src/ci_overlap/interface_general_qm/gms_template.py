
# python
import os
import sys
import re
import copy

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/../tools/")
import tools

# gamess input process for templating.


# % template
#   
#   ==
#   == $XXX
#       == namelist-vars
#       == namelist & namelist-x
#
#   ==
#   2014.3.28 du
#
#
class gms_template():
    """
    process gamess template,
    which is used to generate gamess input.
    """
    def __init__(self, config = {}):
        """ initialize several internal variable """
        # content of the template.
        self.template = {} 
 
        self.files = {'gamess': 'temp.inp', 'template': 'template.json'}
        
        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files']
            gms_file = root_dir + "/" + dirs['template'] + "/" + files['gms_template']
            tpl_file = root_dir + '/template.json'
            self.files = {'gamess': gms_file, 'template': tpl_file}          

        # load gjf & write json
        self.dump()     

        return
    
    # ------------------------------------------------------------------
    #
    # Section 0: convert necessary data from gms-inp template to json format.    
    # dump_template() & load_template is the main called subroutine
    #
    #-------------------------------------------------------------------

    def __remove_comment(self, filename = "temp.inp"):
        """ remove line content after ! """
        # remove comment
        comment = re.compile(r"^(.*)!(.*)$")
        
        text = []
        # 
        filename = self.files['gamess']
        fp = open(filename, "r")
        line = "not-empty-line"
        while line != "":
            line = fp.readline()
            
            m_comment = comment.search(line)            
            if m_comment is not None or line.strip() == "":
                continue
            else:
                text.append(line)
       
        return text

    def __namelist_content(self, text):
        """
        read in one namelist-section. pseudo.
        """       
        mydict = {}
        i_flag = 0
        for line in text:
            rec = line.split()
            if line[1] == "$" and i_flag == 0:
                name = rec[0][1:].upper()
                mydict[name] = line
                i_flag = 1
            elif i_flag == 1:
                mydict[name] += line
            else:
                print "no '$' line, ???"
                exit()
            if rec[-1].upper() == "$END":
                i_flag = 0
        
        return mydict


    def __namelist_parm(self, mystring):
        """ the parameter of each section """
        mylist = mystring.split()[1:-1]
        parm = {}
        for t in mylist:
            tt = t.split("=")
            parm[tt[0].upper()] = tt[1].upper()
                         
        return parm

    
    def __namelist_split(self, mydict):
        """
        split mydict in to pairwise parameters
        """
        # define vars
        template = {}
        # obtain parameters.
        for key in mydict:
            if key != "DATA":
                template["@"+key] = self.__namelist_parm(mydict[key])
                
        # data, the geometry parameters.
        data = mydict['DATA'].split('\n')
        title = data[1]
        symm = data[2].upper()
        content = mydict['DATA']
        i_start = 0 if symm == "C1" else 1
        dd = data[3+i_start:-2]
        # suppose molecular geometry is in the format (angstrom unit)
        # atom-name nuclear-charge coord-x coord-y coord-z
        mol = {'n_atom': len(dd), 'atoms': []}
        for d in dd:
            rec = d.split()
            atomname = rec[0]
            charge = float(rec[1])
            coord = [float(rec[2]), float(rec[3]), float(rec[4])]
            atom = {'name': atomname, 'charge': charge, 'coord': coord}
            mol['atoms'].append(atom)
        
        template['@DATA'] = {'title': title, 'symm': symm, 'mol': mol}

        template.update(mydict)

        self.template = template
        
        return

    # % dump/load template. 
    def dump(self):
        """
        read in gms template file.
        """
        text = self.__remove_comment()
        mydict = self.__namelist_content(text)
        self.__namelist_split(mydict)
        tools.dump_data(self.files['template'], self.template)
        return
         
    def load(self, filename = "template.json"):
        """
        load template.json
        """
        obj = tools.load_data(filename)
        
        return obj
                
# Main Program    
if __name__ == "__main__":    
    gms = gms_template()
    gms.dump()

    

    
    


