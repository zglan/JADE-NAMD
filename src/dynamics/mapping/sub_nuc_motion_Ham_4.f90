subroutine sub_nuc_motion_Ham_4( x_mode, p_mode, &
                           c_n, &
                           freq, k_tun, exci_e, &
                           lambda0, lambda1, &
                           reduced_mass_inv_tor, &
                           tor_pot_para)
use mod_main
implicit none
! --- arguments ---
real(kind=8), dimension(n_mode) :: x_mode, p_mode
real(kind=8), dimension(n_state, n_mode_HO) :: freq
real(kind=8), dimension(n_state) :: exci_e
real(kind=8) c_n(n_state, n_state)
real(kind=8) k_tun(n_state, n_mode_HO)
real(kind=8) lambda0(n_mode_HO, n_state, n_state)
real(kind=8) lambda1(n_mode_HO, n_state, n_state)
real(kind=8) reduced_mass_inv_tor(n_state, n_mode_tor)
real(kind=8) tor_pot_para(n_state, n_mode_tor)

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
if(label_debug >= 2) write(*,*) 'sub_nuc_get_dHmn_div_dX begin!'
call sub_nuc_get_dHmn_div_dX(n_mode_HO, n_state, &
                               x_mode(1:n_mode_HO), &
                               p_mode(1:n_mode_HO), &
                               freq, k_tun, lambda1, &
                               dHmn_div_dX(1:n_mode_HO,:,:))
if(label_debug >= 2) write(*,*) 'sub_nuc_get_dHmn_div_dX_Ham_tor begins!'
call sub_nuc_get_dHmn_div_dX_Ham_tor(n_mode_tor, n_state, &
                               x_mode(n_mode_HO+1:n_mode), &
                               tor_pot_para, &
                               dHmn_div_dX(n_mode_HO+1:n_mode,:,:))
!write(*,*) dHmn_div_dX(1, 1, 1)
if(label_debug >= 2) write(*,*) 'sub_nuc_get_dHmn_div_dX done!'
call sub_nuc_get_dH_div_dX_or_dP(c_n, dHmn_div_dX, &
                       dH_div_dX)
if(label_debug >= 2) write(*,*) 'sub_nuc_get_dH_div_dX_or_dP_aver_PES done!'
delt_P = -dH_div_dX
!write(*,*) delt_P

call sub_move(n_mode, p_mode, delt_P, nuc_dt_half)
!write(*,*) ''
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! one step of X
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if(label_debug >= 2) write(*,*) 'sub_nuc_get_dH_div_dP_aver_PES begin!'
call sub_nuc_get_dH_div_dP(n_mode_HO, n_state, &
                               x_mode(1:n_mode_HO), &
                               p_mode(1:n_mode_HO), &
                               freq,  &
                               dH_div_dP(1:n_mode_HO))

call sub_nuc_get_dH_div_dP(n_mode_tor, n_state, &
                               x_mode(n_mode_HO+1:n_mode), &
                               p_mode(n_mode_HO+1:n_mode), &
                               reduced_mass_inv_tor, &
                               dH_div_dP(n_mode_HO+1:n_mode))
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
delt_X = dH_div_dP
!if(label_debug >= 2) write(*,*) delt_X(n_mode)
call sub_move(n_mode, x_mode, delt_X, nuc_dt)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of P
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if(label_debug >= 2) write(*,*) 'sub_nuc_get_dHmn_div_dX begins!'
call sub_nuc_get_dHmn_div_dX(n_mode_HO, n_state, &
                               x_mode(1:n_mode_HO), &
                               p_mode(1:n_mode_HO), &
                               freq, k_tun, lambda1, &
                               dHmn_div_dX(1:n_mode_HO,:,:))

if(label_debug >= 2) write(*,*) 'sub_nuc_get_dHmn_div_dX_Ham_tor begins!'
call sub_nuc_get_dHmn_div_dX_Ham_tor(n_mode_tor, n_state, &
                               x_mode(n_mode_HO+1:n_mode), &
                               tor_pot_para, &
                               dHmn_div_dX(n_mode_HO+1:n_mode,:,:))
!write(*,*) dHmn_div_dX(1, 1, 1)
if(label_debug >= 2) write(*,*) 'sub_nuc_get_dHmn_div_dX done!'
call sub_nuc_get_dH_div_dX_or_dP(c_n, dHmn_div_dX, &
                       dH_div_dX)
!write(*,*) 'sub_nuc_get_dH_div_dX_or_dP done'
delt_P = -dH_div_dX
!write(*,*) delt_P

call sub_move(n_mode, p_mode, delt_P, nuc_dt_half)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

return
end
