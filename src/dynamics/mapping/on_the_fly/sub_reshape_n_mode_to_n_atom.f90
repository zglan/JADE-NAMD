subroutine sub_reshape_n_mode_to_n_atom(x_nuc_cur, &
                  p_nuc_cur, &
                  grad, &
                  dij_cur, &
                  coor_x, coor_y, coor_z, &
                  vel_x, vel_y, vel_z, &
                  gra_all_x, gra_all_y, gra_all_z, &
                  nac_x, nac_y, nac_z)
use mod_main
implicit none
include 'var_n_atom.h'
include 'var_n_mode.h'
integer i_atom

do i_atom = 1, n_atom
  coor_x(i_atom) = x_nuc_cur(3 * (i_atom - 1) + 1)
  coor_y(i_atom) = x_nuc_cur(3 * (i_atom - 1) + 2)
  coor_z(i_atom) = x_nuc_cur(3 * (i_atom - 1) + 3)
enddo

do i_atom = 1, n_atom
  vel_x(i_atom) = p_nuc_cur(3 * (i_atom - 1) + 1)
  vel_y(i_atom) = p_nuc_cur(3 * (i_atom - 1) + 2)
  vel_z(i_atom) = p_nuc_cur(3 * (i_atom - 1) + 3)
enddo

do i_atom = 1, n_atom
  gra_all_x(:,i_atom) = grad(:,3 * (i_atom - 1) + 1)
  gra_all_y(:,i_atom) = grad(:,3 * (i_atom - 1) + 2)
  gra_all_z(:,i_atom) = grad(:,3 * (i_atom - 1) + 3)
enddo

do i_atom = 1, n_atom
  nac_x(:,:,i_atom) = dij_cur(:,:,3 * (i_atom - 1) + 1)
  nac_y(:,:,i_atom) = dij_cur(:,:,3 * (i_atom - 1) + 2)
  nac_z(:,:,i_atom) = dij_cur(:,:,3 * (i_atom - 1) + 3)
enddo

return
end