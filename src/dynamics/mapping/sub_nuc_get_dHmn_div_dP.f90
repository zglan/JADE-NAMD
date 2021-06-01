subroutine sub_nuc_get_dHmn_div_dP(n_mode, n_state, &
                               x_mode, p_mode, &
                               freq, &
                               dHmn_div_dP)
implicit none
! --- arguments ---
integer n_state
integer n_mode
real(kind=8) nuc_dt
!real(kind=8) k_tun(n_state, n_mode)
!real(kind=8) lambda(n_mode, n_state, n_state)
real(kind=8), dimension(n_mode) :: x_mode, p_mode
real(kind=8), dimension(n_state, n_mode) :: freq
real(kind=8), dimension(n_mode, n_state, n_state) :: dHmn_div_dP

! --- local variables ---
integer i_mode, i_state, j_state



do i_mode = 1, n_mode
  do i_state = 1, n_state
    do j_state = 1, n_state
      if (i_state == j_state) then

        dHmn_div_dP(i_mode, i_state, j_state) &
        = freq(i_state, i_mode) * p_mode(i_mode)

      else

        dHmn_div_dP(i_mode, i_state, j_state) &
        = 0.d0

      endif
    enddo
  enddo
enddo

return
end
