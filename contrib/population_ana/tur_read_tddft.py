#!/usr/bin/python
import os
import sys
from operator import itemgetter
import re
import math
import shutil





#  ---------------------------------------------------------------------
#  Generate the TDDFT input for Turbomole
#-----------------------------------------------------------------------------------------   



#  Run Turbomle calculation after the time zero
def tur_read () :


#   Run Turbomole output 
#   Check whether the calculations finish correctly.

    check_dft()
    check_escf()

#   Check the number of atoms
    n_atom = check_natom ()
  


#   Read Basis
    n_basis_all = read_basis (n_atom)
    func    =  n_basis_all[0]
    n_atom  =  n_basis_all[1]
    n_basis =  n_basis_all[2]
    n_occ   =  n_basis_all[3]
    n_vir   =  n_basis_all[4]
    n_state =  n_basis_all[5]


    #n_state  = 5
    

#   Read Energies
    read_energy (n_state)

#   Read MO
    read_mo (n_basis)

    
    if  func == 0 :
        read_ci_pure (n_basis, n_occ, n_vir, n_state )
    if  func == 1 :
        read_ci_hybrid (n_basis, n_occ, n_vir, n_state )
    if  func == 2 :
        read_ci_hy_tda (n_basis, n_occ, n_vir, n_state )
    if  func == 3 :
        read_ci_hy_tda (n_basis, n_occ, n_vir, n_state )


    collect_qm (n_atom, n_state)


    print 'Finish to read TDDFT output from Turbomole'






#  ---------------------------------------------------------------------
#  Read the TDDFT output of Turbomole output
#  This subrountine is used to read the TDDFT output of Turbomole
#  Three Turbomole outputs files are involved.
#      (1) Grad.out --  Turbomole TDDFT output
#                       Read the number of basis functions (n_basis) 
#                       Read the number of occupied orbitals (n_occ)
#                       Calculate the number of virtual orbitals (n_vir)
#      (2) mos  --      MO coefficients (mo(i_mo, i_ao))
#      (3) sing_a  --   The X and Y vector in Turbomole output
#                       This file is use to reconstruct the CIS-type wavefunction
#                       from TDDFT results.
#                       Please note that the pure and hybrid functionals have different
#                       dimension in sing_a. For pure functionals, only X vector is given. 
#                       For hybrid functionals, both of them are given.
#  Two output files are:
#      (1) mos.dat      The MO coefficient
#      (2) ci.dat       Important CI vector
#-----------------------------------------------------------------------------------------   




#############################################################

#   Check the DFT and TDDFT output


#   Check the DFT output
       
def check_dft():

    outputfile = 'dscf.out'
    if not os.path.isfile(outputfile):
        print "DFT calculation results do not exist!"
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
            print "DFT calculation ends abnormally!"
	    print "Check the DFT calculation!"
	    raise IOerror

#-----------------------------------------------------------------------------


#   Check the Single-point TDDFT (escf)  output

def check_escf():

    outputfile = 'escf.out'
    if not os.path.isfile(outputfile):
        print "Single-point TDDFT (escf) calculation results do not exist!"
	print "Check the ESCF calculation!"
	raise IOerror

    n_line = 0
    filein1=open('escf.out','r')
    for line in filein1:
        n_line += 1
    filein1.close()
 
    line_each = []
    for i_line in range(n_line):
         line_each.append('')

    filein1=open('escf.out','r')
    line_all=filein1.read()
    filein1.close()
    line_each=line_all.split('\n')
  
    for i_line in range(n_line):
        i_find_abnormal = re.search('abnormally', line_each[i_line])
        if  i_find_abnormal is not None:
            print "Single-point TDDFT (escf) calculation ends abnormally!"
	    print "Check the ESCF calculation!"
	    raise IOerror
        i_find_abnormal =  re.search('REFERENCE STATE IS UNSTABLE!', line_each[i_line])
	if  i_find_abnormal is not None:
	    print "-------------------------------------------------------------------"
	    print "Excited-state calculation ends abnormally!"
	    print "ERRORS:  REFERENCE STATE IS UNSTABLE!"
	    print "-------------------------------------------------------------------"
	    raise IOerror


#-----------------------------------------------------------------------------


