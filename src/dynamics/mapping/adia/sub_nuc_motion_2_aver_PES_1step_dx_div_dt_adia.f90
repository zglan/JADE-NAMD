subroutine sub_nuc_motion_2_aver_PES_1step_dx_div_dt_adia( &
                           vel_nuc_kin_cur, &
                           p_nuc_kin_cur, &
                           x_elec, p_elec, &
                           mass)
use mod_main
implicit none

real(kind=8), dimension(n_mode) :: vel_nuc_kin_cur
real(kind=8), dimension(n_mode) :: p_nuc_kin_cur
real(kind=8), dimension(n_mode) :: mass
real(kind=8), dimension(n_state) :: x_elec, p_elec



    vel_nuc_kin_cur = p_nuc_kin_cur / mass
return
end
