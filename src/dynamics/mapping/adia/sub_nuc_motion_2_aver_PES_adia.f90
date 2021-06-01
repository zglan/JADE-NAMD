subroutine sub_nuc_motion_2_aver_PES_adia( x_nuc_cur, &
                    p_nuc_kin_cur, &
                    mass, &
                    x_elec, p_elec, &
                    ene, &
                    grad, dij_cur)
use mod_main
implicit none
! --- arguments ---
real(kind=8), dimension(n_mode) :: x_nuc_cur
real(kind=8), dimension(n_mode) :: p_nuc_kin_cur
real(kind=8), dimension(n_mode) :: mass
real(kind=8), dimension(n_state) :: x_elec
real(kind=8), dimension(n_state) :: p_elec
real(kind=8), dimension(n_state) :: ene
real(kind=8), dimension(n_state, n_mode) :: grad
real(kind=8), dimension(n_state, n_state, n_mode) :: dij_cur

! --- local variables ---
real(kind=8), dimension(n_mode) :: dp_nuc_kin_div_dt
real(kind=8), dimension(n_mode) :: dx_nuc_div_dt
real(kind=8) nuc_dt_half

nuc_dt_half = 0.5d0 * nuc_dt

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of P
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
call sub_nuc_motion_2_aver_PES_1step_dp_div_dt_adia(dp_nuc_kin_div_dt, &
                           grad, &
                           x_elec, p_elec, &
                           ene, &
                           dij_cur)
call sub_move(n_mode, p_nuc_kin_cur, dp_nuc_kin_div_dt, nuc_dt_half)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! one step of X
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! calculate dx_nuc_div_dt
dx_nuc_div_dt = p_nuc_kin_cur / mass
call sub_move(n_mode, x_nuc_cur, dx_nuc_div_dt, nuc_dt)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of P
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
call sub_nuc_motion_2_aver_PES_1step_dp_div_dt_adia(dp_nuc_kin_div_dt, &
                           grad, &
                           x_elec, p_elec, &
                           ene, &
                           dij_cur)
call sub_move(n_mode, p_nuc_kin_cur, dp_nuc_kin_div_dt, nuc_dt_half)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

return
end
