subroutine sub_get_dia_Ham_elec_Ham_tor(x_mode, &
                                  p_mode, &
                                  reduced_mass_inv_tor, &
                                  tor_pot_para, &
                                  Ham)
use mod_main
implicit none                            

! --- arguments ---
real(kind=8), dimension(n_state, n_state) :: Ham
real(kind=8), dimension(n_mode_tor) :: x_mode, &
                                   p_mode
real(kind=8) reduced_mass_inv_tor(n_state, n_mode_tor)
real(kind=8) tor_pot_para(n_state, n_mode_tor)

! -- local variables ---
integer i, j, k
real(kind=8) tmp, x_tmp, p_tmp, freq_tmp

Ham = 0.d0

do i = 1, n_state
  tmp = 0.d0
!  write(*,*) i, tmp
  do j = 1, n_mode_tor
    x_tmp = x_mode(j)
    p_tmp = p_mode(j)
    tmp = tmp + 0.5d0 * reduced_mass_inv_tor(i, j) * p_tmp * p_tmp &
              + 0.5d0 *  tor_pot_para(i, j) * ( 1.d0 - cos(2.d0* x_tmp) )
!    write(*,*) x_tmp, p_tmp, freq_tmp, k_tun(i,j)
  enddo
  Ham(i,i) =  tmp
enddo

!open(10, file='E1_E2.dat', access='append')
!write(10,*) Ham(1,1), Ham(2,2)
!close(10)

return
end
