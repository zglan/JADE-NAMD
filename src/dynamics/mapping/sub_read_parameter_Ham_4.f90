subroutine sub_read_parameter_Ham_4(freq, k_tun, exci_e, &
                          lambda0, &
                          lambda1, &
                          reduced_mass_inv_tor, &
                          tor_pot_para) 
use mod_main
implicit none
include "param.def"
double precision, dimension(n_state) :: exci_e
double precision, dimension(n_mode_HO, n_state, n_state) :: lambda0, &
                                                         lambda1
double precision, dimension(n_state, n_mode_HO) :: k_tun, freq
double precision reduced_mass_inv_tor(n_state, n_mode_tor)
double precision tor_pot_para(n_state, n_mode_tor)

! --- local variable ---
integer i_state, j_state
integer i_mode, file_freq_input

reduced_mass_inv_tor = 0.d0
open(10, file='reduced_mass_inv_tor.input')
do i_mode = 1, n_mode_tor
    write(*,*) i_mode
  read(10,*) reduced_mass_inv_tor(:,i_mode)
enddo
close(10)

tor_pot_para = 0.d0
open(10, file='tor_pot_para.input')
do i_mode = 1, n_mode_tor
    read(10,*) tor_pot_para(:, i_mode)
enddo
close(10)

file_freq_input=11
open(unit=file_freq_input, file="freq.input")
do i_mode = 1 , n_mode_HO
  read (file_freq_input,*) freq(:, i_mode)
enddo
close(11)

open(10, file='ene.input')
do i_state = 1, n_state
  read(10, *) exci_e(i_state)
enddo
close(10)

open(10, file='k_tun.input')
do i_mode = 1, n_mode_HO
  read(10, *) k_tun(:, i_mode)
enddo
close(10)

lambda0 = 0.d0
open(10, file='lambda0_coupling.input')
do while(.true.)
  read(10,*, end=135) i_state, j_state
  do i_mode = 1, n_mode_HO
    read(10,*) lambda0(i_mode, i_state, j_state)
  enddo
enddo
135 close(10)

lambda1 = 0.d0
open(10, file='lambda1_coupling.input')
do while(.true.)
  read(10,*, end=136) i_state, j_state
  do i_mode = 1, n_mode_HO
    read(10,*) lambda1(i_mode, i_state, j_state)
  enddo
enddo
136 close(10)

exci_e = exci_e/TOEV
k_tun = k_tun/TOEV
lambda0 = lambda0/TOEV
lambda1 = lambda1/TOEV
freq = freq/TOEV
reduced_mass_inv_tor = reduced_mass_inv_tor/TOEV
tor_pot_para = tor_pot_para/TOEV


return
end
