subroutine sub_nuc_get_dH_div_dX_or_dP(c_n, dHmn_div_dX, &
                                   dH_div_dX)
use mod_main, only : n_state, n_mode
implicit none
! --- arguments ---

real(kind=8) c_n(n_state, n_state)
real(kind=8), dimension(n_mode, n_state, n_state) :: dHmn_div_dX
real(kind=8), dimension(n_mode) :: dH_div_dX

integer i_mode, i_state, j_state


dH_div_dX = 0.d0

!if (label_debug >= 2) then
!  write(*,*) 'c_n(i_state, j_state)'
!  do i_state = 1, n_state
!    write(*,*)  c_n(i_state, :)
!  enddo
!endif
do i_mode = 1, n_mode
  do i_state = 1, n_state
    do j_state = 1, n_state
      !if(i_mode == 1)then
      !write(*,*) i_mode, i_state, j_state
      !write(*,*) dHmn_div_dX(i_mode, i_state, j_state)
      !endif
      dH_div_dX(i_mode) &
      = dH_div_dX(i_mode) + &
      c_n(i_state, j_state) * &
      dHmn_div_dX(i_mode, i_state, j_state)

    enddo
  enddo
enddo


return
end
