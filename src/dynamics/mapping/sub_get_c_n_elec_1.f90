subroutine sub_get_c_n_elec_1(x, y, p_x, p_y, c_n)
use mod_main, only : label_debug, n_state, ggamma
implicit none

! --- arguments ---
real(kind=8) x(n_state)
real(kind=8) y(n_state)
real(kind=8) p_x(n_state)
real(kind=8) p_y(n_state)
real(kind=8) c_n(n_state, n_state)

! --- local variables ---
integer i, j

do i = 1, n_state
  do j = 1, n_state
    if(i==j) then
      c_n(i,j) = x(i) * p_y(j) - y(i) * p_x(j) - ggamma
    else
      c_n(i,j) = x(i) * p_y(j) - y(i) * p_x(j)
    endif
  enddo
enddo

if (label_debug >= 2)then
open(10, file='c_n.dat', access='append')
do i = 1, n_state
  write(10, *) c_n(i,:)
enddo
close(10)
endif

return
end
