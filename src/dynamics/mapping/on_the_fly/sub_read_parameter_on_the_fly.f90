subroutine sub_read_parameter_on_the_fly(mass, atom_label) 
use mod_main
implicit none
include "param.def"
double precision, dimension(n_mode) :: mass
character*2, dimension(n_atom)  ::  atom_label

double precision :: tmp_mass
integer          :: tmp_charge   
character*2      :: tmp_label
integer i, j


do i=1,n_atom
   tmp_label = atom_label(i)
   call sub_get_mass ( tmp_label, tmp_mass, tmp_charge)
   do j = 1, 3
     mass (3*(i-1)+j) = tmp_mass
   enddo
enddo


return
end
