subroutine sub_elec_motion_mapping_1_Ham_4(x_mode_cur, p_mode_cur, &
                           x_mode_pre, p_mode_pre, &
                           x_elec, y_elec, &
                           p_x_elec, p_y_elec, &
                           freq, k_tun, exci_e, &
                           lambda0, lambda1, &
                           reduced_mass_inv_tor, &
                           tor_pot_para)
use mod_main
implicit none
! --- arguments ---
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
real(kind=8) reduced_mass_inv_tor(n_state, n_mode_tor)
real(kind=8) tor_pot_para(n_state, n_mode_tor)

! --- local variables ---
real(kind=8) Ham(n_state, n_state)
real(kind=8), dimension(n_mode) :: x_mode_cur_tmp, &
                                   p_mode_cur_tmp, &
                                   delt_x, &
                                   delt_p
real(kind=8) ele_dt, ele_dt_half
real(kind=8), dimension(n_state) ::  dH_div_dx, &
                                     dH_div_dy, &
                                     dH_div_dp_x, &
                                     dH_div_dp_y, &
                                     delt_x_elec, &
                                     delt_y_elec, &
                                     delt_p_x_elec, &
                                     delt_p_y_elec
integer i_ele_step



ele_dt = nuc_dt / dble(n_ele_dt)
ele_dt_half = 0.5d0 * ele_dt
delt_x = (x_mode_cur - x_mode_pre) / dble(n_ele_dt)
delt_p = (p_mode_cur - p_mode_pre) / dble(n_ele_dt)

x_mode_cur_tmp = x_mode_pre
p_mode_cur_tmp = p_mode_pre
!  write(*,*) x_elec
do i_ele_step = 1, n_ele_dt
  !write(*,*) i_ele_step
  call sub_get_dia_Ham_elec_Ham_4(x_mode_cur_tmp, p_mode_cur_tmp, &
                            freq, k_tun, exci_e, &
                            lambda0, lambda1, &
                            reduced_mass_inv_tor, &
                            tor_pot_para, &
                            Ham)
  !write(*,*) 'Ham', Ham
  !write(*,*) ele_dt
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of x
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  call sub_elec_get_dH_div_dx_or_dp(n_state, Ham, y_elec, dH_div_dp_x)

  delt_x_elec = -dH_div_dp_x

  call sub_move(n_state, x_elec, delt_x_elec, ele_dt_half) 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of p_x
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  call sub_elec_get_dH_div_dx_or_dp(n_state, Ham, p_y_elec, dH_div_dx)

  delt_p_x_elec = -dH_div_dx

  call sub_move(n_state, p_x_elec, delt_p_x_elec, ele_dt_half) 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! one step of y
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  call sub_elec_get_dH_div_dx_or_dp(n_state, Ham, x_elec, dH_div_dp_y)

  delt_y_elec = dH_div_dp_y

  call sub_move(n_state, y_elec, delt_y_elec, ele_dt)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! one step of p_y
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  call sub_elec_get_dH_div_dx_or_dp(n_state, Ham, p_x_elec, dH_div_dy)

  delt_p_y_elec = dH_div_dy

  call sub_move(n_state, p_y_elec, delt_p_y_elec, ele_dt)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of x
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  call sub_elec_get_dH_div_dx_or_dp(n_state, Ham, y_elec, dH_div_dp_x)

  delt_x_elec = -dH_div_dp_x

  call sub_move(n_state, x_elec, delt_x_elec, ele_dt_half) 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of p_x
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  call sub_elec_get_dH_div_dx_or_dp(n_state, Ham, p_y_elec, dH_div_dx)

  delt_p_x_elec = -dH_div_dx

  call sub_move(n_state, p_x_elec, delt_p_x_elec, ele_dt_half) 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  x_mode_cur_tmp = x_mode_cur_tmp + delt_x
  p_mode_cur_tmp = p_mode_cur_tmp + delt_p
enddo
!  write(*,*) x_elec
!  write(*,*) Ham(1,1), Ham(2,2)

return
end
