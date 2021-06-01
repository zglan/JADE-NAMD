#!/usr/bin/python
import os
import sys
from operator import itemgetter
import re
import math
import shutil



#  ---------------------------------------------------------------------
#  Read the RICC2 output of Turbomole output
#  This subrountine is used to read the RICC output of Turbomole
#  Three Turbomole outputs files are involved.
#      (1) Grad.out --  Turbomole RICC output
#                       Read the number of basis functions (n_basis) 
#                       Read the number of occupied orbitals (n_occ)
#                       Calculate the number of virtual orbitals (n_vir)
#      (2) mos  --      MO coefficients (mo(i_mo, i_ao))
#  Two output files are:
#      (1) mos.dat      The MO coefficient
#      (2) ci.dat       Important CI vector
#-----------------------------------------------------------------------------------------   




#############################################################


#   Check the GS output
       
def check_gs_ricc():

    outputfile = 'dscf.out'
    if not os.path.isfile(outputfile):
        print "Ground-state calculation results do not exist!"
	print "Check the DFT calculation!"
	raise IOerror

    n_line = 0
    filein1=open('dscf.out','r')
    for line in filein1:
        n_line += 1
    filein1.close()
 
    line_each = []
    for i_line in range(n_line):
         line_each.append('')

    filein1=open('dscf.out','r')
    line_all=filein1.read()
    filein1.close()
    line_each=line_all.split('\n')
  
    for i_line in range(n_line):
        i_find_abnormal = re.search('abnormally', line_each[i_line])
        if  i_find_abnormal is not None:
            print "Ground-state calculation ends abnormally!"
	    print "Check the ground-state calculation!"
	    raise IOerror

#-----------------------------------------------------------------------------

#   Check the Gradient output

def check_grad_ricc():

    outputfile = 'grad.out'
    if not os.path.isfile(outputfile):
        print "Gradient calculation results do not exist!"
	print "Check the gradient calculation!"
	raise IOerror

    n_line = 0
    filein1=open('grad.out','r')
    for line in filein1:
        n_line += 1
    filein1.close()
 
    line_each = []
    for i_line in range(n_line):
         line_each.append('')

    filein1=open('grad.out','r')
    line_all=filein1.read()
    filein1.close()
    line_each=line_all.split('\n')
  
    for i_line in range(n_line):
        i_find_abnormal = re.search('abnormally', line_each[i_line])
        if  i_find_abnormal is not None:
            print "-------------------------------------------------------------------"		
            print "Gradient calculation ends abnormally!"
	    print "Check the gradient calculation!"
	    print "-------------------------------------------------------------------"
	    raise IOerror
        i_find_abnormal =  re.search('REFERENCE STATE IS UNSTABLE!', line_each[i_line])
	if  i_find_abnormal is not None:
            print "-------------------------------------------------------------------"		
	    print "Excited-state calculation ends abnormally!"
	    print "ERRORS:  REFERENCE STATE IS UNSTABLE!"
	    print "-------------------------------------------------------------------"
	    raise IOerror

#-----------------------------------------------------------------------------


#   Check the Single-point RICC  output

def check_energy_ricc():

    outputfile = 'ricc.out'
    if not os.path.isfile(outputfile):
        print "Single-point RICC calculation results do not exist!"
	print "Check the CC2 or ADC2 calculation!"
	raise IOerror

    n_line = 0
    filein1=open('ricc.out','r')
    for line in filein1:
        n_line += 1
    filein1.close()
 
    line_each = []
    for i_line in range(n_line):
         line_each.append('')

    filein1=open('ricc.out','r')
    line_all=filein1.read()
    filein1.close()
    line_each=line_all.split('\n')
  
    for i_line in range(n_line):
        i_find_abnormal = re.search('abnormally', line_each[i_line])
        if  i_find_abnormal is not None:
            print "Single-point RICC calculation ends abnormally!"
	    print "Check the CC2 or ADC2 calculation!"
	    raise IOerror
        i_find_abnormal =  re.search('REFERENCE STATE IS UNSTABLE!', line_each[i_line])
	if  i_find_abnormal is not None:
	    print "-------------------------------------------------------------------"
	    print "Excited-state calculation ends abnormally!"
	    print "ERRORS:  REFERENCE STATE IS UNSTABLE!"
	    print "-------------------------------------------------------------------"
	    raise IOerror


#-----------------------------------------------------------------------------




#############################################################################3






