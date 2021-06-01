subroutine sub_evolution_mapping_2_on_the_fly_traj_adjusted
use mod_main
implicit none

include 'param.def'
include 'var_n_atom.h'

integer i_step

real(kind=8), allocatable, dimension(:) :: x_nuc_cur, p_nuc_cur, &
                                               x_nuc_pre, p_nuc_pre, &
                                               p_nuc_kin_cur, &
                                               p_nuc_kin_pre, &
                                               x_elec, p_elec, &
                                               gammas, &
                                               ene_adia_cur, &
                                               ene_adia_pre, mass, &
                                               vel_nuc_cur, &
                                               vel_nuc_kin_cur, &
                                               vel_nuc_kin_pre, &
                                               dp_nuc_kin_div_dt

real(kind=8), allocatable, dimension(:,:) :: hop_pro, c_n

complex(kind=8), allocatable, dimension(:) :: ele_coe
complex(kind=8), allocatable, dimension(:,:) :: dtoa_u
real(kind=8), allocatable, dimension(:,:) :: mat_U
real(kind=8), allocatable, dimension(:,:) :: a_hamiton, &
                                                dia_hamiton, &
                                                Ham, grad
real(kind=8), allocatable, dimension(:,:,:) :: dij_cur, dij_pre
real(kind=8) nuc_dt_half
real(kind=8) zpe_all

integer i_state, i_mode

allocate (x_nuc_cur(n_mode))
allocate (p_nuc_cur(n_mode))
allocate (vel_nuc_cur(n_mode))
allocate (x_nuc_pre(n_mode))
allocate (p_nuc_pre(n_mode))
allocate (p_nuc_kin_cur(n_mode))
allocate (vel_nuc_kin_cur(n_mode))
allocate (vel_nuc_kin_pre(n_mode))
allocate (mass(n_mode))
allocate (x_elec(n_state))
allocate (p_elec(n_state))
allocate (hop_pro(n_state,n_state))
allocate (ele_coe(n_state))
allocate (c_n(n_state, n_state))
allocate ( a_hamiton (n_state, n_state))
allocate (dia_hamiton(n_state, n_state))
allocate (Ham(n_state, n_state))
allocate ( mat_U(n_state, n_state) )
allocate ( ene_adia_cur(n_state) )
allocate ( ene_adia_pre(n_state) )
allocate ( grad(n_state, n_mode) )
allocate ( dij_cur(n_state, n_state, n_mode) )
allocate ( dij_pre(n_state, n_state, n_mode) )
allocate ( dp_nuc_kin_div_dt(n_mode) )
allocate ( gammas(n_state) )

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!      
mass = 0.d0
x_nuc_cur = 0.d0
vel_nuc_cur =0.d0
p_nuc_cur = 0.d0
if(label_debug >= 2) then
  write(*,*) "begining of sub_evolution_mapping_2_on_the_fly_traj_adjusted.f90"
  call sub_test(mass, ene_adia_cur)
endif

if(label_debug >= 2) write(*,*) 'nuc_dt(fs):', nuc_dt
nuc_dt = nuc_dt / TOFS
nuc_dt_half = 0.5d0 * nuc_dt
i_step= 0

!call sub_read_ini_trj_2(x_nuc_cur, p_nuc_cur, &
!                  x_elec, p_elec)
call sub_read_current_geom_mapping(x_nuc_cur, &
                  vel_nuc_cur, & ! vel_nuc
                  atom_label, &
                  x_elec, p_elec, &
                  i_step)
if(label_debug >= 2) then
  write(*,*) "call sub_read_current_geom_mapping done"
  call sub_test(mass, ene_adia_cur)
endif

call sub_cal_gammas(x_elec, p_elec, gammas)

call sub_read_parameter_on_the_fly(mass, atom_label)
if(label_debug >= 2) then
  write(*,*) "sub_evolution_mapping_2_on_the_fly"
  write(*,*) "after sub_read_parameter_on_the_fly"
  call sub_test(mass, ene_adia_cur)
  write(*,*) "i_mode  mass  x_nuc_cur  vel_nuc_cur"
  do i_mode = 1, n_mode
    write(*,*) i_mode, mass(i_mode), x_nuc_cur(i_mode), vel_nuc_cur(i_mode)
  enddo
endif
if(label_debug >= 2) write(*,*) "call sub_read_parameter_on_the_fly done"
if(label_debug >= 2) write(*,*) "vel_nuc_cur(1): ", vel_nuc_cur(1)
p_nuc_cur = vel_nuc_cur * mass
call sub_test(mass, ene_adia_cur)
if(label_debug >= 2) write(*,*) "p_nuc_cur(1): ", p_nuc_cur(1)
      
