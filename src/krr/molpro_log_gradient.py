#!/usr/bin/env python

import re

n_state = 3

logfile = "cas.out"
file_in = open(logfile, "r")

pattern = re.compile("SA-MC GRADIENT FOR STATE")


line = "NOT EMPTY LINE"
for i_state in range(n_state):
    file_out = open("qm_gradient.dat_S" + str(i_state), "w")
    while line != "":
        line = file_in.readline()
        m = pattern.search(line)
        if m is not None:
            break

    line = file_in.readline()
    line = file_in.readline()
    line = file_in.readline()

    while line != "":
        line = file_in.readline()
        if line.strip() == "":
            break

        record = line.split()

        grad_x = float(record[1])
        grad_y = float(record[2])
        grad_z = float(record[3])

        file_out.write('' + str(grad_x) + '   ' + \
                       str(grad_y) + '   ' + str(grad_z) + '  \n')
    file_out.close()
file_in.close()
