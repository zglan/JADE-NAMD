subroutine sub_elec_motion_2_aver_PES(x_mode_cur, p_mode_cur, &
                           x_mode_pre, p_mode_pre, &
                           x_elec, p_elec, &
                           freq, k_tun, exci_e, &
                           lambda0, lambda1)
use mod_main
implicit none
! --- arguments ---
real(kind=8), dimension(n_mode) :: x_mode_cur, p_mode_cur, & 
                                   x_mode_pre, p_mode_pre
real(kind=8), dimension(n_state) :: x_elec, &
                                    p_elec, &
                                    exci_e
real(kind=8) k_tun(n_state, n_mode)
real(kind=8) freq(n_state, n_mode)
real(kind=8) lambda0(n_mode, n_state, n_state)
real(kind=8) lambda1(n_mode, n_state, n_state)

! --- local variables ---
real(kind=8) Ham(n_state, n_state)
real(kind=8), dimension(n_mode) :: x_mode_cur_tmp, &
                                   p_mode_cur_tmp, &
                                   delt_x, &
                                   delt_p
real(kind=8) ele_dt, ele_dt_half
real(kind=8), dimension(n_state) ::  dH_div_dx, &
                                     dH_div_dp, &
                                     delt_x_elec, &
                                     delt_p_elec
integer i_ele_step



ele_dt = nuc_dt / dble(n_ele_dt)
ele_dt_half = 0.5d0 * ele_dt
delt_x = (x_mode_cur - x_mode_pre) / dble(n_ele_dt)
delt_p = (p_mode_cur - p_mode_pre) / dble(n_ele_dt)

x_mode_cur_tmp = x_mode_pre
p_mode_cur_tmp = p_mode_pre
!  write(*,*) x_elec
do i_ele_step = 1, n_ele_dt
  call sub_get_dia_Ham_elec(x_mode_cur_tmp, p_mode_cur_tmp, &
                            freq, k_tun, exci_e, lambda0, lambda1, &
                            Ham)
  !write(*,*) 'Ham', Ham
  !write(*,*) ele_dt
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of p
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  call sub_elec_get_dH_div_dx_or_dp_aver_PES(n_state, Ham, x_elec, dH_div_dx)

  delt_p_elec = -dH_div_dx

  call sub_move(n_state, p_elec, delt_p_elec, ele_dt_half) 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! one step of x
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  call sub_elec_get_dH_div_dx_or_dp_aver_PES(n_state, Ham, p_elec, dH_div_dp)

  delt_x_elec = dH_div_dp

  call sub_move(n_state, x_elec, delt_x_elec, ele_dt)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of p
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  call sub_elec_get_dH_div_dx_or_dp_aver_PES(n_state, Ham, x_elec, dH_div_dx)

  delt_p_elec = -dH_div_dx

  call sub_move(n_state, p_elec, delt_p_elec, ele_dt_half) 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  x_mode_cur_tmp = x_mode_cur_tmp + delt_x
  p_mode_cur_tmp = p_mode_cur_tmp + delt_p
  
enddo


return
end
