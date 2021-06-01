subroutine   sub_mapping_ana_nac ( n_atom, & 
                                n_state, md_state, &
                                ntime, dtime, ntime_ele, &
                                n_sav_stat, n_sav_traj, &
                                qm_method,&
                                seed_random, &
                                label_nac_phase )


use mod_main
implicit none
include 'param.def'

integer, intent(in) :: n_atom     
integer, intent(in) :: ntime, ntime_ele
integer, intent(in) :: n_sav_stat
integer, intent(in) :: qm_method
integer, intent(inout) :: seed_random
integer, intent(in) :: label_nac_phase      

integer, intent(inout), dimension(n_state) :: md_state
double precision, intent(inout) :: dtime   
     
     
      

      

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!  - Define local variables
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
real(kind=8), dimension(n_state) x_elec, p_elec

double precision, dimension(n_atom) ::   &
                                                coor_x, &
                                                coor_y, &
                                                coor_z

double precision, dimension(n_atom) ::   &
                                                vel_x, &
                                                vel_y, &
                                                vel_z
real(kind=8) x_nuc_cur(3*n_atom)
real(kind=8) p_nuc_cur(3*n_atom)
real(kind=8) x_nuc_pre(3*n_atom)
real(kind=8) p_nuc_pre(3*n_atom)
real(kind=8) p_nuc_kin_cur(3*n_atom)
real(kind=8) p_nuc_kin_pre(3*n_atom)
real(kind=8) x_elec(n_state)
real(kind=8) p_elec(n_state)
real(kind=8) grad_xyz(n_state, 3*n_atom)
real(kind=8) dij_cur(n_state, n_state, 3*n_atom)
real(kind=8) dij_pre(n_state, n_state, 3*n_atom)
real(kind=8) p_nuc_kin_cur_div_mass(3*n_atom)
real(kind=8) p_nuc_kin_pre_div_mass(3*n_atom)
real(kind=8) dx_nuc_div_dt(3*n_atom)
real(kind=8) dp_nuc_kin_div_dt(3*n_atom)            
                                     
character*2, dimension(n_atom)  ::  atom_label



integer :: file_save_energy, file_save_traj,  &
           file_save_grad, &
           file_save_vel, file_md_out, &
           file_save_state, file_save_all, &
           file_save_ele, file_save_pe, &
           file_save_dipole



integer :: i, j, it, i_mode, i_atom

double precision, dimension(n_atom) ::   mass, charge
integer :: input_numer

double precision, dimension(n_atom) ::   gradient_x, &
                                         gradient_y, &
                                         gradient_z 




double precision, dimension(n_state, n_atom) ::   &
                                         gra_all_x, &
                                         gra_all_y, &
                                         gra_all_z

double precision, dimension(n_state, n_atom) ::   &
                                         old_gra_all_x, &
                                         old_gra_all_y, &
                                         old_gra_all_z


double precision, dimension(n_state, n_state, n_atom) ::   &
                                         nac_x, &
                                         nac_y, &
                                         nac_z

double precision, dimension(n_state, n_state, n_atom) ::   &
                                         old_nac_x, &
                                         old_nac_y, &
                                         old_nac_z

double precision, dimension(n_atom) ::   &
                                         old_vel_x, &
                                         old_vel_y, &
                                         old_vel_z


double precision :: time, pes_ref, pes_current


double precision, dimension(n_state) ::  pes_all,  &
                                         old_pes_all 
complex (kind=8), dimension(n_state, n_state) :: rho 


integer :: index_state, old_index_state, new_index_state

!       integer :: i_state, j_state, k

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
double precision :: tmp_mass
integer          :: tmp_charge   
character*2      :: tmp_label

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! random number initialized
call init_random_seed(seed_random)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!   -       Find all masses !!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



file_md_out=23
open(unit=file_md_out, file="dynamics.out")

