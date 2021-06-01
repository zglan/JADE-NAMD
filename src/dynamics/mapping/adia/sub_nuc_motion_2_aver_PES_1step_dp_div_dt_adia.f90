subroutine sub_nuc_motion_2_aver_PES_1step_dp_div_dt_adia(dp_div_dt, &
                           grad, &
                           x_elec, p_elec, &
                           ene, &
                           dij)
use mod_main
implicit none
! --- arguments ---
real(kind=8), dimension(n_mode) :: dp_div_dt
real(kind=8), dimension(n_state, n_mode) :: grad
real(kind=8), dimension(n_state) :: x_elec, p_elec
real(kind=8), dimension(n_state) :: ene
real(kind=8), dimension(n_state, n_state, n_mode) :: dij

! --- local variables ---
real(kind=8), dimension(n_mode) :: dV_eff_div_dx_nuc
real(kind=8), dimension(n_mode) :: dp_nuc_kin__dij_term


call sub_calc_dV_eff_div_dx_nuc_adia(dV_eff_div_dx_nuc, &
                           x_elec, p_elec, &
                           grad)

call sub_calc_dp_nuc_kin__dij_term_adia(dp_nuc_kin__dij_term, &
                           x_elec, p_elec, &
                           ene, &
                           dij)

dp_div_dt = - dV_eff_div_dx_nuc - dp_nuc_kin__dij_term

return
end