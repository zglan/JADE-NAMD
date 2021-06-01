subroutine sub_elec_motion_2_aver_PES_1step_adia(p_nuc_div_mass, &
                           x_elec, &
                           p_elec, &
                           ene, &
                           dij, &
                           ele_dt)
use mod_main
implicit none
! --- arguments ---
real(kind=8), dimension(n_mode) :: p_nuc_div_mass
real(kind=8), dimension(n_state) :: x_elec, &
                                    p_elec
real(kind=8), dimension(n_state) :: ene
real(kind=8), dimension(n_state, n_state, n_mode):: dij
real(kind=8) ele_dt, ele_dt_half
real(kind=8) dssign

! --- local variables ---
real(kind=8), dimension(n_state) :: delt_x_elec, &
                                    delt_p_elec
integer i_state, i_mode
real(kind=8) dtmp

ele_dt_half = ele_dt * 0.5d0
delt_x_elec = 0.d0
delt_p_elec = 0.d0

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of p
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
dssign = -1.d0
call sub_elec_motion_2_aver_PES_1step_dx_div_dt_adia(dssign, &
                           p_nuc_div_mass, &
                           p_elec, &
                           x_elec, &
                           ene, &
                           dij, &
                           delt_p_elec)
if(label_debug >= 2) then
  write(*,*) 'sub_elec_motion_2_aver_PES_1step_adia'
  write(*,*) 'call sub_elec_motion_2_aver_PES_1step_dx_div_dt_adia done'
  write(*,*) 'i_state, x_elec, p_elec, delt_p_elec'
  do i_state = 1, n_state
    write(*,*) i_state, x_elec(i_state), p_elec(i_state), delt_p_elec(i_state)
  enddo
  write(*,*) 'ele_dt_half:',ele_dt_half
  write(*,*)
endif
call sub_move(n_state, p_elec, delt_p_elec, ele_dt_half)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! one step of x
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
dssign = 1.d0
call sub_elec_motion_2_aver_PES_1step_dx_div_dt_adia(dssign, &
                           p_nuc_div_mass, &
                           x_elec, &
                           p_elec, &
                           ene, &
                           dij, &
                           delt_x_elec)
call sub_move(n_state, x_elec, delt_x_elec, ele_dt)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of p
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
dssign = -1.d0
call sub_elec_motion_2_aver_PES_1step_dx_div_dt_adia(dssign, &
                           p_nuc_div_mass, &
                           p_elec, &
                           x_elec, &
                           ene, &
                           dij, &
                           delt_p_elec)
call sub_move(n_state, p_elec, delt_p_elec, ele_dt_half)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

return
end