write (file_md_out, *) "--------------------------------------"
write (file_md_out, *) "Run the mapping dynamics!"
write (file_md_out, *) "--------------------------------------"
write (file_md_out, *)
write (file_md_out, *)
write (file_md_out, *) "Initialization" 
write (file_md_out, *) "Parameters for the dynamics calculations"
write (file_md_out, *) " Total time:", dtime*ntime
write (file_md_out, *) " Time step:",  dtime
write (file_md_out, *) " The number of time steps:", ntime       
write (file_md_out, *) "The frequency to save the energy:", n_sav_stat
write (file_md_out, *) "The frequency to save the geometry:", n_sav_traj
write (file_md_out, *)
write (file_md_out, *) "The quantum calculations"
write (file_md_out, *) "Which methods? ", qm_method
write (file_md_out, *) "(1: MNDO, 2: CASSCF-MOLPRO, &
                         11: TDDFT-Turbomole,...)"
write (file_md_out, *)
write (file_md_out, *) "which state to start?",  i_state
write (file_md_out, *) "How many states are involved?",  n_state
write (file_md_out, 9998) "Which states are involved?",  md_state(:)
write (file_md_out, *) " Time step for electronic motions", ntime_ele
if (0  .ge. cor_dec )  then
    write (file_md_out, *) "No decoherent correction"
else
    write (file_md_out, *) "Decoherent correction factor",cor_dec
endif       
if (label_nac_phase  .eq. 0 )  then
     write (file_md_out, *) "Do not follow the phase of NAC"
endif
if (label_nac_phase  .eq. 1 )  then
     write (file_md_out, *) "Follow the phase of NAC"
endif
if ( (label_nac_phase  .ne. 0 ) &
     .and.                      & 
     (label_nac_phase  .ne. 1 ) &
   ) then
     write (file_md_out, *) "How to treat the phase of NAC?"
     stop
endif
     

9998   format( a, 10(i3,";")) 

write (file_md_out, *) "--------------------------------------"  


n_mode = 3 * n_atom
n_ele_dt = ntime_ele
nuc_dt = dtime
nuc_dt_half = 0.5d0 * nuc_dt

file_save_energy=24
file_save_traj=25
file_save_grad=32
file_save_vel=26
file_save_state=27
file_save_all=28 
file_save_ele=29
file_save_pe=30
file_save_dipole=31

open(unit=file_save_energy, file="energy_time.out")
open(unit=file_save_traj,   file="traj_time.out")
open(unit=file_save_grad,   file="grad_time.out")
open(unit=file_save_vel,    file="vel_time.out")
open(unit=file_save_ele,    file="ele_time.out")
open(unit=file_save_pe,    file="pe_time.out")
open(unit=file_save_dipole,    file="di_time.out")

!       write (*,*) file_save_energy



!      Obttain the gradient and pes at time zero
write (file_md_out, *) "Calculate the gradient"



it=0
time=0

write (file_md_out, *) "Time steps:", it
write (*, *) "Time steps:", it

!      Read initial coordinates

call sub_read_current_geom (n_atom, &
                         coor_x, coor_y, coor_z, &
                         vel_x, vel_y, vel_z, &
                         atom_label, &
                         n_state, &
                         rho, &
                         index_state, &
                         it, time )
call sub_mapping_read_ini_trj_elec_2(x_elec, p_elec)

do i=1,n_atom
   tmp_label = atom_label(i)
   call sub_get_mass ( tmp_label, tmp_mass, tmp_charge)
   mass (i) = tmp_mass
   charge(i) = tmp_charge
enddo


call sub_many_ana_pes  (n_atom, &
                  n_state, md_state, &
                  atom_label, &
                  coor_x, coor_y, coor_z, &
                  label_ZN, &
                  qm_method, &
                  index_state, &
                  gra_all_x, &
                  gra_all_y, &
                  gra_all_z, &
                  nac_x, &
                  nac_y, &
                  nac_z, &
                  pes_all, &
                  it, &
                  file_md_out, &
                  file_save_dipole )


call sub_save_restart (n_atom, &
     coor_x, coor_y, coor_z, &
     vel_x, vel_y, vel_z, &
     atom_label, &
     n_state, &
     rho, &
     index_state, &
     it, time)


