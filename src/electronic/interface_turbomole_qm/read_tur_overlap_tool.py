#!/usr/bin/python
import os
import sys
from operator import itemgetter
import re
import math

#  ---------------------------------------------------------------------
#  Read the Turbomole DFT calculations of double-molecule calculation 
#  Read the overlap matrix between Geom R and Geom R+dR
#  Three Turbomole outputs files are involved.
#      (1) dscf.out --  Turbomole DFT output
#                       Read the number of basis functions (n_basis) 
#                       Read the number of occupied orbitals (n_occ)
#                       Calculate the number of virtual orbitals (n_vir)
#                       Read the overlap matrix
#  One output files is:
#      (1) ao_overlap.dat      The overlap matrix between Geom R and Geom R+dR
#-----------------------------------------------------------------------------------------   


#---------------------------------------------------------------------------
#   Read the MO coefficients
#   Every block of MOs contains four elements in each line.

def read_ao_overlap () :


    n_double_basis = 0	 
    filein1=open('dscf.out','r')
    filein1.readline()
    for line in filein1:
        i_find_basis = re.search('number of basis functions', line)
        if  i_find_basis is not None:
            n_double_basis=int(line.split()[-1])
            break
    filein1.close()
    if n_double_basis == 0 :
        print "Check the calculation of AO overlap!"
#	break

    n_basis = n_double_basis / 2
    n_ele = (n_double_basis*n_double_basis - n_double_basis)/2 + n_double_basis
    n_res= int(math.fmod(n_ele, 3))
    n_block = int( (n_ele-n_res)/3 )

    mo_overlap =[]
    for i_mo_1 in range(n_double_basis):
        mo_overlap.append([])
        for i_mo_2 in range(n_double_basis):
            mo_overlap[i_mo_1].append([])



    element = []
    for i_ele in range(n_ele) :
        element.append(0.0)


    n_line = 0
    filein2=open('dscf.out','r')
    for line in filein2:
        n_line += 1
    filein2.close()

    line_each = []
    for i_line in range(n_line):
        line_each.append(0.0)




    filein2=open('dscf.out','r')
    line_all=filein2.read()
    filein2.close()
    line_each=line_all.split('\n')


    mo_energy = []
    for i_mo_1 in range(n_basis) :
        mo_energy.append(0.0)
    

    for i_line in range(n_line):
        i_find_mo = re.search('OVERLAP', line_each[i_line])
        i_line = i_line+2
        if  i_find_mo is not None:
            i_ele = 0
            for i_block in range(n_block) :
                for i_res in range(3):
#                    print n_block, i_block, i_line, i_res, line_each[i_line].split()[i_res]
                    element[i_ele] = line_each[i_line].split()[i_res]
#                    print i_ele, element[i_ele]
                    i_ele = i_ele + 1
                i_line = i_line + 1
            if n_res > 0 :
#                print "n_res", n_res
                for i_res in range(n_res):
#                    print "i_res", i_res
                    element[i_ele] = line_each[i_line].split()[i_res]
#                    print i_ele, element[i_ele]
                    i_ele = i_ele +1
                i_line = i_line + 1
            break

    i_ele = 0  
    for i_mo_1 in range (n_double_basis) :
#        print "i_mo_1", i_mo_1
        for i_mo_2 in range(i_mo_1+1) :
#             print "element", element[i_ele]
             mo_overlap[i_mo_1][i_mo_2] = element[i_ele]
             mo_overlap[i_mo_2][i_mo_1] = element[i_ele]
#             print i_mo_1, i_mo_2,  mo_overlap[i_mo_1][i_mo_2]
             i_ele = i_ele + 1


    fileout2=open('ao_overlap.dat', 'w')
    fileout2.write('#  Overlap between R and R+dR : i_MO_R, j_MO_R+dR, S_ij  \n')
    for i_mo_1 in range(n_basis) :
        for i_mo_2 in range(n_basis) :  
            fileout2.write(''+str(i_mo_1+1)+'    '+str(i_mo_2+1)+'    '+str(mo_overlap[i_mo_1][i_mo_2+n_basis])+' \n')            


    fileout3=open('overlap_all.dat', 'w')
    fileout3.write('#  All Overlap: i_MO, j_MO, S_ij  \n')
    for i_mo_1 in range(2*n_basis) :
        for i_mo_2 in range(2*n_basis) :
            fileout3.write(''+str(i_mo_1+1)+'    '+str(i_mo_2+1)+'    '+str(mo_overlap[i_mo_1][i_mo_2])+' \n')



 
