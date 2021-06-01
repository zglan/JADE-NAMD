#!/usr/bin/env python


def distance_matrix(file_name, file_type):
    filein = open(file_name, 'r')
    lines = filein.readlines()
    filein.close()
    n_atom = len(lines) - 2

    n_dim = 3

    atom_name = []
    charge = []
    coord = []
    distance = []
    coulomb = []

    for i in range(n_atom):
        charge.append(0.0)
        atom_name.append(0.0)
        coord.append([])
        distance.append([])
        coulomb.append([])

        for j in range(n_atom):
            distance[i].append(0.0)
            coulomb[i].append(0.0)

        for i_dim in range(n_dim):
            coord[i].append(0.0)

    filein = open(file_name, 'r')
    file_all = filein.read()
    filein.close()

    file_text = file_all.split('\n')
    for i in range(n_atom):
        atom_name[i] = (file_text[i + 2].split()[0]).lower()
        coord[i][0] = float(file_text[i + 2].split()[1]) / 0.529177
        coord[i][1] = float(file_text[i + 2].split()[2]) / 0.529177
        coord[i][2] = float(file_text[i + 2].split()[3]) / 0.529177

    charge_list = {'h': 1, 'he': 2, 'li': 3, 'be': 4, 'b': 5, 'c': 6, 'n': 7, 'o': 8, 'f': 9, 'ne': 10, 'na': 11,
                   'mg': 12, 'al': 13, 'si': 14, 'p': 15, 's': 16, 'cl': 17, 'ar': 18, 'k': 19, 'ca': 20}

    for i in range(n_atom):
        charge[i] = charge_list[atom_name[i]]

    for i in range(n_atom):
        for j in range(n_atom):
            for k in range(n_dim):
                distance[i][j] = distance[i][j] + (coord[i][k] - coord[j][k]) ** 2
            distance[i][j] = distance[i][j] ** 0.5

            if i == j:
                coulomb[i][j] = 0.5 * charge[i] ** 2.4
            else:
                coulomb[i][j] = charge[i] * charge[j] / distance[i][j]

    fileout1 = open('standard.xyz', 'w')
    fileout2 = open('distance_matrix.dat', 'w')
    fileout3 = open('coulomb_matrix.dat', 'w')

    fileout1.write(' ' + str(n_atom) + '\n')
    fileout1.write('atom unit' + '\n')

    for i in range(n_atom):
        fileout1.write(str(atom_name[i]) + '   ' + "%14.8f" % (coord[i][0]) + '   ' + "%14.8f" % (
            coord[i][1]) + '   ' + "%14.8f" % (coord[i][2]) + '   ' + str(charge[i]) + '\n')
        for j in range(n_atom):
            fileout2.write(' ' + "%14.8f" % (distance[i][j]))
            fileout3.write(' ' + "%14.8f" % (coulomb[i][j]))
        fileout2.write('\n')
        fileout3.write('\n')

    return n_atom, atom_name, coord


if __name__ == '__main__':
    distance_matrix('geom.xyz', 'xyz')
