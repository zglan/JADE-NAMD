import sub_inp_json as json 
import os
from os import system
import numpy as np
import shutil
import subprocess 
import multiprocessing
import time
import itertools
import copy

def exch_singl(atoms,i,exch):

    atoms[[(exch[i][0]-1),(exch[i][1]-1)],:] =  atoms[[(exch[i][1]-1),(exch[i][0]-1)],:]
    return atoms

def exch_atom(coord,exch,list1,natom):
    """ exchange the coordinate in the atoms"""
    list2 = []
    change_save = []
    per = 1
    for i in range(1,len(list1)+1):
        iter = itertools.combinations(list1,i)
        list2.append(list(iter))

    for i in range(len(list2)):
        na = list2[i]
        for j in range(len(na)):
            nb = na[j]
            atoms = copy.deepcopy(coord)
            for k in range(len(nb)):
                atoms = exch_singl(atoms,int(nb[k])-1,exch)
            change_save.append(atoms)
            per = per + 1
    return change_save
def Exch(coord):
    inp = json.load_json('inp.json')
    exch = []
    exch = eval(inp['exch_matrix'].encode('utf-8'))
    list1 = inp['exch_list']
    natom = inp['n_atom']
    list2 = []
    change_save = []
    change_save = exch_atom(coord,exch,list1,natom)
    return change_save
def Chara(coord):
    atoms = copy.deepcopy(coord)
    for i in range(np.shape(atoms)[0]):
        atoms[i][2] = -atoms[i][2]
    return atoms


if __name__ == '__main__': 
    coord = np.loadtxt('inp.xyz')
    Charality(coord)
#    Exch(coord)
#    job2 = charality()
#    job2.chara_chage()
