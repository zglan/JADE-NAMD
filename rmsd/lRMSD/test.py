import numpy
import lrmsd
xyz1=numpy.array([[0.,1.1],[0.,1.],[0.,1.]],dtype=float)
xyz1_T = xyz1.T
xyz2=numpy.array([[0.,1.],[0.,2.2],[0.,1.1]],dtype=float)
xyz2_T = xyz2.T
xyz3=numpy.zeros((3,2))
#r=0.
r= numpy.array([0.])
lrmsd.sub_whole_overlap(xyz1,xyz2,r)

print r[0]
print xyz2
