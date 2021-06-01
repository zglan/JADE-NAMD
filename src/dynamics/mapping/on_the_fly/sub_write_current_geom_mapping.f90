subroutine sub_write_current_geom_mapping(x_nuc_cur, &
                  p_nuc_cur, &
                  atom_label, &
                  x_elec, p_elec, &
                  i_step)
use mod_main
implicit none
include 'var_n_atom.h'
include 'var_n_mode.h'
integer index_state !useless
integer i_step
integer i_state


call sub_reshape_n_mode_to_n_atom(x_nuc_cur, &
                  p_nuc_cur, &
                  grad, &
                  dij_cur, &
                  coor_x, coor_y, coor_z, &
                  vel_x, vel_y, vel_z, &
                  gra_all_x, gra_all_y, gra_all_z, &
                  nac_x, nac_y, nac_z)
!write(*,*) atom_label(1)
call sub_write_current_geom (n_atom, &
                  coor_x, coor_y, coor_z, &
                  vel_x, vel_y, vel_z, &
                  atom_label, &
                  n_state, &
                  rho, &
                  index_state, &
                  i_step, time )

return
end