#   Read RICC output from Turbomole
def read_gradient_ricc(n_atom, n_state, index_state):

    n_line = 0
    filein3=open('gradient','r')
    for line in filein3:
        n_line += 1
    filein3.close()

    line_each = []
    for i_line in range(n_line):
        line_each.append('')

    filein3=open('gradient','r')
    line_all=filein3.read()
    filein3.close()
    line_each=line_all.split('\n')

    grad_x = [] 
    grad_y = []
    grad_z = []
    for i_atom in range(n_atom): 
        grad_x.append(0.0)
        grad_y.append(0.0)
        grad_z.append(0.0)

    i_line = 2 + n_atom
    for i_atom in range(n_atom):
       grad_x[i_atom] = line_each[i_line].split()[0]  
       grad_y[i_atom] = line_each[i_line].split()[1]
       grad_z[i_atom] = line_each[i_line].split()[2]
       i_line = i_line+1

    
    #  Write "gradient" file    
    fileout1=open('qm_gradient.dat', 'w')
    for i_atom in range(n_atom) :
        fileout1.write(''+str( grad_x [i_atom])+'   '+str( grad_y [i_atom])+'   '+str( grad_z [i_atom])+'  \n')

    

###################################################################


#  Read the number of basis sets and occupied MOs.
def read_energy_ricc (n_state, index_state):


    energy = []
    for i_energy in range(n_state):
        energy.append(0.0)
 
    if index_state == 1 :
       file_energy='ricc.out'
    else:
       file_energy='grad.out'    

    n_line = 0
    filein3=open(file_energy,'r')
    for line in filein3:
        n_line += 1
    filein3.close()
 
    line_each = []
    for i_line in range(n_line):
        line_each.append(0.0)
 
    filein3=open(file_energy,'r')
    line_all=filein3.read()
    filein3.close()
    line_each=line_all.split('\n')
 
    i_energy = 0
    for i_line in range(n_line):
        i_find_gs = ''
        i_find_gs_energy = ''
        i_find_gs = re.search('Final', line_each[i_line])
        if  i_find_gs is not None:
            i_find_gs_energy = re.search('energy', line_each[i_line])
            if i_find_gs_energy is not None: 
               print  line_each[i_line]
               energy[i_energy] = float(line_each[i_line].split()[5])
#            print energy[i_energy]
               i_energy = i_energy + 1     
        i_find_ex = ''
        i_find_ex_energy = ''
        i_find_ex = re.search('Energy:', line_each[i_line])
        if i_find_ex is not None:     
           print line_each[i_line]
           energy[i_energy] = float(line_each[i_line].split()[1])
           energy[i_energy] = energy[i_energy] + energy[0]
           i_energy = i_energy + 1
           if i_energy ==  n_state :
              break


# Write "gradient" file    
    fileout1=open('qm_energy.dat', 'w')
    for i_energy in range(n_state) :
        fileout1.write('S'+str( i_energy)+'   '+str( energy [i_energy])+'  \n')
    fileout1.close()

#---------------------------------------------------------------------------
#  Read the number of basis sets and occupied MOs.
def read_basis_ricc (index_state):



#   Check whether the current is ground state or not!
#   Then we should read "escf.out" or "grad.out"!
#   


    if index_state == 1 :
       basis_file = 'ricc.out'
    else:
       basis_file = 'grad.out'



#   If RICC2 is used, we set func =0   
#   If ADC2 is used, we set func=1


    n_line = 0
    filein1=open(basis_file,'r')
    for line in filein1:
        n_line += 1
    filein1.close()

    line_each = []
    for i_line in range(n_line):
        line_each.append(0.0)

    filein1=open(basis_file,'r')
    line_all=filein1.read()
    filein1.close()
    line_each=line_all.split('\n')

    

    func = 0
    for i_line in range(n_line):

        i_find_func = re.search('ADC', line_each[i_line])
        if i_find_func is not None:
           func = 1		

        i_find_basis = re.search('all together', line_each[i_line])   
        if  i_find_basis is not None:
            n_basis      = int(line_each[i_line].split()[3]) 
            n_vir_fro    = int(line_each[i_line-1].split()[3])
            n_vir_act    = int(line_each[i_line-2].split()[3])
            break

    filein1.close()
    n_vir = n_vir_fro + n_vir_act
    n_occ = n_basis - n_vir

#    print n_basis
#    print n_occ
#    print n_vir 


    fileout1=open('qm_basis.dat', 'w')
    fileout1.write('CC2 or ADC2?  0 (CC2),  1 (ADC2):   '+str(func)+'  \n' )
    fileout1.write('number of basis functions: '+str(n_basis)+'  \n')
    fileout1.write('number of occupied orbitals: '+str(n_occ)+'  \n')
    fileout1.close()

    return (n_basis, n_occ, n_vir, func)


# -------------------------------------------------------------------------
#   Read the MO coefficients
#   Every block of MOs contains four elements in each line.

