#! /usr/bin/env python
import os
import math
import re
import numpy as np

class activeset():
    def __init__(self):
        """ """
        self.vars = {}

        return

    def read_xyz(self, filename = "xyz"):
        """ current coord. & frozen dimension """
        fp = open(filename, "r")
        # number of site
        line = fp.readline().strip()
        n_site = int(line)
        # title
        line = fp.readline()
        coord = []
        name = []
        frozen = []
        # read coord
        for i in xrange(n_site):
            line = fp.readline()
            record = line.split()
            n_col = len(record)
            c = np.array([float(f) for f in record[1:4]])
            name.append(record[0])
            coord.append(c)
            ndx = [-1, -1, -1]
            frozen.append(ndx)
            self.vars['xyz'] = \
            {'name': name, 'coord': coord, 'frozen': frozen, 'n_site': n_site}

        return

    def setup_gjf(self, filename = "oniom.gjf"):
        """ read in gjf file with oniom feature """
        fp = open(filename, "r")
        head = ""
        tail = ""
        body = []
        i_blank = 0
        while True:
            line = fp.readline()
            head += line
            if line.strip() == "":
                i_blank += 1
            if i_blank == 2:
                break
            if line == "":
                break

        # read in spin etc.
        line = fp.readline()
        head += line
        while True:
            line = fp.readline()
            if line.strip() == "":
                break
            record = line.split()
            name = record[0]
            ndx = int(record[1])
            other = " ".join(record[2:])
            atom = {'name': name, 'ndx': ndx, 'other': other}
            body.append(atom)
        # read in other
        while True:
            line = fp.readline()
            tail += line
            if line == "":
                break
        fp.close()
        
        fp = open("active-"+filename, "w")
        print >>fp, "%s" % head,
        # setup active
        for i_site in self.vars['activelist']:
            body[i_site]['ndx'] = -1
        # body
        for atom in body:
            print >>fp, "%30s%5d\t%s" % (atom['name'], atom['ndx'], atom['other'])
        print >>fp, ""
        print >>fp, "%s" % tail
        fp.close()
        
        return

    def read_active(self, filename = "region"):
        """ read in active atom id, start from zero """
        fp = open(filename, "r")
        pat = re.compile("set\s+active\s+\{([\d\s]+)\}")
        line = fp.readline()
        m = pat.search(line)
        if m is None:
            print "Fail to find active region."
            exit(1)
        region = m.group(1)
        activelist = region.split()
        self.vars['activelist'] = [int(i_site) for i_site in activelist]
        return

    def setup(self):
        xyz = self.vars['xyz']
        frozen = xyz['frozen']
        activelist = self.vars['activelist']

        for i_site in activelist:
            ndx = [-1 for i in xrange(3)]
            frozen[i] = ndx
        self.vars['xyz']['frozen'] = frozen
        return

    def write_xyz(self, filename = "ref.xyz"):
        """
        write down ref coord.
        """
        xyz = self.vars['xyz']
        n_site = xyz['n_site']
        frozen = xyz['frozen']
        coord = xyz['coord']
        name = xyz['name']

        fp = open(filename, "w")
        print >>fp, "%10d" % n_site
        print >>fp, ""
        for i in xrange(n_site):
            print >>fp, "%5s%15.8f%15.8f%15.8f%5d%5d%5d" % \
            (name[i], coord[i][0], coord[i][1], coord[i][2], \
            frozen[i][0], frozen[i][1], frozen[i][2])
        fp.close()
        return


if __name__ == "__main__":
    a = activeset()
    a.read_xyz()
    a.read_active()
    a.setup()
    a.write_xyz()

    print "Hello World!!"
    a.setup_gjf(filename = "admp.gjf")
