#!/usr/bin/env python3

import os
import shutil
from multiprocessing import Pool
import sub_inp_json
import sub_kernel_regression_tool
import sub_plot_kkr
import numpy as np


##############################################################################

class kkr_fit():
    def __init__(self):
        file_json = 'input.json'
        xxx_input = sub_inp_json.load_json(file_json)
        self.rescale = xxx_input['rescale']
        self.n_x_dim = int(xxx_input['n_x_dim'])
        self.n_y_dim = int(xxx_input['n_y_dim'])
        self.para_gamma = xxx_input['para_gamma']
        self.para_alpha = xxx_input['para_alpha']
        self.para_kernel = xxx_input['para_kernel']
        self.para_gamma = self.para_gamma[1:-1]
        self.para_gamma = self.para_gamma.split(',')
        self.para_alpha = self.para_alpha[1:-1]
        self.para_alpha = self.para_alpha.split(',')
        self.npro_train = int(xxx_input['npro_train'])

    def kkr_fit_single_case(self, para_gamma1, para_alpha1):
        n_x_dim = self.n_x_dim
        para_kernel = self.para_kernel
        para_gamma_current = para_gamma1
        para_alpha_current = para_alpha1
        rescale = self.rescale

        work_path = os.getcwd()

        x_train = np.loadtxt('x_train.dat')

        kkr = sub_kernel_regression_tool.kkr_all(n_x_dim, x_train, para_kernel, para_gamma_current, para_alpha_current,
                                                 work_path, rescale)
        print("Load all data.")
        kkr.load_data_train()
        kkr.load_data_test()
        print("Scale data")
        kkr.rescale_data()
        print("Starting KKR ")
        kkr.kernel_ridge_regression()
        print("Fitting error is: ", kkr.train_error)
        print("Test KKR")
        kkr.test_kkr()
        print("Test error is: ", kkr.test_error)
        self.train_error = kkr.train_error
        self.test_error = kkr.test_error

    def kkr_fit_data_collection(self, i_state, fit_path):
        if os.path.exists(fit_path):
            shutil.rmtree(fit_path)
        os.makedirs(fit_path)

        command1 = 'cp ./all_1/x* ' + str(fit_path)
        os.system(command1)
        command2 = 'cp ./all_1/y_train.dat_' + str(i_state) + '     ' + str(fit_path) + '/y_train.dat'
        os.system(command2)
        command3 = 'cp ./all_1/y_test.dat_' + str(i_state) + '     ' + str(fit_path) + '/y_test.dat'
        os.system(command3)
        return fit_path

    def kkr_fit_single_all(self, current_gamma, current_alpha, i_state, fit_path):
        print(current_gamma, current_alpha, i_state, fit_path)
        curr_dir = os.getcwd()
        self.kkr_fit_data_collection(i_state, fit_path)
        os.chdir(fit_path)
        self.kkr_fit_single_case(current_gamma, current_alpha)
        file_result = open('error_summary.out', 'w')
        file_result.write("current_gamma: " + str(current_gamma))
        file_result.write('   ')
        file_result.write('current_alpha: ' + str(current_alpha))
        file_result.write('   ')
        file_result.write('S: ' + str(i_state))
        file_result.write('   ')
        file_result.write('Train_error: ' + str(self.train_error))
        file_result.write('   ')
        file_result.write('Test_error: ' + str(self.test_error))
        file_result.write('   ')
        file_result.close()
        os.chdir(curr_dir)


def do_kkr_fit_single_all(args):
    test, current_gamma, current_alpha, i_state, fit_path = args
    return test.kkr_fit_single_all(current_gamma, current_alpha, i_state, fit_path)


def kkr_many():
    path_of_data = './all_1'
    if os.path.exists(path_of_data):
        shutil.rmtree(path_of_data)
    command = 'cp  -r ../train_test_data_set/all_1   ./'
    os.system(command)
    os.system('cp ../train_test_data_set/input.json  ./')

    kkr_fit_all = kkr_fit()
    para_gamma = kkr_fit_all.para_gamma
    para_alpha = kkr_fit_all.para_alpha
    n_y_dim = kkr_fit_all.n_y_dim
    npro_train = kkr_fit_all.npro_train

    if npro_train > 1:
        pool = multiprocessing.Pool(processes=npro_train)
        for para_gamma1 in para_gamma:
            for para_alpha1 in para_alpha:
                for i_state in range(n_y_dim):
                    current_gamma = float(para_gamma1)
                    current_alpha = float(para_alpha1)
                    fit_path = 'fit_result_kkr' + '_gamma_' + str(para_gamma1) + '_alpha_' + str(
                        para_alpha1) + '_S' + str(
                        i_state)
                    pool.apply_async(do_kkr_fit_single_all,
                                     ((kkr_fit_all, current_gamma, current_alpha, i_state, fit_path),))
        pool.close()
        pool.join()

    elif npro_train == 1:
        for para_gamma1 in para_gamma:
            for para_alpha1 in para_alpha:
                for i_state in range(n_y_dim):
                    current_gamma = float(para_gamma1)
                    current_alpha = float(para_alpha1)
                    fit_path = 'fit_result_kkr' + '_gamma_' + str(para_gamma1) + '_alpha_' + str(
                        para_alpha1) + '_S' + str(
                        i_state)
                    kkr_fit_all.kkr_fit_single_all(current_gamma, current_alpha, i_state, fit_path)

    error = []
    for para_gamma1 in para_gamma:
        for para_alpha1 in para_alpha:
            for i_state in range(n_y_dim):
                fit_path = 'fit_result_kkr' + '_gamma_' + str(para_gamma1) + '_alpha_' + str(para_alpha1) + '_S' + str(
                    i_state)
                file_error = fit_path + '/error_summary.out'
                file_read = open(file_error, 'r')
                error.append(file_read.read())
                file_read.close()
    file_write_error = 'error_summary_all.out'
    file_write = open(file_write_error, 'w')
    for i in error:
        file_write.write(i)
        file_write.write('\n')

    for para_gamma1 in para_gamma:
        for para_alpha1 in para_alpha:
            for i_state in range(n_y_dim):
                current_gamma = float(para_gamma1)
                current_alpha = float(para_alpha1)
                fit_path = 'fit_result_kkr' + '_gamma_' + str(para_gamma1) + '_alpha_' + str(para_alpha1) + '_S' + str(
                    i_state)
                sub_plot_kkr.read_and_plot(fit_path, current_gamma, current_alpha, i_state)
    pdfmerge = 'pdfjam   ./*/kkr_train*.pdf  -o kkr_train.pdf'
    os.system(pdfmerge)
    pdfmerge = 'pdfjam   ./*/kkr_test*.pdf  -o kkr_test.pdf'
    os.system(pdfmerge)


if __name__ == "__main__":
    kkr_many()