def read_mo_ricc (n_basis):

    n_res=int(math.fmod(n_basis, 4))
    n_block = int((n_basis - n_res)/4)

    mo =[]
    for i_mo_1 in range(n_basis):
        mo.append([])
        for i_mo_2 in range(n_basis):
            mo[i_mo_1].append([])


    n_line = 0
    filein2=open('mos','r')
    for line in filein2:
        n_line += 1
    filein2.close()

    line_each = []
    for i_line in range(n_line):
        line_each.append(0.0)

    filein2=open('mos','r')
    line_all=filein2.read()
    filein2.close()
    line_each=line_all.split('\n')


    mo_energy = []
    for i_mo_1 in range(n_basis) :
        mo_energy.append(0.0)
    

    for i_line in range(n_line):
        i_find_mo = re.search('eigenvalue', line_each[i_line])
        if  i_find_mo is not None:
            for i_mo_1 in range(n_basis) :
#                print i_line, line_each[i_line]
                mo_energy[i_mo_1] = line_each[i_line].split()[2] 
#                print mo_energy
                i_line = i_line + 1                    
                i_mo_2 = 0
                for i_block in range(n_block) :
#                    print i_mo_1, i_mo_2, line_each[i_line]
                    mo[i_mo_1][i_mo_2] = line_each[i_line][0:20]
#                    print i_mo_1, i_mo_2
#                    print mo[i_mo_1][i_mo_2], line_each[i_line][19]
                    i_mo_2 = i_mo_2+1
                    mo[i_mo_1][i_mo_2] = line_each[i_line][20:40]
#                    print i_mo_1, i_mo_2
#                    print mo[i_mo_1][i_mo_2], line_each[i_line][20]
                    i_mo_2 = i_mo_2+1
                    mo[i_mo_1][i_mo_2] = line_each[i_line][40:60]
#                    print i_mo_1, i_mo_2
#                    print mo[i_mo_1][i_mo_2], line_each[i_line][40]
                    i_mo_2 = i_mo_2+1
                    mo[i_mo_1][i_mo_2] = line_each[i_line][60:80]
#                    print i_mo_1, i_mo_2
#                    print mo[i_mo_1][i_mo_2], line_each[i_line][60]
                    i_mo_2 = i_mo_2+1 
                    i_line = i_line+1
                if n_res > 0 :
                    for i_res in range(n_res): 
#                        i_mo_1 = i_mo_1
                        mo[i_mo_1][i_mo_2] = line_each[i_line][ i_res*20 : i_res*20+20]
                        i_mo_2 = i_mo_2+1
                    i_line = i_line + 1
            break
    filein2.close()
  
    fileout2=open('mo.dat', 'w')
    fileout2.write('#  MO coefficient (i_MO, j_AO, M_ij)    \n')
    for i_mo_1 in range(n_basis) :
        fileout2.write('MO:'+str(i_mo_1+1)+'   '+str(mo_energy[i_mo_1])+'\n')
        for i_mo_2 in range(n_basis) :  
            fileout2.write(''+str(i_mo_1+1)+'    '+str(i_mo_2+1)+'    '+str(mo[i_mo_1][i_mo_2])+' \n')            


# -------------------------------------------------------------------------
#   Read the CI vector from RICC calculations
# --------------------------------------------------------------------------------------------------


def read_ci_ricc (n_basis, n_occ, n_vir, n_state, index_state ):
    
    n_res=int(math.fmod(n_occ*n_vir, 4))
    n_block = int ((n_occ*n_vir - n_res)/4)

    print 'Begin to read the CI vector from RICC calculation output'
#    print n_basis, n_occ, n_vir, n_state
#    print n_block, n_res

    energy = []
    for i_state in range(n_state):
        energy.append([])

    element = []
    for i_ele in range(n_occ*n_vir) :
        element.append(0.0)

    ci =[]
    for i_state in range(n_state):
        ci.append([])
        for i_ci_1 in range(n_occ):
            ci[i_state].append([])
            for i_ci_2 in range(n_vir):
                ci[i_state][i_ci_1].append(0.0)
   
#   Read the CI vector

    if index_state == 1 :
       ci_file = 'ricc.out'
    else:
       ci_file = 'grad.out'

    n_line = 0
    filein3=open(ci_file,'r')
    for line in filein3:
        n_line += 1
    filein3.close()

    line_each = []
    for i_line in range(n_line):
        line_each.append(0.0)

    filein3=open(ci_file,'r')
    line_all=filein3.read()
    filein3.close()
    line_each=line_all.split('\n')


    i_state = 0
    for i_line in range(n_line):
        i_find_ci = re.search('Energy:', line_each[i_line])
        if  i_find_ci is not None:
            i_state = i_state + 1
            energy[i_state] = line_each[i_line].split()[1]
            print "Transition energy:", energy[i_state]
            i_line=i_line+6
            i_find_label = re.search('===============', line_each[i_line])
            if  i_find_label is not None:
                for i_conv in range(200):
                    i_line = i_line +1
                    i_find_label2 = re.search('===============', line_each[i_line])
                    if i_find_label2 is not None: 
                       break
                    else:
