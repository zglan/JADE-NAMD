from math import *
import numpy as np

# MATRIX 3D MAN.


# FUNCTION:
# obtain 4v movable matrix
# Formula: R*A(old) = E(new), so R=A^-1; T*O(old)=zero(new), so T=-O
# use R*T to obtain & make the 4v matrix for rot. and trans.
# variable:
# origin is the coordinate of the new orgin in old axis system
# Pa, Pb, Pc ; the three point to define the new axis
# axis x: PaPb; axis z: PaPb X PaPc; axis y: x X z
def get_rt_mat(origin, Pa, Pb, Pc):
	
	# define the vector for new axis
	# the x y z axis
	vab = np.subtract(Pb, Pa)
	vac = np.subtract(Pc, Pa)
	vz = np.cross(vab, vac)
	# the origin 
	vtrans = np.negative(origin)	
	
	# the normalized new x y z vector in old axis represent
	ex = vab/np.sqrt(np.dot(vab,vab))
	ez = vz/np.sqrt(np.dot(vz,vz))	
	vy = np.cross(vz, ex)
	ey = vy/np.sqrt(np.dot(vy, vy))
	# print "the normalized x y z vector:"
	# print ex
	# print ey
	# print ez
	
	# Make the rot. mat.
	matA = np.array([ex,ey,ez])	
	# print "mat. A before transpose (xyz in row represent:"
	# print matA
	matA = matA.transpose()
	# print "mat. A after transpose, the coordinate axis (xyz in col):"
	# print matA
	matR = np.linalg.inv(matA)
	# print "after inv, the real rotation matrix (in row):"
	# print matR
	
	# try to make 4v rot. mat.
	ex = np.append(matR[:,0], 0)
	ey = np.append(matR[:,1], 0)
	ez = np.append(matR[:,2], 0)
	trans = np.array([0.0, 0.0, 0.0, 1.0])	
	matR4v = np.array([ex,ey,ez,trans])	
 	matR4v= matR4v.transpose()
	# print "final 4v rot. mat.:"
	# print matR4v
	
	# try to make 4v trans. mat.
	matT4v = np.array([[1.0, 0.0, 0.0,vtrans[0]], [0.0, 1.0, 0.0, vtrans[1]], [0.0, 0.0, 1.0, vtrans[2]], [0.0, 0.0, 0.0, 1.0]])
	# print "final 4v trans. mat.:"
	# print matT4v
	
	# try to get the final 4v mat. ( R * T mat.)
	move4v = np.dot(matR4v, matT4v)
	# print "final 4v R*T mat.:"
	# print move4v
	
	# for checking by users
	a = np.dot(move4v, pto4v(Pa))
	b = np.dot(move4v, pto4v(Pb))
	c = np.dot(move4v, pto4v(Pc))
	# print "the input Pa Pb Pc in new axis (shown in order: new old):"
	# print Pa, a.reshape(1,4)
	# print Pb, b.reshape(1,4)
	# print Pc, c.reshape(1,4)
	
	return move4v


def pto4v(point):
	p4 = np.append(point, 1.0).reshape(4,1)
	return p4
	
# default is 1x3 vector
def get_new_point(point, move4v):
	""" move a point. one may need to reshape to 3x1 vector, default is 1x3 vector. """
	pointx = pto4v(point)
	new_pointx = np.dot(move4v,pointx)
	
	point3 = new_pointx[0:3]
	# print "old_p4, new_p4, point3:"
	# print pointx
	# print new_pointx
	# print point3
	
	return point3
	
# POINT ROTATE around arbitary vector
# P is the point, A is arbitary 
# P' = Pcostheta + (A cross P)sintheta + A(AdotP)(1 - costheta)
# http://www.cppblog.com/wicbnu/archive/2009/08/13/93215.html
def point_rotate_ar_vector(point, vector, theta):
	""" point rotate around arbitary vector by theta degree angle """
	d = sqrt(np.dot(vector, vector))
	v = np.divide(vector, d)
	p1 = np.multiply(point, cos(theta))
	vcap = np.cross(v, point)
	p2 = np.multiply(vcap, sin(theta))
	dap = np.dot(v, point)*(1-cos(theta))
	p3 = np.multiply(v, dap)
	p = np.add(p1, p2)
	p = np.add(p, p3)
	return p		
