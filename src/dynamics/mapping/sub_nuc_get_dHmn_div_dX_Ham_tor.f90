subroutine sub_nuc_get_dHmn_div_dX_Ham_tor(n_mode, n_state, &
                               x_mode, &
                               tor_pot_para, &
                               dHmn_div_dX)
implicit none
! --- arguments ---
integer n_state
integer n_mode
real(kind=8), dimension(n_mode) :: x_mode
real(kind=8) tor_pot_para(n_state, n_mode)
real(kind=8) dHmn_div_dX(n_mode, n_state, n_state)

! --- local variables ---
integer i_mode, i_state, j_state

dHmn_div_dX = 0.d0
do i_mode = 1, n_mode
    !write(*,*) x_mode(i_mode)
  do i_state = 1, n_state
    dHmn_div_dX(i_mode, i_state, i_state) &
    = tor_pot_para(i_state, i_mode) * 2.d0 * sin( 2.d0 * x_mode(i_mode) )
  enddo
enddo



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
