subroutine sub_nuc_get_dHmn_div_dX(n_mode, n_state, &
                               x_mode, p_mode, &
                               freq, k_tun, lambda1, &
                               dHmn_div_dX)
implicit none
! --- arguments ---
integer n_state
integer n_mode
real(kind=8) nuc_dt
real(kind=8) k_tun(n_state, n_mode)
real(kind=8) freq(n_state, n_mode)
real(kind=8) lambda1(n_mode, n_state, n_state)
real(kind=8), dimension(n_mode) :: x_mode, p_mode
real(kind=8), dimension(n_mode, n_state, n_state) :: dHmn_div_dX

! --- local variables ---
integer i_mode, i_state, j_state



do i_mode = 1, n_mode
  !write(*,*) i_mode
  do i_state = 1, n_state
    do j_state = 1, n_state
      if (i_state == j_state) then

        dHmn_div_dX(i_mode, i_state, j_state) &
        = ( freq(i_state, i_mode) * x_mode(i_mode) + &
        k_tun(i_state, i_mode) )

      else

        dHmn_div_dX(i_mode, i_state, j_state) &
        = lambda1(i_mode, i_state, j_state)

      endif
    enddo
  enddo
enddo

!open(10, file= 'x_p_debug.dat')
!do i_mode = 1, n_mode
!  write(10,*) x_mode(i_mode), p_mode(i_mode)
!enddo
!close(10)

!open(10, file= 'dHmn_div_dX.dat', access='append')
!do i_mode = 1, n_mode
!  write(10,*) i_mode
!  do i_state = 1, n_state
!    write(10,*) dHmn_div_dX(i_mode, i_state, :)
!  enddo
!enddo
!close(10)

return
end
