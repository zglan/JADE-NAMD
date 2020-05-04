#! /usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
data = np.loadtxt('mds_distance.dat') 
plt.imshow(data, cmap=plt.cm.spectral)
plt.xticks(np.linspace(1,3888,7,endpoint=True,fontsize=30))
plt.xlabel('xlabel',fontsize=30)
plt.colorbar()
plt.show()
