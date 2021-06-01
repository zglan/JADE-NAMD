subroutine sub_read_parameter(freq, k_tun, exci_e, &
                          lambda0, &
                          lambda1) 
use mod_main
implicit none
include "param.def"
double precision, dimension(n_state) :: exci_e
double precision, dimension(n_mode, n_state, n_state) :: lambda0, &
                                                         lambda1
double precision, dimension(n_state,n_mode) :: k_tun, freq
integer i_state, j_state, i_mode, file_freq_input

file_freq_input=11
open(unit=file_freq_input, file="freq.input")
do i_mode = 1 , n_mode
  read (file_freq_input,*) freq(:, i_mode)
enddo
close(11)

open(10, file='ene.input')
do i_state = 1, n_state
  read(10, *) exci_e(i_state)
enddo
close(10)

open(10, file='k_tun.input')
do i_mode = 1, n_mode
  read(10, *) k_tun(:, i_mode)
enddo
close(10)

lambda0 = 0.d0
open(10, file='lambda0_coupling.input')
do while(.true.)
  read(10,*, end=135) i_state, j_state
!  write(*,*) i_state, j_state
  do i_mode = 1, n_mode
    read(10,*) lambda0(i_mode, i_state, j_state)
  enddo
enddo
135 close(10)

lambda1 = 0.d0
open(10, file='lambda1_coupling.input')
do while(.true.)
  read(10,*, end=136) i_state, j_state
  do i_mode = 1, n_mode
    read(10,*) lambda1(i_mode, i_state, j_state)
  enddo
enddo
136 close(10)

exci_e = exci_e/TOEV
k_tun = k_tun/TOEV
lambda0 = lambda0/TOEV
lambda1 = lambda1/TOEV
freq = freq/TOEV

return
end
