subroutine sub_elec_motion_3_step2(n_state, &
                                   x_elec, &
                                   y_elec, &
                                   p_x_elec, &
                                   p_y_elec, &
                                   Ham, &
                                   ele_dt)
implicit none
! --- arguments ---
integer n_state
real(kind=8) Ham(n_state, n_state)
real(kind=8), dimension(n_state) :: x_elec
real(kind=8), dimension(n_state) :: y_elec
real(kind=8), dimension(n_state) :: p_x_elec
real(kind=8), dimension(n_state) :: p_y_elec
real(kind=8)  ele_dt

! --- local variables ---
integer i,j
real(kind=8) ele_dt_half, ele_dt_4th, ele_dt_8th
real(kind=8) Ham_nn(n_state)
real(kind=8) delt(n_state)
real(kind=8), dimension(n_state) :: dH_div_dx

ele_dt_half = 0.5d0 * ele_dt
ele_dt_4th = 0.25d0 * ele_dt
ele_dt_8th = 0.125d0 * ele_dt

do i = 1, n_state
  Ham_nn(i) = Ham(i,i)
enddo

! update p_y_elec 1/4 dt
delt = - Ham_nn * y_elec
call sub_move(n_state, p_y_elec, delt, ele_dt_4th)

! update y_elec 1/2 dt
call sub_elec_motion_3_step2_2(n_state, Ham, y_elec, x_elec, ele_dt_half)

! update p_y_elec 1/2 dt
call sub_elec_motion_3_step2_2(n_state, Ham, p_y_elec, p_x_elec, ele_dt_half)

! update y_elec 1/2 dt
delt = Ham_nn * p_y_elec
call sub_move(n_state, y_elec, delt, ele_dt_half)

! update y_elec 1/2 dt
call sub_elec_motion_3_step2_2(n_state, Ham, y_elec, x_elec, ele_dt_half)

! update p_y_elec 1/2 dt
call sub_elec_motion_3_step2_2(n_state, Ham, p_y_elec, p_x_elec, ele_dt_half)

! update p_y_elec 1/4 dt
delt = - Ham_nn * y_elec
call sub_move(n_state, p_y_elec, delt, ele_dt_4th)


return
end
