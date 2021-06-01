subroutine sub_read_control
use mod_main
implicit none
integer file_dyn_in
integer ntime, n_sav_stat, n_sav_traj
integer ntime_ele
integer dyn_method, label_ZN
integer i_state, seed_random
integer label_reject_hops, label_read_velocity
real(kind=8) time, dtime, cor_dec, hop_e
character (len=256) md_state_list
namelist /control/ dyn_method, label_ZN, ntime, dtime, & 
         n_sav_stat, n_sav_traj, ntime_ele, &
         qm_method, & ! used and in mod_main
         n_state, & ! re-read in mapping_control
         md_state_list, i_state, &
         seed_random, cor_dec, &
         label_nac_phase, &  ! used and in mod_main
         label_reject_hops, &
         hop_e, label_read_velocity, label_restart
namelist /mapping_control/ n_mode, n_mode_HO, n_mode_tor, &
         n_step, nuc_dt, n_ele_dt, &
         n_save_trj, label_restart,label_diabatic, &
         n_state, ggamma, label_debug, hamilton_type, &
         mapping_model, label_aver_PES
file_dyn_in=11       
open(unit=file_dyn_in, file="dyn.inp")      
read(file_dyn_in, nml = control)
read(file_dyn_in, nml = mapping_control)
close(11)

if (mapping_model == 102 .or. mapping_model == 1021) then
  open(10, file="stru_xyz.in")
  read (10, *) n_atom
  close(11)
endif

if ( hamilton_type == 3 ) then
  if (n_mode /= n_mode_HO) stop 'Input error! This hamilton type 3, so n_mode should be equal to n_mode_HO!'
  if (n_mode_tor /= 0) stop 'Input error! n_mode_tor /= 0. If including torsional modes, please use hamiltonian type 4!'
elseif ( hamilton_type == 4 ) then
  if (n_mode /= n_mode_HO + n_mode_tor) stop 'Input error!  n_mode /= n_mode_HO + n_mode_tor'
  if (n_mode_tor == 0) stop 'Input error! n_mode_tor should not be zero for hamiltonian type 4!'
elseif ( hamilton_type == 0 ) then
  if ( mod(n_mode, 3) == 0 ) then
    n_atom = n_mode/3
  else
    stop "n_mode/3 .ne. n_atom"
  endif
endif

end
