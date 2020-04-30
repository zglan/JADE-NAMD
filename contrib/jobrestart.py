#! /usr/bin/env python2.7

import os
import re


class jobrestart():
    def __init__(self):
        self.params = {}
        self.params['n_step_old'] = 0
        self.params['n_step_new'] = 0
        self.params['dt_old'] = 0
        self.params['dt_new'] = 0

        return
    
    def get_old_inp(self):

        filename = "./pe_time.out"
        self.params['n_step_old'] = len(open(filename).readlines())
            
        dyn = "./dyn.inp"
	dyn_file = open(dyn, "r")
	pattern = re.compile("dtime")
	line = "NOT EMPTY LINE"
	while line != "":
           line = dyn_file.readline()
	   m = pattern.search(line)
	   if m is not None:
              record = line.split()
	      self.params['dt_old'] = float(record[2].strip(','))
	      break
        return
        

    def get_new_inp(self):

        filename = "./restart/pe_time.out"
        self.params['n_step_new'] = len(open(filename).readlines())
            
        dyn = "./restart/dyn.inp"
	dyn_file = open(dyn, "r")
	pattern = re.compile("dtime")
	line = "NOT EMPTY LINE"
	while line != "":
           line = dyn_file.readline()
	   m = pattern.search(line)
	   if m is not None:
              record = line.split()
	      self.params['dt_new'] = float(record[2].strip(','))
	      break
        dyn_file.close()

        return
 
    def collect_state(self):

	n_step_n =  self.params['n_step_new']
	n_step_o =  self.params['n_step_old']

	file_old = "./current_state.out"
	file_new = "./restart/current_state.out"

	label_new = open(file_new, "r")
	label_old = open(file_old, "a")

	label_new.readline()
	label_new.readline()
	label_new.readline()

	for i_line in range(n_step_n - 1):
           line=label_new.readline()
	   record = line.split()
	   record[0] = n_step_o + i_line
	   record[1] = record[0]*self.params['dt_new']

	   label_old.write('      '+ str(record[0])+'    ' +str(record[1])+'            ' +str(record[2])+'      ' + str(record[3])+'         ' +str(record[4])+'         ' +str(record[5])+'\n')

        label_new.close()
        label_old.close()
	return
	   
	
    def collect_pe(self):

	n_step_n =  self.params['n_step_new']
	n_step_o =  self.params['n_step_old']

	file_old = "./pe_time.out"
	file_new = "./restart/pe_time.out"

	label_new = open(file_new, "r")
	label_old = open(file_old, "a")

	label_new.readline()

	for i_line in range(n_step_n - 1):
           line=label_new.readline()
	   record = line.split()
	   record[0] = n_step_o + i_line
	   record[1] = record[0]*self.params['dt_new']

	   label_old.write('      '+ str(record[0])+'       ' +str(record[1])+'               ' +str(record[2])+'      ' + str(record[3])+'      ' +str(record[4])+'      ' +str(record[5])+'\n')

        label_new.close()
        label_old.close()
        

    def collect_hop(self):

	n_step_n =  self.params['n_step_new']
	n_step_o =  self.params['n_step_old']

	file_old = "./hop_all_time.out"
	file_new = "./restart/hop_all_time.out"

	label_new = open(file_new, "r")
	label_old = open(file_old, "a")

	label_new.readline()
	pattern = re.compile("------------------")
	line = "NOT EMPTY LINE"

	while line != "":
           line = label_new.readline()
	   m = pattern.search(line)
	   if m is not None:
	      break

        for i_step in range(n_step_n-1):

           line=label_new.readline()
	   label_old.write(line)
	   
	   while line != "":
              line = label_new.readline()

	      m = pattern.search(line)
	      if m is not None:
	         label_old.write(line)
	         break
              
	      record = line.split()

	      record[0] = n_step_o + i_step
	      record[1] = record[0]*self.params['dt_new']

	      n_list = len(record)
	      for i_list in range(n_list):
	         label_old.write(' '+ str(record[i_list]))

	      label_old.write('\n')


        label_new.close()
        label_old.close()

	return
        

    def collect_traj(self):

	n_step_n =  self.params['n_step_new']
	n_step_o =  self.params['n_step_old']

	file_old = "./traj_time.out"
	file_new = "./restart/traj_time.out"

	label_new = open(file_new, "r")
	label_old = open(file_old, "a")

	n_atom=int(label_new.readline())

	for i_line in range(n_atom+1):
           line=label_new.readline()

	for i_step in range(n_step_n-1):
           line=label_new.readline()
	   label_old.write(line)

           line=label_new.readline()
	   record = line.split()
	   record[2] = n_step_o + i_step
	   record[4] = record[2]*self.params['dt_new']*41.3407927177

	   label_old.write(str(record[0])+' ' +str(record[1])+'          ' +str(record[2])+' ' + str(record[3])+'        ' +str(record[4])+'\n')


	   for i_line in range(n_atom):
              line=label_new.readline()
	      label_old.write(line)


        label_new.close()
        label_old.close()

	return

    def collect_vel(self):

	n_step_n =  self.params['n_step_new']
	n_step_o =  self.params['n_step_old']

	file_old = "./vel_time.out"
	file_new = "./restart/vel_time.out"

	label_new = open(file_new, "r")
	label_old = open(file_old, "a")

	n_atom=int(label_new.readline())

	for i_line in range(n_atom+1):
           line=label_new.readline()

	for i_step in range(n_step_n-1):
           line=label_new.readline()
	   label_old.write(line)

           line=label_new.readline()
	   record = line.split()
	   record[2] = n_step_o + i_step
	   record[4] = record[2]*self.params['dt_new']*41.3407927177

	   label_old.write(str(record[0])+' ' +str(record[1])+'          ' +str(record[2])+' ' + str(record[3])+'        ' +str(record[4])+'\n')


	   for i_line in range(n_atom):
              line=label_new.readline()
	      label_old.write(line)


        label_new.close()
        label_old.close()

	return
        

    def collect_gra(self):

	n_step_n =  self.params['n_step_new']
	n_step_o =  self.params['n_step_old']

	file_old = "./grad_time.out"
	file_new = "./restart/grad_time.out"

	label_new = open(file_new, "r")
	label_old = open(file_old, "a")

	n_atom=int(label_new.readline())

	for i_line in range(n_atom+1):
           line=label_new.readline()

	for i_step in range(n_step_n-1):
           line=label_new.readline()
	   label_old.write(line)

           line=label_new.readline()
	   record = line.split()
	   record[2] = n_step_o + i_step
	   record[4] = record[2]*self.params['dt_new']*41.3407927177

	   label_old.write(str(record[0])+' ' +str(record[1])+'          ' +str(record[2])+' ' + str(record[3])+'        ' +str(record[4])+'\n')


	   for i_line in range(n_atom):
              line=label_new.readline()
	      label_old.write(line)


        label_new.close()
        label_old.close()

	return
        
    def collect_energy(self):

	n_step_n =  self.params['n_step_new']
	n_step_o =  self.params['n_step_old']

	file_old = "./energy_time.out"
	file_new = "./restart/energy_time.out"

	label_new = open(file_new, "r")
	label_old = open(file_old, "a")

	label_new.readline()
	label_new.readline()
	label_new.readline()

	for i_line in range(n_step_n - 1):
           line=label_new.readline()
	   record = line.split()
	   record[0] = n_step_o + i_line
	   record[1] = record[0]*self.params['dt_new']

	   label_old.write('      '+ str(record[0])+'       ' +str(record[1])+'              ' +str(record[2])+'         ' + str(record[3])+'      ' +str(record[4])+'         ' +str(record[5])+'         ' +str(record[6])+'         ' +str(record[7])+'\n')

        label_new.close()
        label_old.close()
	return
	   
    def collect_ele(self):

	n_step_n =  self.params['n_step_new']
	n_step_o =  self.params['n_step_old']

	file_old = "./ele_time.out"
	file_new = "./restart/ele_time.out"

	label_new = open(file_new, "r")
	label_old = open(file_old, "a")

	pattern = re.compile("------------------")
	line = "NOT EMPTY LINE"

        for i_step in range(n_step_n-1):

           line=label_new.readline()
	   label_old.write(line)
	   
	   while line != "":
              line = label_new.readline()

	      m = pattern.search(line)
	      if m is not None:
	         label_old.write(line)
	         break
              
	      record = line.split()

	      record[0] = n_step_o + i_step
	      record[1] = record[0]*self.params['dt_new']

	      n_list = len(record)
	      for i_list in range(n_list):
	         label_old.write(' '+ str(record[i_list]))

	      label_old.write('\n')


        label_new.close()
        label_old.close()

	return

    def collect_others(self):
        shell_txt = """
	        rm -rf QC_TMP
		cp -r restart/QC_TMP      ./
		cp restart/coor_temp.xyz  ./
		cp restart/qm_interface   ./
		cp restart/interface.json ./
		cp restart/qm_results.dat ./
		cp restart/curr_geom.tmp  ./
		cp restart/*err           ./
		cp restart/*log           ./
		cp restart/restart_all    ./
		cp restart/dynamics.out   ./
		cp restart/fort*          ./
	            """              
        os.system(shell_txt)
	return
       
        

if __name__ == "__main__":
    restart = jobrestart()
    restart.get_old_inp()
    restart.get_new_inp()
    restart.collect_state()
    restart.collect_pe()
    restart.collect_hop()
    restart.collect_traj()
    restart.collect_vel()
    restart.collect_gra()
    restart.collect_energy()
    restart.collect_ele()
    restart.collect_others()
