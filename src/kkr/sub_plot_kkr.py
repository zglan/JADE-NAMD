#!/usr/bin/env python

import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os


def plot_single(x, figure_file, plot_label):
    x_plot = x[:, 0]
    y1_plot = x[:, 1]
    y2_plot = x_plot
    err = x[:, 2]

    fig, axs = plt.subplots(2, 1)
    ax = axs[0]
    ax.scatter(x_plot, y1_plot)
    ax.plot(x_plot, y2_plot)
    ax = axs[1]
    ax.hist(err, bins=200)
    ax.set_xlim(-0.6, 0.6)
    plt.title(plot_label)
    #    plt.show()
    fig.savefig(figure_file)
    plt.close()


def plot_single_time(x, figure_file, plot_label):
    x_plot = x[:, 0]
    y1_plot = x[:, 1]
    err = x[:, 2]
    n_points = x.shape[0]
    time = np.arange(0, n_points, 1)

    fig, axs = plt.subplots(2, 1)
    ax = axs[0]
    ax.scatter(time, x_plot)
    ax.plot(time, y1_plot)
    ax = axs[1]
    ax.hist(err, bins=200)
    ax.set_xlim(-3, 3)
    plt.title(plot_label)
    #    plt.show()
    fig.savefig(figure_file)
    plt.close()


def read_and_plot(fit_path, current_gamma, current_alpha, i_state):
    curr_dir = os.getcwd()
    os.chdir(fit_path)

    file_plot_input = 'kkr_train.dat'
    plot_label = 'kkr_train_gamma_' + str(current_gamma) + '_alpha_' + str(current_alpha) + '_S_' + str(i_state)
    file_plot_output = 'kkr_train_gamma_' + str(current_gamma) + '_alpha_' + str(current_alpha) + '_S_' + str(
        i_state) + '.pdf'
    xx = np.loadtxt(file_plot_input)
    #    x = xx[:, 0:2 ]
    plot_single(xx, file_plot_output, plot_label)

    file_plot_input = 'kkr_test.dat'
    plot_label = 'kkr_test_gamma_' + str(current_gamma) + '_alpha_' + str(current_alpha) + '_S_' + str(i_state)
    file_plot_output = 'kkr_test_gamma_' + str(current_gamma) + '_alpha_' + str(current_alpha) + '_S_' + str(
        i_state) + '.pdf'
    xx = np.loadtxt(file_plot_input)
    x = xx[:, 0:2]
    plot_single(xx, file_plot_output, plot_label)

    os.chdir(curr_dir)


def read_and_plot_additional(n_traj, fit_path, current_gamma, current_alpha, i_state):
    curr_dir = os.getcwd()
    os.chdir(fit_path)
    for i_traj in range(1, n_traj):
        file_plot_input = 'kkr_test.dat_' + str(i_traj)
        plot_label = 'kkr_test_gamma_' + str(current_gamma) + '_alpha_' + str(current_alpha) + '_S_' + str(
            i_state) + '_traj_' + str(i_traj)
        file_plot_output = 'kkr_test_gamma_' + str(current_gamma) + '_alpha_' + str(current_alpha) + '_S_' + str(
            i_state) + '_traj_' + str(i_traj) + '.pdf'
        xx = np.loadtxt(file_plot_input)
        x = xx[:, 0:2]
        plot_single_time(xx, file_plot_output, plot_label)
    pdfmerge = 'pdfjam   kkr_test_*traj*.pdf  -o kkr_test_traj.pdf'
    os.system(pdfmerge)
    os.chdir(curr_dir)


def _test_plot():
    para_gamma1 = '0.01'
    para_alpha1 = '0.0000001'
    i_state = 0
    fit_path = 'fit_result_kkr' + '_gamma_' + str(para_gamma1) + '_alpha_' + str(para_alpha1) + '_S' + str(i_state)
    read_and_plot(fit_path, para_gamma1, para_alpha1, i_state)
    n_traj = 100
    read_and_plot_additional(n_traj, fit_path, para_gamma1, para_alpha1, i_state)


if __name__ == "__main__":
    _test_plot()
