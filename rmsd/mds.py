#! /usr/bin/env python
import rmsd_analys
import mds_cla
import mds_analys
import sub_inp_json as json
import os
import shutil

inp = json.load_json('inp.json')
inp['job_select'] = raw_input("which job do u choose,classical or isomap(classical/isomap):")
inp['rmsd_cutoff'] = raw_input("Input the rmsd_cutoff value:")
if inp['job_select'] == 'isomap':
    inp['mds_cutoff'] = raw_input("Input the mds_cutoff value:")
inp['mds_dimension'] = raw_input("Choose mds dimension:")
json.dump_json('inp.json',inp)

if inp['job_select'] == 'isomap':
    file_name = inp['job_select'] + '_rmsdcut_' + inp['rmsd_cutoff'] + '_mdscut_' + inp['mds_cutoff']
if inp['job_select'] == 'classical':
    file_name = inp['job_select'] + '_rmsdcut_' + inp['rmsd_cutoff'] 
curr_dir = os.getcwd()
workdir = curr_dir + '/' + file_name
if os.path.exists(workdir):
    shutil.rmtree(workdir)
os.mkdir(workdir)
command1 = 'cp -r all ' +  workdir
command2 = 'cp inp.json '  + workdir
os.system(command1)
os.system(command2)
os.chdir(workdir)
rmsd_analys.make()
mds_cla.make()
mds_analys.make()
os.chdir(curr_dir)