def check_natom():

    outputfile = 'coord'
    if not os.path.isfile(outputfile):
        print "The coordinate file does not exist!"
        print "Check the file 'coord'!"
        raise IOerror

    n_line = 0
    filein1=open('coord','r')
    for line in filein1:
        n_line += 1
    filein1.close()

    line_each = []
    for i_line in range(n_line):
         line_each.append('')

    filein1=open('coord','r')
    line_all=filein1.read()
    filein1.close()
    line_each=line_all.split('\n')

     
    for i_line in range(n_line):
        i_find_coord = re.search('\$coord', line_each[i_line])
        if  i_find_coord is not None:
            i_atom = 0
            for i in range(10000000):
                i_line=i_line+1
                i_find_stop = re.search('\$', line_each[i_line])              
                if  i_find_stop is not None:
                    break
                else :   
                    i_atom = i_atom + 1 
                      

    n_atom = i_atom
#    print n_atom  
    return (n_atom) 

#############################################################################3






###################################################################


#  Read the number of electronic states, s, occupied MOs.
def read_energy (n_state):


    energy = []
    for i_energy in range(n_state):
        energy.append(0.0)
 
    n_line = 0
    filein3=open('escf.out','r')
    for line in filein3:
        n_line += 1
    filein3.close()
 
    line_each = []
    for i_line in range(n_line):
        line_each.append(0.0)
 
    filein3=open('escf.out','r')
    line_all=filein3.read()
    filein3.close()
    line_each=line_all.split('\n')
 
    i_energy = 0
    for i_line in range(n_line):
        i_find_energy = re.search('Total energy', line_each[i_line])
        if  i_find_energy is not None:
#            print  line_each[i_line]
            energy[i_energy] = line_each[i_line].split()[2]
#            print energy[i_energy]
            i_energy = i_energy + 1           
        if i_energy == n_state :
           break

# Write "gradient" file    
    fileout1=open('qm_energy.dat', 'w')
    for i_energy in range(n_state) :
        fileout1.write('S'+str( i_energy)+'   '+str( energy [i_energy])+'  \n')
    fileout1.close()

#---------------------------------------------------------------------------
#  Read the number of basis sets and occupied MOs.
def read_basis (n_atom):
    """ dimentional dat """
    
    basis_file = 'escf.out'

    # DFT OR HF
    HF_OR_DFT = "HF"
    filein1=open(basis_file,'r')
    filein1.readline()
    for line in filein1:
        i_find_functional = re.search('FOUND DFT-FLAG', line)
        if (i_find_functional is not None):			  
            HF_OR_DFT = "DFT"
            break
    filein1.close()

    #   Check whether the hybrid functional is used
    #   By default we suppose to use pure functional (func = 0)    
    # pure functionals without tda; func = 0
    func = 0
    
#   If hybrid functional is used, func = 1
    filein1=open(basis_file,'r')
    filein1.readline()
    for line in filein1:
        i_find_functional = re.search('hybrid', line)
        if i_find_functional is not None:
            func = 1
            break
    filein1.close()

    #	hybrid functional + TDA 
    #	func = 3 
    #	Read ciss_a
    if func == 1 and HF_OR_DFT == "DFT":
        filein1=open(basis_file,'r')
        filein1.readline()
        for line in filein1:
            i_find_tda = re.search('TAMM-DANCOFF-APPROXIMATION',line)
            if i_find_tda is not None:
                func = 3
                break
        filein1.close() 

    # pure functional + tda
    # read ciss_a
    if func == 0 and HF_OR_DFT == "DFT":
        filein1=open(basis_file,'r')
        filein1.readline()
        for line in filein1:
            i_find_tda = re.search('TAMM-DANCOFF-APPROXIMATION',line)
            if i_find_tda is not None:
                func = 2
                break
        filein1.close()


    # cis
#   Read ciss_a
    if func == 0 and HF_OR_DFT == "HF":
        filein1=open(basis_file,'r')
        filein1.readline()
        for line in filein1:
            i_find_tda = re.search('TAMM-DANCOFF-APPROXIMATION',line)
            if i_find_tda is not None:
                func = 2
                break
        filein1.close()

    # if tda is not used & method is hf.
    # this would be tdhf
    # use hyb_dft func type
    if func < 2 and HF_OR_DFT == "HF":
        func = 1


#  When hybrid functional is used, check whether the TDA approximation is used!
#  Please note that TDA approximation and pure functional give same size of sing_a

