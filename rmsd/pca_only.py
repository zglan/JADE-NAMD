print(__doc__)

# Authors: Kyle Kastner
# License: BSD 3 clause

import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.decomposition import PCA, IncrementalPCA
from sklearn.decomposition import KernelPCA

from sklearn import (manifold, datasets, decomposition, ensemble,
                     discriminant_analysis, random_projection)
from sklearn import preprocessing
from mpl_toolkits.mplot3d import Axes3D
import os
import sys


work_dir = 'all'
os.chdir(work_dir)

xx = np.loadtxt('mds_reduced_dimen.dat_dim_20')

scale_xdata = preprocessing.StandardScaler().fit(xx)
x_train_scale = scale_xdata.transform(xx)

#x_train_scale = xx

x_final = x_train_scale[:, 0:2]


n_components = 2


pca = PCA(n_components=n_components)
X_pca = pca.fit_transform(x_final)


filename1 = 'pca.dat_dimension_'+str(n_components)
np.savetxt(filename1, X_pca)


plt.figure(figsize=(8, 8))
plt.scatter(X_pca[:,0], X_pca[:,1] )
plt.show()






