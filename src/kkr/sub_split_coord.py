#!/usr/bin/env python


class split_coord():
    def __init__(self):
        self.dim = {}
        self.filename = 'input.xyz'
        self.model = []

    def __rd_xyz_nmol(self):
        """ read how many mol in the xyz file"""
        filename = self.filename

        fpin = open(filename, "r")
        nmol = 0
        # read number of atom
        line = fpin.readline()
        while line.strip() != "":
            natom = int(line.split()[0])
            line = fpin.readline()
            # read a mol
            for i in range(natom):
                line = fpin.readline()
            nmol = nmol + 1

            line = fpin.readline()
        fpin.close()

        self.dim['n_mol'] = nmol

        return

    def read_xyz(self):
        """ read in xyz format in ang """
        self.__rd_xyz_nmol()
        n_mol = self.dim['n_mol']

        filename = self.filename
        fpin = open(filename, "r")

        model = []
        for i in range(n_mol):
            # number of atom, 
            line = fpin.readline()
            natom = int(line)
            line = fpin.readline()[0:-1]
            molinfo = {'n_atom': natom, 'title': line}

            atom = []
            for j in range(natom):
                line = fpin.readline()
                rec = line.split()
                atomname, x, y, z = rec[0:4]
                record = {'name': atomname, 'coord': [float(x), float(y), float(z)]}
                atom.append(record)
            mol = {'info': molinfo, 'atoms': atom}
            model.append(mol)
        fpin.close()

        self.model = model
        return

    def write_coord(self):
        """ write xyz in angstrom unit """
        self.read_xyz()
        n_mol = self.dim['n_mol']
        for id in range(n_mol):
            filename = "all_sample.xyz_" + str(id + 1)
            fp = open(filename, "w")
            mol = self.model[id]
            molinfo = mol['info']
            atoms = mol['atoms']
            n_atom = molinfo['n_atom']
            title = molinfo['title']
            print("%d" % (n_atom), file=fp)
            print("%s" % title, file=fp)
            for rec in atoms:
                coord = rec['coord']
                atom_name = rec['name']
                print("%s%15.8f%15.8f%15.8f" % (atom_name,
                                                coord[0],
                                                coord[1],
                                                coord[2]), file=fp)
            fp.close()

        return


if __name__ == '__main__':
    jobs = split_coord()
    jobs.write_coord()


def make():
    jobs = split_coord()
    jobs.write_coord()
