subroutine sub_reshape_n_atom_to_n_mode_coor(x_nuc_cur, &
                  coor_x, coor_y, coor_z)
use mod_main
implicit none
real(kind=8) x_nuc_cur(n_mode)
double precision, dimension(n_atom) ::   &
                                                coor_x, &
                                                coor_y, &
                                                coor_z
integer i_atom

do i_atom = 1, n_atom
  x_nuc_cur(3 * (i_atom - 1) + 1) = coor_x(i_atom)
  x_nuc_cur(3 * (i_atom - 1) + 2) = coor_y(i_atom)
  x_nuc_cur(3 * (i_atom - 1) + 3) = coor_z(i_atom)
enddo

return
end
