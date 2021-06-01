# python
import copy
import os
import re
import sys

sys.path.append("../tools/")
import tools


class qchem_log_parser():
    """
    parse qchem log file
    """
    def __init__(self, config={}):
        """ init """

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
        self.files["mo"] = self.directory['work'] + "/" + files['qchem_log']

        self.qm_interface = tools.load_data(self.files["interface"])
        self.n_atom = self.qm_interface['parm']['n_atom']
        self.n_state = self.qm_interface['parm']['n_state']
        self.i_state = self.qm_interface['parm']['i_state']
        self.geom = self.qm_interface['mol']
        self.atoms = self.geom['atoms']

    def collect_qm(self):
        """
        wrt down in one file
        """
        fileout3 = open('qm_results.dat', 'w')

        fileout3.write('     ' + str(self.n_atom) + '\n')
        fileout3.write(' The coordinates' + '\n')
        for i in range(self.n_atom):
            record = self.atoms[i]
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

        logfile = self.files['mo']
        file_in = open(logfile, "r")
        file_out = open("qm_energy.dat", "w")

        file_out.write(' Energy of electronic states' + '\n')


        line = "NOT EMPTY LINE"


#find ground state energy
        pattern = re.compile("Convergence criterion met")

        while line != "":
            line = file_in.readline()
            m = pattern.search(line)
            if m is not None:
                record = line.split()
                energy = float(record[1])
                file_out.write('' + str(energy) + '   ' + '\n')

                break

#find excited state energy

        pattern = re.compile("Total energy for state")

        for i_state in range(self.n_state -1):
            while line != "":
                line = file_in.readline()
                m = pattern.search(line)
                if m is not None:
                    record = line.split()
                    energy = float(record[-2])
                    file_out.write('' + str(energy) + '   ' + '\n')

                    break

        file_in.close()
        file_out.close()

        return

    def get_gradient(self):
        """ read gradient and punch out """

        gradient = []
        n_row = self.n_atom / 6
        n_rem = self.n_atom % 6

        for i_state in range(self.n_state):
           gradient.append([])
          
           for i_atom in range(self.n_atom):
              gradient[i_state].append([])

              gradient[i_state][i_atom].append(0.0)
              gradient[i_state][i_atom].append(0.0)
              gradient[i_state][i_atom].append(0.0)

        logfile = self.files['mo']

###find ground state gradient
        file_in = open(logfile, "r")

        pattern = re.compile("Gradient of SCF Energy")

        line = "NOT EMPTY LINE"
        while line != "":
            line = file_in.readline()
            m = pattern.search(line)
            if m is not None:
                break


        if line != "":

           for i_row in range(n_row):

              line = file_in.readline()

              for i_dim in range(3):
                  line = file_in.readline()

                  record = line.split()

                  for i in range(6):

                      current_atom = i_row*6+i

                      gradient[0][current_atom][i_dim] = float(record[i+1])

           if n_rem > 0:

              line = file_in.readline()

              for i_dim in range(3):
                  line = file_in.readline()

                  record = line.split()

                  for i in range(n_rem):

                      current_atom = n_row*6+i

                      gradient[0][current_atom][i_dim] = float(record[i+1])


        file_in.close()

###find excited state gradient

        file_in = open(logfile, "r")

        pattern = re.compile("State Energy")
        
        line = "NOT EMPTY LINE"

        while line != "":

            while line != "":
                line = file_in.readline()
                m = pattern.search(line)
                if m is not None:
                   record = line.split()

                   current_state = int(record[1])

                   line = file_in.readline()

                   for i_row in range(n_row):

                      line = file_in.readline()

                      for i_dim in range(3):

                          line = file_in.readline()

                          record = line.split()

                          for i in range(6):

                              current_atom = i_row*6+i

                              gradient[current_state][current_atom][i_dim] = float(record[i+1])

                   if n_rem > 0:

                      line = file_in.readline()

                      for i_dim in range(3):
                          line = file_in.readline()

                          record = line.split()

                          for i in range(n_rem):

                              current_atom = n_row*6+i

                              gradient[current_state][current_atom][i_dim] = float(record[i+1])


                   break

        file_in.close()

        file_out = open("qm_gradient.dat", "w")

        file_out.write(' Gradient of electronic states' + '\n')

        for i_state in range(self.n_state):

            file_out.write('State:    ' + str(i_state +1) + '\n')

            for i_atom in range(self.n_atom):
            
                file_out.write('' + str(gradient[i_state][i_atom][0]) + '   ' + \
                               str(gradient[i_state][i_atom][1]) + '   ' + str(gradient[i_state][i_atom][2]) + '  \n')


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

        file_in = open(logfile, "r")


        line = "NOT EMPTY LINE"
        while line != "":

            pattern = re.compile("between states")
            while line != "":
                line = file_in.readline()
                m = pattern.search(line)
                if m is not None:
                    i = int(line.split()[2])
                    j = int(line.split()[4])
                    break

            pattern = re.compile("with ETF")

            while line != "":
                line = file_in.readline()
                m = pattern.search(line)
                if m is not None:

                  line = file_in.readline()
                  line = file_in.readline()

                  for i_atom in range(self.n_atom):

                      line = file_in.readline()
                      record = line.split()

                      nac[i][j][i_atom][0] = -float(record[1])
                      nac[i][j][i_atom][1] = -float(record[2])
                      nac[i][j][i_atom][2] = -float(record[3])

                      nac[j][i][i_atom][0] = -nac[i][j][i_atom][0]
                      nac[j][i][i_atom][1] = -nac[i][j][i_atom][1]
                      nac[j][i][i_atom][2] = -nac[i][j][i_atom][2]

                  break

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

    # -------------------------------------------------------------------------
    #   %%% Read all other important information of QM output
    #   qchem.log file is required.
    #   For example: Transition dipole moment and so on
    # ---------------------------------------------------------------------------
    def get_other(self):
        """
        Write other important information in QM output 
        """
        start = re.compile("STATE-TO-STATE TRANSITION MOMENTS")
        end = re.compile("END OF TRANSITION MOMEMT CALCULATION")

        logfile = self.files['mo']

        fileout = open('qm_other.dat', 'w')

        filein = open(logfile, "r")

        line = "NOT EMPTY LINE"


        flag = 0

        while line != "":

            line = filein.readline()

            m = start.search(line)

            if m is not None:

               fileout.write(line)

               while line != "":

                  line = filein.readline()
                  n = end.search(line)

                  if n is not None:

                     fileout.write(line)

                     flag = 1
                     break

                  fileout.write(line)

            if (flag==1):

               break

        fileout.write(
            '------------------------------------------------------------- \n')

        filein.close()
        fileout.close()

        return


### main program
if __name__ == "__main__":
    ao = qchem_log_parser()

    ao.get_gradient()
    ao.get_nac()
# ao.get_other()