if(label_debug >= 2) then
  write(*,*) 'sub_evolution_mapping_2_on_the_fly'
  write(*,*) 'call sub_read_ini_trj_2 done'
  write(*,*) 'p_nuc_cur'
  do i_mode = 1, n_mode
    write(*,*) p_nuc_cur(i_mode)
  enddo
  write(*,*)
endif
!
! vij = lambda0 + lambda1 * X
!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

call sub_many_ana_pes_mapping(x_nuc_cur, &
                  grad, &
                  dij_cur, &
                  ene_adia_cur, &
                  atom_label, &
                  i_step)
if(label_debug >= 2) write(*,*) "ene_adia_cur", ene_adia_cur
zpe_all = ene_adia_cur(1)
ene_adia_cur = ene_adia_cur - zpe_all
!dij_cur = 0
!c_n = 0.d0
!c_n(1,1) = 1.d0

call sub_p_to_p_kin(p_nuc_cur, p_nuc_kin_cur, &
                    dij_cur, &
                    x_elec, p_elec)
vel_nuc_kin_cur = p_nuc_kin_cur / mass

!call sub_calc_mat_d2a(mat_U)

call sub_write_trj_2_adia(i_step, &
                         x_elec, p_elec, &
                         x_nuc_cur, p_nuc_cur, &
                         mat_U)
write(*,*) "ene_adia_cur", ene_adia_cur
if(label_debug >= 2) then
  write(*,*) "sub_evolution_mapping_2_on_the_fly"
  write(*,*) "before sub_write_geom_mapping"
  write(*,*) "i_mode  mass  x_nuc_cur  p_nuc_cur"
  do i_mode = 1, n_mode
    write(*,*) i_mode, mass(i_mode), x_nuc_cur(i_mode), p_nuc_cur(i_mode)
  enddo
endif
call sub_write_geom_mapping_traj_adjusted(x_nuc_cur, &
              p_nuc_cur, & ! vel_nuc
              p_nuc_kin_cur, &
              atom_label, &
              mass, &
              x_elec, p_elec, &
              gammas, &
              ene_adia_cur, &
              i_step)
if(label_debug >= 2) then
  write(*,*) "sub_evolution_mapping_2_on_the_fly_traj_adjusted"
  write(*,*) "after sub_write_geom_mapping"
  do i_mode = 1, n_mode
    write(*,*) "mass",i_mode, mass(i_mode)
  enddo
endif

if (label_aver_PES == 1) then
  do i_step=1, n_step
    vel_nuc_kin_pre = vel_nuc_kin_cur
    ene_adia_pre = ene_adia_cur
    dij_pre = dij_cur
    
    
!    write(*,*) 'bug below?'
    call sub_elec_motion_2_aver_PES_adia(vel_nuc_kin_cur, &
                    vel_nuc_kin_pre, &
                    x_elec, p_elec,&
                    ene_adia_cur, ene_adia_pre, &
                    dij_cur, dij_pre)
      if(label_debug >= 2) then
        write(*,*) 'sub_evolution_mapping_2_on_the_fly'
        write(*,*) 'call sub_elec_motion_2_aver_PES_adia done'
      endif
!#  write(*,*) 'sub_elec_motion done'
!#!     call sub_get_c_n_elec_2(x_elec, p_elec, c_n)
!#!
    if(label_debug >= 2) then
      write(*,*) 'p_nuc_cur'
      do i_mode = 1, n_mode
        write(*,*) p_nuc_cur(i_mode)
      enddo
      write(*,*)
      write(*,*) 'i_state, x_elec, p_elec'
      do i_state = 1, n_state
        write(*,*) i_state, x_elec(i_state), p_elec(i_state)
      enddo
    endif

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of P
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    call sub_nuc_motion_2_aver_PES_1step_dp_div_dt_adia_traj_adjusted( &
                           dp_nuc_kin_div_dt, &
                           grad, &
                           x_elec, p_elec, gammas, &
                           ene_adia_cur, &
                           dij_cur)
      if(label_debug >= 2) then
        write(*,*) 'sub_evolution_mapping_2_on_the_fly'
        write(*,*) 'call sub_nuc_motion_2_aver_PES_1step_dp_div_dt_adia done'
      endif
    if(label_debug >= 2) then
       write(*,*) 'dp_nuc_kin_div_dt(1): ', dp_nuc_kin_div_dt(1)
    endif
    call sub_move(n_mode, p_nuc_kin_cur, dp_nuc_kin_div_dt, nuc_dt_half)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! one step of X
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! calculate vel_nuc_kin_cur
    vel_nuc_kin_cur = p_nuc_kin_cur / mass
    call sub_move(n_mode, x_nuc_cur, vel_nuc_kin_cur, nuc_dt)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! update force
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    call sub_many_ana_pes_mapping(x_nuc_cur, &
                  grad, &
                  dij_cur, &
                  ene_adia_cur, &
                  atom_label, &
                  i_step)
