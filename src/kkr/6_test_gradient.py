#!/usr/bin/env python

import errno
import matplotlib
import numpy as np
import os
import re

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from multiprocessing import Pool
import shutil
import sub_compare_vectors as cv
import sub_inp_json
from sub_kkr_prediction_tool import kkr_single_all_step


class additional_test_gradient():
    def __init__(self, dir_fit_dat, dir_all_traj, dir_result):
        self.home_dir = os.getcwd()
        self.dir_fit_dat = dir_fit_dat
        self.dir_all_traj = dir_all_traj
        self.dir_result = dir_result

        com = 'cp ' + dir_fit_dat + '/input.json  ./'
        os.system(com)
        file_json = 'input.json'
        xxx_input = sub_inp_json.load_json(file_json)

        self.n_atom = int(xxx_input['n_atom'])
        self.n_traj = int(xxx_input['n_traj'])
        self.n_x_dim = int(xxx_input['n_x_dim'])
        self.n_y_dim = int(xxx_input['n_y_dim'])
        self.n_state = self.n_y_dim
        self.para_gamma = xxx_input['para_gamma'][1:-1].split(',')
        self.para_alpha = xxx_input['para_alpha'][1:-1].split(',')
        self.para_kernel = xxx_input['para_kernel']
        self.npro_train = int(xxx_input['npro_train'])

        self.fit_files = ['fitting_para.dat', 'x_train.dat', 'y_train.dat', 'x_range.dat']
        gamma = self.para_gamma[0]
        alpha = self.para_alpha[0]
        i_state = 0
        dir_gamma = '/fit_result_kkr_gamma_' + str(gamma) + \
                    '_alpha_' + str(alpha) + \
                    '_S' + str(i_state)
        tmp_dir = self.dir_fit_dat + dir_gamma
        list_tmp = os.listdir(tmp_dir)
        for ffile in list_tmp:
            m = re.match('kkr.pkl', ffile)
            if m:
                self.fit_files.append(ffile)

        self.filename_pe_dyn_gather = 'pe_time_aferselect.out'
        self.filename_geom_dyn_sample = 'geom.xyz'
        self.filename_grad_dyn_sample = 'grad_dyn.xyz'
        self.filename_grad_kkr_sample = 'gradient_1d.xyz'
        self.filename_grad_kkr_gather = 'grad_kkr.xyz'
        self.filename_grad_cmp_sample = '/grad_cmp.dat'
        self.filename_grad_cmp_gather = '/grad_cmp.dat'

    def mkdir_gamma_alpha_single(self, gamma, alpha, i_state):
        self.gamma = float(gamma)
        self.alpha = float(alpha)
        dir_gamma = '/fit_result_kkr_gamma_' + str(gamma) + \
                    '_alpha_' + str(alpha) + \
                    '_S' + str(i_state)
        dir_new = self.dir_result + dir_gamma
        print(dir_new)
        dir_old = self.dir_fit_dat + dir_gamma
        self.mkdir_p(dir_new)
        self.cp_fit_files(dir_old, dir_new)
        self.mkdir_traj(dir_new)
        pdfmerge = 'pdfjam '
        for i in range(self.n_traj):
            dir_traj = str(i + 1)
            dir_traj_new = dir_new + '/' + dir_traj
            pdfmerge = pdfmerge + dir_traj_new + '/vec_len__cos_A.pdf '
        pdfmerge = pdfmerge + '-o ' + dir_new + '/vec_len_cos_A_traj.pdf'
        os.system(pdfmerge)

    def cp_fit_files(self, dir_old, dir_new):
        for tmp_file in self.fit_files:
            file_new = dir_new + '/' + tmp_file
            file_old = dir_old + '/' + tmp_file
            shutil.copy(file_old, file_new)

    def mkdir_traj(self, curr_dir):
        x_train = np.loadtxt(curr_dir+'/'+'x_train.dat')
        i_state = curr_dir.split('/')[-1].split('_S')[-1]
        print('S' + str(i_state))
        for i in range(self.n_traj):
            dir_traj = str(i + 1)
            dir_traj_new = curr_dir + '/' + dir_traj
            dir_traj_old = self.dir_all_traj + '/' + dir_traj
            self.mkdir_p(dir_traj_new)
            file_pe_dyn = dir_traj_old + '/' + self.filename_pe_dyn_gather
            file_grad_dyn = dir_traj_old + '/grad_time.out_S' + str(i_state)
            file_grad_new_for_compare = dir_traj_new + '/grad_time.out_S' + str(i_state)
            shutil.copy(file_grad_dyn, file_grad_new_for_compare)
            f_pe = open(file_pe_dyn, 'r')
            arr = f_pe.readlines()
            n_sample = len(arr)
            for j in range(n_sample):
                dir_sample = dir_traj_new + '/sample_' + str(j + 1)
                self.mkdir_p(dir_sample)
                file_geom_old = dir_traj_old + '/sample.xyz_' + str(j + 1)
                file_geom_new = dir_sample + '/' + self.filename_geom_dyn_sample
                file_grad_old = dir_traj_old + '/grad_sample_S' + str(i_state) + \
                                '.xyz_' + str(j + 1)
                file_grad_new = dir_sample + '/' + self.filename_grad_dyn_sample
                shutil.copy(file_geom_old, file_geom_new)
                shutil.copy(file_grad_old, file_grad_new)

                fit_files = ['fitting_para.dat', 'y_train.dat', 'x_range.dat']

                for tmp_file in fit_files:
                    file_new = dir_sample + '/' + tmp_file
                    file_old = curr_dir + '/' + tmp_file
                    shutil.copy(file_old, file_new)

                print(dir_sample)
                kkr_single_all = kkr_single_all_step(self.n_x_dim,
                                                     self.n_y_dim,
                                                     x_train,
                                                     self.para_kernel,
                                                     self.gamma,
                                                     self.alpha,
                                                     './',  # fit_path,
                                                     './',  # work_path
                                                     "Robust",  # rescale
                                                     "Yes",  # label_grad
                                                     0  # label_x_descriptor
                                                     )
                os.chdir(dir_sample)
                kkr_single_all.kkr_all_step()
                file_grad_1 = dir_sample + '/' + self.filename_grad_kkr_sample
                file_grad_2 = file_grad_new
                file_cmp = dir_sample + '/' + self.filename_grad_cmp_sample
                self.cmp_grad_vec(file_grad_1, file_grad_2, file_cmp)

            self.gather_grad(n_sample, dir_traj_new)
            self.gather_grad_cmp(n_sample, dir_traj_new)
            self.plot_grad_cmp_gather(dir_traj_new)
            os.chdir(dir_traj_new)
            for j in range(n_sample):
                dir_sample = dir_traj_new + '/sample_' + str(j + 1)
                shutil.rmtree(dir_sample)
        print('S' + str(i_state))

    def gather_grad(self, n_sample, dir_traj_new):
        file_grad_gather = dir_traj_new + '/' + self.filename_grad_kkr_gather
        f_grad_gather = open(file_grad_gather, 'w')
        for j in range(n_sample):
            dir_sample = dir_traj_new + '/sample_' + str(j + 1)
            file_grad = dir_sample + '/' + self.filename_grad_kkr_sample
            line1 = '%d\n%5s%12d\n' % (self.n_atom, 'Geom', j + 1)
            f_grad = open(file_grad, 'r')
            lines = f_grad.read()
            f_grad.close()
            f_grad_gather.write(line1)
            f_grad_gather.write(lines)
        f_grad_gather.close()

    def gather_grad_cmp(self, n_sample, dir_traj_new):
        file_grad_cmp_gather = dir_traj_new + '/' + self.filename_grad_cmp_gather
        f_grad_cmp_gather = open(file_grad_cmp_gather, 'w')
        line1 = '# |vec1|   |vec2|   cos_A   |vec1-vec2|\n'
        f_grad_cmp_gather.write(line1)
        for j in range(n_sample):
            dir_sample = dir_traj_new + '/sample_' + str(j + 1)
            file_grad_cmp = dir_sample + '/' + self.filename_grad_cmp_sample
            f_grad_cmp = open(file_grad_cmp, 'r')
            lines = f_grad_cmp.read()
            f_grad_cmp.close()
            f_grad_cmp_gather.write(lines)
        f_grad_cmp_gather.close()

    def cmp_grad_vec(self, file_grad_1, file_grad_2, file_cmp):
        vec_1 = cv.vec_input(file_grad_1)
        vec_2 = cv.vec_input_xyz_type(file_grad_2)
        t1 = cv.compare_vectors(vec_1, vec_2)
        line = '%.4f   ' * 4 % (t1.vec_1_len, t1.vec_2_len, t1.cos_A, t1.vec_3_len)
        line = line + '\n'
        f_cmp = open(file_cmp, 'w')
        f_cmp.write(line)
        f_cmp.close()

    def plot_grad_cmp_gather(self, dir_traj_new):
        file_grad_cmp_gather = dir_traj_new + '/' + self.filename_grad_cmp_gather
        mat = np.loadtxt(file_grad_cmp_gather, skiprows=1)
        X = np.arange(mat.shape[0])
        vec_1_len = mat[:, 0]
        vec_2_len = mat[:, 1]
        vec_3_len = mat[:, 3]
        cos_A = mat[:, 2]
        plot_label = dir_traj_new.split('/')[-2] + '_traj_' + dir_traj_new.split('/')[-1]
        self.plot_vec_len_cos_A(dir_traj_new, X, vec_1_len, vec_2_len,
                                vec_3_len, cos_A, plot_label)

    def plot_vec_len(self, dir_traj_new, X, vec_1_len, vec_2_len, vec_3_len):
        lw = 2.5
        plt.figure(figsize=(8, 6), dpi=80)
        plt.plot(X, vec_1_len, color='black', linewidth=lw, linestyle='-', label='|vec1|')
        plt.plot(X, vec_2_len, color='red', linewidth=lw, linestyle='-', label='|vec2|')
        plt.plot(X, vec_3_len, color='blue', linewidth=lw, linestyle='-', label='|vec1-vec2|')
        plt.legend(loc='upper left')
        png_file_vec_len = dir_traj_new + '/' + 'vec_len.png'
        plt.savefig(png_file_vec_len, dpi=80)

    def plot_cos_A(self, dir_traj_new, X, cos_A):
        lw = 2.5
        plt.figure(figsize=(8, 6), dpi=80)
        plt.plot(X, cos_A, color='black', linewidth=lw, linestyle='-', label='cos_A')
        plt.legend(loc='upper left')
        plt.ylim(cos_A.min() * 1.1, cos_A.max() * 1.1)
        png_file_vec_len = dir_traj_new + '/' + 'cos_A.png'
        plt.savefig(png_file_vec_len, dpi=80)

    def plot_vec_len_cos_A(self, dir_traj_new, X, vec_1_len, vec_2_len,
                           vec_3_len, cos_A, plot_label):
        lw = 2.5
        fig, axs = plt.subplots(2, 1)
        ax1 = axs[0]
        ax2 = axs[1]
        plt.title(plot_label)
        ax1.plot(X, vec_1_len, color='black', linewidth=lw, linestyle='-', label='|vec1|')
        ax1.plot(X, vec_2_len, color='red', linewidth=lw, linestyle='-', label='|vec2|')
        ax1.plot(X, vec_3_len, color='blue', linewidth=lw, linestyle='-', label='|vec1-vec2|')
        ax1.legend(loc='upper left')
        ax2.plot(X, cos_A, color='black', linewidth=lw, linestyle='-', label='cos_A')
        ax2.set_ylim(-1.1, 1.1)
        ax2.legend(loc='lower left')
        pdf_file = dir_traj_new + '/' + 'vec_len__cos_A.pdf'
        fig.savefig(pdf_file)

    def mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


