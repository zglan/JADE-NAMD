subroutine sub_read_current_geom_mapping(x_nuc_cur, &
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
integer i_state, i

               
call sub_read_current_geom (n_atom, &
                  coor_x, coor_y, coor_z, &
                  vel_x, vel_y, vel_z, &
                  atom_label, &
                  n_state, &
                  rho, &
                  index_state, &
                  i_step, time )
if (label_debug >= 2 ) then
  write(*,*) 'call sub_read_current_geom done'
  write(*,*) "vel"
  do i = 1, n_atom
    write(*,*) i, vel_x(i), vel_y(i), vel_z(i)
  enddo
endif
call sub_reshape_n_atom_to_n_mode(x_nuc_cur, &
                  p_nuc_cur, &
                  grad, &
                  dij_cur, &
                  coor_x, coor_y, coor_z, &
                  vel_x, vel_y, vel_z, &
                  gra_all_x, gra_all_y, gra_all_z, &
                  nac_x, nac_y, nac_z)
if (label_debug >= 2 ) then
  write(*,*) 'call sub_reshape_n_atom_to_n_mode done'
  write(*,*) "i_mode  p_nuc_cur"
  do i = 1, n_mode
    write(*,*) i, p_nuc_cur(i)
  enddo
endif
if (i_step == 0) then
  if (label_debug >= 2 ) write(*,*) 'Read trj_elec input.'
  open(21, file="trj_elec.input")
  do i_state = 1, n_state
    if (label_debug >= 2 ) write(*,*) i_state
    read(21, *) x_elec(i_state), p_elec(i_state)
    if (label_debug >= 2 ) write(*,*) x_elec(i_state), p_elec(i_state)
  enddo
  if (label_debug >= 2 ) write(*,*) "Cycle done"
  close(21)
  if (label_debug >= 2 ) write(*,*) 'Read trj_elec input done.'
endif



return
end
