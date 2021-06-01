subroutine sub_nuc_get_dH_div_dP(n_mode, n_state, &
                               x_mode, p_mode, &
                               freq, &
                               dH_div_dP)
implicit none
! --- arguments ---
integer n_state
integer n_mode
real(kind=8) nuc_dt
!real(kind=8) k_tun(n_state, n_mode)
!real(kind=8) lambda(n_mode, n_state, n_state)
real(kind=8), dimension(n_mode) :: x_mode, p_mode
real(kind=8), dimension(n_state, n_mode) :: freq
real(kind=8), dimension(n_mode) :: dH_div_dP

! --- local variables ---
integer i_mode, i_state, j_state

!write(*,*) freq(1,n_mode)

do i_mode = 1, n_mode
  do i_state = 1, n_state
!    do j_state = 1, n_state
!      if ( freq(i_state, i_mode) /= freq(j_state, i_mode) ) then
!        write(*,*) "freq of mode", i_mode, "of state ", i_state, "is different from that of state", j_state
!        write(*,*) "Now this program is only designed for the same-frequency cases!"
!        stop
!      endif
!    enddo
    dH_div_dP(i_mode) &
        = freq(i_state, i_mode) * p_mode(i_mode)
  enddo
enddo


return
end