#                       print line_each[i_line]
                       i_ci_1 = int(line_each[i_line].split()[1])
                       i_ci_1 = i_ci_1 - 1 
#                       print i_ci_1
                       i_ci_2 = int(line_each[i_line].split()[5])
                       i_ci_2 = i_ci_2 - n_occ -1
#                       print i_ci_2
#                       print i_state, i_ci_1, i_ci_2
#                       print line_each[i_line].split()[9]
                       ci[i_state][i_ci_1][i_ci_2] = float (line_each[i_line].split()[9])  
#                       print i_state, i_ci_1, i_ci_2, ci[i_state][i_ci_1][i_ci_2]
    filein3.close()


#    for i_state in range(1,n_state):
#        print "Check normalization for State:", i_state+1 
#        norm = 0.0
#        for i_ci_1 in range(n_occ) :
#             for i_ci_2 in range(n_vir) :
#                 norm  =   norm + ci[i_state][i_ci_1][i_ci_2] * ci[i_state][i_ci_1][i_ci_2]
#        print "Norm before Normailzation: ", norm
#        for i_ci_1 in range(n_occ) :
#             for i_ci_2 in range(n_vir) :
#                 ci[i_state][i_ci_1][i_ci_2] = ci[i_state][i_ci_1][i_ci_2] / (math.sqrt(norm))
#        norm = 0.0
#        for i_ci_1 in range(n_occ) :
#             for i_ci_2 in range(n_vir) :
#                 norm  =   norm + ci[i_state][i_ci_1][i_ci_2] * ci[i_state][i_ci_1][i_ci_2]
#        print "Norm after Normalization:", norm  




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
#        print "Norm (Saved CI vector):", norm

    

        for i_index in range(n_index) :
            fileout3.write('S'+str(ci_info_state[i_index]['state'])+'  '+str(ci_info_state[i_index]['civector'])+'    '+str(ci_info_state[i_index]['index_occ'])+'   '+str(ci_info_state[i_index]['index_vir'])+'  '+str((ci_info_state[i_index]['prob']))+'    \n')

    fileout3.close()      







def collect_qm (n_atom, n_state, index_state):

     fileout3=open('qm_results.dat', 'w')

     fileout3.write('-----------------------------------------  \n')
     fileout3.write('Summary of QM calculations: \n')
     fileout3.write('-----------------------------------------  \n')

     filein4=open('turbomole_interface','r')
     fileout3.write(filein4.read())
     fileout3.write('-----------------------------------------  \n')  
     filein4.close()


     fileout3.write('The electronic calculations focus on '+str(n_state)+' states: \n')
     for i_state in range(n_state) :
         fileout3.write('S'+str(i_state)+ '   ..  ' )
     fileout3.write('\n')
     fileout3.write('The S'+str(index_state-1)+' gradient should be computed !   \n') 
     fileout3.write('-----------------------------------------  \n')


     fileout3.write('Basis information: \n')
     filein4=open('qm_basis.dat','r') 
     fileout3.write(filein4.read())
     fileout3.write('-----------------------------------------  \n')
     filein4.close()

     fileout3.write('Energy of electronic states: \n')
     filein4=open('qm_energy.dat','r')
     fileout3.write(filein4.read())  
     fileout3.write('-----------------------------------------  \n')
     filein4.close()

     fileout3.write('Gradient on S'+str(index_state-1)+'  \n')
     filein4=open('qm_gradient.dat','r')
     fileout3.write(filein4.read())  
     fileout3.write('-----------------------------------------  \n')
     filein4.close()
    
     
     fileout3.write('Nonadiabatic coupling elements  \n') 
     sourceFile = 'qm_nac.dat'
     if os.path.isfile(sourceFile):
          filein4=open('qm_nac.dat','r')
          fileout3.write(filein4.read())
          fileout3.write('-----------------------------------------  \n')
          filein4.close()
     else : 
          for i_state in range(n_state):
              for j_state in range(n_state):
                  fileout3.write('S'+str(i_state)+'    S'+str(j_state)+'   0.00000   \n')

     fileout3.write('-----------------------------------------  \n')               
     fileout3.close()
 
     
   
 

















