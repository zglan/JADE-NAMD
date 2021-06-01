subroutine sub_get_dia_Ham_elec_Ham_4( x_mode, p_mode, &
                                   freq, k_tun, exci_e, &
                                   lambda0, lambda1, &
                                   reduced_mass_inv_tor, &
                                   tor_pot_para, &
                                   Ham)
use mod_main
implicit none                            

! --- arguments ---
real(kind=8) exci_e(n_state)
real(kind=8), dimension(n_state, n_state) :: Ham
real(kind=8), dimension(n_mode_HO, n_state, n_state) :: lambda0, lambda1
real(kind=8), dimension(n_mode) :: x_mode, &
                                   p_mode
real(kind=8) k_tun(n_state,n_mode_HO)
real(kind=8) freq(n_state,n_mode_HO)
real(kind=8) reduced_mass_inv_tor(n_state, n_mode_tor)
real(kind=8) tor_pot_para(n_state, n_mode_tor)

! -- local variables ---
integer i, j, k
real(kind=8) tmp, x_tmp, p_tmp, freq_tmp
real(kind=8) Ham_tmp(n_state, n_state)

Ham = 0.d0
call sub_get_dia_Ham_elec(x_mode(1:n_mode_HO), &
                          p_mode(1:n_mode_HO), &
                          freq, &
                          k_tun, &
                          exci_e, &
                          lambda0, &
                          lambda1, &
                          Ham)

Ham_tmp = 0.d0
call sub_get_dia_Ham_elec_Ham_tor(x_mode(n_mode_HO+1 : n_mode), &
                                  p_mode(n_mode_HO+1 : n_mode), &
                                  reduced_mass_inv_tor, &
                                  tor_pot_para, &
                                  Ham_tmp)

Ham = Ham + Ham_tmp

return
end
