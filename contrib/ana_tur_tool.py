#!/usr/bin/python
import os
import sys
from operator import itemgetter
import re
import math
import shutil
import string


def read_state (n_state):


    file_state = "current_state.out"
    n_line = 0
    filein4=open(file_state,'r')
    for line in filein4:
        n_line += 1
    filein4.close()

    line_each = []
    for i_line in range(n_line):
        line_each.append('')

    filein4=open(file_state,'r')
    line_all=filein4.read()
    filein4.close()
    line_each=line_all.split('\n')



    step = []
    time = []
    current_state = []
    current_energy = []
    for i_line in range(2,n_line):
        step.append(line_each[i_line].split()[0])
        time.append(line_each[i_line].split()[1]) 
        current_state.append(line_each[i_line].split()[2])
        current_energy.append(line_each[i_line].split()[3])       

    n_step = len(step)    
         
    return (n_step, step, time, current_state, current_energy)

######################################################################

def read_di (n_step, current_state):


    file_energy='di_time.out'
     
    n_line = 0
    filein4=open(file_energy,'r')
    for line in filein4:
        n_line += 1
    filein4.close()

    line_each = []
    for i_line in range(n_line):
        line_each.append('')

    filein4=open(file_energy,'r')
    line_all=filein4.read()
    filein4.close()
    line_each=line_all.split('\n')
  
    
    excitation_energy = [] 
    tra_x = []
    tra_y = []
    tra_z = []
    for i_step in range(n_step)  :
        excitation_energy.append([])
        tra_x.append([])
        tra_y.append([])
        tra_z.append([])
        for i_state in range(n_state) :
            excitation_energy[i_step].append([])   
            tra_x[i_step].append([])
            tra_y[i_step].append([])
            tra_z[i_step].append([])

    i_step  = 0 
    i_state = 0
    for i_line in range(n_line):
         i_find_ex = re.search('singlet a excitation', line_each[i_line])
         if i_find_ex is not None:
             i_state = i_state + 1
             for k_line in range (i_line, i_line+5000) :
                 i_find_energy = re.search('Excitation energy / eV:', line_each[k_line]) 
#                 print i_find_energy, line_each[k_line]
                 if i_find_energy is not None:
#                    print  "excitation_energy", line_each[k_line].split()[4]
                    excitation_energy[i_step][i_state] = line_each[k_line].split()[4]
                 
                 i_find_tra_dipo1 = None
                 i_find_tra_dipo2 = None
		 i_find_tra_dipo1 = re.search( "transition dipole moment" ,  line_each[k_line])
#                 print i_find_tra_dipo1, line_each[k_line]
                 if i_find_tra_dipo1 is not None:
                    i_find_tra_dipo2 = re.search( "length" ,  line_each[k_line])
                    if i_find_tra_dipo2 is not None:
#                       print i_find_tra_dipo2, line_each[k_line+1].split()[1]
                       tra_x[i_step][i_state] = line_each[k_line+1].split()[1]
                       tra_y[i_step][i_state] = line_each[k_line+2].split()[1]
                       tra_z[i_step][i_state] = line_each[k_line+3].split()[1]
#                      print i_step, i_state, tra_x[i_step][i_state]
                       break    
        
         if i_state == n_state -1 :
            i_step = i_step + 1
            i_state = 0
    
#    for i in range(n_step) : 
#        for j in range(n_state) :
#            print i, j, tra_x[i][j]

    current_excitation_energy = [] 
    current_tra_x = []
    current_tra_y = []
    current_tra_z = []
   

    for i_step in range(n_step) :
         if current_state[i_step] == 1 :
            current_excitation_energy.append(0.0)
            current_tra_x.append(0.0)
            current_tra_y.append(0.0)
            current_tra_z.append(0.0)
         else :
#            print i_step
#            print current_state[i_step]
            tmp_state = int (current_state[i_step]) - 1
#            print tmp_state
#            print excitation_energy[i_step][tmp_state]
#            print i_step, tmp_state, tra_x[i_step][ tmp_state ]
            current_excitation_energy.append( float ( excitation_energy[i_step][tmp_state] ) )
            current_tra_x.append( float ( tra_x[i_step][ tmp_state ] ) )
            current_tra_y.append( float ( tra_y[i_step][ tmp_state ] ) )
            current_tra_z.append( float ( tra_z[i_step][ tmp_state ] ) )     
      
         
    return (current_excitation_energy, current_tra_x, current_tra_y, current_tra_z)


def  write_di (n_step, n_state, current_state, current_energy, current_excitation_energy, current_tra_x, current_tra_y, current_tra_z)  :

     fileout1=open('transition_dipole.dat', 'w')
     fileout2=open('emission.dat', 'w')
     fileout3=open('anistropy.dat', 'w')


     fileout1.write('# Step, Time (fs), current_state, transition energy (eV), tra_x, tra_y, tra_z, tra_t \n')
     fileout2.write('# Step,   Time (fs),      mu(0) * mu(t), cos(theta),  theta, theta (0-90)  Anistropy  \n')
     fileout3.write('# Time (fs), Anistropy  \n')
  

     tra_t = []
     cos_angle = []
     
     product_u0_ut = []
     angle = []
     angle1 = []
     cos_2 = []
     ani = []
     for i_step in range(n_step) :
         if current_state[i_step] == 1 :
            tra_t = 0.0
            product_u0_ut = 0.0
            cos_angle = 0
            angle = 3.1415926/2
            cos_2 = 0
         else :    
            tmp = 0.0
            tmp = (current_tra_x[i_step]**2 + current_tra_y[i_step]**2 + current_tra_z[i_step]**2)**0.5 
            tra_t.append(float(tmp))
              
            tmp = 0.0
            tmp =  tmp +  current_tra_x[i_step] * current_tra_x[0] 
            tmp =  tmp +  current_tra_y[i_step] * current_tra_y[0] 
            tmp =  tmp +  current_tra_z[i_step] * current_tra_z[0] 
            product_u0_ut.append ( float(tmp) )
          
            tmp =  0.0      
