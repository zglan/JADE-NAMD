#!/usr/bin/python
import os
import sys
from operator import itemgetter
import re
import math
import shutil




#   Read the CI vector  for hybrid functional with TDA approximation

def read_ci_hy_tda (n_basis, n_occ, n_vir, n_state ):
    
    n_res=int(math.fmod(n_occ*n_vir, 4))
    n_block = int ((n_occ*n_vir - n_res)/4)

    print 'Begin to read the CI vector from ciss_a (hybrid functional with TDA approximation)'
#    print n_basis, n_occ, n_vir, n_state
#    print n_block, n_res

    energy = []
    for i_state in range(n_state):
        energy.append([])

    element = []
    for i_ele in range(n_occ*n_vir) :
        element.append(0.0)

    Xvector = []
    for i_ci_1 in range(n_occ):
         Xvector.append([])
         for i_ci_2 in range(n_vir):
             Xvector[i_ci_1].append([])

#   Please note that Yvector is not used here.
    Yvector = []
    for i_ci_1 in range(n_occ):
         Yvector.append([])
         for i_ci_2 in range(n_vir):
             Yvector[i_ci_1].append([])

 

    ci =[]
    for i_state in range(n_state):
        ci.append([])
        for i_ci_1 in range(n_occ):
            ci[i_state].append([])
            for i_ci_2 in range(n_vir):
                ci[i_state][i_ci_1].append(0.0)
   
#   Read the CI vector

    n_line = 0
    filein3=open('ciss_a','r')
    for line in filein3:
        n_line += 1
    filein3.close()

    line_each = []
    for i_line in range(n_line):
        line_each.append(0.0)

    filein3=open('ciss_a','r')
    line_all=filein3.read()
    filein3.close()
    line_each=line_all.split('\n')


    for i_line in range(n_line):
        i_find_ci = re.search('eigenpairs', line_each[i_line])
        if  i_find_ci is not None:
            i_line=i_line+1
            for i_state in range(1,n_state) :
                energy[i_state] = line_each[i_line].split()[3]
                print "Transition energy:", energy[i_state] 
                i_line = i_line+1
                i_ele=0
                for i_block in range(n_block) :
                    element[i_ele]=line_each[i_line][0:20]
#                    print i_ele, element[i_ele], i_line
                    i_ele=i_ele+1 
                    element[i_ele]=line_each[i_line][20:40]
#                    print i_ele, element[i_ele], i_line
                    i_ele=i_ele+1
                    element[i_ele]=line_each[i_line][40:60]
#                    print i_ele, element[i_ele], i_line
                    i_ele=i_ele+1
                    element[i_ele]=line_each[i_line][60:80]
#                    print i_ele, element[i_ele], i_line
                    i_ele=i_ele+1
                    i_line=i_line+1
                if n_res > 0 :
                    for i_res in range(n_res) :
                        element[i_ele] = line_each[i_line][i_res*20 : (i_res+1)*20]
#                        print i_ele, element[i_ele], i_line 
                        i_ele=i_ele+1
                    i_line=i_line+1
                
                for i_ci_1 in range(n_occ) :
                     for i_ci_2 in range(n_vir) :
                        i_ele = i_ci_1 * n_vir + i_ci_2 
#                        print i_ele, element[i_ele], element [i_ele+ n_occ*n_vir]
                        Xvector[i_ci_1][i_ci_2] = re.sub('D', 'E', element[i_ele])
                        Xvector[i_ci_1][i_ci_2] = float (Xvector[i_ci_1][i_ci_2] )
                        ci[i_state][i_ci_1][i_ci_2] = Xvector[i_ci_1][i_ci_2]
    filein3.close()


    for i_state in range(1,n_state):
        print "Check normalization for State:", i_state+1 
        norm = 0.0
        for i_ci_1 in range(n_occ) :
             for i_ci_2 in range(n_vir) :
                 norm  =   norm + ci[i_state][i_ci_1][i_ci_2] * ci[i_state][i_ci_1][i_ci_2]
        print "Norm before Normailzation: ", norm
        for i_ci_1 in range(n_occ) :
             for i_ci_2 in range(n_vir) :
                 ci[i_state][i_ci_1][i_ci_2] = ci[i_state][i_ci_1][i_ci_2] / (math.sqrt(norm))
        norm = 0.0
        for i_ci_1 in range(n_occ) :
             for i_ci_2 in range(n_vir) :
                 norm  =   norm + ci[i_state][i_ci_1][i_ci_2] * ci[i_state][i_ci_1][i_ci_2]
        print "Norm after Normalization:", norm  






    fileout3=open('ci.dat', 'w')
    fileout3.write('#  State, CI vector, i_occ, j_vir,  |Coeff^2|)    \n')
    if n_occ*n_vir  > 20 :
        n_index = 20
    else :
        n_index =  n_occ*n_vir 

#   Find the most important CI vector

    print "CI vector"
    ci_info_state = []
    for i_all in range(n_occ*n_vir) :
        ci_info_state.append([])


#    ci_dict = {}
    for i_state in range(1,n_state) :
        i_all=0
        for i_ci_1 in range(n_occ) :
            for i_ci_2 in range(n_vir) :
                ci_dict= {}
#             ci_vector_value[i_ci_1][i_ci_2] = float(re.sub('D', 'E', ci[i_ci_1][i_ci_2])) 
                ci_dict['state'] = i_state
                ci_dict['index'] = i_ci_1 * n_vir + i_ci_2+1
                ci_dict['civector'] = ci[i_state][i_ci_1][i_ci_2]
                ci_dict['prob'] = math.pow(ci[i_state][i_ci_1][i_ci_2] ,2)
#                print ci[i_state][i_ci_1][i_ci_2]
                ci_dict['index_occ'] = i_ci_1 + 1
                ci_dict['index_vir'] = i_ci_2 + 1 + n_occ
                ci_info_state[i_all]=ci_dict
#                print "ci_dict", ci_dict
#                print "ci_all", i_all, ci_info_state[i_all]
#                if i_all > 0 :
#                   print "ci_all", i_all-1, ci_all[i_all-1] 
                i_all=i_all+1 
                

#        print "Before sort"
#        for i_all in range(n_occ*n_vir) :
#            print i_all, ci_info_state[i_all]

        ci_info_state = sorted(ci_info_state, key=itemgetter('prob'), reverse=True)

#        print "After sort"
#        print ci_info_state[i_all]


        norm = 0.0
        for i_index in range(n_index) :
            norm  =   norm + ci_info_state[i_index]['civector']**2
        print "Norm (Saved CI vector):", norm

    

        for i_index in range(n_index) :
            fileout3.write('S'+str(ci_info_state[i_index]['state'])+'  '+str(ci_info_state[i_index]['civector'])+'    '+str(ci_info_state[i_index]['index_occ'])+'   '+str(ci_info_state[i_index]['index_vir'])+'  '+str((ci_info_state[i_index]['prob']))+'    \n')

    fileout3.close()      





