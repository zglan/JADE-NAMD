subroutine sub_nuc_get_dH_div_dX_or_dP_aver_PES(c_n, dHmn_div_dX, &
                                   dH_div_dX)
use mod_main, only : n_state, n_mode
implicit none
! --- arguments ---

real(kind=8) c_n(n_state, n_state)
real(kind=8), dimension(n_mode, n_state, n_state) :: dHmn_div_dX
real(kind=8), dimension(n_mode) :: dH_div_dX

integer i_mode, i_state, j_state
real(kind=8) tmp
real(kind=8) d_n_state_inv

d_n_state_inv = 1.d0 / dble(n_state)

dH_div_dX = 0.d0

!if (label_debug >= 2) then
!  write(*,*) 'c_n(i_state, j_state)'
!  do i_state = 1, n_state
!    write(*,*)  c_n(i_state, :)
!  enddo
!endif

do i_mode = 1, n_mode
  tmp = 0.d0
  do i_state = 1, n_state
    tmp = tmp + dHmn_div_dX(i_mode, i_state, i_state)
  enddo
  tmp = tmp * d_n_state_inv
  dH_div_dX(i_mode) = tmp
enddo

do i_mode = 1, n_mode
  tmp = 0.d0
  do i_state = 1, n_state - 1
    do j_state = i_state + 1, n_state
      tmp = tmp &
           + d_n_state_inv &
           * (&
           dHmn_div_dX(i_mode, i_state, i_state) &
           - dHmn_div_dX(i_mode, j_state, j_state)&
           ) &
           * (c_n(i_state, i_state) - c_n(j_state, j_state)) &
           + dHmn_div_dX(i_mode, i_state, j_state) * c_n(i_state, j_state)
    enddo
  enddo
  dH_div_dX(i_mode) = dH_div_dX(i_mode) + tmp
enddo


return
end
