#! /usr/bin/env python

import os

class elements():   
    table = {}
    def __init__(self):
    
        self.read()
        
        return
        
    def read(self):
        """ read in periodic table """
        script_dir = os.path.split(os.path.realpath(__file__))[0]
        fp = open(script_dir + "/elements.dat", "r")
        line = fp.readline()
        line = fp.readline()
        n_atom = int(line.split()[0])
        self.table['number'] = n_atom
        self.table['elements'] = []
        # read in p table
        line = fp.readline()
        for i in xrange(n_atom):
            line = fp.readline()
            #atom-label; atom-std-type; atom-eng-type; charge; mass(a.u.)
            record = line.split()
            atom_label = record[0]
            atom_type  = record[1]
            atom_eng_type = record[2]
            charge = float(record[3])
            mass = float(record[4])
            element = {'atom_label': atom_label, 'atom_type': atom_type, \
                       'atom_eng_type': atom_eng_type, 'atom_number': charge, \
                       'mass': mass}
            self.table['elements'].append(element)
        return

    def number2label(self, atom_number = 1):
        """
        provide an atom number, return an atom label
        """
        atom_label = ""
        for emt in self.table['elements']:
            if emt['atom_number'] == atom_number:
                atom_label = emt['atom_label']
                break
        if atom_label == "":
            print "NO such element type in the pd table"
            exit()
        return atom_label   


        

if __name__ == "__main__":
    pd = elements()
    print pd.number2label(3)
    

        