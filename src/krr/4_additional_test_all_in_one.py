#!/usr/bin/env python

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing
import numpy as np
import os
import sub_collect_x_y
import sub_copy_additional_test_data
import sub_inp_json
import sub_kernel_regression_tool


def descriptor_file(label_x_descriptor):
    if label_x_descriptor == 0:
        filename = 'x_y_coulomb.dat'
    if label_x_descriptor == 1:
        filename = 'x_y_distance.dat'
    if label_x_descriptor == 2:
        filename = 'x_y_inversed_distance.dat'
    return filename


def construct_data_input(n_traj, filename, n_x_dim, n_y_dim):
    curr_dir = os.getcwd()
    for i_traj in range(1, n_traj):
        work_dir = str(i_traj)
        os.chdir(work_dir)

        x = np.loadtxt(filename)
        n_dim = x.shape[1]
        if n_dim != n_x_dim + n_y_dim:
            print("check input dimensionality")
            raise IOError
        np.savetxt('x_test_ad.dat', x[:, 0: n_x_dim])
        for i_y in range(n_y_dim):
            file_y = 'y_test_ad.dat_S' + str(i_y)
            np.savetxt(file_y, x[:, n_x_dim + i_y])
        os.chdir(curr_dir)


def kkr_prediction_single(n_x_dim, x_train, para_kernel, para_gamma, para_alpha, work_path, fit_path, rescale):
    #       print "KKR", n_x_dim, para_kernel, para_gamma, para_alpha, fit_path, rescale
    kkr = sub_kernel_regression_tool.kkr_all(n_x_dim, x_train, para_kernel, para_gamma, para_alpha, fit_path, rescale)
    #       print "Load all data."
    kkr.load_data_train()
    #       print "Finish to load all data"
    kkr.load_data_test()
    #       print "Scale data"
    kkr.rescale_data()
    #       print "Test KKR"
    kkr.test_kkr()
    #       print "Test error is: ", kkr.test_error
    return kkr.test_error


def plot_many_pes_time(n_traj, n_y_dim, para_gamma1, para_alpha1):
    current_gamma = float(para_gamma1)
    current_alpha = float(para_alpha1)

    print("Plot PES v.s. time")
    for i_traj in range(1, n_traj):
        fig, axs = plt.subplots(1, 2)
        plot_label = 'kkr_test_gamma_' + str(current_gamma) + '_alpha_' + str(current_alpha) + '_traj_' + str(i_traj)
        figure_file = './plot_result/kkr_test_gamma_' + str(current_gamma) + '_alpha_' + str(
            current_alpha) + '_traj_' + str(i_traj) + '.pdf'
        plt.title(plot_label)
        for i_state in range(n_y_dim):
            model_dir = 'fit_result_kkr' + '_gamma_' + str(para_gamma1) + '_alpha_' + str(para_alpha1) + '_S' + str(
                i_state)
            filename = str(model_dir) + '/kkr_test.dat_' + str(i_traj)
            x = np.loadtxt(filename)
            y1_plot = x[:, 0]
            y2_plot = x[:, 1]
            err = x[:, 2]
            n_points = x.shape[0]
            time = np.arange(0, n_points, 1)

            ax = axs[0]
            ax.scatter(time, y1_plot)
            ax.plot(time, y2_plot)

            ax = axs[1]
            ax.hist(err, bins=200)
            ax.set_xlim(-3, 3)
        fig.savefig(figure_file)
        plt.close()

    pdfmerge = 'pdfjam   ./plot_result/kkr_test_gamma_' + str(current_gamma) + '_alpha_' + str(
        current_alpha) + '*.pdf   -o ./plot_result/kkr_test_gamma_' + str(current_gamma) + '_alpha_' + str(
        current_alpha) + '_all.pdf'
    os.system(pdfmerge)
    for i_traj in range(1, n_traj):
        command_remove = 'rm  ./plot_result/kkr_test_gamma_' + str(current_gamma) + '_alpha_' + str(
            current_alpha) + '_traj_' + str(i_traj) + '.pdf'
        os.system(command_remove)


