subroutine sub_dia_to_adia(x_mode, p_mode, &
                           freq,k_tun, ene_dia, &
                           lambda0, lambda1, &
                           Ham, ene_adia, &
                           dHmn_div_dX_adia, &
                           mat_U)
use mod_main
implicit none                            

! --- arguments ---
real(kind=8) ene_dia(n_state), ene_adia(n_state)
real(kind=8), dimension(n_state, n_state) :: Ham
real(kind=8), dimension(n_mode_HO, n_state, n_state) :: lambda0, lambda1
real(kind=8), dimension(n_mode_HO) :: x_mode, &
                                   p_mode
real(kind=8) k_tun(n_state,n_mode_HO)
real(kind=8) freq(n_state,n_mode_HO)
real(kind=8), dimension(n_mode, n_state, n_state) :: dHmn_div_dX_adia
real(kind=8), dimension(n_state,n_state) ::  mat_U

! -- local variables ---
integer i, j, k, i_mode, i_state
real(kind=8), dimension(n_mode, n_state, n_state) :: dHmn_div_dX
real(kind=8) tmp, x_tmp, p_tmp, freq_tmp

if(label_debug >= 2) then
  write(*,*) 'sub_dia_to_adia'
  write(*,*) 'p_nuc_cur'
  do i_mode = 1, n_mode
    write(*,*) p_mode(i_mode)
  enddo
  write(*,*)
endif


Ham = 0.d0
call sub_get_dia_Ham_elec(x_mode, p_mode, &
                          freq, k_tun, ene_dia, &
                          lambda0, lambda1, &
                          Ham)
call sub_nuc_get_dHmn_div_dX(n_mode, n_state, &
                          x_mode, p_mode, &
                          freq, k_tun, lambda1, &
                          dHmn_div_dX)
call sub_diag(n_state, Ham, mat_U, ene_adia)
if(label_debug >= 2) then
  write(*,*) 'mat_U'
  do i_state = 1, n_state
    write(*,*) mat_U(i_state,:)
  enddo
  write(*,*)
  write(*,*) 'Ham'
  do i_state = 1, n_state
    write(*,*) Ham(i_state,:)
  enddo
  write(*,*)
  write(*,*) 'ene_adia'
  write(*,*) ene_adia(:)
  write(*,*)
endif
call sub_nuc_get_dHmn_div_dX_adia(dHmn_div_dX, &
                          mat_U, &
                          dHmn_div_dX_adia)


return
end
