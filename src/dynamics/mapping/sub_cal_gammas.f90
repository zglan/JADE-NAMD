subroutine sub_cal_gammas(x_elec, p_elec, &
                         gammas)
use mod_main
implicit none
! --- arguments ---
integer i_step
real(kind=8), dimension(n_state) :: x_elec, p_elec, gammas

! --- lacal variables ---
integer i, j, i_state
real(kind=8) tmp

! Here, the defination of gamma is different from Miller's.
! 0.5 * ( x**2 + p**2 - gamma)
do i_state = 1, n_state
  tmp = x_elec(i_state) ** 2 + p_elec(i_state) ** 2
  if ( tmp >= 2.d0 ) then
    write(*,*) "gammas > 2.0, gammas = gammas - 2.0"
    gammas(i_state) = tmp - 2.d0
  else
    gammas(i_state) = tmp
  endif
enddo

return
end