def do_mkdir_gamma_alpha_single(args):
    test_grad, gamma, alpha, state = args
    return test_grad.mkdir_gamma_alpha_single(gamma, alpha, state)


def sub_additional_test_gradient_pool(dir_fit_dat='../test_additional',
                                      dir_all_traj='../data_prescreening',
                                      dir_result='./result'):
    test_grad = additional_test_gradient(dir_fit_dat, dir_all_traj, dir_result)

    if test_grad.npro_train > 1:
        pool = Pool(processes=test_grad.npro_train)
        print(test_grad.npro_train)
        print("Start work on test")
        for gamma in test_grad.para_gamma:
            for alpha in test_grad.para_alpha:
                for i in range(test_grad.n_state):
                    print(i)
                    pool.apply_async(do_mkdir_gamma_alpha_single,
                                     ((test_grad, gamma, alpha, i),)
                                     )
        pool.close()
        pool.join()
    elif test_grad.npro_train == 1:
        for gamma in test_grad.para_gamma:
            for alpha in test_grad.para_alpha:
                for i in range(test_grad.n_state):
                    print(i)
                    test_grad.mkdir_gamma_alpha_single(gamma, alpha, i)


if __name__ == "__main__":
    home_dir = os.getcwd()
    dir_fit_dat = home_dir + '/../test_additional'
    dir_all_traj = home_dir + '/../data_prescreening'
    dir_result = home_dir + '/result'
    sub_additional_test_gradient_pool(dir_fit_dat=dir_fit_dat,
                                      dir_all_traj=dir_all_traj,
                                      dir_result=dir_result)
