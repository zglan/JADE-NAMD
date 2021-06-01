subroutine sub_calc_dV_eff_div_dx_nuc_adia_traj_adjusted(dV_eff_div_dx_nuc, &
                           x_elec, p_elec, gammas, &
                           grad)
use mod_main
implicit none
! --- arguments ---
real(kind=8), dimension(n_mode) :: dV_eff_div_dx_nuc
real(kind=8), dimension(n_state, n_mode) :: grad
real(kind=8), dimension(n_state) :: x_elec, p_elec
real(kind=8) gammas(n_state)

! --- local variables ---
integer i_mode, i_state, j_state
real(kind=8) dtmp, dtmp2, dn_state_inv
real(kind=8) c_n_i, c_n_j
real(kind=8) grad_i, grad_j
real(kind=8) c_n(n_state, n_state)

dn_state_inv = 1.d0/dble(n_state)

call sub_get_c_n_elec_2_traj_adjusted(x_elec, p_elec, gammas, c_n)

! 1/n_state * sum(grad_i)
do i_mode = 1, n_mode
  dtmp = 0.d0
  do i_state = 1, n_state
    dtmp = dtmp + grad(i_state,i_mode)
  enddo
  dtmp = dtmp * dn_state_inv
  dV_eff_div_dx_nuc(i_mode) = dtmp
enddo

! 1/n_state * sum(1/2 * (c_i - c_j) * (grad_i - grad_j) )
do i_mode = 1, n_mode
  dtmp = dV_eff_div_dx_nuc(i_mode)
  dtmp2 = 0.d0
  do i_state = 1, n_state
    c_n_i = c_n(i_state, i_state)
    grad_i = grad(i_state, i_mode)
    do j_state = 1, n_state
      c_n_j = c_n(j_state, j_state)
      grad_j = grad(j_state, i_mode)
      dtmp2 = dtmp2 + (c_n_i - c_n_j) * (grad_i - grad_j)
    enddo
  enddo
  dtmp2 = dtmp2 *dn_state_inv * 0.5d0
  dtmp = dtmp + dtmp2
  dV_eff_div_dx_nuc(i_mode) = dtmp
enddo

return
end