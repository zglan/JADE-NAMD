subroutine sub_test(mass, ene_adia_cur)
use mod_main
implicit none
include 'var_n_mode.h'
integer i_mode

write(*,*) "sub_test"
write(*,*) "mass"
do i_mode = 1, n_mode
  write(*,*) i_mode, mass(i_mode)
enddo
write(*,*) "ene_adia_cur", ene_adia_cur
return
end
