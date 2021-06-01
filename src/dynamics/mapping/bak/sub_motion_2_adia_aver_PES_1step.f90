subroutine sub_mapping_motion_2_adia_aver_PES_1step(&
                            x_elec, &
                            p_elec, &
                            coor_x, &
                            coor_y, &
                            coor_z, &
                            vel_x, &
                            vel_y, &
                            vel_z, &
                            ene_adia_cur, &
                            gra_all_x, &
                            gra_all_y, &
                            gra_all_z, &
                            nac_x, &
                            nac_y, &
                            nac_z, &
                            mass, &
                            old_coor_x, &
                            old_coor_y, &
                            old_coor_z, &
                            old_vel_x, &
                            old_vel_y, &
                            old_vel_z, &
                            ene_adia_pre, &
                            old_gra_all_x, &
                            old_gra_all_y, &
                            old_gra_all_z, &
                            old_nac_x, &
                            old_nac_y, &
                            old_nac_z)
use mod_main
implicit none

include 'param.def'

real(kind=8) x_nuc_cur(n_mode)
real(kind=8) p_nuc_cur(n_mode)
real(kind=8) x_nuc_pre(n_mode)
real(kind=8) p_nuc_pre(n_mode)
real(kind=8) p_nuc_kin_cur(n_mode)
real(kind=8) p_nuc_kin_pre(n_mode)
real(kind=8) mass(n_mode)
real(kind=8) x_elec(n_state)
real(kind=8) p_elec(n_state)
real(kind=8) ene_adia_cur(n_state)
real(kind=8) ene_adia_pre(n_state)
real(kind=8) c_n(n_state, n_state)
real(kind=8)  a_hamiton (n_state, n_state)
real(kind=8) dia_hamiton(n_state, n_state)
real(kind=8) grad(n_state, n_mode)
real(kind=8) dij_cur(n_state, n_state, n_mode)
real(kind=8) dij_pre(n_state, n_state, n_mode)

! --- local variables ---
real(kind=8), dimension(n_mode) :: p_nuc_kin_cur_div_mass
real(kind=8), dimension(n_mode) :: p_nuc_kin_pre_div_mass
real(kind=8) delt_ene_pre, delt_ene_cur, dtmp1, dtmp2
integer i_mode, i_state, j_state


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!      
if(label_debug >= 1) then
  write(*,*) 'sub_motion_2_adia_aver_PES_1step'
  write(*,*) 'p_nuc_cur:'
  do i_mode = 1, n_mode
    write(*,*) p_nuc_cur(i_mode)
  enddo
  write(*,*) 'nuc_dt', nuc_dt
  write(*,*)
endif
do i_mode = 1, n_mode
  dij_pre(:,:,i_mode) = dHmn_div_dX_adia_pre(i_mode,:,:)
  dij_cur(:,:,i_mode) = dHmn_div_dX_adia_cur(i_mode,:,:)
enddo
do i_state = 1, n_state
  dij_pre(i_state,i_state,:) = 0.d0
  dij_cur(i_state,i_state,:) = 0.d0
enddo
do i_state = 1, n_state - 1
  do j_state = i_state + 1, n_state
    delt_ene_pre = ene_adia_pre(i_state) - ene_adia_pre(j_state)
    delt_ene_cur = ene_adia_cur(i_state) - ene_adia_cur(j_state)
    do i_mode = 1, n_mode
      dij_pre(i_state, j_state, i_mode) = dij_pre(i_state, j_state, i_mode) / delt_ene_pre
      dij_cur(i_state, j_state, i_mode) = dij_cur(i_state, j_state, i_mode) / delt_ene_cur
      dij_pre(j_state, i_state, i_mode) = - dij_pre(j_state, i_state, i_mode) / delt_ene_pre
      dij_cur(j_state, i_state, i_mode) = - dij_cur(j_state, i_state, i_mode) / delt_ene_cur
    enddo
  enddo
enddo

