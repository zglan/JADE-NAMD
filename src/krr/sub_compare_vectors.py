#!/usr/bin/env python

import numpy as np


class compare_vectors():
    def __init__(self, vec_1=np.array([0, 1, 0]),
                 vec_2=np.array([0, 0, 1])):
        self.vec_1 = vec_1
        self.vec_2 = vec_2
        self.vec_3 = self.vec_2 - self.vec_1
        self.check_dim()
        self.calc_angle_1_2()

    def check_dim(self):
        n1 = self.vec_1.shape
        n2 = self.vec_2.shape
        if len(n1) == 1 and n1 == n2:
            pass
        else:
            print('Vectors dimenssion error!')
            raise IOError

    def calc_vec_len(self, vec):
        vec_len = np.dot(vec, vec.T) ** 0.5
        return vec_len

    def calc_angle_1_2(self):
        self.vec_1_len = self.calc_vec_len(self.vec_1)
        self.vec_2_len = self.calc_vec_len(self.vec_2)
        self.vec_3_len = self.calc_vec_len(self.vec_3)
        a = self.vec_3_len
        b = self.vec_1_len
        c = self.vec_2_len
        self.cos_A = (b ** 2. + c ** 2. - a ** 2.) / (2. * b * c)


def vec_input(filename):
    mat = np.loadtxt(filename)
    n1, n2 = mat.shape
    n = n1 * n2
    vec = np.reshape(mat, n)
    return vec


def vec_input_xyz_type(filename):
    mat = np.loadtxt(filename, skiprows=2, usecols=(1, 2, 3))
    n1, n2 = mat.shape
    n = n1 * n2
    vec = np.reshape(mat, n)
    return vec


def compare_vectors_in_files(file_1, file_2):
    vec_1 = vec_input(file_1)
    vec_2 = vec_input(file_2)
    t1 = compare_vectors(vec_1, vec_2)
    return t1.vec_1_len, t1.vec_2_len, t1.cos_A, t1.vec_3_len


if __name__ == "__main__":
    t1 = compare_vectors()
    print(t1.vec_1_len, t1.vec_2_len, t1.cos_A, t1.vec_3_len)
    file_1 = 'gradient_fit_1.xyz'
    file_2 = 'gradient_cal_1.xyz'
    print('%.4f   ' * 4 % compare_vectors_in_files(file_1, file_2))