!        Save the energy

pes_ref = pes_all (1)



write (file_save_energy, *)  &
                      "# Step,  Time,  &
                         Potential energy, &
                         Kinetic energy, &
                         Total energy, &
                         linear_momenta_x, &
                         linear_momenta_y, &
                         linear_momenta_z"

 
call sub_save_energy ( n_atom, &
                   pes_current, &
                    vel_x, vel_y, vel_z, &
                    mass, &
                    it,time, &
                    file_save_energy)
  

call sub_save_pe (    it,time, &
                      n_state, &
                      index_state, &
                      pes_all, &
                      file_save_pe )


call sub_save_traj ( n_atom, &
                    coor_x, coor_y, coor_z, &
                    vel_x, vel_y, vel_z, &
                    atom_label, &
                    it, time, &
                    file_save_traj, file_save_vel )

call sub_save_grad (n_atom, n_state, index_state, &
                        gra_all_x, &
                        gra_all_y, &
                        gra_all_z, &
                        atom_label, &
                        it, time, &
                        file_save_grad )


write (file_save_state, *)  &
                      "# Step, Time, &
                         Current state, &
                         Current potential, &
                         Velocity norm, &
                         current gradient"

p_nuc_cur = 0.d0
p_nuc_kin_cur = 0.d0
dij_cur = 0.d0
dij_pre = 0.d0


!      Begin the propagation      
do it=1, ntime

  time = it*dtime

  write (file_md_out, *) "Time steps:", it
  write (*, *) "Time steps:", it

  old_gra_all_x = gra_all_x
  old_gra_all_y = gra_all_y
  old_gra_all_z = gra_all_z

  old_nac_x = nac_x
  old_nac_y = nac_y
  old_nac_z = nac_z

  old_pes_all = pes_all  

  old_vel_x = vel_x
  old_vel_y = vel_y
  old_vel_z = vel_z   

  do i_atom = 1, n_atom
    p_nuc_cur(3 * (i_atom - 1) + 1) = vel_x(i_atom)*mass(i_atom)
    p_nuc_cur(3 * (i_atom - 1) + 2) = vel_y(i_atom)*mass(i_atom)
    p_nuc_cur(3 * (i_atom - 1) + 3) = vel_z(i_atom)*mass(i_atom)
  enddo
  do i_atom = 1, n_atom
    grad_xyz(:,3 * (i_atom - 1) + 1) = gra_all_x(:,i_atom)
    grad_xyz(:,3 * (i_atom - 1) + 2) = gra_all_y(:,i_atom)
    grad_xyz(:,3 * (i_atom - 1) + 3) = gra_all_z(:,i_atom)
  enddo
  do i_atom = 1, n_atom
    dij_cur(:,:,3 * (i_atom - 1) + 1) = nac_x(:,:,i_atom)
    dij_cur(:,:,3 * (i_atom - 1) + 2) = nac_y(:,:,i_atom)
    dij_cur(:,:,3 * (i_atom - 1) + 3) = nac_z(:,:,i_atom)
  enddo
    
  call sub_p_to_p_kin(p_nuc_cur, p_nuc_kin_cur, &
                      dij_cur, &
                      x_elec, p_elec)

  p_nuc_kin_pre = p_nuc_kin_cur
  dij_pre = dij_cur
  
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of P
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  call sub_nuc_motion_2_aver_PES_1step_dp_div_dt_adia(dp_nuc_kin_div_dt, &
                           grad_xyz, &
                           x_elec, p_elec, &
                           pes_all, &
                           dij_cur)
  call sub_move(n_mode, p_nuc_kin_cur, dp_nuc_kin_div_dt, nuc_dt)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! one step of X
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! calculate dx_nuc_div_dt
  do i_atom = 1, n_atom
    do i = 1, 3
      dx_nuc_div_dt(3 * (i_atom - 1) + i) = p_nuc_kin_cur(3 * (i_atom - 1) + i) / mass(i_atom)
    enddo
  enddo
  call sub_move(n_mode, x_nuc_cur, dx_nuc_div_dt, nuc_dt)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!          Get all gradients
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  call sub_many_ana_pes (n_atom, &
                  n_state, md_state, &
                  atom_label, &
                  coor_x, coor_y, coor_z, &
                  label_ZN, &
                  qm_method, &
                  index_state, &
                  gra_all_x, &
                  gra_all_y, &
                  gra_all_z, &
                  nac_x, &
                  nac_y, &
                  nac_z, &
                  pes_all, &
                  it, &
                  file_md_out, &
                  file_save_dipole )
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                  
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! half step of P
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  call sub_nuc_motion_2_aver_PES_1step_dp_div_dt_adia(dp_nuc_kin_div_dt, &
                           grad_xyz, &
                           x_elec, p_elec, &
                           pes_all, &
                           dij_cur)
  call sub_move(n_mode, p_nuc_kin_cur, dp_nuc_kin_div_dt, nuc_dt)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! elec propagation
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  do i_atom = 1, n_atom
    do i = 1, 3
      p_nuc_kin_cur_div_mass(3 * (i_atom - 1) + i) = p_nuc_kin_cur(3 * (i_atom - 1) + i) / mass(i_atom)
      p_nuc_kin_pre_div_mass(3 * (i_atom - 1) + i) = p_nuc_kin_pre(3 * (i_atom - 1) + i) / mass(i_atom)
    enddo
  enddo
  call sub_elec_motion_2_aver_PES_adia(p_nuc_kin_cur_div_mass, &
                    p_nuc_kin_pre_div_mass, &
                    x_elec, p_elec, &
                    pes_all, old_pes_all, &
                    dij_cur, dij_pre)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  if (label_nac_phase  .eq.  1) then
    call sub_nac_phase (n_atom, &
                  n_state, &
                  old_nac_x, &
                  old_nac_y, &
                  old_nac_z, &
                  nac_x, &
                  nac_y, &
                  nac_z)
  endif
 


