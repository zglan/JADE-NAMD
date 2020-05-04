#! /usr/bin/env python
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np


x = np.linspace(1,8,8)
curr_path = os.getcwd()
work_file = curr_path + '/all/eigenvalue.dat'
y = np.loadtxt(work_file)


fig = plt.figure(dpi=80)
plt.bar(x,y)

plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

plt.xlabel('Dimentions', fontsize=18)
plt.ylabel('Eigenvalue', fontsize=18)
fig.savefig('eigenvalue.png')

plt.show()

