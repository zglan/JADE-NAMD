#!/usr/bin/env python

import numpy as np
import os


def scale_energy(file_energy_input, energy_zero, scaling_factor, file_energy_output, n_y_dim):
    en = np.loadtxt(file_energy_input)
    n_dim = en.ndim
    if n_dim == 1:
        if n_dim != n_y_dim:
            #          print "A"
            print("Check the dimension of y: n_y_dim and energy")
            raise IOError
        else:
            #          print "B"
            n_points = en.shape[0]
            n_state = n_dim
    else:
        n_points = en.shape[0]
        n_state = en.shape[1]
    en = en.reshape(n_points, n_state)
    en_new = (en - energy_zero) * scaling_factor
    np.savetxt(file_energy_output, en_new)


def scale_energy_many(n_traj, energy_zero, scaling_factor, n_y_dim):
    curr_dir = os.getcwd()
    for i_traj in range(1, n_traj + 1):
        os.chdir(str(i_traj))
        file_energy_input = "pe_time_aferselect.out"
        file_energy_output = "pe_time_aferselect_afterscale.out"
        scale_energy(file_energy_input, energy_zero, scaling_factor, file_energy_output, n_y_dim)
        os.chdir(curr_dir)
