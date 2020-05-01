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


#---------------------------------------------------------------------------

#  Read the interface between surface-hopping code and turbomole calculations
#  Get the number of states, the number of atoms and current state. Return these values
#  Read the Geometries and write to Turbomole input format file "coord".

# 20130829: read_coord ==> set_coord 
def set_coord () :
   
    print "create coord file"
    n_line = 0
    filein1=open('turbomole_interface','r')
    for line in filein1:
        n_line += 1
    filein1.close()

    line_each = []
    for i_line in range(n_line):
        line_each.append(0.0)

    filein1=open('turbomole_interface','r')
    line_all=filein1.read()
    filein1.close()
    line_each=line_all.split('\n')

    for i_line in range(n_line):
 
        i_find_geom = re.search('Number of atom', line_each[i_line])
        if  i_find_geom is not None:
            n_atom = int(line_each[i_line].split()[3])

        i_find_state1 = re.search('Number of state', line_each[i_line])
        if  i_find_state1 is not None:
            n_state = int(line_each[i_line].split()[7])
            print "Number of states", n_state 
        i_find_state2 = re.search('Current state', line_each[i_line])
        if  i_find_state2 is not None:
            index_state = int(line_each[i_line].split()[2])
            break



    atom_label = []
    coor_x = []
    coor_y = []
    coor_z = []
    for i_atom in range(n_atom):
         atom_label.append([])
         coor_x.append(0.0)
         coor_y.append(0.0)
         coor_z.append(0.0)


   
    for i_line in range(n_line):
        i_find_geom = re.search('Current Geometry', line_each[i_line])
        if  i_find_geom is not None:
            i_line = i_line + 3
            for i_atom in range(n_atom):
                atom_label[i_atom] = line_each[i_line].split()[0].lower()       
                coor_x [i_atom] =    line_each[i_line].split()[1]
                coor_y [i_atom] =    line_each[i_line].split()[2]
                coor_z [i_atom] =    line_each[i_line].split()[3]
                i_line = i_line + 1


#  Write "coord" file    
    fileout1=open('coord', 'w')
    fileout1.write('$coord   \n')
    for i_atom in range(n_atom) :
        fileout1.write(''+str( coor_x [i_atom])+'   '+str( coor_y [i_atom])+'   '+str( coor_z [i_atom])+'  '+str(atom_label[i_atom])+' \n')
    fileout1.write('$user-defined bonds \n')
    fileout1.write('$end')
    
    return (n_atom, n_state, index_state)






def modify_control (n_atom, n_state, index_state) :


    print "Modify control file"
    n_line = 0
    filein1=open('control','r')
    for line in filein1:
        n_line += 1
    filein1.close()

    line_each = []
    for i_line in range(n_line):
        line_each.append(0.0)

    filein1=open('control','r')
    line_all=filein1.read()
    filein1.close()
    line_each=line_all.split('\n')


    line_delete_1= ''
    line_delete_2= ''
    line_delete_3= ''
    line_delete_4= ''
    line_delete_5= ''
    line_delete_6= ''
  
#   Change the states involved
    for i_line in range(n_line):
#        print i_line, line_each[i_line]
        i_find_delete = re.search('\$statistics', line_each[i_line])
#        print i_find_delete
        if  i_find_delete is not None:
            line_delete_1 = line_each[i_line]
#            print line_delete_1
        i_find_delete = re.search('MPP', line_each[i_line])
        if  i_find_delete is not None:
            line_delete_2 = line_each[i_line]
        i_find_delete = re.search('\$numprocs', line_each[i_line])
        if  i_find_delete is not None:
            line_delete_3 = line_each[i_line]
        i_find_delete = re.search('\$exopt', line_each[i_line])
        if  i_find_delete is not None:
            line_delete_4 = line_each[i_line]
        i_find_delete = re.search('metastase', line_each[i_line])
        if  i_find_delete is not None:
            line_delete_5 = line_each[i_line]




#   Set the number of states involved in the TDDFT work.
        i_find_state = re.search('\$soes', line_each[i_line])
        if  i_find_state is not None:
            soes_line = '$soes'
            soes_line += '   all  '
            soes_line += str(int(n_state-1))
            line_each[i_line] = soes_line
         

            i_line = i_line + 1
#            print line_each[i_line]
            i_find_label = re.search('\$', line_each[i_line])
            if  i_find_label is None:
		line_delete_6 = line_each[i_line]  
    
#    Delete some useless lines
         
    if len(line_delete_1) > 1 :
        line_each.remove(str(line_delete_1))
    if len(line_delete_2) > 1 :
        line_each.remove(str(line_delete_2))
    if len(line_delete_3) > 1 :
        line_each.remove(str(line_delete_3))
    if len(line_delete_4) > 1 :
        line_each.remove(str(line_delete_4))
    if len(line_delete_5) > 1 :
        line_each.remove(str(line_delete_5))
    if len(line_delete_6) > 1 :
	line_each.remove(str(line_delete_6))


#   Add the target state for gradient calculations
    if index_state > 1 :
        n_line_write = len(line_each)
        exopt_line  = '$exopt  '
        exopt_line += str(int(index_state)-1)
        line_each.insert(n_line_write-2, str(exopt_line))
#        print exopt_line
    
    
    n_line_write = len(line_each)
    fileout2=open('control_new', 'w')
    for i_line in range(n_line_write):
         fileout2.write(''+str(line_each[i_line])+' \n')
    fileout2.close()
 
    sourceFile = 'control_new'
    destFile   = 'control'
    shutil.copyfile("./control_new", "./control")
     




#############################################################

