#!/usr/bin/env python

import numpy as np
import os


class select_train():
    def __init__(self, n_train, filename, n_x_dim, n_y_dim, equal_or_random='R'):
        self.n_train = n_train
        self.filename = filename
        self.n_x_dim = n_x_dim
        self.n_y_dim = n_y_dim
        self.label = 1

    def number(self):
        self.y = np.loadtxt(self.filename)
        self.n_total = self.y.shape[0]
        self.n_test = self.n_total - self.n_train
        if self.n_test <= 0:
            print("The training-set data number in training set is larger than the total data number !!")
            print("n_total:  ", self.n_total)
            print("n_train:  ", self.n_train)
            raise IOError
        print("n_total:  ", self.n_total)
        print("n_train:  ", self.n_train, "n_test:  ", self.n_test)

        self.n_dim = self.y.shape[1]
        print(self.n_dim, self.n_x_dim, self.n_y_dim)
        if self.n_dim != self.n_x_dim + self.n_y_dim:
            print("check input dimensionality")
            raise IOError

    def select_x_y(self):

        if self.label == 1:
            y = np.random.permutation(self.y)
            np.savetxt('x_train.dat', y[0: self.n_train, 0: self.n_x_dim])
            np.savetxt('x_test.dat', y[self.n_train: self.n_total, 0: self.n_x_dim])

            for i_y in range(self.n_y_dim):
                file_y_train = 'y_train.dat_' + str(i_y)
                np.savetxt(file_y_train, y[0: self.n_train, self.n_x_dim + i_y])
                file_y_test = 'y_test.dat_' + str(i_y)
                np.savetxt(file_y_test, y[self.n_train: self.n_total, self.n_x_dim + i_y])


def get_train_test(n_train, filename, n_x_dim, n_y_dim):
    work_dir = './all_1'
    os.chdir(work_dir)
    select = select_train(n_train, filename, n_x_dim, n_y_dim)
    select.number()
    select.select_x_y()


def get_train_test_from_outside(n_train, filename, n_x_dim, n_y_dim):
    print("get_train_test_from_outside")
    get_train_test(n_train, filename, n_x_dim, n_y_dim)


if __name__ == "__main__":
    get_train_test_from_outside()
