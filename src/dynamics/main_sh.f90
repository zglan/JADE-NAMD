       Program main

   
       implicit none
       include 'param.def'

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!  - Define all input files
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

       integer :: file_ini_coor,  file_ini_vel
              
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!       
!!!!!!!!-- Define all variables to read the geometry----
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
      integer :: n_atom
      double precision, allocatable, dimension(:) ::  coor_x, &
                                                      coor_y, &
                                                      coor_z
      double precision, allocatable, dimension(:) ::  vel_x, &
                                                      vel_y, &
                                                      vel_z

      character*2, allocatable, dimension(:)      ::  atom_label




!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!  - Define all input files
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

       integer :: file_dynvar_in


       integer :: i, j, it, i_state
       integer :: ntime, n_sav_stat, n_sav_traj
       integer :: n_state, ntime_ele
       
       integer :: qm_method, dyn_method, qm_package, label_ZN
     
       integer, allocatable, dimension(:) ::  md_state
       character (len=256) md_state_list
       
      

       double precision :: time,  dtime, cor_dec
       integer :: seed_random
 
       integer :: label_read_velocity
       integer :: label_nac_phase      
       integer :: label_reject_hops
       integer :: label_restart
       double precision ::   hop_e   
        
       complex (kind=8), allocatable, dimension(:, :) :: rho
       integer :: index_state

       namelist /control/ dyn_method, label_ZN, ntime, dtime, & 
            n_sav_stat, n_sav_traj, ntime_ele, &
            qm_method, n_state, md_state_list, i_state, &
            seed_random, cor_dec, label_nac_phase, label_reject_hops, &
            hop_e, label_read_velocity, label_restart
            
       double precision :: gamma0, temperature
       namelist /langevin/ gamma0, temperature

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

       write (*,*) "------------------------"
       write (*,*) "JADE (version 1.0 alpha)"
       write (*,*) "========================"
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!   ---  Initialize the parameters for dynamics
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!       

       write (*,*) "Initialization"
       file_dynvar_in=21       
       open(unit=file_dynvar_in, file="dyn.inp")      
       write (*,*) "dyn.inp open to read.."
       read(file_dynvar_in, nml = control)
       if (dyn_method == 201) then
          write(*, *) "Langevin Method is used to Control Temperature"
          read(file_dynvar_in, nml = langevin)
       endif
       close(file_dynvar_in)
       allocate (md_state(n_state))       
       read(md_state_list, *) (md_state(i),i=1,n_state)
       write(*,nml=control) 
       write(*,nml=langevin)
       dtime = dtime/TOFS

       write (*,*) " Finish  the initialization"


!     Read the initial geometry

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!  -   Find how many atoms !!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!     if (dyn_method /= 11) then
       file_ini_coor=11
       open(unit=file_ini_coor, file="stru_xyz.in")
       write (*,*) "hahah"
       read (file_ini_coor, *) n_atom
       close(11)
       


       allocate (coor_x(n_atom))
       allocate (coor_y(n_atom))
       allocate (coor_z(n_atom))
       allocate (atom_label(n_atom))

       allocate (vel_x(n_atom))
       allocate (vel_y(n_atom))
       allocate (vel_z(n_atom))
       allocate (rho(n_state, n_state))

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!! --   Initialize the coordinates  and momentum !!!!!!!!      
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

      
      
        file_ini_coor=11
        open(unit=file_ini_coor, file="stru_xyz.in")
        call sub_read_coor ( n_atom, coor_x, coor_y, coor_z, &
                         atom_label, file_ini_coor)
        close(11)
       !write(*,*)"atom_label(1)  ", atom_label(1)
      

       vel_x =0.d0
       vel_y =0.d0
       vel_z =0.d0

!     Read  the initial velocity if necessary
      if (label_read_velocity .eq. 1) then
          file_ini_vel=12
          open(unit=file_ini_vel, file="vel_xyz.in")
          call sub_read_ini_vel (n_atom, vel_x, vel_y, vel_z, &
                             atom_label, file_ini_vel)
          close(file_ini_vel)
      endif      

   
      if (label_restart .eq. 0 ) then
         do i=1, n_state
            if (md_state(i)  .eq.  i_state) then
               index_state=i
            endif
         enddo

         do i=1, n_state
            do j=1, n_state
               rho(i,j)=0.d0
            enddo
         enddo

         rho(index_state, index_state) = 1.d0


         call system ("rm *.dat")
         call system ("rm *.out")
         call system ("rm -rf QC_TMP")