if(label_debug >= 2) then
  write(*,*) 'dij_cur(1,2,:)'
  write(*,*) dij_cur(1,2,:)
  write(*,*) 'dij_pre(1,2,:)'
  write(*,*) dij_pre(1,2,:)
  write(*,*)
endif
do i_state = 1, n_state
  grad(i_state,:) = dHmn_div_dX_adia_cur(:,i_state,i_state)
enddo

!      call sub_init_random_seed()
!call sub_read_trj_2(x_nuc_cur, p_nuc_cur, &
!                    x_nuc_pre, p_nuc_pre, &
!                    x_elec, p_elec)
!                    
!call sub_read_parameter(ene_adia_cur, ene_adia_pre, &
!                    grad, dij_cur, dij_pre, mass)

p_nuc_kin_cur = 0.d0

if(label_debug > 1) write(*,*) "cur"
call sub_p_to_p_kin(p_nuc_cur, p_nuc_kin_cur, &
                    dij_cur, &
                    x_elec, p_elec)
if(label_debug > 1) write(*,*)

if(label_debug > 1) write(*,*) "pre"                
call sub_p_to_p_kin(p_nuc_pre, p_nuc_kin_pre, &
                    dij_pre, &
                    x_elec, p_elec)
if(label_debug > 1) write(*,*)
p_nuc_kin_cur_div_mass = p_nuc_kin_cur / mass
p_nuc_kin_pre_div_mass = p_nuc_kin_pre / mass

if (label_aver_PES == 1) then


  x_nuc_pre = x_nuc_cur
  p_nuc_pre = p_nuc_cur
  dHmn_div_dX_adia_pre = dHmn_div_dX_adia_cur
  ene_adia_pre = ene_adia_cur
  call sub_nuc_motion_2_aver_PES_adia( x_nuc_cur, &
                    p_nuc_kin_cur, &
                    mass, &
                    x_elec, p_elec, &
                    ene_adia_cur, &
                    grad, dij_cur)
!#!   write(*,*) 'sub_nuc_motion done'
!#
  if(label_debug > 1) then
    write(*,*) 'sub_motion_2_adia_aver_PES_1step'
    write(*,*) 'call sub_nuc_motion_2_aver_PES_adia done'
    write(*,*) 'p_nuc_kin_cur'
    do i_mode = 1, n_mode
      write(*,*) p_nuc_kin_cur(i_mode)
    enddo
    write(*,*)
  endif
else
  write(*,*) "Subroutines for non-aver_PES are not available now!"
endif

call sub_p_kin_to_p(p_nuc_cur, p_nuc_kin_cur, &
                    dij_cur, &
                    x_elec, p_elec)
!call sub_write_trj_2(x_elec, p_elec, x_nuc_cur, p_nuc_cur)
if(label_debug >= 1) then
  write(*,*) 'sub_motion_2_adia_aver_PES_1step'
  write(*,*) 'call sub_p_kin_to_p done'
  write(*,*) 'p_nuc_cur'
  do i_mode = 1, n_mode
    write(*,*) p_nuc_cur(i_mode)
  enddo
  write(*,*)
endif
  call sub_elec_motion_2_aver_PES_adia(p_nuc_kin_cur_div_mass, &
                    p_nuc_kin_pre_div_mass, &
                    x_elec, p_elec, &
                    ene_adia_cur, ene_adia_pre, &
                    dij_cur, dij_pre)
!#  write(*,*) 'sub_elec_motion done'
!#!     call sub_get_c_n_elec_2(x_elec, p_elec, c_n)
!#!
  if(label_debug > 1) then
    write(*,*) 'sub_motion_2_adia_aver_PES_1step'
    write(*,*) 'call sub_elec_motion_2_aver_PES_adia done'
    write(*,*) 'p_nuc_cur'
    do i_mode = 1, n_mode
      write(*,*) p_nuc_cur(i_mode)
    enddo
    write(*,*)
    write(*,*) 'i_state, x_elec, p_elec'
    do i_state = 1, n_state
      write(*,*) i_state, x_elec(i_state), p_elec(i_state)
    enddo
  endif
end
