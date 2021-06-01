#!/usr/bin/env python

import os

import sub_collect_x_y
import sub_copy_data
import sub_inp_json
import sub_select_train_test


def descriptor_file(label_x_descriptor):
    if label_x_descriptor == 0:
        filename = 'x_y_coulomb.dat'
    if label_x_descriptor == 1:
        filename = 'x_y_distance.dat'
    if label_x_descriptor == 2:
        filename = 'x_y_inversed_distance.dat'

    return filename


def all_train_and_test_from_outside():
    os.system('cp ../data_prescreening/input.json  ./')
    file_json = 'input.json'
    xxx_input = sub_inp_json.load_json(file_json)
    n_traj_select_train = int(xxx_input['n_traj_select_train'])
    n_x_dim = int(xxx_input['n_x_dim'])
    n_y_dim = int(xxx_input['n_y_dim'])
    label_x_descriptor = int(xxx_input['label_x_descriptor'])
    n_train_geom = int(xxx_input['n_train'])

    #      Copy geometries and energies
    curr_dir = os.getcwd()
    # -----------------------------------------------------
    sub_copy_data.copy_and_check_from_outside(n_traj_select_train)
    os.chdir(curr_dir)

    #     Collect all data
    # -----------------------------------------------------
    sub_collect_x_y.collect_all_from_file()
    os.chdir(curr_dir)
    # ----------------------------------------------------------------
    filename = descriptor_file(label_x_descriptor)
    sub_select_train_test.get_train_test_from_outside(n_train_geom, filename, n_x_dim, n_y_dim)
    os.chdir(curr_dir)


if __name__ == "__main__":
    all_train_and_test_from_outside()
