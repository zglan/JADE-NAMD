#! /usr/bin/env python

import os

class periodictable():
    def __init__(self):
        """
        common data
        """
        if 'SH_HOME' in os.environ:
            database_dir = os.environ.get('SH_HOME')
        else:
            print "SH_HOME DIRECTORY IS NOT EXIST ??? CHECK???"
            exit()
            
        print "DATABSE DIRECTORY: ", database_dir
        self.files = {}
        
        self.files['table'] = database_dir + "/database/elements.dat"
        self.table = {}
        

        # exec
        self.read_table()
        
        return

    def read_table(self):
        """ read in periodic table """
        elements = []
        
        filename = self.files['table']
        fp = open(filename, "r")
        # comments
        line = fp.readline()
        # number-of-atoms
        line = fp.readline()
        n_type = int(line)
        # comments
        line = fp.readline()
        for i in xrange(n_type):
            line = fp.readline()
            rec = line.split()
            atom = {'label': rec[0].lower(),
                    'std_name': rec[1], 'eng_name': rec[2],
                    'charge': int(rec[3]), 'mass': float(rec[4])}

            elements.append(atom)
            
        self.table = {'elements': elements, 'n_type': n_type}

        fp.close()

        return

    def get_charge(self, label = "H"):
        """
        return charge
        """
        charge = -1
        
        elements = self.table['elements']
        lower_name = label.lower()
        for atom in elements:
            if atom['label'] == lower_name:
                charge = atom['charge']
                break
        if charge < 0:
            print "cannot find this elements.. ???"
            exit()
            
        return charge
        
   
if __name__ == "__main__":
    pt = periodictable()
 
    charge = pt.get_charge(label = "N")
    print charge
