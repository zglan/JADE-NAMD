#!/usr/bin/env python

import os
import sys
import numpy as np
import time
from sklearn import preprocessing
from sklearn.externals import joblib
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error
from sklearn.metrics.pairwise import rbf_kernel


#############################################################################


class kkr_all():
    def __init__(self, n_x_dim, x_train, para_kernel, para_gamma, para_alpha, fit_path, rescale):
        self.n_x_dim = n_x_dim
        self.x_train = x_train
        self.para_kernel = para_kernel
        self.kernel = para_kernel
        self.para_gamma = para_gamma
        self.gamma = para_gamma
        self.para_alpha = para_alpha
        self.alpha = para_alpha
        self.fit_path = fit_path
        self.rescale = rescale

    def load_data_train(self):
        #        self.x_train = np.loadtxt('x_train.dat')
        self.y_train = np.loadtxt('y_train.dat')
        self.n_train = self.x_train.shape[0]
        if self.n_x_dim == 1:
            self.x_train = self.x_train.reshape(self.n_train, 1)
        self.y_train = self.y_train.reshape(self.n_train, 1)

    def load_data_test(self):
        self.x_test = np.loadtxt('x_test.dat')
        self.y_test = np.loadtxt('y_test.dat')
        self.n_test = self.x_test.shape[0]
        if self.n_x_dim == 1:
            self.x_test = self.x_test.reshape(self.n_test, 1)
        self.y_test = self.y_test.reshape(self.n_test, 1)

    def rescale_data(self):
        if self.rescale != "NO":
            #      Scale X
            if self.rescale == "Normal":
                scale_xdata = preprocessing.StandardScaler()
                scale_xdata.fit(self.x_train)
                self.scale_x_factor = scale_xdata.scale_
                self.mean_x = scale_xdata.mean

            elif self.rescale == "Robust":
#                scale_xdata = preprocessing.RobustScaler(quantile_range=(0, 100))
#                scale_xdata.fit(self.x_train)
#                self.scale_x_factor = scale_xdata.scale_
#                self.mean_x = scale_xdata.center_

                file_x_range = open('x_range.dat', 'w')

                x_train = self.x_train
                x_train_tmp = list(map(list,zip(*x_train)))

                for i in range(len(x_train_tmp)):
                   x_min_tmp = min(x_train_tmp[i])
                   x_max_tmp = max(x_train_tmp[i])
                   file_x_range.write(str(x_min_tmp) + ' ' + str(x_max_tmp) + '\n')

                file_x_range.close()

                scale_xdata = preprocessing.RobustScaler()
                scale_xdata.fit(self.x_train)
                self.scale_x_factor = scale_xdata.scale_
                self.mean_x = scale_xdata.center_

            x_train_scale = scale_xdata.transform(self.x_train)
            self.x_train = x_train_scale
            x_test_scale = scale_xdata.transform(self.x_test)
            self.x_test = x_test_scale

            #    Scale y
            scale_ydata = preprocessing.RobustScaler()
            scale_ydata.fit(self.y_train)
            self.scale_y_factor = scale_ydata.scale_
            self.mean_y = scale_ydata.center_

    def kernel_ridge_regression(self):

        kkr = KernelRidge(kernel=self.para_kernel, gamma=self.para_gamma, alpha=self.para_alpha)

        print("Start KKR fitting.")

        y_train = self.y_train
        for i in range(self.n_train):
            y_train[i, :] = self.y_train[i, :] - self.mean_y[:]

        t0 = time.time()
        kkr.fit(self.x_train, y_train)
        kkr_fit = time.time() - t0
        print(("KKR complexity and bandwidth selected and model fitted in %.3f s"
               % kkr_fit))

        #        Check the fitting for training data
        y_train_kkr = kkr.predict(self.x_train)
        for i in range(self.n_train):
            y_train[i, :] = y_train[i, :] + self.mean_y[:]
            y_train_kkr[i, :] = y_train_kkr[i, :] + self.mean_y[:]

        y_diff = np.subtract(y_train_kkr, self.y_train)
        train_kkr = np.hstack((self.y_train, y_train_kkr))
        print(self.x_train.shape, self.y_train.shape, y_train_kkr.shape, y_diff.shape)
        train_kkr = np.hstack((train_kkr, y_diff))
        filename = str(self.fit_path) + '/kkr_train.dat'
        np.savetxt(filename, train_kkr)
        err = mean_squared_error(self.y_train, y_train_kkr)
        self.train_error = err

        filename = str(self.fit_path) + '/kkr.pkl'
        joblib.dump(kkr, filename)
        kkr_coef = kkr.dual_coef_
        np.set_printoptions(threshold='nan')
        filename = str(self.fit_path) + '/fitting_para.dat'
        np.savetxt(filename, kkr_coef)

    def test_kkr(self):

        #   Read the training data
        filename = str(self.fit_path) + '/kkr.pkl'
        kkr = joblib.load(filename)

        print("Starting KKR prediction")
        y_test_kkr = kkr.predict(self.x_test)
        for i in range(self.n_test):
            y_test_kkr[i, :] = y_test_kkr[i, :] + self.mean_y[:]

        y_diff = np.subtract(y_test_kkr, self.y_test)
        print(self.y_test.shape, y_test_kkr.shape, y_diff.shape)
        test_kkr = np.hstack((self.y_test, y_test_kkr))
        test_kkr = np.hstack((test_kkr, y_diff))
        filename = str(self.fit_path) + '/kkr_test.dat'
        np.savetxt(filename, test_kkr)
        err = mean_squared_error(self.y_test, y_test_kkr)
        np.savetxt(filename, test_kkr)

        self.test_error = err

    def load_data_prediction(self):
        self.x_pre = np.loadtxt('x_pre.dat')
        self.x_range = np.loadtxt('x_range.dat')
        for i in range(len(self.x_pre)):
            if self.x_pre[i] < self.x_range[i][0] or self.x_pre[i] > self.x_range[i][1]:
                print('The structure is out of range, go to QM calulation')
