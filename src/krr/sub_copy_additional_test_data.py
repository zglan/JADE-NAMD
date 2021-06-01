#!/usr/bin/env python

import os


def copy_geom_energy(n_traj):
    for i in range(1, n_traj + 1):
        tmp_dir = str(i)
        if os.path.exists(tmp_dir):
            command1 = 'rm -r ' + str(i)
            os.system(command1)
        command2 = 'mkdir ' + str(i)
        os.system(command2)
        command3 = "cp  ../data_prescreening/" + str(i) + '/pe_time_aferselect_afterscale.out     ./' + str(i)
        os.system(command3)
        command4 = "cp  ../data_prescreening/" + str(i) + '/sample.xyz*                ./' + str(i)
        os.system(command4)


def data_copy():
    n_traj = 100
    copy_geom_energy(n_traj)


if __name__ == "__main__":
    data_copy()
