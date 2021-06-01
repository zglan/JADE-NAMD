subroutine sub_nac_phase_mapping(dij_pre, &
                        dij_cur)
use mod_main
implicit none
include 'var_n_atom.h'
include 'var_n_mode.h'
integer index_state
integer label_ZN
integer i_step

label_ZN = 0

call sub_reshape_n_mode_to_n_atom(x_nuc_cur, &
                  p_nuc_cur, &
                  grad, &
                  dij_cur, &
                  coor_x, coor_y, coor_z, &
                  vel_x, vel_y, vel_z, &
                  gra_all_x, gra_all_y, gra_all_z, &
                  nac_x, nac_y, nac_z)

call sub_reshape_n_mode_to_n_atom(x_nuc_cur, &
                  p_nuc_cur, &
                  grad, &
                  dij_pre, &
                  coor_x, coor_y, coor_z, &
                  vel_x, vel_y, vel_z, &
                  gra_all_x, gra_all_y, gra_all_z, &
                  old_nac_x, old_nac_y, old_nac_z)
                  
call sub_nac_phase (n_atom, &
                  n_state, &
                  old_nac_x, &
                  old_nac_y, &
                  old_nac_z, &
                  nac_x, &
                  nac_y, &
                  nac_z)

call sub_reshape_n_atom_to_n_mode(x_nuc_cur, &
                  p_nuc_cur, &
                  grad, &
                  dij_cur, &
                  coor_x, coor_y, coor_z, &
                  vel_x, vel_y, vel_z, &
                  gra_all_x, gra_all_y, gra_all_z, &
                  nac_x, nac_y, nac_z)

call sub_reshape_n_atom_to_n_mode(x_nuc_cur, &
                  p_nuc_cur, &
                  grad, &
                  dij_pre, &
                  coor_x, coor_y, coor_z, &
                  vel_x, vel_y, vel_z, &
                  gra_all_x, gra_all_y, gra_all_z, &
                  old_nac_x, old_nac_y, old_nac_z)
return
end
