#!/usr/bin/env python

import errno
import os

import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import shutil
import sub_compare_vectors as cv


class additional_test_gradient():
    def __init__(self, n_traj, dir_fit_dat, dir_all_traj, dir_result):
        self.n_traj = n_traj
        self.dir_fit_dat = dir_fit_dat
        self.dir_all_traj = dir_all_traj
        self.dir_result = dir_result

    def mkdir_gamma_alpha_single(self, i_state):

        dir_new = self.dir_result + '/' + str(i_state)
        self.mkdir_p(dir_new)
        os.chdir(dir_new)
        file_cmp = dir_new + '/grad_cmp.dat'
        f_cmp = open(file_cmp, 'w')

        for i_traj in range(self.n_traj):
            file_old_fit = self.dir_fit_dat + '/' + str(i_traj + 1) + '/kkr' + '/' + str(
                i_state + 1) + '/gradient_1d.xyz'
            file_new_fit = dir_new + '/' + 'gradient_fit_' + str(i_traj + 1) + '.xyz'
            shutil.copy(file_old_fit, file_new_fit)

            file_old_cal = self.dir_all_traj + '/' + str(i_traj + 1) + '/' + "qm_gradient.dat_S" + str(i_state)
            file_new_cal = dir_new + '/' + 'gradient_cal_' + str(i_traj + 1) + '.xyz'
            shutil.copy(file_old_cal, file_new_cal)

            vec_1 = cv.vec_input(file_new_fit)
            vec_2 = cv.vec_input(file_new_cal)
            t1 = cv.compare_vectors(vec_1, vec_2)
            line = '%.4f   ' * 4 % (t1.vec_1_len, t1.vec_2_len, t1.cos_A, t1.vec_3_len)
            line = line + '\n'
            f_cmp.write(line)
        f_cmp.close()

        mat = np.loadtxt(file_cmp, skiprows=1)
        X = np.arange(mat.shape[0])
        vec_1_len = mat[:, 0]
        vec_2_len = mat[:, 1]
        vec_3_len = mat[:, 3]
        cos_A = mat[:, 2]
        plot_label = "1"
        self.plot_vec_len_cos_A(dir_new, X, vec_1_len, vec_2_len,
                                vec_3_len, cos_A, plot_label)

    def plot_vec_len_cos_A(self, dir_new, X, vec_1_len, vec_2_len,
                           vec_3_len, cos_A, plot_label):
        lw = 2.5
        fig, axs = plt.subplots(2, 1)
        ax1 = axs[0]
        ax2 = axs[1]
        plt.title(plot_label)
        ax1.plot(X, vec_1_len, color='black', linewidth=lw, linestyle='-', label='|fit|')
        ax1.plot(X, vec_2_len, color='red', linewidth=lw, linestyle='-', label='|cal|')
        ax1.plot(X, vec_3_len, color='blue', linewidth=lw, linestyle='-', label='|fit-cal|')
        ax1.legend(loc='upper left')
        ax2.plot(X, cos_A, color='black', linewidth=lw, linestyle='-', label='cos_A')
        ax2.set_ylim(-1.1, 1.1)
        ax2.legend(loc='lower left')
        pdf_file = dir_new + '/' + 'vec_len__cos_A.pdf'
        fig.savefig(pdf_file)

    def mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


if __name__ == "__main__":
    home_dir = os.getcwd()
    dir_fit_dat = home_dir + '/kkr_1_2'
    dir_all_traj = home_dir + '/molpro'
    dir_result = home_dir + '/result'
    n_state = 3
    n_traj = 30
    test_grad = additional_test_gradient(n_traj, dir_fit_dat, dir_all_traj, dir_result)
    for i_state in range(n_state):
        test_grad.mkdir_gamma_alpha_single(i_state)
