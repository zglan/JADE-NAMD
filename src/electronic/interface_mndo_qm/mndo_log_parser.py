# python
import os
import sys
import re
import copy
import math
from operator import itemgetter
import shutil

sys.path.append("../tools/")
import tools


class mndo_log_parser():
    """
    parse mndo log file
    """
    def __init__(self, config={}):
        """ init """

        self.files = {
            'interface': 'interface.json',
            'mo': 'mndo.log',
            'fort': 'fort.15'
        }

        if config != {}:
            root_dir = config['root']
            dirs = config['dirs']
            files = config['files']

            # working directory & files >>>
            self.directory = {}
            self.directory['root'] = root_dir
            self.directory['home'] = root_dir + "/" + dirs['home']
            self.directory[
                'work'] = self.directory['home'] + "/" + dirs['work']

            self.files = {}
            self.files["interface"] = self.directory['work'] + "/" + files[
                'interface']
            self.files["mo"] = self.directory['work'] + "/" + files['mndo_log']
            self.files[
                "fort"] = self.directory['work'] + "/" + files['mndo_fort']

        filename = self.files['interface']
        obj = tools.load_data(filename)
        self.interface = copy.deepcopy(obj)

        self.n_state = int(self.interface['parm']['n_state'])
        self.n_atom = int(self.interface['parm']['n_atom'])

        return

# -------------------------------------------------------------------------

    def collect_qm(self):
        """
        wrt down in one file
        """
        fileout3 = open('qm_results.dat', 'w')

        qm_interface = tools.load_data("interface.json")
        geom = qm_interface['mol']
        atoms = geom['atoms']

        fileout3.write('     ' + str(self.n_atom) + '\n')
        fileout3.write(' The coordinates' + '\n')
        for i in range(self.n_atom):
            record = atoms[i]
            atomname = record['name']
            coord = record['coord']
            fileout3.write(
                str(atomname) + '   ' + str(coord[0]) + '   ' + str(coord[1]) +
                '   ' + str(coord[2]) + '\n')

        filein4 = open('qm_energy.dat', 'r')
        fileout3.write(filein4.read())
        filein4.close()

        filein4 = open('qm_gradient.dat', 'r')
        fileout3.write(filein4.read())
        filein4.close()

        sourceFile = 'qm_nac.dat'
        if os.path.isfile(sourceFile):
            filein4 = open('qm_nac.dat', 'r')
            fileout3.write(filein4.read())
            filein4.close()
        else:
            for i_state in range(self.n_state):
                for j_state in range(self.n_state):
                    fileout3.write('S' + str(i_state) + '    S' +
                                   str(j_state) + '   0.00000   \n')

        fileout3.close()

        return

# ---------------------------------------------------------------------------

#   %%% Read the energy
#   qm_energy.dat
#   Attention:

    def get_energy(self):
        """ read energy and punch out """
        fortfile = self.files['fort']
        file_in = open(fortfile, "r")
        file_out = open("qm_energy.dat", "w")

        file_out.write(' Energy of electronic states' + '\n')

        pattern = re.compile(
            " STATES, ENERGIES, CARTESIAN AND INTERNAL GRADIENT NORMS")

        KCANGTOEV = 0.0433641
        TOEV = 27.2113961
        ANSTOBOHR = 1.8897261328856432

        line = "NOT EMPTY LINE"
        while line != "":
            line = file_in.readline()
            m = pattern.search(line)
            if m is not None:
                break

        for i_line in range(self.n_state):

            line = file_in.readline()

            record = line.split()

            energy = float(record[1]) * KCANGTOEV / TOEV

            file_out.write('' + str(energy) + '   ' + '\n')

        file_in.close()
        file_out.close()

        return

    def get_gradient(self):
        """ read gradient and punch out """
        logfile = self.files['mo']
        fortfile = self.files['fort']
        file_in = open(fortfile, "r")
        file_out = open("qm_gradient.dat", "w")

        file_out.write(' Gradient of electronic states' + '\n')

        pattern = re.compile("CARTESIAN GRADIENT FOR STATE")

        KCANGTOEV = 0.0433641
        TOEV = 27.2113961
        ANSTOBOHR = 1.8897261328856432

        line = "NOT EMPTY LINE"
        for i_state in range(self.n_state):
            while line != "":
                line = file_in.readline()
                m = pattern.search(line)
                if m is not None:
                    break

            file_out.write(' State:           ' + str(i_state +1) + '\n')

            for i_atom in range(self.n_atom):
                line = file_in.readline()

                record = line.split()

                grad_x = float(record[2]) * KCANGTOEV / (TOEV * ANSTOBOHR)
                grad_y = float(record[3]) * KCANGTOEV / (TOEV * ANSTOBOHR)
                grad_z = float(record[4]) * KCANGTOEV / (TOEV * ANSTOBOHR)

                file_out.write(''+str( grad_x )+'   '+ \
                                str( grad_y )+'   '+str( grad_z )+'  \n')
        file_in.close()
        file_out.close()

        return

# -------------------------------------------------------------------------
#   %%% Read the nac
#   qm_nac.dat
#   Attention:
# ---------------------------------------------------------------------------

    def get_nac(self):

        n_dime = 3

        nac = []
        for i in range(self.n_state):
            nac.append([])
            for j in range(self.n_state):
                nac[i].append([])
                for k in range(self.n_atom):
                    nac[i][j].append([])
                    for l in range(n_dime):
                        nac[i][j][k].append(0.0)
        """ read nac and punch out """
        logfile = self.files['mo']
        fortfile = self.files['fort']

        file_in = open(fortfile, "r")

        pattern = re.compile(
            " CARTESIAN INTERSTATE COUPLING GRADIENT FOR STATES")

        KCANGTOEV = 0.0433641
        TOEV = 27.2113961
        ANSTOBOHR = 1.8897261328856432

        line = "NOT EMPTY LINE"
        while line != "":
            while line != "":
                line = file_in.readline()
                m = pattern.search(line)
                if m is not None:
                    i = int(line.split()[-2]) - 1
                    j = int(line.split()[-1]) - 1
                    break

            if (i >= self.n_state or j >= self.n_state):
                continue

            k = 0
            while line != "":
                line = file_in.readline()
                if line.strip() == "":
                    break

                record = line.split()

                nac[i][j][k][0] = -float(record[2]) / ANSTOBOHR
                nac[i][j][k][1] = -float(record[3]) / ANSTOBOHR
                nac[i][j][k][2] = -float(record[4]) / ANSTOBOHR

                nac[j][i][k][0] = -nac[i][j][k][0]
                nac[j][i][k][1] = -nac[i][j][k][1]
                nac[j][i][k][2] = -nac[i][j][k][2]

                k = k + 1

        file_in.close()

        file_out = open("qm_nac.dat", "w")

        file_out.write('Nonadiabatic couplings' + '\n')
        for i in range(self.n_state):
            for j in range(self.n_state):
                file_out.write(' State:           ' + str(i + 1) + '        ' +
                               str(j + 1) + '\n')
                for k in range(self.n_atom):
                    file_out.write(
                        str(nac[i][j][k][0]) + '   ' + str(nac[i][j][k][1]) +
                        '    ' + str(nac[i][j][k][2]) + '  \n')

        file_out.close()

        return

### main program
if __name__ == "__main__":
    ao = mndo_log_parser()
    ao.get_gradient()
    ao.get_nac()