#            print tmp, current_tra_x[i_step], tra_t[i_step], current_tra_x[0], tra_t[0]
            tmp =  tmp + (current_tra_x[i_step] /  tra_t[i_step]) * (current_tra_x[0] /  tra_t[0])
            tmp =  tmp + (current_tra_y[i_step] /  tra_t[i_step]) * (current_tra_y[0] /  tra_t[0])
            tmp =  tmp + (current_tra_z[i_step] /  tra_t[i_step]) * (current_tra_z[0] /  tra_t[0])
            cos_angle.append (float(tmp))
  
            

            
            if cos_angle[i_step] >= 1.0 :
               cos_angle[i_step] = 0.9999999
                
#            print i_step, cos_angle[i_step]
            
            angle.append ( math.acos( float (cos_angle[i_step]) ) )
            angle1.append ( math.acos( float ( abs( cos_angle[i_step])) ) )
            cos_2.append ( cos_angle[i_step]**2 )
#            print i_step, cos_angle[i_step], abs( cos_angle[i_step]), angle[i_step], angle1[i_step]

         ani.append( 0.4 * (3 * cos_2[i_step]-1)/2 )
       
         time[i_step] = '%f' % float(time[i_step])
         current_energy[i_step] = '%f' %  float(current_energy[i_step])
         current_excitation_energy[i_step] = '%f' % float(current_excitation_energy[i_step])
#         tra_t[i_step] = '%f' %  tra_t[i_step]
         product_u0_ut[i_step] = '%f' %  product_u0_ut[i_step]
         cos_angle[i_step] = '%f' %  cos_angle[i_step]
         angle[i_step] = '%f' % (angle[i_step]/3.1415926 * 180)
         angle1[i_step] = '%f' % (angle1[i_step]/3.1415926 * 180)
         ani[i_step] = '%f' %  ani[i_step] 
#         print i_step, ani[i_step]

         tmp1  = str(i_step)
         tmp2  = str(time[i_step])
         tmp22 = str(current_state[i_step])
         tmp3  = str(current_energy[i_step])
         tmp4  = str(current_excitation_energy[i_step])
         tmp5  = str(current_tra_x[i_step])
         tmp6  = str(current_tra_y[i_step])
         tmp7  = str(current_tra_z[i_step])
         tmp8  = str(tra_t[i_step]) 
         tmp9  = str(product_u0_ut[i_step])
         tmp10 = str(cos_angle[i_step])
         tmp11 = str(angle[i_step])
         tmp112 = str(angle1[i_step])
         tmp12 = str(ani[i_step])
   
         tmp1 = tmp1.ljust(10)
         tmp2 = tmp2[0:8]
         tmp22 = tmp22[0:8]
         tmp3 = tmp3[0:10]
         tmp4 = tmp4[0:8] 
         tmp5 = tmp5[0:8]
         tmp6 = tmp6[0:8]
         tmp7 = tmp7[0:8]
         tmp8 = tmp8[0:8]
         tmp9 = tmp9[0:8]
         tmp10 = tmp10[0:8]
         tmp11 = tmp11[0:8]
         tmp112 = tmp112[0:8]
         tmp12 = tmp12[0:5] 

#         fileout3.write(' '+str(i_step+1)+'  '+str(time(i_step)+'   '+str(current_energy[i_step])+'  '+str(current_transition_energy[i_step])+'')
#         fileout3.write(' '+str(tra_x(i_step)+'   '+str(tra_y[i_step])+'  '+str(tra_z[i_step])+'  '+str(tra_t[i_step])+'  ')
#         fileout3.write(' '+str(product_u0_ut(i_step)+'   '+str(cos_angle[i_step])+'  '+str(angle[i_step])+'  '+str(ani[i_step])+'  ')
         
         fileout1.write(''+str(tmp1)+' ' ) 
         fileout1.write(''+str(tmp2)+'  ' )
         fileout1.write(''+str(tmp22)+'  ' )
#         fileout1.write(''+str(tmp3)+'  ' )
         fileout1.write(''+str(tmp4)+'  ' )
         fileout1.write(''+str(tmp5)+'  ' )
         fileout1.write(''+str(tmp6)+'  ' )
         fileout1.write(''+str(tmp7)+'  ' )
         fileout1.write(''+str(tmp8)+'  ' )
         fileout1.write(' \n' )

         fileout2.write(''+str(tmp1)+' ' )
         fileout2.write(''+str(tmp2)+'  ' )
         fileout2.write(''+str(tmp9)+'        ' )
         fileout2.write(''+str(tmp10)+'  ' )
         fileout2.write(''+str(tmp11)+'  ' )
         fileout2.write(''+str(tmp112)+'  ' )
         fileout2.write(''+str(tmp12)+'  ' )   
         fileout2.write(' \n ' )

         fileout3.write(''+str(tmp2)+'  ' )
         fileout3.write(''+str(tmp12)+'  ' )
         fileout3.write(' \n' )

if __name__ == "__main__":
    
    
    n_state = 3

    b = read_state (n_state)
    n_step = b[0]
    step = b[1]
    time = b[2]
    current_state = b[3]
    current_energy = b[4]

    c =  read_di (n_step, current_state)
 
      
    current_excitation_energy = c[0] 
    current_tra_x = c[1] 
    current_tra_y = c[2]
    current_tra_z = c[3] 

    write_di (n_step, n_state, current_state, current_energy, current_excitation_energy, current_tra_x, current_tra_y, current_tra_z)    
 
