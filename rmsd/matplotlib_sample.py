import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['xtick.direction'] = 'out'
plt.rcParams['ytick.direction'] = 'out'
fig, ax = plt.subplots( squeeze=True)
ax.set_xlabel('RCI',fontsize=30)
ax.set_ylabel('RCII',fontsize=30)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

xticklines = ax.xaxis.get_ticklines()
xticklabels = ax.xaxis.get_ticklabels() 
for tickline in xticklines:
    tickline.set_markersize(5)
    tickline.set_markeredgewidth(3)
for ticklabel in xticklabels:
    ticklabel.set_fontsize(24)

yticklines = ax.yaxis.get_ticklines()
yticklabels = ax.yaxis.get_ticklabels() 
for tickline in yticklines:
    tickline.set_markersize(5)
    tickline.set_markeredgewidth(3)
for ticklabel in yticklabels:
    ticklabel.set_fontsize(24)
ax.spines['bottom'].set_linewidth(3)
ax.spines['right'].set_linewidth(3)
ax.spines['left'].set_linewidth(3)
ax.spines['top'].set_linewidth(3)


ax.set_xlim(-4,4)
ax.set_xticks(np.linspace(-4,4,5,endpoint=True))
ax.set_ylim(-4,4)
ax.set_yticks(np.linspace(-4,4,5,endpoint=True))

n=1024
X = np.random.normal(0,1,n)
Y = np.random.normal(0,1,n)
plt.scatter(X,Y)
plt.savefig('photo.png')
plt.show()