def additional_test():
    os.system('cp ../train_and_test/input.json  ./')

    file_json = 'input.json'
    xxx_input = sub_inp_json.load_json(file_json)
    n_traj_test = int(xxx_input['n_predict_traj'])
    n_x_dim = int(xxx_input['n_x_dim'])
    n_y_dim = int(xxx_input['n_y_dim'])
    label_x_descriptor = int(xxx_input['label_x_descriptor'])
    para_gamma = xxx_input['para_gamma']
    para_alpha = xxx_input['para_alpha']
    para_gamma = para_gamma[1:-1]
    para_gamma = para_gamma.split(',')
    para_alpha = para_alpha[1:-1]
    para_alpha = para_alpha.split(',')
    para_kernel = xxx_input['para_kernel']
    rescale = xxx_input['rescale']
    npro_train = int(xxx_input['npro_train'])

    print("Copy add geometries for testing!")
    curr_dir = os.getcwd()
    sub_copy_additional_test_data.copy_geom_energy(n_traj_test)
    os.chdir(curr_dir)

    print("collect all geometries for testing!")
    #     Collect all data
    # -----------------------------------------------------
    sub_collect_x_y.collect_all_traj(n_traj_test)
    os.chdir(curr_dir)
    # ----------------------------------------------------------------
    filename = descriptor_file(label_x_descriptor)
    construct_data_input(n_traj_test, filename, n_x_dim, n_y_dim)
    os.chdir(curr_dir)

    #   Additional Test
    if npro_train > 1:
        pool = multiprocessing.Pool(processes=npro_train)
        print("Start work on test")
        for para_gamma1 in para_gamma:
            for para_alpha1 in para_alpha:
                for i_state in range(n_y_dim):
                    pool.apply_async(test_single,
                                     (para_gamma1, para_alpha1, i_state, n_traj_test, n_x_dim, para_kernel, rescale,))

        pool.close()
        pool.join()
    elif npro_train == 1:
        for para_gamma1 in para_gamma:
            for para_alpha1 in para_alpha:
                for i_state in range(n_y_dim):
                    test_single(para_gamma1, para_alpha1, i_state, n_traj_test, n_x_dim, para_kernel, rescale)

    plot_dir = 'plot_result'
    if os.path.exists(plot_dir):
        command1 = 'rm -r ' + str(plot_dir)
        os.system(command1)
    os.system('mkdir plot_result')
    for para_gamma1 in para_gamma:
        for para_alpha1 in para_alpha:
            plot_many_pes_time(n_traj_test, n_y_dim, para_gamma1, para_alpha1)
            os.chdir(curr_dir)


def test_single(para_gamma1, para_alpha1, i_state, n_traj_test, n_x_dim, para_kernel, rescale):
    curr_dir = os.getcwd()
    current_gamma = float(para_gamma1)
    current_alpha = float(para_alpha1)

    model_dir = 'fit_result_kkr' + '_gamma_' + str(para_gamma1) + '_alpha_' + str(para_alpha1) + '_S' + str(i_state)
    if os.path.exists(model_dir):
        command1 = 'rm -r ' + str(model_dir)
        os.system(command1)
    command2 = 'cp   -r ../train_and_test/' + str(model_dir) + '     ./'
    os.system(command2)

    for i_traj in range(1, n_traj_test):
        command3 = 'cp  ./' + str(i_traj) + '/x_test_ad.dat    ./' + str(model_dir) + '/x_test_ad.dat_' + str(i_traj)
        os.system(command3)
        command4 = 'cp  ./' + str(i_traj) + '/y_test_ad.dat_S' + str(i_state) + '     ./' + str(
            model_dir) + '/y_test_ad.dat_S' + str(i_state) + '_' + str(i_traj)
        os.system(command4)

    # print "Test jobs on ", para_gamma1, para_alpha1, i_state
    os.chdir(model_dir)
    x_train = np.loadtxt('x_train.dat')
    for i_traj in range(1, n_traj_test):
        command5 = 'cp  x_test_ad.dat_' + str(i_traj) + '    x_test.dat'
        os.system(command5)
        command5 = 'cp  y_test_ad.dat_S' + str(i_state) + '_' + str(i_traj) + '    y_test.dat'
        os.system(command5)
        work_path = os.getcwd()
        fit_path = os.getcwd()
        #                    print n_x_dim, para_kernel, current_gamma, current_alpha, work_path, fit_path,  rescale
        error = kkr_prediction_single(n_x_dim, x_train, para_kernel, current_gamma, current_alpha, work_path, fit_path, rescale)
        print("Gamma: ", current_gamma, ', Alpha: ', current_alpha, ',  State: ', i_state, ', Traj: ', i_traj,
              ', Error: ', error)
        command6 = 'cp kkr_test.dat    kkr_test.dat_' + str(i_traj)
        os.system(command6)
    os.chdir(curr_dir)


if __name__ == "__main__":
    additional_test()