#   Read the number of coordinates
    
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
 #   print "line_each", line_each[0]

    label = "NONSTOP"
    atom = [] 
    i_atom = 0
    for i_line in range(n_line):
        if label == "STOP" :
           break
        i_find_coord = re.search('atomic coordinates',  line_each[i_line])
        if i_find_coord is not None :
#            print "i_line", i_line, line_each[i_line]
            for i_atom in range(n_atom) :
                i_line = i_line+1
                atom.append(line_each[i_line].split()[3])
            if i_atom == n_atom :
                label = "STOP" 
                break
    


    filein1=open(basis_file,'r')
    line_all=filein1.read()
    filein1.close()
    line_each=line_all.split('\n')

    label = "NONSTOP"    
    atom_type  = []
    basis_type = []
    for i_line in range(n_line):
        if label == "STOP" :
           break
        i_find_basis_each = re.search('type   atoms  prim   cont   basis',  line_each[i_line])
        if i_find_basis_each is not None:
           i_line = i_line + 2 
           for i  in range(10000):
               if label == "STOP" :
                   break
               else :   
                  if line_each[i_line][10] != '-' : 
#                     print line_each[i_line].split()
                     atom_type.append  ( line_each[i_line].split()[0] )
                     basis_type.append ( line_each[i_line].split()[3] )
                     i_line = i_line + 1
                  else :
                      label = "STOP"

    n_type = len(atom_type)
 
    basis =[]
    for i_atom in range(n_atom):
        for i_type in range (n_type) :
#            print i_atom, atom[i_atom], i_type, atom_type[i_type]
            if  atom[i_atom] == atom_type[i_type] : 
#                print basis_type[i_type]
                basis.append(basis_type[i_type])
#                print basis[i_atom]

    n_state = 0
    for i_line in range(n_line): 
        i_find_energy = re.search ('Total energy:' ,  line_each[i_line])
        if i_find_energy is not None:
           n_state = n_state + 1

    filein1=open(basis_file,'r')
    filein1.readline()
    for line in filein1:
        i_find_basis = re.search('number of basis functions   :', line)   
        if  i_find_basis is not None:
            n_basis=int(line.split()[5])         
        i_find_occ = re.search('number of occupied orbitals :', line)
        if  i_find_occ is not None:
            n_occ=int(line.split()[5])
            break
    filein1.close()
    n_vir = n_basis - n_occ

#    print n_basis
#    print n_occ
#    print n_vir 


    fileout1=open('qm_basis.dat', 'w')
    fileout1.write('Functional: 0(pure), 1 (hybrid),  2 (pure+ TDA) , 3 (hybrid + TDA):  '+str(func)+'  \n' )
    fileout1.write('-----------------------------------------  \n')
    fileout1.write('Molecular system:   '+str(n_atom)+'  (total number of atom) \n' )
    fileout1.write('Atom,   Number of basis functions: \n' ) 
    for i_atom in range(n_atom) :
        fileout1.write(''+str(atom[i_atom])+'        '+str(basis[i_atom])+' \n')
    fileout1.write('-----------------------------------------  \n')
    fileout1.write('Total number of basis functions: '+str(n_basis)+'  \n')
    fileout1.write('Total number of occupied orbitals: '+str(n_occ)+'  \n')
    fileout1.write('Total number of unoccupied orbitals: '+str(n_vir)+'  \n')
    fileout1.write('Total number of electronic states: '+str(n_state)+'  \n')
    fileout1.close()

    return (func, n_atom, n_basis, n_occ, n_vir, n_state)

# -------------------------------------------------------------------------
#   Read the MO coefficients
#   Every block of MOs contains four elements in each line.

def read_mo (n_basis):

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
#                print i_line, line_each[i_line].split(), n_block
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
#   Read the CI vector
#   We need to be careful on the pure and hybrid functionals since they have different size of sing_a
# --------------------------------------------------------------------------------------------------

#   Read the CI vector  for pure functional

