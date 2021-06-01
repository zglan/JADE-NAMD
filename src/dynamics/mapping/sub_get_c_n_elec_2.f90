subroutine sub_get_c_n_elec_2(x, p, c_n)
use mod_main, only : label_debug, n_state, ggamma
implicit none

! --- arguments ---
real(kind=8) x(n_state)
real(kind=8) p(n_state)
real(kind=8) c_n(n_state, n_state)

! --- local variables ---
integer i, j


do i = 1, n_state
  c_n(i,i) = 0.5 * (x(i)**2 + p(i)**2 - ggamma)
enddo

do i = 1, n_state-1
  do j = i+1, n_state
    c_n(i,j) = 0.5 * ( x(i) * x(j) + p(i) * p(j) )
    c_n(j,i) = c_n(i,j)
  enddo
enddo

open(10, file='c_n.dat', access='append')
do i = 1, n_state
  write(10, 9999, advance='no') c_n(i,:)
enddo
  write(10, *)
close(10)

9999  format(10(f20.10, 1x))

return
end
