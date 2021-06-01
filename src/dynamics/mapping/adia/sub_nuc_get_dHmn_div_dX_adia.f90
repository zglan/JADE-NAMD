subroutine sub_nuc_get_dHmn_div_dX_adia(dHmn_div_dX, &
                    mat_U, &
                    dHmn_div_dX_adia)
use mod_main
implicit none
include "param.def"
real(kind=8), dimension(n_state, n_state) :: mat_U, &
                                             delta_v_tmp1
real(kind=8), dimension(n_mode, n_state, n_state) :: dHmn_div_dX_adia, &
                                                     dHmn_div_dX
integer :: k


!adiabatic gradient
do k = 1, n_mode
  delta_v_tmp1 = dHmn_div_dX(k, :, :)
  delta_v_tmp1 = matmul(transpose(mat_U), delta_v_tmp1)
  delta_v_tmp1 = matmul(delta_v_tmp1, mat_U)
  dHmn_div_dX_adia(k, :, :) = delta_v_tmp1
enddo

return
end 
