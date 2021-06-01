subroutine sub_calc_dp_nuc_kin__dij_term_adia(dp_nuc_kin__dij_term, &
                           x_elec, p_elec, &
                           ene, &
                           dij)
use mod_main
implicit none
! --- arguments ---
real(kind=8), dimension(n_mode) :: dp_nuc_kin__dij_term
real(kind=8), dimension(n_state) :: x_elec, p_elec
real(kind=8), dimension(n_state) :: ene
real(kind=8), dimension(n_state, n_state, n_mode) :: dij

! --- local variables ---
integer i_mode, i_state, j_state
real(kind=8) dtmp
real(kind=8) x_elec_tmp_i, p_elec_tmp_i
real(kind=8) x_elec_tmp_j, p_elec_tmp_j
real(kind=8) ene_j, ene_i
real(kind=8) dij_tmp

do i_mode = 1, n_mode
  dtmp = 0
  do i_state = 1, n_state
    x_elec_tmp_i = x_elec(i_state)
    p_elec_tmp_i = p_elec(i_state)
    ene_i = ene(i_state)
    do j_state = 1, n_state
      x_elec_tmp_j = x_elec(j_state)
      p_elec_tmp_j = p_elec(j_state)
      ene_j = ene(j_state)
      dij_tmp = dij(i_state, j_state, i_mode)
      dtmp = dtmp + (x_elec_tmp_i * x_elec_tmp_j &
       + p_elec_tmp_i * p_elec_tmp_j) * (ene_j - ene_i) &
       * dij_tmp
    enddo
  enddo
  dp_nuc_kin__dij_term(i_mode) = dtmp * 0.5d0
enddo

return
end