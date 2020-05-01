#!/usr/bin/python
import os
count=0
from os import system
from sys import exit



# n_step = int(input('How many step? '))
# print n_step


e_min = float(raw_input('Minimum energy? '))

e_max = float(raw_input('Maximum energy? '))

ne = int(raw_input('How many bins? '))

e_sigma = float(raw_input('HHFW? '))

inputfile = raw_input('Input File? ')

outputfile = raw_input('Output File? ')


de = (e_max-e_min)/float(ne)


emission_energy = []
for i_e in range(ne):
    emission_energy.append(0.0)



emission_intensity =[]
for i_e in range(ne):
    emission_intensity.append(0.0)



freq = []
os = []

n_freq = 0
filein1=open(''+str(inputfile)+'')
for line in filein1:
    n_freq += 1
filein1.close()


filein1=open(''+str(inputfile)+'','r')
spec_all=filein1.read()
filein1.close()
spec_text=spec_all.split('\n')



for i_freq in range(n_freq-1):
    freq.append(float(spec_text[i_freq+1].split()[0]))
    os.append(float(spec_text[i_freq+1].split()[1]))
        

for i_e in range(ne):
    emission_energy[i_e]=e_min+float(i_e)*de
    emission_intensity[i_e]= 0.0
    for i_freq in range(n_freq-1):
        lineshape = 1/ 3.1415926  * e_sigma / ( ( emission_energy[i_e] - freq[i_freq] )**2 + e_sigma**2 )
        tmp_os = os[i_freq] * lineshape
        emission_intensity[i_e]= emission_intensity[i_e] + tmp_os

                

filein4=open(''+str(outputfile)+'','w')
filein4.write('#  Energy(eV)  Intensity  \n' )
for i_e in range(ne): 
    emission_energy[i_e]=e_min+float(i_e)*de
    filein4.write(''+str(emission_energy[i_e])+'    '+str(emission_intensity[i_e])+' \n ')       
