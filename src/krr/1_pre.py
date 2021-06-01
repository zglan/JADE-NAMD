#!/usr/bin/env python3


import os

import sub_energy_rescale
import sub_inp_json
from sub_select_sampling_rmsa_lixs import select_coord

os.system('cp ../input_initial.json ./')
filename = 'input_initial.json'
xxx_input = sub_inp_json.load_json(filename)
print(xxx_input)
n_atom = int(xxx_input['n_atom'])
n_traj = int(xxx_input['n_traj'])
n_freq = int(xxx_input['n_freq'])
n_select = int(xxx_input['n_select'])
n_s0 = int(xxx_input['n_s0'])
n_ci = int(xxx_input['n_ci'])
Energy_judge = float(xxx_input['Energy_judge'])
State_judge = float(xxx_input['State_judge'])
label_energy_scaling = xxx_input['label_energy_scaling']
n_y_dim = int(xxx_input['n_y_dim'])

if label_energy_scaling == "False":
    energy_zero = 0.0
    scaling_energy = 1.0
else:
    energy_zero = float(xxx_input['energy_zero'])
    scaling_energy = float(xxx_input['scaling_energy'])

if xxx_input['label_grad'] == 'YES':

    for i_y in range(n_y_dim):
        filename = "grad_time.out_S" + str(i_y)
        savefile = 'grad_sample_S' + str(i_y) + '.xyz'

        filein = 'inp.dat'
        fp = open(filein, "w")
        fp.write('n_atom       ' + str(n_atom) + '  \n')
        fp.write('n_y_dim      ' + str(n_y_dim) + '  \n')
        fp.write('n_traj       ' + str(n_traj) + '  \n')
        fp.write('n_freq       ' + str(n_freq) + '  \n')
        fp.write('n_select     ' + str(n_select) + '  \n')
        fp.write('n_s0         ' + str(n_s0) + '  \n')
        fp.write('n_ci         ' + str(n_ci) + '  \n')
        fp.write('Energy_judge ' + str(Energy_judge) + '  \n')
        fp.write('State_judge  ' + str(State_judge) + '  \n')
        fp.write('filename     ' + str(filename) + ' \n')
        fp.write('savefile     ' + str(savefile) + ' \n')
        fp.close()

        jobs = select_coord()
        jobs.make()

# --------------------------------------------------------

filename = "traj_time.out"
savefile = 'sample.xyz'

filein = 'inp.dat'
fp = open(filein, "w")
fp.write('n_atom       ' + str(n_atom) + '  \n')
fp.write('n_y_dim      ' + str(n_y_dim) + '  \n')
fp.write('n_traj       ' + str(n_traj) + '  \n')
fp.write('n_freq       ' + str(n_freq) + '  \n')
fp.write('n_select     ' + str(n_select) + '  \n')
fp.write('n_s0         ' + str(n_s0) + '  \n')
fp.write('n_ci         ' + str(n_ci) + '  \n')
fp.write('Energy_judge ' + str(Energy_judge) + '  \n')
fp.write('State_judge  ' + str(State_judge) + '  \n')
fp.write('filename     ' + str(filename) + ' \n')
fp.write('savefile     ' + str(savefile) + ' ')
fp.close()

jobs = select_coord()
jobs.make()
n_geom = jobs.num

xxx_input['n_geom'] = str(n_geom)
sub_inp_json.dump_json('input.json', xxx_input)

sub_energy_rescale.scale_energy_many(n_traj, energy_zero, scaling_energy, n_y_dim)
