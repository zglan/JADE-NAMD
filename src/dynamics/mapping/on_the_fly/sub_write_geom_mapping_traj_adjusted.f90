subroutine sub_write_geom_mapping_traj_adjusted(x_nuc_cur, &
                  p_nuc_cur, &
                  p_nuc_kin_cur, &
                  atom_label, &
                  mass, &
                  x_elec, p_elec, &
                  gammas, &
                  ene_adia_cur, &
                  i_step)
use mod_main
implicit none
include 'var_n_atom.h'
include 'var_n_mode.h'
include 'param.def'
integer index_state !useless
integer i_step
integer i_state
integer j_state
integer i_mode
real(kind=8) c_n(n_state, n_state)
real(kind=8) ene_all_cur
real(kind=8) ene_nuc_kin
real(kind=8) ene_nuc_kin_mapping
real(kind=8) tmp

time = dble(i_step) * nuc_dt * TOFS

if(label_debug >= 2) then
  write(*,*)
  write(*,*) "sub_write_geom_mapping"
  write(*,*) "i_step:", i_step
  write(*,*) "i_mode  mass  x_nuc_cur  p_nuc_cur"
  do i_mode = 1, n_mode
    write(*,*) i_mode, mass(i_mode), x_nuc_cur(i_mode), p_nuc_cur(i_mode)
  enddo
  write(*,*) "atom_label"
  do i_mode = 1, n_atom
    write(*,*) i_mode, atom_label(i_mode)
  enddo
  write(*,*) "i_state  x_elec  p_elec  ene_adia_cur"
  do i_state = 1, n_state
    write(*,*) i_state, x_elec(i_state), p_elec(i_state), ene_adia_cur(i_state)
  enddo
endif

ene_all_cur = 0.d0
tmp = 0.d0
do i_state = 1, n_state
  tmp = tmp + ene_adia_cur(i_state)
enddo
ene_all_cur = ene_all_cur + tmp/dble(n_state)

tmp = 0.d0

call sub_get_c_n_elec_2_traj_adjusted(x_elec, &
                                      p_elec, &
                                      gammas, &
                                      c_n)

do i_state = 1, n_state
  do j_state = 1, n_state
    tmp = tmp + ( c_n(i_state, i_state) - c_n(j_state, j_state) )  &
              *  (ene_adia_cur(i_state) - ene_adia_cur(j_state))
  enddo
enddo
ene_all_cur = ene_all_cur + tmp/(dble(n_state)*2.d0)

!do i_state = 1, n_state
!  ene_all_cur = ene_all_cur + &
!  ene_adia_cur(i_state) * 0.5 * (x_elec(i_state)**2 + p_elec(i_state)**2 - ggamma)
!enddo

ene_nuc_kin = 0.d0
do i_mode = 1, n_mode
  ene_nuc_kin = ene_nuc_kin + 0.5 * p_nuc_kin_cur(i_mode) **2 / mass(i_mode)
enddo

ene_all_cur = ene_all_cur + ene_nuc_kin

call sub_reshape_n_mode_to_n_atom(x_nuc_cur, &
                  p_nuc_cur, &
                  grad, &
                  dij_cur, &
                  coor_x, coor_y, coor_z, &
                  vel_x, vel_y, vel_z, &
                  gra_all_x, gra_all_y, gra_all_z, &
                  nac_x, nac_y, nac_z)

call sub_write_geom (n_atom, &
                  coor_x, coor_y, coor_z, &
                  vel_x, vel_y, vel_z, &
                  atom_label, &
                  n_state, &
                  rho, &
                  index_state, &
                  i_step, time )

if (i_step .eq. 0) then
  open(100, file="ene.dat")
  open(101, file="pe_time.out")
  write(100,*) "#i_step     time     ene_all(AU)    ene_nuc_kin   ene_1   ene_2  ..."
else
  open(100, position='append', file="ene.dat")
  open(101, position='append', file="pe_time.out")
endif
write(100,9997) i_step, time, ene_all_cur, ene_nuc_kin, ene_adia_cur(:)
write(101,9997) i_step, time, ene_adia_cur(:)

close(100)
close(101)
9997   format(i10, 1x, 20(f20.10, 1x))
return
end
