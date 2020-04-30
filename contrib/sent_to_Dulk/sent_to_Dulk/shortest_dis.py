#!/usr/bin/python
import os
import math
count=0
from os import system
from sys import exit

# This script is used to select bond between tow atoms with the shortest distance.





value_x = []
value_x.append(0.0)

value_y = []
value_y.append(0.0)

index_all = []




#   Check how many geometries and read these geometries. 
n_geom = 0
filein1=open('dis_11-14.log')
for line in filein1:
    n_geom += 1
filein1.close()

index_each = []
for i_index in range(n_geom):
    index_each.append(0.0)

m_geom = 0
filein2=open('dis_12-13.log')
for line in filein2:
    m_geom += 1
filein2.close()

index_each = []
for j_index in range(m_geom):
    index_each.append(0.0)

if n_geom != m_geom: 
   sys.exit(0)




geom_x = []
for i_geom in range(n_geom):
    geom_x.append([])


geom_y = []
for i_geom in range(n_geom):
    geom_y.append([])



# Read all geometries


filein1=open('dis_11-14.log','r')
index_all=filein1.read()
filein1.close()
index_each=index_all.split('\n')


for i_geom in range(n_geom):
    geom_x[i_geom] = float(index_each[i_geom].split()[1])


filein2=open('dis_12-13.log','r')
index_all=filein2.read()
filein2.close()
index_each=index_all.split('\n')


for i_geom in range(n_geom):
    geom_y[i_geom] = float(index_each[i_geom].split()[1])



fileout3=open('shortest_OH_dis.log','w')
for i_geom in range(n_geom):
      value_x = geom_x[i_geom]
      value_y = geom_y[i_geom]
      if value_x <= value_y:
          fileout3.write(''+str(value_x)+' \n ')
      else:
          fileout3.write(''+str(value_y)+' \n ')
fileout3.close()
