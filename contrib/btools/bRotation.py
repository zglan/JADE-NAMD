#! /usr/bin/env python

import math
import numpy as np


# various roation matrix and method
#

class bPlane:
    norm = []
    dist = 0
    

class bRotation:
    def __init__(self):

        return
    
    @staticmethod
    def make_plane(pA, pB, pC):
        """
        http://keisan.casio.com/exec/system/1223596129
        known: A, B, C: three points
        ax+by+cz+d=0
        v_norm = (a,b,c) = AB \cross AC
        d = -v_n \cdot A
        """
        AB = pB - pA
        AC = pC - pA
        norm = np.cross(AB, AC) # (a,b,c)
        d = - np.dot(norm, pA)
        return np.append(norm, d)


    @staticmethod
    def get_trans_mat4(vec):
        m = np.eye(4)
        m[0:3,3] = vec
        return m
    
    @staticmethod    
    def get_axis_theta(v1, v2):
        """
        give two vector, get rotation axis and rotation angle.
        """
        vi = v1[0:3]; vj = v2[0:3]
        vi = vi / np.linalg.norm(vi)
        vj = vj / np.linalg.norm(vj)
        axis = np.cross(vi, vj)
        if np.linalg.norm(axis) < 1.0e-15:
            print "vector i \cross j is zero !!!", vi, vj
            axis = np.array([0., 0., 1.])
            theta = 0.0
        else:    
            costheta = np.dot(vi, vj)
            theta = np.arccos(costheta)
        return axis, theta
        

    @staticmethod    
    def get_rot_mat3(axis, theta):
        """
        given two vector, get rot matrix
        vecter: axis; anti-clock angle: theta
        http://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
        http://www.cnblogs.com/graphics/archive/2012/08/08/2609005.html
        pull (a,b,c) to origin
        trans. mat.
        \begin{bmatrix}
		1 & 0 & 0 & -a \\
		0 & 1 & 0 & -b \\
		0 & 0 & 1 & -c \\
        0 & 0 & 0 &  1 \\
        \end{bmatrix}
        """
        m = np.zeros((4,4))
        axis = axis / np.linalg.norm(axis)
        cost = np.cos(theta); sint = np.sin(theta)
        x = axis[0]; y = axis[1]; z = axis[2]
        # http://blog.csdn.net/pizi0475/article/details/7932909
        m[0][0] = cost + x*x*(1-cost)
        m[0][1] = x*y*(1-cost) + z*sint
        m[0][2] = x*z*(1-cost) - y*sint
        m[0][3] = 0.0
        m[1][0] = x*y*(1-cost) - z*sint
        m[1][1] = cost + y*y*(1-cost)
        m[1][2] = z*y*(1-cost) + x*sint
        m[1][3] = 0.0
        m[2][0] = x*z*(1-cost) + y*sint
        m[2][1] = y*z*(1-cost) - x*sint
        m[2][2] = cost + z*z*(1-cost)
        m[2][3] = 0.0
        m[3][0] = 0.0
        m[3][1] = 0.0
        m[3][2] = 0.0
        m[3][3] = 1.0
        return m
    
        
        
    # POINT ROTATE around arbitary vector
    # P is the point, A is arbitary vector
    # P' = Pcostheta + (A cross P)sintheta + A(AdotP)(1 - costheta)
    # http://www.cppblog.com/wicbnu/archive/2009/08/13/93215.html
    @staticmethod
    def rotate_ar_vector(point, vector, theta):
        """ point rotate around arbitary vector by theta angle """
        v = vector / np.linalg.norm(vector)
        p1 = point * np.cos(theta)
        p2 = np.cross(v, point) * np.sin(theta)
        p3 = v * np.dot(v, point) * (1-np.cos(theta))
        p = p1 + p2 + p3
        return p		
    
    @staticmethod
    def get_rot_mat3(axis, theta):
        """
        http://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
        Rodrigues' rotation formula
        R = cos\theta I + sin\theta ux + (1-cos\theta)u\circle u
        """
        axis = axis / np.linalg.norm(axis)
        cost = np.cos(theta); sint = np.sin(theta)
        x = axis[0]; y = axis[1]; z = axis[2]
        t = np.array([[x*x, x*y, x*z],
                      [x*y, y*y, y*z],
                      [x*z, y*z, z*z]])
        c = np.array([[ 0, -z,  y],
                      [ z,  0, -x],
                      [-y,  x,  0]])
                           
        i = np.eye(3)
        m = cost * i + sint * c + (1-cost) * t 
        
        return m
        
    @staticmethod
    def get_rot_mat4(axis, theta):
        """
        axis, theta is the rotation axis and angle
        """
        m = np.eye(4)
        m[0:3,0:3] = bRotation.get_rot_mat3(axis, theta)
        return m   

    @staticmethod
    def get_mat4(axis, theta, vt):
        m = bRotation.get_rot_mat4(axis, theta)
        m[0:3,3] = vt
        return m
        
    @staticmethod
    def get_rot_mat3v(v1, v2):
        """
        v1 v2 is the directional vector
        rotation from v1 to v2
        that means
        v2 = M * v1
        """
        axis, theta = bRotation.get_axis_theta(v1, v2)
        m = bRotation.get_rot_mat3(axis, theta)        
        return m
        
        
    @staticmethod
    def get_rot_mat4v(v1, v2):
        """
        v1 v2 is the directional vector
        and
        rotation from v1 to v2
        v2 = M * v1
        """
        axis, theta = bRotation.get_axis_theta(v1, v2)
        #print axis, theta
        m = bRotation.get_rot_mat4(axis, theta)        
        return m
        
    @staticmethod
    def get_mat4v(v1, v2, vt):
        m = bRotation.get_rot_mat4v(v1, v2)
        m[0:3,3] = vt
        return m
        
    @staticmethod    
    def get_mat4t(v1, v2, t1, t2):
        """
        t1: start point, t2: end point
        v1: start , v2: ref. end. target.
        """
        vt = t2 - t1
        m = bRotation.get_mat4v(v1, v2, vt)
        return m
        
    
    @staticmethod
    def euler_to_matrix(a, b, c, out):
        return
