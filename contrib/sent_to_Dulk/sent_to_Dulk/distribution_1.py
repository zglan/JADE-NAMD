#!/usr/bin/python
import os
import math
count=0
from os import system
from sys import exit





x_min = float(input('Minimum x? '))
x_max = float(input('Maximum x? '))
n_x = int(input('How many bins for x? '))
e_x = float(input('HHFW for x? '))

y_min = float(input('Minimum y? '))
y_max = float(input('Maximum y? '))
n_y = int(input('How many bins for y? '))
e_y = float(input('HHFW for y? '))

d_x = (x_max-x_min)/float(n_x)
d_y = (y_max-y_min)/float(n_y)



value_x = []
for i_x in range(n_x):
    value_x.append(0.0)

value_y = []
for i_y in range(n_y):
    value_y.append(0.0)


intensity_x_y = []
for i_x in range(n_x):
    intensity_x_y.append([])
    for i_y in range(n_y):
        intensity_x_y[i_x].append(0.0)



#   Check how many geometries 
n_geom = 0
filein1=open('geoman_1.log')
for line in filein1:
    n_geom += 1
filein1.close()


index_each = []
for i_index in range(n_geom):
    index_each.append(0.0)

# Read all geometries


filein1=open('geoman_1.log','r')
index_all=filein1.read()
filein1.close()
index_each=index_all.split('\n')



geom_x = []
for i_geom in range(n_geom):
    geom_x.append([])


geom_y = []
for i_geom in range(n_geom):
    geom_y.append([])
        

# Give values to all geometries



for i_geom in range(n_geom):
    geom_x[i_geom] = float(index_each[i_geom].split()[0])


for i_geom in range(n_geom):
    geom_y[i_geom] = float(index_each[i_geom].split()[1])


for i_x in range(n_x):   
    value_x[i_x] = x_min + i_x * d_x           
    for i_y in range(n_y):
        value_y[i_y] = y_min + i_y * d_y
        intensity_x_y[i_x][i_y] = 0.0
        for i_geom in range(n_geom):
            lineshape =   1/ ( (2*3.1415926)**0.5 * e_x) * math.exp ( -( value_x[i_x] - geom_x[i_geom] )**2 / (2* e_x**2 ))  \
                        * 1/ ( (2*3.1415926)**0.5 * e_y) * math.exp ( -( value_y[i_y] - geom_y[i_geom] )**2 / (2* e_y**2 ))
            intensity_x_y[i_x][i_y]= intensity_x_y[i_x][i_y] + lineshape 

                

filein4=open('distribution.dat','w')
filein4.write('#  X, Y,  Intensity  \n' )
for i_x in range(n_x): 
    for i_y in range(n_y):
        filein4.write(''+str(value_x[i_x])+'    '+str(value_y[i_y])+'    '+str(intensity_x_y[i_x][i_y])+' \n ')       




filein5=open('distribution_gnuplot.dat','w')
filein5.write('#  X, Y,  Intensity  \n' )
for i_x in range(n_x):
    for i_y in range(n_y):
        filein5.write(''+str(value_x[i_x])+'    '+str(value_y[i_y])+'    '+str(intensity_x_y[i_x][i_y])+' \n ')
    filein5.write(' \n')

