#!/usr/bin/env python

import numpy as np
import os


def copy_energy(n_traj_select):
    for i in range(n_traj_select + 1):
        command3 = "cp  ../data_prescreening/" + str(
            i) + '/pe_time_aferselect_afterscale.out     ./all/pe_time_aferselect_afterscale.out_' + str(i)
        os.system(command3)
        command4 = 'cat  ./all/energy_all.dat    ./all/pe_time_aferselect_afterscale.out_' + str(
            i) + '      > ./all/energy_tmp.dat  '
        os.system(command4)
        command5 = 'cp  ./all/energy_tmp.dat    ./all/energy_all.dat  '
        os.system(command5)


def geom_file_list_copy(n_traj_select):
    os.system('cp  ../data_prescreening/all/list_file_save.dat  ./')
    file_list = np.loadtxt('list_file_save.dat')
    nline = file_list.shape[0]
    label_n_select_geom = 0
    for i_line in range(nline):
        if file_list[i_line, 0] > n_traj_select:
            label_n_select_geom = 1
            n_select_geom = int(file_list[i_line - 1, 2])
            break
    if label_n_select_geom == 0:
        n_select_geom = int(file_list[i_line, 2])
    return n_select_geom


def copy_geom(n_select_geom):
    energy_dir = './all/'
    if os.path.exists(energy_dir):
        command2 = 'rm -r ./all/'
        os.system(command2)
    os.system('mkdir ./all')
    for i in range(1, n_select_geom + 1):
        command3 = 'cp ../data_prescreening/all/all_sample.xyz_' + str(i) + '   ./all'
        os.system(command3)


def check_geom_energy():
    x = np.loadtxt('./all/energy_all.dat')
    n_energy = x.shape[0]

    work_dir = './all'
    n_geom = 0
    for parentdir, dirname, filenames in os.walk(work_dir):
        for filename in filenames:
            if "all_sample.xyz_" in filename:
                n_geom = n_geom + 1

    if n_geom == n_energy:
        print("The task of copying data is finished correctly.")
        print('n_geom: ', n_geom)
        print('n_energy:  ', n_energy)
    else:
        print("Check the numbers of geometries and energies ")
        print('n_geom: ', n_geom)
        print('n_energy:  ', n_energy)
        raise IOError


def copy_and_check_from_outside(n_traj_select):
    n_select_geom = geom_file_list_copy(n_traj_select)
    copy_geom(n_select_geom)
    copy_energy(n_traj_select)
    check_geom_energy()


if __name__ == "__main__":
    data_copy()
    copy_geom_energy(n_select_geom)
    check_geom_energy()