def read_ci_pure (n_basis, n_occ, n_vir, n_state ):
    
    n_res=int(math.fmod(n_occ*n_vir, 4))
    n_block = int ((n_occ*n_vir - n_res)/4)

    print 'Begin to read the CI vector from sing_a (pure functional)'
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
    filein3=open('sing_a','r')
    for line in filein3:
        n_line += 1
    filein3.close()

    line_each = []
    for i_line in range(n_line):
        line_each.append(0.0)

    filein3=open('sing_a','r')
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
#        print "Norm (Saved CI vector):", norm

    

        for i_index in range(n_index) :
            fileout3.write('S'+str(ci_info_state[i_index]['state'])+'  '+str(ci_info_state[i_index]['civector'])+'    '+str(ci_info_state[i_index]['index_occ'])+'   '+str(ci_info_state[i_index]['index_vir'])+'  '+str((ci_info_state[i_index]['prob']))+'    \n')

    fileout3.close()      









#   Read the CI vector  for hybrid functional with TDA approximation

def read_ci_hy_tda (n_basis, n_occ, n_vir, n_state ):
    
    n_res=int(math.fmod(n_occ*n_vir, 4))
    n_block = int ((n_occ*n_vir - n_res)/4)

    print 'Begin to read the CI vector from ciss_a (pure or hybrid functional with TDA approximation)'
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
#        print "Norm (Saved CI vector):", norm

    

        for i_index in range(n_index) :
            fileout3.write('S'+str(ci_info_state[i_index]['state'])+'  '+str(ci_info_state[i_index]['civector'])+'    '+str(ci_info_state[i_index]['index_occ'])+'   '+str(ci_info_state[i_index]['index_vir'])+'  '+str((ci_info_state[i_index]['prob']))+'    \n')

    fileout3.close()      










#   Read the CI vector from hybrid functional

def read_ci_hybrid (n_basis, n_occ, n_vir, n_state ):
    
    n_res=int(math.fmod(n_occ*n_vir*2, 4))
    n_block = int ((n_occ*n_vir*2 - n_res)/4)

    print 'Begin to read the CI vector from sing_a (hybrid functional)'
#    print n_basis, n_occ, n_vir, n_state
#    print n_block, n_res

    energy = []
    for i_state in range(n_state):
        energy.append([])

    element = []
    for i_ele in range(n_occ*n_vir*2) :
        element.append(0.0)

    Xvector = []
    for i_ci_1 in range(n_occ):
         Xvector.append([])
         for i_ci_2 in range(n_vir):
             Xvector[i_ci_1].append([])

    Yvector = []
    for i_ci_1 in range(n_occ):
         Yvector.append([])
         for i_ci_2 in range(n_vir):
             Yvector[i_ci_1].append([])

 

    sum_XYvector = []
    for i_ci_1 in range(n_occ):
         sum_XYvector.append([])
         for i_ci_2 in range(n_vir):
             sum_XYvector[i_ci_1].append([])

    diff_XYvector = []
    for i_ci_1 in range(n_occ):
         diff_XYvector.append([])
         for i_ci_2 in range(n_vir):
             diff_XYvector[i_ci_1].append([])



    ci =[]
    for i_state in range(n_state):
        ci.append([])
        for i_ci_1 in range(n_occ):
            ci[i_state].append([])
            for i_ci_2 in range(n_vir):
                ci[i_state][i_ci_1].append(0.0)
   
#   Read the CI vector

    n_line = 0
    filein3=open('sing_a','r')
    for line in filein3:
        n_line += 1
    filein3.close()

    line_each = []
    for i_line in range(n_line):
        line_each.append(0.0)

    filein3=open('sing_a','r')
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
                        sum_XYvector[i_ci_1][i_ci_2] = re.sub('D', 'E', element[i_ele])
                        diff_XYvector[i_ci_1][i_ci_2] = re.sub('D', 'E', element[i_ele+n_occ*n_vir])
                        sum_XYvector[i_ci_1][i_ci_2] = float (sum_XYvector[i_ci_1][i_ci_2] )
                        diff_XYvector[i_ci_1][i_ci_2] = float (diff_XYvector[i_ci_1][i_ci_2] )
                        Xvector[i_ci_1][i_ci_2] = 0.5* (sum_XYvector[i_ci_1][i_ci_2] + diff_XYvector[i_ci_1][i_ci_2])
                        Yvector[i_ci_1][i_ci_2] = 0.5* (sum_XYvector[i_ci_1][i_ci_2] - diff_XYvector[i_ci_1][i_ci_2]) 
                        ci[i_state][i_ci_1][i_ci_2] = Xvector[i_ci_1][i_ci_2] + Yvector[i_ci_1][i_ci_2] 
