subroutine sub_elec_motion_3(n_mode, n_state, &
                           x_mode_cur, p_mode_cur, &
                           x_mode_pre, p_mode_pre, &
                           x_elec, y_elec, &
                           p_x_elec, p_y_elec, &
                           nuc_dt, n_ele_dt, &
                           freq, k_tun, exci_e, &
                           lambda0, lambda1)
implicit none
! --- arguments ---
integer n_state
integer n_mode
integer n_ele_dt
real(kind=8) nuc_dt
real(kind=8), dimension(n_mode) :: x_mode_cur, p_mode_cur, & 
                                   x_mode_pre, p_mode_pre
real(kind=8), dimension(n_state) :: x_elec, &
                                    y_elec, &
                                    p_x_elec, &
                                    p_y_elec, &
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
real(kind=8) ele_dt, ele_dt_half, ele_dt_4th, ele_dt_8th
real(kind=8), dimension(n_state) ::  dH_div_dx, &
                                     dH_div_dy, &
                                     dH_div_dp_x, &
                                     dH_div_dp_y, &
                                     delt_x_elec, &
                                     delt_y_elec, &
                                     delt_p_x_elec, &
                                     delt_p_y_elec
integer i_ele_step, i



ele_dt = nuc_dt / dble(n_ele_dt)
ele_dt_half = 0.5d0 * ele_dt
ele_dt_4th = 0.25d0 * ele_dt
ele_dt_8th = 0.125d0 * ele_dt
delt_x = (x_mode_cur - x_mode_pre) / dble(n_ele_dt)
delt_p = (p_mode_cur - p_mode_pre) / dble(n_ele_dt)

x_mode_cur_tmp = x_mode_pre
p_mode_cur_tmp = p_mode_pre
!  write(*,*) x_elec
do i_ele_step = 1, n_ele_dt
  !write(*,*) i_ele_step
  call sub_get_dia_Ham_elec(n_state, n_mode, x_mode_cur_tmp, p_mode_cur_tmp, &
                            freq, k_tun, exci_e, lambda0, lambda1, &
                            Ham)
  !write(*,*) 'Ham', Ham
  !write(*,*) ele_dt
  call sub_elec_motion_3_step1(n_state, x_elec, y_elec, p_x_elec, p_y_elec, Ham, ele_dt)
  !write(*,*) x_elec(1), y_elec(1), p_x_elec(1), p_y_elec(1)

  call sub_elec_motion_3_step2(n_state, x_elec, y_elec, p_x_elec, p_y_elec, Ham, ele_dt)
  !write(*,*) x_elec(1), y_elec(1), p_x_elec(1), p_y_elec(1)

  call sub_elec_motion_3_step1(n_state, x_elec, y_elec, p_x_elec, p_y_elec, Ham, ele_dt)
  !write(*,*) x_elec(1), y_elec(1), p_x_elec(1), p_y_elec(1)

  x_mode_cur_tmp = x_mode_cur_tmp + delt_x
  p_mode_cur_tmp = p_mode_cur_tmp + delt_p
enddo
!  write(*,*) x_elec
!  write(*,*) Ham(1,1), Ham(2,2)

return
end
