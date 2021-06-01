# python
import copy
import os
import re
import sys

sys.path.append("../tools/")
import tools


class bagel_log_parser():
    """
    parse bagel log file
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
        self.files[
            "mo"] = self.directory['work'] + "/" + files['bagel_log']


        self.load()

        return

    # -------------------------------------------------------------------------

    def load(self):
        """
        load interface.json
        """
        self.qm_interface = tools.load_data(self.files["interface"])
        self.n_atom = self.qm_interface['parm']['n_atom']
        self.n_state = self.qm_interface['parm']['n_state']
        self.i_state = self.qm_interface['parm']['i_state']
        self.geom = self.qm_interface['mol']

    def collect_qm(self):
        """
        wrt down in one file
        """
        fileout3 = open('qm_results.dat', 'w')

        atoms = self.geom['atoms']

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


        logfile = 'ENERGY.out'
        file_in = open(logfile, "r")
        file_out = open("qm_energy.dat", "w")

        file_out.write(' Energy of electronic states' + '\n')

        for i_state in range(self.n_state):
            line = file_in.readline()
            record =  line.split()
            energy = float(record[0])
            file_out.write('' + str(energy) + '   ' + '\n')

        file_in.close()
        file_out.close()
           

        return

    def get_gradient(self):
        """ read gradient and punch out """



        gradient = []
        for i_state in range(self.n_state):
           gradient.append([])
          
           for i_atom in range(self.n_atom):
              gradient[i_state].append([])

              gradient[i_state][i_atom].append(0.0)
              gradient[i_state][i_atom].append(0.0)
              gradient[i_state][i_atom].append(0.0)


        current_state = self.i_state

        for i_state in range(self.n_state):
        
            logfile = 'FORCE_' + str(i_state) + '.out'

            if os.path.exists(logfile):

               file_in = open(logfile, "r")
               file_in.readline()

               for i_atom in range(self.n_atom):

                  record = file_in.readline().split()

                  gradient[i_state][i_atom][0] = float(record[1])
                  gradient[i_state][i_atom][1] = float(record[2])
                  gradient[i_state][i_atom][2] = float(record[3])

               file_in.close
               

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

        for i in range(self.n_state):
            for j in range(self.n_state):

                logfile = 'NACME_' + str(i) + '_' + str(j) + '.out'

                if os.path.exists(logfile):
        
                   file_in = open(logfile, "r")
                   file_in.readline()

                   for i_atom in range(self.n_atom):

                      record = file_in.readline().split()

                      nac[i][j][i_atom][0] = -float(record[1])
                      nac[i][j][i_atom][1] = -float(record[2])
                      nac[i][j][i_atom][2] = -float(record[3])


                      nac[j][i][i_atom][0] = -nac[i][j][i_atom][0]
                      nac[j][i][i_atom][1] = -nac[i][j][i_atom][1]
                      nac[j][i][i_atom][2] = -nac[i][j][i_atom][2]


                   file_in.close

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
    ao = bagel_log_parser()
    ao.get_gradient()
    ao.get_nac()