!dij_cur = 0
      if(label_debug >= 2) then
        write(*,*) 'sub_evolution_mapping_2_on_the_fly'
        write(*,*) 'call sub_many_ana_pes_mapping done'
      endif
    if(label_debug >= 2) write(*,*) "ene_adia_cur", ene_adia_cur
    ene_adia_cur = ene_adia_cur - zpe_all
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!write(*,*) ene_adia_cur
 
    if (label_nac_phase  .eq.  1) then
      call sub_nac_phase_mapping (dij_pre, &
                        dij_cur)
    endif
    
 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of P
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    call sub_nuc_motion_2_aver_PES_1step_dp_div_dt_adia_traj_adjusted( &
                           dp_nuc_kin_div_dt, &
                           grad, &
                           x_elec, p_elec, gammas, &
                           ene_adia_cur, &
                           dij_cur)
    call sub_move(n_mode, p_nuc_kin_cur, dp_nuc_kin_div_dt, nuc_dt_half)
    vel_nuc_kin_cur = p_nuc_kin_cur / mass
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    call sub_p_kin_to_p(p_nuc_cur, p_nuc_kin_cur, &
                  dij_cur, &
                  x_elec, p_elec)
    vel_nuc_cur = p_nuc_cur / mass
    call sub_write_current_geom_mapping(x_nuc_cur, &
                  p_nuc_cur, & ! vel_nuc
                  p_nuc_kin_cur, &
                  atom_label, &
                  x_elec, p_elec, &
                  i_step)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if(label_debug >= 2) then
      write(*,*) 'sub_evolution_mapping_2_on_the_fly'
      write(*,*) 'call sub_nuc_motion_2_aver_PES_adia done'
      write(*,*) 'p_nuc_kin_cur'
      do i_mode = 1, n_mode
        write(*,*) p_nuc_kin_cur(i_mode)
      enddo
      write(*,*)
    endif
    if (mod(i_step,n_save_trj) .eq. 0 ) then
      call sub_p_kin_to_p(p_nuc_cur, p_nuc_kin_cur, &
                        dij_cur, &
                        x_elec, p_elec)
!call sub_write_trj_2(x_elec, p_elec, x_nuc_cur, p_nuc_cur)
      if(label_debug >= 2) then
        write(*,*) 'sub_evolution_mapping_2_on_the_fly'
        write(*,*) 'call sub_p_kin_to_p done'
      endif
      if(label_debug >= 2) then
        write(*,*) 'p_nuc_cur'
        do i_mode = 1, n_mode
          write(*,*) p_nuc_cur(i_mode)
        enddo
        write(*,*)
      endif
      call sub_write_trj_2_adia(i_step, &
                         x_elec, p_elec, &
                         x_nuc_cur, p_nuc_cur, &
                         mat_U)
      if(label_debug >= 2) then
        write(*,*) 'sub_evolution_mapping_2_on_the_fly'
        write(*,*) 'call sub_write_trj_2_adia done'
      endif
      call sub_write_geom_mapping_traj_adjusted(x_nuc_cur, &
                  p_nuc_cur, & ! vel_nuc
                  p_nuc_kin_cur, &
                  atom_label, &
                  mass, &
                  x_elec, p_elec, &
                  gammas, &
                  ene_adia_cur, &
                  i_step)
      if(label_debug >= 2) then
        write(*,*) 'sub_evolution_mapping_2_on_the_fly'
        write(*,*) 'call sub_write_geom_mapping done'
      endif
    endif
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    
  enddo
else
  write(*,*) "Non-aver-pes subroutine is not available now!"
endif

deallocate (x_nuc_cur)
deallocate (p_nuc_cur)
deallocate (x_nuc_pre)
deallocate (p_nuc_pre)
deallocate (x_elec)
deallocate (p_elec)
deallocate (ele_coe)
deallocate (hop_pro)
deallocate (c_n)
deallocate (vel_nuc_cur)
deallocate (p_nuc_kin_cur)
deallocate (vel_nuc_kin_cur)
deallocate (vel_nuc_kin_pre)
deallocate (mass)
deallocate ( a_hamiton )
deallocate (dia_hamiton)
deallocate (Ham)
deallocate ( mat_U )
deallocate ( ene_adia_cur )
deallocate ( ene_adia_pre )
deallocate ( grad )
deallocate ( dij_cur )
deallocate ( dij_pre )
deallocate ( dp_nuc_kin_div_dt )
deallocate ( gammas )


end