#                raise IOError

        print(self.x_pre.ndim)

        if self.x_pre.ndim == 0:
            self.n_pre = 1
        if self.x_pre.ndim == 1:
            if self.n_x_dim == 1:
                self.n_pre = self.x_pre.shape[0]
            else:
                self.n_pre = 1
        if self.x_pre.ndim > 1:
            self.n_pre = self.x_pre.shape[0]

        if self.n_pre == 1 and self.n_x_dim == 1:
            self.x_pre = self.x_pre.reshape(1, 1)
        if self.n_pre == 1 and self.n_x_dim != 1:
            self.x_pre = self.x_pre.reshape(1, -1)
        if self.n_pre != 1 and self.n_x_dim == 1:
            self.x_pre = self.x_pre.reshape(self.n_pre, 1)
        self.x_pre_old = self.x_pre

        if self.rescale != "NO":
            if self.rescale == "Normal":
                scale_xdata = preprocessing.StandardScaler()
                scale_xdata.fit(self.x_train)
                self.scale_x_factor = scale_xdata.scale_
                self.mean_x = scale_xdata.mean
            elif self.rescale == "Robust":
                scale_xdata = preprocessing.RobustScaler()
                scale_xdata.fit(self.x_train)
                self.scale_x_factor = scale_xdata.scale_
                self.mean_x = scale_xdata.center_

            x_train_scale = scale_xdata.transform(self.x_train)
            self.x_train = x_train_scale
            x_pre_scale = scale_xdata.transform(self.x_pre)
            self.x_pre = x_pre_scale

            #    Scale y
            scale_ydata = preprocessing.RobustScaler()
            scale_ydata.fit(self.y_train)
            self.scale_y_factor = scale_ydata.scale_
            self.mean_y = scale_ydata.center_

    def kkr_prediction_gradient(self):

        parameter_file = str(self.fit_path) + '/fitting_para.dat'
        coeff = np.loadtxt(parameter_file)
        print(coeff.shape)
        coeff = coeff.reshape(self.n_train, 1)
        print(coeff.shape)

        kernel_term = rbf_kernel(self.x_pre, self.x_train, self.gamma)
        print(kernel_term.shape)

        x_diff = np.arange(self.n_pre * self.n_train * self.n_x_dim).reshape(self.n_pre, self.n_train, self.n_x_dim)
        x_diff = x_diff.astype(float)
        print(x_diff.shape)

        print("Compute energy")
        energy = np.dot(kernel_term, coeff)
        for i_pre in range(self.n_pre):
            energy[i_pre, :] = energy[i_pre, :] + self.mean_y[:]

        print("Compute distance matrix")

        start = time.clock()

        for i_dim in range(self.n_x_dim):
            for i_train in range(self.n_train):
                for i_test in range(self.n_pre):
                    x_diff[i_test, i_train, i_dim] = self.x_pre[i_test, i_dim] - self.x_train[i_train, i_dim]
        print(x_diff.shape)


        for i_dim in range(self.n_x_dim):
            x_diff[:, :, i_dim] = -2 * self.gamma * x_diff[:, :, i_dim] / self.scale_x_factor[i_dim]

        elapsed = (time.clock() - start)
        print("compute distance matrix Time used:",elapsed)

        print("Compute KKR gradient")

        start = time.clock()

        kkr_gradient = np.zeros((self.n_pre, self.n_x_dim))
        for i_dim in range(self.n_x_dim):
            for i_test in range(self.n_pre):
                for i_train in range(self.n_train):
                    kkr_gradient[i_test, i_dim] = kkr_gradient[i_test, i_dim] + coeff[i_train, 0] * x_diff[
                        i_test, i_train, i_dim] * kernel_term[i_test, i_train]


        elapsed = (time.clock() - start)
        print("compute KKR gradient Time used:",elapsed)

        # Check the fitting for training data
        self.y_pre_kkr = np.array([[0.0]])
        gradient_kkr = np.hstack((self.x_pre_old, energy, self.y_pre_kkr))
        gradient_kkr = np.hstack((gradient_kkr, kkr_gradient))

        filename = str(self.fit_path) + '/energy_gradient_col.dat'
        np.savetxt(filename, gradient_kkr)


if __name__ == "__main__":
    print('Nothing Done!')