!       save restart file
       call sub_save_restart (n_atom, &
            coor_x, coor_y, coor_z, &
            vel_x, vel_y, vel_z, &
            atom_label, &
            n_state, &
            rho, &
            index_state, &
            it, time)



          call sub_save_pe (  it,time, &
                              n_state, &
                              index_state, &
                              pes_all, &
                              file_save_pe )


!!!       Save the current geometry and velocity
          call  sub_write_current_geom (n_atom, &
                                coor_x, coor_y, coor_z, &
                                vel_x, vel_y, vel_z, &
                                atom_label, &
                                n_state, &
                                rho, &
                                index_state, &
                                it, time )





!!!!!!    Save the energy
          if (  mod(it, n_sav_stat) .eq. 0 ) then
          pes_current =  pes_all (index_state) 
          call sub_save_energy ( n_atom, &
                            pes_current, &
                            vel_x, vel_y, vel_z, &
                            mass, &
                            it,time, &
                            file_save_energy )

          endif



!!!!!     Save the trajectory
          if ( mod(it, n_sav_traj) .eq. 0 ) then
          call sub_save_traj ( n_atom, &
                            coor_x, coor_y, coor_z, &
                            vel_x, vel_y, vel_z, &
                            atom_label, &
                            it, time, &
                            file_save_traj, file_save_vel )
          endif


!!!!!     Save the gradient
          if ( mod(it, n_sav_traj) .eq. 0 ) then
          call sub_save_grad (n_atom, n_state, index_state, &
                                gra_all_x, &
                                gra_all_y, &
                                gra_all_z, &
                                atom_label, &
                                it, time, &
                                file_save_grad )

          endif



!          write (28,9999) it, coor_x(:), gradient_x(:), vel_x(:)


       enddo


       close(file_md_out)
       close(file_save_energy)
       close(file_save_traj)
       close(file_save_vel)
       close(file_save_state)
       close(file_save_all)
       close(file_save_ele)
       close(file_save_pe)
       close(file_save_grad)

9999   format (i10,10(f20.10,1x) )
9997   format (a)

       return
 
       end 