# static inline void
# euler_to_matrix(double a, double b, double c, mat_t *out)
# {
	# double sina = sin(a), cosa = cos(a);
	# double sinb = sin(b), cosb = cos(b);
	# double sinc = sin(c), cosc = cos(c);

	# out->xx =  cosa * cosc - sina * cosb * sinc;
	# out->xy = -cosa * sinc - sina * cosb * cosc;
	# out->xz =  sinb * sina;
	# out->yx =  sina * cosc + cosa * cosb * sinc;
	# out->yy = -sina * sinc + cosa * cosb * cosc;
	# out->yz = -sinb * cosa;
	# out->zx =  sinb * sinc;
	# out->zy =  sinb * cosc;
	# out->zz =  cosb;
# }

# static inline void
# matrix_to_euler(const mat_t *rotmat, double *ea, double *eb, double *ec)
# {
	# double a, b, c, sinb;

	# b = acos(rotmat->zz);
	# sinb = sqrt(1.0 - rotmat->zz * rotmat->zz);

	# if (fabs(sinb) < 1.0e-7) {
		# a = atan2(-rotmat->xy, rotmat->xx);
		# c = 0.0;
	# }
	# else {
		# a = atan2(rotmat->xz, -rotmat->yz);
		# c = atan2(rotmat->zx, rotmat->zy);
	# }

	# *ea = a, *eb = b, *ec = c;
# }
        
    def get_dist(self):
        """
        http://en.wikipedia.org/wiki/Distance_from_a_point_to_a_plane
        http://mathworld.wolfram.com/Point-PlaneDistance.html
        """
        r = np.linalg.norm(P[0:2])
        x = a * x0 + b * y0 + c * z0 + d
        
        return x / r
        

if __name__ == "__main__":
    br = bRotation()
    point = np.array([1, -1, 0])
    vector = np.array([1, 0, 0])
    theta = np.pi/2
    print br.rotate_ar_vector(point, vector, theta)
    m = br.get_rot_mat(vector, theta)
    print m
    print br.get_rot_mat2(vector, theta)
    print np.dot(m, np.transpose(point))
    # pa = np.array([1, 0, 0])
    # pb = np.array([0, 0, 0])
    # pc = np.array([0, 1, 0])
    # print br.make_plane(pa, pb,pc)
    
    
    
    
