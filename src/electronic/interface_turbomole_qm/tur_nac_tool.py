#!/usr/bin/python
import os
import sys
from operator import itemgetter
import re
import math
import shutil 

#---------------------------------------------------------------------------

#  Creat the coordinates for double-molecule 
def create_nac_input () :


     n_line = 0
     filein1=open('qm_results.dat','r')
     for line in filein1:
         n_line += 1
     filein1.close()
     line_each = []
     for i_line in range(n_line):
         line_each.append(0.0)
 
     filein1=open('qm_results.dat','r')
     line_all=filein1.read()
     filein1.close()
     line_each=line_all.split('\n')



     
     for i_line in range(n_line):

         i_find_n_atom = None
	 i_find_n_atom = re.search ('Number of atom:', line_each[i_line] )
	 if i_find_n_atom is not None:
             n_atom = int (line_each[i_line].split()[-1])
         
	 i_find_n_state = None
	 i_find_n_state = re.search ('Number of states', line_each[i_line] )
	 if i_find_n_state is not None:
             n_state = int (line_each[i_line].split()[-1])
     
         i_find_n_ao = None
	 i_find_n_ao = re.search ('number of basis functions', line_each[i_line] )
	 if i_find_n_ao is not None:
             n_ao = int (line_each[i_line].split()[-1])

         
         i_find_n_occ = None
	 i_find_n_occ = re.search ('number of occupied orbitals', line_each[i_line] )
	 if i_find_n_occ is not None:
	     n_occ = int (line_each[i_line].split()[-1])



     fileout1=open('main_overlap_slater_input','w')
     fileout1.write('                        read (*,*)  \n')
     fileout1.write(''+str(n_atom)+'               read (*,*) n_atom \n')
     fileout1.write(''+str(n_ao)+'                 read (*,*) n_ao \n')
     fileout1.write(''+str(n_occ)+'               read (*,*) n_ele_alpha \n')
     fileout1.write(''+str(n_occ)+'               read (*,*) n_ele_beta \n')
     fileout1.write('                        read (*,*)  \n')
     fileout1.write(''+str(n_state)+'               read (*,*) n_state \n')
     fileout1.write('                        read (*,*)  \n')
     fileout1.write('1                       read (*,*)  type_input  \n')
     fileout1.write('ci_1.dat                read (*,*)  filename_input1  \n')
     fileout1.write('ci_2.dat                read (*,*)  filename_input2  \n')
     fileout1.write('overlap.dat             read (*,*)  filename_input2  \n')
     fileout1.write('                        read (*,*)  \n')
     fileout1.write('0                       read (*,*) output_level  \n')
     fileout1.write('ci_overlap.dat          read (*,*) filename_output  \n')
     fileout1.close()


def run_nac() :

     os.system("main_overlap_slater.exe  < main_overlap_slater_input")


def read_nac () :
   
    
     n_line = 0
     filein1=open('qm_results.dat','r')                                                 
     for line in filein1:                                                               
         n_line += 1
     filein1.close()
     line_each = []
     for i_line in range(n_line):
         line_each.append(0.0)
     
     filein1=open('qm_results.dat','r')
     line_all=filein1.read()
     filein1.close()
     line_each=line_all.split('\n')
    
    
     
     for i_line in range(n_line):
         i_find_n_state = None
         i_find_n_state = re.search ('Number of states', line_each[i_line] )
         if i_find_n_state is not None:
               n_state = int (line_each[i_line].split()[-1])

 
     
     n_line_2 = 0
     filein2=open('wavefuction_overlap.dat','r')                                                 
     for line in filein2:                                                               
         n_line_2 += 1
     filein2.close()
     line_each_2 = []
     for i_line_2 in range(n_line_2):
         line_each_2.append(0.0)
     
     filein2=open('wavefuction_overlap.dat','r')
     line_all=filein2.read()
     filein2.close()
     line_each_2=line_all.split('\n')

     i_line_2=1
     ci_overlap = []
     for i_state in range(n_state*n_state):
         ci_overlap.append(line_each_2[i_line_2].split()[-1]) 
         i_line_2 += 1		 
     	     

     fileout1=open('qm_result_update.dat','w')
     for i_line in range(n_line-n_state*n_state-2):
         fileout1.write(''+str(line_each[i_line])+'  \n')
     fileout1.write('Wave-function overlap between R and R+dR \n') 	 
     i_line=0	 
     for i_state in range(n_state) :
	 for j_state in range(n_state) :     
	     fileout1.write('S'+str(i_state)+'   S'+str(j_state)+'    '+str(ci_overlap[i_line])+'  \n')
	     i_line = i_line + 1
     fileout1.write('----------------------------------------------')
     fileout1.close()




     shutil.copyfile("./qm_result_update.dat", "./qm_results.dat")
     shutil.copyfile("./qm_results.dat", "../../qm_results.dat")