!         call system ("rm -rf ZN QC_TMP")
 
      endif

   


      if (label_restart .eq. 1 ) then
 
          call sub_read_restart (n_atom, &
                             coor_x, coor_y, coor_z, &
                             vel_x, vel_y, vel_z, &
                             atom_label, &
                             n_state, &
                             rho, &
                             index_state, &
                             it, time )

      endif



       it = 0
       time = 0
       !write(*,*)"atom_label(1)  ", atom_label(1)
       call  sub_write_current_geom (n_atom, &
                            coor_x, coor_y, coor_z, &
                            vel_x, vel_y, vel_z, &
                            atom_label, &
                            n_state, &
                            rho, &
                            index_state, & 
                            it, time )

       deallocate (coor_x)
       deallocate (coor_y)
       deallocate (coor_z)
       deallocate (atom_label)

       deallocate (vel_x)
       deallocate (vel_y)
       deallocate (vel_z)
!     endif


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!   - Dynamics Methods !!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 

       if ( (n_state .gt. 1)  .and. &
            ( dyn_method .eq. 1 ) )  then
          write (*,*) "Surface Hopping with analytical NAC"
          
          if (label_ZN .eq. 0) then 
             write (*,*) "Surface Hopping with tully method"
             call  sub_sh_ana_nac   ( n_atom, &
                                      i_state, & 
                                      n_state, md_state, &
                                      ntime, dtime, ntime_ele, &
                                      n_sav_stat, n_sav_traj, &
                                      label_ZN, &
                                      qm_method,&
                                      seed_random, &
                                      cor_dec, &
                                      label_nac_phase, &
                                      label_reject_hops, &
                                      hop_e )
          else
             write (*,*) "Surface Hopping with ZN method"
             write (*,*) "hop_e", hop_e
             call  sub_sh_zn        ( n_atom, &
                                      i_state, & 
                                      n_state, md_state, &
                                      ntime, dtime, ntime_ele, &
                                      n_sav_stat, n_sav_traj, &
                                      label_ZN, &
                                      qm_method,&
                                      seed_random, &
                                      label_reject_hops, &
                                      hop_e )
          endif

       endif

       
       if ( (n_state .gt. 1)  .and. &
            (dyn_method .eq. 2 ) )  then
             write (*,*) "Surface Hopping with numerical NAC"
             write (*,*) "RANDOM", seed_random
             call  sub_sh_num_nac  ( n_atom, &
                                   i_state, & 
                                   n_state, md_state, &
                                   ntime, dtime, ntime_ele, &
                                   n_sav_stat, n_sav_traj, &
                                   qm_method,&
                                   seed_random, &
                                   cor_dec, &
                                   label_nac_phase, &
                                   label_reject_hops, &
                                   hop_e )
       endif

       if ( (n_state .gt. 1)  .and. &
            (dyn_method .eq. 201 ) )  then
             write (*,*) "Surface Hopping with numerical NAC and langevin thermostat"
             write (*,*) "RANDOM", seed_random
             call  sub_lang_sh_num_nac  ( n_atom, &
                                   i_state, &                           
                                   n_state, md_state, &
                                   ntime, dtime, ntime_ele, &
                                   n_sav_stat, n_sav_traj, &
                                   qm_method,&
                                   seed_random, &
                                   cor_dec, &
                                   label_nac_phase, &
                                   label_reject_hops, &
                                   hop_e, &
                                   gamma0, &
                                   temperature )
       endif


       
       if ( (n_state .gt. 1)  .and. &
            (dyn_method .eq. 3 ) )  then
          write (*,*) "ab initio dynamics at single surface (BOMD)."
!       call  takasuka          ( n_atom, &
!                                 coor_x, coor_y, coor_z, &
!                                 vel_x, vel_y, vel_z, &
!                                 atom_label, &
!                                 n_states, md_state )
       endif


       if (  dyn_method .eq. 5  )  then
       write (*,*) "Surface Hopping with SOC, only for first spin excited states."
       call  sub_sh_ana_nac      ( n_atom, &
                                   i_state, &                                 
                                   n_state, md_state, &
                                   ntime, dtime, ntime_ele, &
                                   n_sav_stat, n_sav_traj, &
                                   qm_method,&
                                   seed_random, &
                                   cor_dec, &
                                   label_nac_phase, &
                                   label_reject_hops, &
                                   hop_e )
       endif

       !if ( (n_state .gt. 1)  .and. &
       !     ( dyn_method .eq. 11 ) )  then
       !   write (*,*) "Mapping dynamics with Meyer-Miller Model."
       !   write (*,*) "J. Chem. Phys. 147, 064112 (2017)."
       !      call  sub_mapping_ana_nac()

       !endif
      
       deallocate (md_state)


       end 
