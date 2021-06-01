#!/usr/bin/env python

import numpy as np
import os

import sub_coord_single


class single_x_descriptor():
    def __init__(self, filename, file_type):
        self.file_name = filename
        self.file_type = file_type

    def descriptor(self):
        sub_coord_single.distance_matrix(self.file_name, self.file_type)


class generate_many_x_descriptor():
    def __init__(self, n_total, filename_common, file_type):
        self.n_total = n_total
        self.filename_common = filename_common
        self.file_type = file_type

    def many_x(self):
        for i in range(self.n_total):
            single_filename = str(self.filename_common) + "_" + str(i + 1)
            single = single_x_descriptor(single_filename, self.file_type)
            single.descriptor()

            file_old_name = 'standard.xyz'
            file_new_name = file_old_name + "_" + str(i + 1)
            os.rename(file_old_name, file_new_name)

            file_old_name = 'distance_matrix.dat'
            file_new_name = file_old_name + "_" + str(i + 1)
            os.rename(file_old_name, file_new_name)

            file_old_name = 'coulomb_matrix.dat'
            file_new_name = file_old_name + "_" + str(i + 1)
            os.rename(file_old_name, file_new_name)


class collect_descriptor():
    def __init__(self, n_total):
        self.n_total = n_total

    def extract_x_input(self, file_distance):

        x_all = np.loadtxt(file_distance)
        n_dim = x_all.shape[0]
        n_input_len = (n_dim * (n_dim - 1)) / 2
        x_input = np.zeros((1, int(n_input_len)))

        i_input = 0
        for i_row in range(n_dim):
            for i_column in range(i_row):
                x_input[0, i_input] = x_all[i_row, i_column]
                i_input = i_input + 1
        self.x_input = x_input

    def descriptor_x(self):
        for i_geom in range(self.n_total):
            file_distance_matrix = 'distance_matrix.dat_' + str(i_geom + 1)
            self.extract_x_input(file_distance_matrix)
            if i_geom == 0:
                x_old = self.x_input
            else:
                x_old = np.vstack((x_old, self.x_input))
        np.savetxt('x_input.dat', x_old)

    def descriptor_1_x(self):
        for i_geom in range(self.n_total):
            file_distance_matrix = 'distance_matrix.dat_' + str(i_geom + 1)
            self.extract_x_input(file_distance_matrix)
            if i_geom == 0:
                x_old = 1.0 / self.x_input
            else:
                x_old = np.vstack((x_old, 1.0 / self.x_input))
        np.savetxt('x_inversed_input.dat', x_old)

    def descriptor_coulomb_matrix(self):
        for i_geom in range(self.n_total):
            file_distance_matrix = 'coulomb_matrix.dat_' + str(i_geom + 1)
            self.extract_x_input(file_distance_matrix)
            if i_geom == 0:
                x_old = self.x_input
            else:
                x_old = np.vstack((x_old, self.x_input))
        np.savetxt('coulomb_input.dat', x_old)


class collect_x_y():
    def __init__(self, n_total, y_file):
        self.n_total = n_total
        self.y_file = y_file

    def collect_x_y_from_file_tool(self, filex, fileoutput):
        x = np.loadtxt(filex)
        nnx_dim = x.ndim
        if nnx_dim == 1:
            n_x_lines = x.shape[0]
            x = x.reshape(n_x_lines, 1)
        else:
            n_x_lines = x.shape[0]
        if n_x_lines != self.n_total:
            print("The numbers of x and y are not consistent!")
            raise IOError
        y = np.loadtxt(self.y_file)
        nny_dim = y.ndim
        if nny_dim == 1:
            y = y.reshape(-1, 1)
        if y.shape[0] != self.n_total:
            print("The numbers of x and y are not consistent!")
            raise IOError
        x_y = np.hstack((x, y))
        np.savetxt(fileoutput, x_y)

    def collect_x_y_from_file(self):
        filex = 'x_input.dat'
        fileoutput = 'x_y_distance.dat'
        self.collect_x_y_from_file_tool(filex, fileoutput)

        filex = 'x_inversed_input.dat'
        fileoutput = 'x_y_inversed_distance.dat'
        self.collect_x_y_from_file_tool(filex, fileoutput)

        filex = 'coulomb_input.dat'
        fileoutput = 'x_y_coulomb.dat'
        self.collect_x_y_from_file_tool(filex, fileoutput)


# ------------------------------------------------------------------------------------------------     
#      Collection of all x and y from one file
# ---------------------------------------------------------------------------------------------------------
def collect_all_from_file():
    file_x = 'all_sample.xyz'
    file_type = 'xyz'
    file_y = 'energy_all.dat'

    curr_dir = os.getcwd()

    work_dir = './all'
    os.chdir(work_dir)

    y = np.loadtxt(file_y)
    n_total = y.shape[0]

    print("Generate the descriptors for all x")
    generate_x_input = generate_many_x_descriptor(n_total, file_x, file_type)
    generate_x_input.many_x()

    print("Collect descriptors for all x")
    collect_x = collect_descriptor(n_total)
    collect_x.descriptor_x()
    collect_x.descriptor_1_x()
    collect_x.descriptor_coulomb_matrix()

    print("Collect all x and y")
    collect_all_x_y = collect_x_y(n_total, file_y)
    collect_all_x_y.collect_x_y_from_file()

    os.chdir(curr_dir)

    x_y_dir = './all_1'
    if os.path.exists(x_y_dir):
        command2 = 'rm -r ./all_1'
        os.system(command2)
    os.system('mkdir all_1')
    os.system('cp ./all/x_y_*.dat  ./all_1')


# --------------------------------------------------------------------------------
#    Collection of all x and y from trajectories 
#    X and y from a single trajectrory
def collect_all_for_single_traj(file_x, file_type, file_y):
    y = np.loadtxt(file_y)
    n_total = y.shape[0]

    print("Generate the descriptors for all x")
    generate_x_input = generate_many_x_descriptor(n_total, file_x, file_type)
    generate_x_input.many_x()

    print("Collect descriptors for all x")
    collect_x = collect_descriptor(n_total)
    collect_x.descriptor_x()
    collect_x.descriptor_1_x()
    collect_x.descriptor_coulomb_matrix()

    print("Collect all x and y")
    collect_all_x_y = collect_x_y(n_total, file_y)
    collect_all_x_y.collect_x_y_from_file()


#  X and y from many trajectories 


def collect_all_traj(n_traj):
    file_x = 'sample.xyz'
    file_type = 'xyz'
    file_y = 'pe_time_aferselect_afterscale.out'

    curr_dir = os.getcwd()

    for i_traj in range(1, n_traj):
        work_dir = str(i_traj)
        os.chdir(work_dir)
        collect_all_for_single_traj(file_x, file_type, file_y)
        os.chdir(curr_dir)


if __name__ == "__main__":
    n_traj = 40
    collect_all_traj(n_traj)
