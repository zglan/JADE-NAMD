#!/usr/bin/env python

import numpy as np
import os


class file_contents():
    def __init__(self, file_name):
        self.file_in = file_name
        self.n_line = 0
        self.line_each = []

    def n_total_line_file(self):
        self.n_line = 0
        filein = open(self.file_in, "r")
        for line in filein:
            self.n_line += 1
        filein.close()

    def file_contents(self):
        self.line_each = []
        for i_line in range(self.n_line):
            self.line_each.append(0.0)
        filein = open(self.file_in, "r")
        line_all = filein.read().strip()
        filein.close()
        self.line_each = line_all.split('\n')


class single_traj():
    def __init__(self):
        self.n_line = 0
        self.line_each = []

    def read_current_state(self):
        file_state = 'current_state.out'
        read_state = file_contents(file_state)
        read_state.n_total_line_file()
        read_state.file_contents()
        n_line = read_state.n_line
        line_each = read_state.line_each

        self.current_state = np.zeros((n_line - 1), dtype=np.int32).reshape(n_line - 1, 1)
        for i_line in range(n_line - 1):
            self.current_state[i_line, 0] = int(line_each[i_line + 1].split()[2])

    def read_total_energy(self):
        file_state = 'energy_time.out'
        read_state = file_contents(file_state)
        read_state.n_total_line_file()
        read_state.file_contents()
        n_line = read_state.n_line
        line_each = read_state.line_each

        self.total_energy = np.zeros((n_line - 2), dtype=np.float64).reshape(n_line - 2, 1)
        for i_line in range(n_line - 2):
            self.total_energy[i_line, 0] = float(line_each[i_line + 2].split()[4])

    def put_all_together(self):
        pe = np.loadtxt('pe_time.out')
        all_in_one = np.hstack((pe, self.current_state))
        all_in_one = np.hstack((all_in_one, self.total_energy))
        if os.path.exists('all_in_one.dat'):
            os.system('rm all_in_one.dat')
        np.savetxt('all_in_one.dat', all_in_one)


def all_traj(n_traj):
    n_traj = n_traj
    curr_dir = os.getcwd()
    for i_traj in range(n_traj):
        print("the %i file's data is merging" % (i_traj + 1))
        new_dir = "./" + str(i_traj + 1)
        os.chdir(new_dir)
        collect_info = single_traj()
        collect_info.read_current_state()
        collect_info.read_total_energy()
        collect_info.put_all_together()
        os.chdir(curr_dir)


def singl_traj(i):
    collect_info = single_traj()
    collect_info.read_current_state()
    collect_info.read_total_energy()
    collect_info.put_all_together()


if __name__ == '__main__':
    all_traj(100)
