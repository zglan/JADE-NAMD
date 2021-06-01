module mod_main
integer :: n_state, &
           n_atom, &
           n_mode, &
           n_mode_HO, &
           n_mode_tor, &
           n_step, &
           n_save_trj, &
           label_restart, &
           label_diabatic, &
           n_ele_dt, &
           qm_method, &
           label_aver_PES
integer label_debug
integer label_nac_phase
integer hamilton_type
integer mapping_model
double precision :: nuc_dt
double precision :: ggamma

end
