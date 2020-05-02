import numpy as np
import os
import math 

def distance(AB):
    dis = math.sqrt(AB[0]**2 + AB[1]**2 + AB[2]**2)
    return dis
def cross_product(AB,BC):
    n = [AB[1]*BC[2]-AB[2]*BC[1],AB[2]*BC[0]-AB[0]*BC[2],AB[0]*BC[1]-AB[1]*BC[0]]
    return n

def dot_product(AB,BC):
    m = AB[0]*BC[0] + AB[1]*BC[1] + AB[2]*BC[2]
    return m

def normal(AB):
    dis = distance(AB)
    nor = [i/dis for i in AB]
    return nor

def read_xyz(filename='geo.xyz'):
    """ read in xyz format in au """
    fpin = open(filename, "r")
    line = fpin.readline()
    natom = int(line)
    line = fpin.readline()
    atom = []
    for j in range(natom):
        line = fpin.readline()
        rec = line.split()
        atomname, x, y, z= rec[0:4]
        record = {'name': atomname, 'coord': [float(x),float(y),float(z)]}
        atom.append(record)
    fpin.close()

    return atom
def get_dist(atom1,atom2):
    atom = read_xyz()
    coord1 = atom[atom1-1]['coord']
    coord2 = atom[atom2-1]['coord']
    AB = [j-i for i,j in zip(coord1,coord2)]
    dist = distance(AB)
    return dist
def get_angle(atom1,atom2,atom3):
    atom = read_xyz()
    coord1 = atom[atom1-1]['coord']
    coord2 = atom[atom2-1]['coord']
    coord3 = atom[atom3-1]['coord']
    BA = [j-i for i,j in zip(coord2,coord1)]
    BC = [j-i for i,j in zip(coord2,coord3)]
    BA_dis = distance(BA)
    BC_dis = distance(BC)
    BaBc = dot_product(BA,BC)
    angle = (math.acos(BaBc/(BA_dis*BC_dis)))/math.pi*180

    return angle

def get_dihedral(atom1,atom2,atom3,atom4):
    atom = read_xyz()
    coord1 = atom[atom1-1]['coord']
    coord2 = atom[atom2-1]['coord']
    coord3 = atom[atom3-1]['coord']
    coord4 = atom[atom4-1]['coord']

    AB = [j-i for i,j in zip(coord1,coord2)]
    BC = [j-i for i,j in zip(coord2,coord3)]
    CD = [j-i for i,j in zip(coord3,coord4)]

    n_ABC = cross_product(AB,BC)
    n_ABC_nor = normal(n_ABC)
    n_BCD = cross_product(BC,CD)
    n_BCD_nor = normal(n_BCD)

    cos_theta = dot_product(n_ABC_nor,n_BCD_nor)
    theta = math.acos(cos_theta)/math.pi*180

    DD = cross_product(n_ABC,n_BCD)
    par = dot_product(BC,DD)
#    if par < 0:
#        theta = -theta
    return theta


if __name__ == "__main__":
    read_xyz()
    get_dist(1,2)
    get_angle(3,1,2)
    get_dihedral(3,1,2,6) 
    get_dihedral(3,1,2,5) 
    get_dihedral(4,1,2,6) 
    get_dihedral(4,1,2,5) 
