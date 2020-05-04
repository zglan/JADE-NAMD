import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np

curr_path = os.getcwd()
work_file = curr_path + '/all/rmsd_all.dat_old'
xx = np.loadtxt(work_file)
y = xx[1,:]

fig = plt.figure(dpi=80)
fig.suptitle('Distribution of the RMSD values', fontsize=20)
plt.hist(y,color='green', bins=100)

plt.xlim(0,3)
plt.xticks(np.linspace(0,2.5,6,endpoint=True),fontsize=18)
plt.ylim(0,3)
plt.yticks(np.linspace(0,80,9,endpoint=True),fontsize=18)

#iig.suptitle('test title', fontsize=20)
plt.xlabel('RMSD', fontsize=18)
plt.ylabel('Distribution', fontsize=18)
fig.savefig('rmsd_distri.jpg')
plt.show()



