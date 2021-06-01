subroutine sub_elec_motion_2_aver_PES_1step_dx_div_dt_adia(dssign, &
                           p_nuc_div_mass, &
                           x_elec, &
                           p_elec, &
                           ene, &
                           dij, &
                           dx_elec_div_dt)
use mod_main
implicit none
! --- arguments ---
real(kind=8), dimension(n_mode) :: p_nuc_div_mass
real(kind=8), dimension(n_state) :: x_elec, &
                                    p_elec
real(kind=8), dimension(n_state) :: ene
real(kind=8), dimension(n_state) :: dx_elec_div_dt
real(kind=8), dimension(n_state, n_state, n_mode):: dij
real(kind=8) dssign

! --- local variables ---
integer i_state, j_state, i_mode
real(kind=8) dtmp, dtmp2, dtmp3
real(kind=8) dij_tmp(n_mode)

dx_elec_div_dt = 0.d0
if(label_debug > 1) then
  write(*,*) 'sub_elec_motion_2_aver_PES_1step_dx_div_dt_adia'
  write(*,*) 'begining'
  write(*,*) 'i_state, x_elec, p_elec'
  do i_state = 1, n_state
    write(*,*) i_state, x_elec(i_state), p_elec(i_state)
  enddo
  write(*,*)
endif
do i_state = 1, n_state
  dtmp = 0.d0
  dtmp2 = ene(i_state)
  do j_state = 1, n_state
    dtmp = dtmp + dtmp2 - ene(j_state)
  enddo
  dx_elec_div_dt(i_state) = dssign * p_elec(i_state) / dble(n_state) &
   * dtmp
enddo
if(label_debug > 1) then
  write(*,*) 'sub_elec_motion_2_aver_PES_1step_dx_div_dt_adia'
  write(*,*) '1'
  write(*,*) 'i_state, x_elec, p_elec, dx_elec_div_dt'
  do i_state = 1, n_state
    write(*,*) i_state, x_elec(i_state), p_elec(i_state), dx_elec_div_dt(i_state)
  enddo
  write(*,*)
  write(*,*) 'dij(1,2,:)'
  write(*,*) dij(1,2,:)
  write(*,*)
endif
do i_state = 1, n_state
  dtmp = dx_elec_div_dt(i_state)
  dtmp2 = 0.d0
  do j_state = 1, n_state
    dtmp3 = 0.d0
    dij_tmp = dij(j_state, i_state, :)
    do i_mode = 1, n_mode
      dtmp3 = dtmp3 + dij_tmp(i_mode) * p_nuc_div_mass(i_mode)
    enddo
    dtmp2 = dtmp2 + x_elec(j_state) * dtmp3
  enddo
  dtmp = dtmp + dtmp2
  dx_elec_div_dt(i_state) = dtmp
enddo
if(label_debug > 1) then
  write(*,*) 'sub_elec_motion_2_aver_PES_1step_dx_div_dt_adia'
  write(*,*) '2'
  write(*,*) 'i_state, x_elec, p_elec, dx_elec_div_dt'
  do i_state = 1, n_state
    write(*,*) i_state, x_elec(i_state), p_elec(i_state), dx_elec_div_dt(i_state)
  enddo
  write(*,*)
endif

return
end