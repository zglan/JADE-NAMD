subroutine sub_elec_motion_2_aver_PES_adia( p_mode_cur_div_mass, &
                           p_mode_pre_div_mass, &
                           x_elec, p_elec, &
                           exci_e_cur, exci_e_pre, &
                           dij_cur, dij_pre)
use mod_main
implicit none
! --- arguments ---
real(kind=8), dimension(n_mode) :: p_mode_cur_div_mass, & 
                                   p_mode_pre_div_mass
real(kind=8), dimension(n_state) :: x_elec, &
                                    p_elec, &
                                    exci_e_cur, &
                                    exci_e_pre
real(kind=8), dimension(n_state, n_state, n_mode) :: dij_cur, &
                                                     dij_pre

! --- local variables ---
real(kind=8) Ham(n_state, n_state)
real(kind=8), dimension(n_mode) :: delt_p_mode_div_mass, &
                                   p_mode_cur_div_mass_tmp
real(kind=8), dimension(n_state) :: delt_exci_e, &
                                    exci_e_cur_tmp
real(kind=8), dimension(n_state, n_state, n_mode):: delt_dij, &
                                   dij_cur_tmp
real(kind=8) ele_dt, ele_dt_half
real(kind=8) dn_ele_dt
real(kind=8), dimension(n_state) ::  delt_x_elec, &
                                     delt_p_elec
integer i_ele_step


if(label_debug >= 2) then
  write(*,*) 'sub_elec_motion_2_aver_PES_adia'
  write(*,*) 'n_ele_dt', n_ele_dt
  write(*,*)  'nuc_dt', nuc_dt
endif
dn_ele_dt = dble(n_ele_dt)
ele_dt = nuc_dt / dn_ele_dt
ele_dt_half = 0.5d0 * ele_dt

delt_p_mode_div_mass = (p_mode_cur_div_mass - p_mode_pre_div_mass) / dn_ele_dt
delt_exci_e = (exci_e_cur - exci_e_pre) / dn_ele_dt
delt_dij = (dij_cur - dij_pre) / dn_ele_dt

p_mode_cur_div_mass_tmp = p_mode_pre_div_mass
exci_e_cur_tmp = exci_e_pre
dij_cur_tmp = dij_pre
do i_ele_step = 1, n_ele_dt
  p_mode_cur_div_mass_tmp = p_mode_cur_div_mass_tmp + delt_p_mode_div_mass
  exci_e_cur_tmp = exci_e_cur_tmp + delt_exci_e
  dij_cur_tmp = dij_cur_tmp + delt_dij
  call sub_elec_motion_2_aver_PES_1step_adia(p_mode_cur_div_mass_tmp, &
                           x_elec, &
                           p_elec, &
                           exci_e_cur_tmp, &
                           dij_cur_tmp, &
                           ele_dt)
enddo


return
end
