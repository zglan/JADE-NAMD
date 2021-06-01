subroutine sub_get_dia_grad(x_mode,  &
                            freq,k_tun,  &
                            grad)
use mod_main
implicit none                            

! --- arguments ---
real(kind=8), dimension(n_state, n_state) :: Ham
real(kind=8), dimension(n_mode_HO, n_state, n_state) :: lambda0, lambda1
real(kind=8), dimension(n_mode_HO) :: x_mode, &
                                   p_mode
real(kind=8) k_tun(n_state,n_mode_HO)
real(kind=8) freq(n_state,n_mode_HO)
real(kind=8) grad(n_state,n_mode_HO)

! -- local variables ---
integer i, j, k
real(kind=8) tmp, x_tmp, p_tmp, freq_tmp

Ham = 0.d0

do i = 1, n_state
  do j = 1, n_mode_HO
    x_tmp = x_mode(j)
    freq_tmp = freq(i,j)
    grad(i,j) = 0.5d0 * freq_tmp * x_tmp &
              + k_tun(i,j)
  enddo
enddo


return
end
