subroutine sub_nuc_motion( x_mode, p_mode, &
                           c_n, &
                           freq, k_tun, exci_e, &
                           lambda0, lambda1)
use mod_main, only : n_state, n_mode, nuc_dt
implicit none
! --- arguments ---
real(kind=8), dimension(n_mode) :: x_mode, p_mode
real(kind=8), dimension(n_state, n_mode) :: freq
real(kind=8), dimension(n_state) :: exci_e
real(kind=8) c_n(n_state, n_state)
real(kind=8) k_tun(n_state, n_mode)
real(kind=8) lambda0(n_mode, n_state, n_state)
real(kind=8) lambda1(n_mode, n_state, n_state)

! --- local variables ---
real(kind=8), dimension(n_mode) :: delt_X, &
                                   delt_P, &
                                   dH_div_dX, &
                                   dH_div_dP
real(kind=8), dimension(n_mode, n_state, n_state) :: dHmn_div_dX, &
                                                     dHmn_div_dP
real(kind=8) nuc_dt_half
integer i_mode, i_state, j_state


!if(label_debug >= 2)then
!open(10, access='append', file='c_n_sub_nuc_motion.dat')
!do i_state = 1, n_state
!  write(10, *) c_n(i_state,:)
!enddo
!close(10)
!endif

!write(*,*) 'ini'
nuc_dt_half = 0.5d0 * nuc_dt
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of P
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
call sub_nuc_get_dHmn_div_dX(n_mode, n_state, &
                               x_mode, p_mode, &
                               freq, k_tun, lambda1, &
                               dHmn_div_dX)
!write(*,*) dHmn_div_dX(1, 1, 1)
!write(*,*) 'sub_nuc_get_dHmn_div_dX done!'
call sub_nuc_get_dH_div_dX_or_dP(c_n, dHmn_div_dX, &
                       dH_div_dX)
!write(*,*) 'sub_nuc_get_dH_div_dX_or_dP done'

delt_P = -dH_div_dX
!write(*,*) delt_P

call sub_move(n_mode, p_mode, delt_P, nuc_dt_half)
!write(*,*) ''
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! one step of X
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
call sub_nuc_get_dHmn_div_dP(n_mode, n_state, &
                               x_mode, p_mode, &
                               freq, &
                               dHmn_div_dP)
call sub_nuc_get_dH_div_dX_or_dP(c_n, dHmn_div_dP, &
                       dH_div_dP)
delt_X = dH_div_dP
!write(*,*) delt_X
call sub_move(n_mode, x_mode, delt_X, nuc_dt)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of P
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
call sub_nuc_get_dHmn_div_dX(n_mode, n_state, &
                               x_mode, p_mode, &
                               freq, k_tun, lambda1, &
                               dHmn_div_dX)

call sub_nuc_get_dH_div_dX_or_dP(c_n, dHmn_div_dX, &
                       dH_div_dX)

delt_P = -dH_div_dX
!write(*,*) delt_P
call sub_move(n_mode, p_mode, delt_P, nuc_dt_half)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

return
end