#                        ci[i_state][i_ci_1][i_ci_2] = Xvector[i_ci_1][i_ci_2]
    filein3.close()

 



#   Check the normalization condition ( X^T * X  - Y^T *Y = 1)

    check_XY = []
    for i_ci_2 in range(n_vir):
         check_XY.append([]) 

    for i_state in range(1, n_state) :
        check_XY_norm = 0.0
        for i_ci_2 in range(n_vir):
            check_XY[i_ci_2] = 0.0
            for i_ci_1 in range(n_occ):
                 check_XY_norm = check_XY_norm + Xvector[i_ci_1][i_ci_2] * Xvector[i_ci_1][i_ci_2] -  Yvector[i_ci_1][i_ci_2] * Yvector[i_ci_1][i_ci_2]  
        print  "Normalization condition (X^T * X  - Y^T *Y = 1) for State "+str(i_state+1)+". The computed values is", check_XY_norm







    for i_state in range(1, n_state):
        print "Check normalization for State:", i_state+1
        norm = 0.0
        for i_ci_1 in range(n_occ) :
             for i_ci_2 in range(n_vir) :
                 norm  =   norm + ci[i_state][i_ci_1][i_ci_2] * ci[i_state][i_ci_1][i_ci_2]
        print "Norm before Normailzation: ", norm
        for i_ci_1 in range(n_occ) :
             for i_ci_2 in range(n_vir) :
                 ci[i_state][i_ci_1][i_ci_2] = ci[i_state][i_ci_1][i_ci_2] / (math.sqrt(norm))
#                 print "CI vector after normalization", i_state, i_ci_1, i_ci_2, ci[i_state][i_ci_1][i_ci_2]
        norm = 0.0
        for i_ci_1 in range(n_occ) :
             for i_ci_2 in range(n_vir) :
                 norm  =   norm + ci[i_state][i_ci_1][i_ci_2] * ci[i_state][i_ci_1][i_ci_2]
        print "Norm after Normalization:", norm  




    fileout3=open('ci.dat', 'w')
    fileout3.write('#  State, CI vector, i_occ, j_vir,  |Coeff^2|)    \n')
    if n_occ*n_vir  > 20 :
        n_index =  20
    else :
        n_index =  n_occ*n_vir 

#   Find the most important CI vector

    print "CI vector"
    ci_info_state = []
    for i_all in range(n_occ*n_vir) :
        ci_info_state.append([])


#    ci_dict = {}
    for i_state in range(1, n_state) :
        i_all=0
        for i_ci_1 in range(n_occ) :
            for i_ci_2 in range(n_vir) :
                ci_dict= {}
#             ci_vector_value[i_ci_1][i_ci_2] = float(re.sub('D', 'E', ci[i_ci_1][i_ci_2])) 
                ci_dict['state'] = i_state 
                ci_dict['index'] = i_ci_1 * n_vir + i_ci_2+1
                ci_dict['civector'] = ci[i_state][i_ci_1][i_ci_2]
                ci_dict['prob'] = math.pow(ci[i_state][i_ci_1][i_ci_2],2 )
#                print "ci_dict:", i_state, i_ci_1, i_ci_2, ci_dict['civector']
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
#            print "ci_dict_1:", ci_info_state[i_index]['civector']
            norm  =   norm + ci_info_state[i_index]['civector']*ci_info_state[i_index]['civector']
#        print "Norm (Saved CI vector):", norm



        for i_index in range(n_index) :
            fileout3.write('S'+str(ci_info_state[i_index]['state'])+'  '+str(ci_info_state[i_index]['civector'])+'    '+str(ci_info_state[i_index]['index_occ'])+'   '+str(ci_info_state[i_index]['index_vir'])+'  '+str((ci_info_state[i_index]['prob']))+'    \n')

    fileout3.close()      



def collect_qm (n_atom, n_state):

     fileout3=open('qm_results.dat', 'w')

     fileout3.write('-----------------------------------------  \n')
     fileout3.write('Summary of QM calculations: \n')
     fileout3.write('-----------------------------------------  \n')

     fileout3.write('The electronic calculations focus on '+str(n_state)+' states: \n')
     for i_state in range(n_state) :
         fileout3.write('S'+str(i_state)+ '   ..   ' )
     fileout3.write('\n -----------------------------------------  \n')

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
    
     fileout3.close()
 
if __name__ == "__main__":
    tur_read()
