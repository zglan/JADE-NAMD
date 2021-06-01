subroutine sub_calc_dV_eff_div_dx_nuc_adia(dV_eff_div_dx_nuc, &
                           x_elec, p_elec, &
                           grad)
use mod_main
implicit none
! --- arguments ---
real(kind=8), dimension(n_mode) :: dV_eff_div_dx_nuc
real(kind=8), dimension(n_state, n_mode) :: grad
real(kind=8), dimension(n_state) :: x_elec, p_elec

! --- local variables ---
integer i_mode, i_state, j_state
real(kind=8) dtmp, dtmp2, dn_state_inv
real(kind=8) x_elec_tmp_i, p_elec_tmp_i
real(kind=8) x_elec_tmp_j, p_elec_tmp_j
real(kind=8) grad_i, grad_j

dn_state_inv = 1.d0/dble(n_state)

! 1/n_state * sum(grad_i)
do i_mode = 1, n_mode
  dtmp = 0.d0
  do i_state = 1, n_state
    dtmp = dtmp + grad(i_state,i_mode)
  enddo
  dtmp = dtmp * dn_state_inv
  dV_eff_div_dx_nuc(i_mode) = dtmp
enddo

! 1/n_state * sum(1/4 * (x_i**2 + p_i**2 - x_j**2 + p_j**2) * (grad_i - grad_j) )
do i_mode = 1, n_mode
  dtmp = dV_eff_div_dx_nuc(i_mode)
  dtmp2 = 0.d0
  do i_state = 1, n_state
    x_elec_tmp_i = x_elec(i_state)
    p_elec_tmp_i = p_elec(i_state)
    x_elec_tmp_i = x_elec_tmp_i**2
    p_elec_tmp_i = p_elec_tmp_i**2
    grad_i = grad(i_state, i_mode)
    do j_state = 1, n_state
      x_elec_tmp_j = x_elec(j_state)
      p_elec_tmp_j = p_elec(j_state)
      x_elec_tmp_j = x_elec_tmp_j**2
      p_elec_tmp_j = p_elec_tmp_j**2
      grad_j = grad(j_state, i_mode)
      dtmp2 = dtmp2 &
       + (x_elec_tmp_i + p_elec_tmp_i - x_elec_tmp_j - p_elec_tmp_j) &
       * (grad_i - grad_j)
    enddo
  enddo
  dtmp2 = dtmp2 *dn_state_inv * 0.25d0
  dtmp = dtmp + dtmp2
  dV_eff_div_dx_nuc(i_mode) = dtmp
enddo

return
end