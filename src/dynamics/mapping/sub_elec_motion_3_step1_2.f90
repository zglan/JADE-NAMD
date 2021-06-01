subroutine sub_elec_motion_3_step1_2(n_state, Ham, x_elec, y_elec, ele_dt)
implicit none
! --- arguments ---
integer n_state
real(kind=8) Ham(n_state, n_state)
real(kind=8), dimension(n_state) :: x_elec
real(kind=8), dimension(n_state) :: y_elec
real(kind=8) ele_dt

! --- local variables ---
integer i,j
real(kind=8), dimension(n_state) :: dH_div_dx
real(kind=8) delt(n_state)

call sub_elec_get_dH_div_dx_or_dp_3(n_state, Ham, y_elec, dH_div_dx)
!write(*,*) 'dH_div_d', dH_div_dx
delt = - dH_div_dx   !!!
!write(*,*) 'delt', delt
call sub_move(n_state, x_elec, delt, ele_dt)

return
end
