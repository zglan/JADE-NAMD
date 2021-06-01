#! /usr/bin/env python3
import os


class cut_coord():
    def __init__(self, filename, cutlist, cut_atom, state):
        self.filename = filename
        self.cutlist = cutlist
        self.cutatom = cut_atom
        self.state = state
        self.dim = {}
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

    def write_xyz(self):
        self.__rd_xyz_nmol()
        self.read_xyz()
        nmol = self.dim['n_mol']
        model = self.model

        """get the a_num after cut"""
        mol = model[0]
        molinfo = mol['info']
        atom = mol['atoms']
        natom = int(molinfo['n_atom'])
        n_atom_new = natom
        for i in range(natom):
            if i + 1 in self.cutlist or atom[i]['name'] in self.cutatom:
                n_atom_new = n_atom_new - 1

        """write the coord afercut  into a new file named filename_aftercut """
        for sta in range(self.state):
            savefile = self.filename + '_S' + str(sta)
            if os.path.isfile(savefile):
                os.remove(savefile)
            fp = open(savefile, 'a')

            par = sta + 1
            if sta == (self.state - 1):
                par = 0

            for i in range(nmol):
                if (i + 1) % self.state == par:
                    mol = model[i]
                    molinfo = mol['info']
                    atom = mol['atoms']
                    print(n_atom_new, file=fp)
                    print(molinfo['title'], file=fp)
                    natom = int(molinfo['n_atom'])
                    for i in range(natom):
                        if i + 1 in self.cutlist:
                            continue
                        name = atom[i]['name']
                        if name in self.cutatom:
                            continue
                        coord = atom[i]['coord']
                        print("%s%15.8f%15.8f%15.8f" % (name,
                                                        coord[0],
                                                        coord[1],
                                                        coord[2]), file=fp)
            fp.close()


def single_traj(filename, state):
    cut_list = []
    cut_atom = []
    jobs = cut_coord(filename, cut_list, cut_atom, state)
    jobs.write_xyz()


def many_traj(i_traj, filename, state):
    curr_dir = os.getcwd()
    work_path = './' + str(i_traj + 1)
    os.chdir(work_path)
    single_traj(filename, state)
    os.chdir(curr_dir)


def many_traj_test():
    filename = 'grad_time.out'
    state = int(input("how many states?\n"))
    n_traj = int(input("how many trajectories?\n"))
    for i_traj in range(n_traj):
        print (i_traj+1)
        many_traj(i_traj, filename, state)


if __name__ == '__main__':
    many_traj_test()
