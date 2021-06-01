      subroutine   sub_sh_zn ( n_atom, &
                               i_state, &
                               n_state, &
                               md_state, &
                               ntime, &
                               dtime, &
                               ntime_ele, &
                               n_sav_stat, &
                               n_sav_traj, &
                               label_ZN, &
                               qm_method, &
                               seed_random, &
                               label_reject_hops, &
                               hop_e)



      implicit none
      include 'param.def'

      integer, intent(in) :: n_atom, i_state, n_state      
      integer, intent(in) :: ntime, ntime_ele
      integer, intent(in) :: n_sav_stat, n_sav_traj
      integer, intent(in) :: qm_method, label_ZN
      integer, intent(inout) :: seed_random
      integer, intent(in) :: label_reject_hops
      double precision, intent(in) ::  hop_e      

      integer, intent(inout), dimension(n_state) :: md_state
      double precision, intent(inout) :: dtime   
     
     

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!  - Define local variables
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


      double precision, dimension(n_atom) ::   &
                                                      coor_x, &
                                                      coor_y, &
                                                      coor_z, &
                                                      old_coor_x, &
                                                      old_coor_y, &
                                                      old_coor_z, &
                                                      old_2_coor_x, &
                                                      old_2_coor_y, &
                                                      old_2_coor_z

      double precision, dimension(n_atom) ::   &
                                                      vel_x, &
                                                      vel_y, &
                                                      vel_z, &
                                                      old_vel_x, &
                                                      old_vel_y, &
                                                      old_vel_z, &
                                                      tmp_vel_x, &
                                                      tmp_vel_y, &
                                                      tmp_vel_z

      double precision, dimension(n_state, n_atom) ::   &
                                                gra_all_x, &
                                                gra_all_y, &
                                                gra_all_z, &
                                                old_gra_all_x, &
                                                old_gra_all_y, &
                                                old_gra_all_z, &
                                                old_2_gra_all_x, &
                                                old_2_gra_all_y, &
                                                old_2_gra_all_z

      double precision, dimension(n_state, n_state, n_atom) ::   &
                                                nac_x, &
                                                nac_y, &
                                                nac_z, &
                                                old_nac_x, &
                                                old_nac_y, &
                                                old_nac_z

      double precision, dimension(n_state) ::  pes_all,  &
                                                old_pes_all, &
                                                old_2_pes_all 

      double precision :: time, pes_ref, pes_current


      character*2, dimension(n_atom)  ::  atom_label



      integer :: file_save_energy, file_save_traj,  &
                  file_save_grad, &
                  file_save_vel, file_md_out, &
                  file_save_state, file_save_all, &
                  file_save_ele, file_save_pe, &
                  file_save_dipole

 

      integer :: i, j, it, it_tmp,i_state_kkr,j_state_kkr,label_kkr

      double precision, dimension(n_atom) ::   mass, charge
      integer :: input_numer

      double precision, dimension(n_atom) ::   gradient_x, &
                                                gradient_y, &
                                                gradient_z 


      complex (kind=8), dimension(n_state, n_state) :: rho 


      integer :: index_state, old_index_state, new_index_state


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      double precision :: tmp_mass, energy_gap
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
      write (file_md_out, *) "Run the surface hopping dynamics!"
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
     
      if (  label_reject_hops .eq. 0 ) then
            write (file_md_out, *) & 
            "Do not reject the hops with large energy gap"
      else
            write (file_md_out, *) &
          "Reject the hops when energy gap is larger than",hop_e,"(eV)"
      endif

9998  format( a, 10(i3,";")) 

      write (file_md_out, *) "--------------------------------------"  


      file_save_energy=24
      file_save_traj=25
      file_save_vel=26
      file_save_state=27
      file_save_all=28 
      file_save_ele=29
      file_save_pe=30
      file_save_dipole=31
      file_save_grad=32

      open(unit=file_save_energy, file="energy_time.out")
      open(unit=file_save_traj,   file="traj_time.out")
      open(unit=file_save_grad,   file="grad_time.out")
      open(unit=file_save_vel,    file="vel_time.out")
      open(unit=file_save_state,  file="current_state.out")
      open(unit=file_save_all,    file="hop_all_time.out")
      open(unit=file_save_ele,    file="ele_time.out")
      open(unit=file_save_pe,    file="pe_time.out")
      open(unit=file_save_dipole,    file="di_time.out")


!     Obttain the gradient and pes at time zero
      write (file_md_out, *) "Calculate the gradient"


      it=0
      time=0
      label_kkr=1

      write (file_md_out, *) "Time steps:", it
      write (*, *) "Time steps:", it

!     Read initial coordinates

      call sub_read_current_geom (n_atom, &
                               coor_x, coor_y, coor_z, &
                               vel_x, vel_y, vel_z, &
                               atom_label, &
                               n_state, &
                               rho, &
                               index_state, &
                               it, time )


      do i=1,n_atom
         tmp_label = atom_label(i)
         call sub_get_mass ( tmp_label, tmp_mass, tmp_charge)
         mass (i) = tmp_mass
         charge(i) = tmp_charge
      enddo

      nac_x = 0.d0
      nac_y = 0.d0
      nac_z = 0.d0

      call sub_many_ana_pes  (n_atom, &
                               n_state, md_state, &
                               atom_label, &
                               coor_x, coor_y, coor_z, &
                               label_ZN, &
                               label_kkr, &
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


!      Save the energy
       pes_current =  pes_all (index_state) 
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

      gradient_x (:) = gra_all_x (index_state,:)
      gradient_y (:) = gra_all_y (index_state,:)
      gradient_z (:) = gra_all_z (index_state,:)

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


      call sub_save_hopping_ana_nac (n_atom, n_state, md_state, &
                             it,time, &
                             index_state, &
                             pes_all, &
                             gra_all_x, &
                             gra_all_y, &
                             gra_all_z, &
                             nac_x, &
                             nac_y, &
                             nac_z, &
                             vel_x, vel_y, vel_z, &
                             rho, &
                             file_save_state, &
                             file_save_all )

!     Begin the propagation      
      do it_tmp=1, ntime
        it = it_tmp

        if (index_state .eq. 1) then
                exit
        endif

        if (it .eq. 1) then
          
          label_kkr = 1
          do i_state_kkr=1,n_state
             do j_state_kkr=1, n_state
                 if (j_state_kkr .ne. i_state_kkr) then
                    energy_gap =abs(pes_all(i_state_kkr)-pes_all(j_state_kkr))*27.2112
                    if(energy_gap .lt. 0.3) then
                       label_kkr = 0
                    endif
                 endif
             enddo
          enddo
         
          time = it*dtime

          old_pes_all = pes_all  

          old_gra_all_x = gra_all_x
          old_gra_all_y = gra_all_y
          old_gra_all_z = gra_all_z

          old_nac_x = nac_x
          old_nac_y = nac_y
          old_nac_z = nac_z


          old_vel_x = vel_x
          old_vel_y = vel_y
          old_vel_z = vel_z     

          old_coor_x = coor_x
          old_coor_y = coor_y
          old_coor_z = coor_z     

          gradient_x (:) = gra_all_x (index_state,:)
          gradient_y (:) = gra_all_y (index_state,:)
          gradient_z (:) = gra_all_z (index_state,:)

          call sub_newton_vel (n_atom, &
                      vel_x, vel_y, vel_z, &
                      gradient_x, &
                      gradient_y, &
                      gradient_z, &
                      mass, &
                      dtime )

          call sub_newton_coor (n_atom, &
                      coor_x, coor_y, coor_z, &
                      vel_x, vel_y, vel_z, &
                      dtime )

          call    sub_many_ana_pes  (n_atom, &
                               n_state, md_state, &
                               atom_label, &
                               coor_x, coor_y, coor_z, &
                               label_ZN, &
                               label_kkr, &
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

          
          gradient_x (:) = gra_all_x (index_state,:)
          gradient_y (:) = gra_all_y (index_state,:)
          gradient_z (:) = gra_all_z (index_state,:)


          call sub_newton_vel (n_atom, &
                      vel_x, vel_y, vel_z, &
                      gradient_x, &
                      gradient_y, &
                      gradient_z, &
                      mass, &
                      dtime )
        else

          it = it -1

          time = it*dtime

          label_kkr = 1
          do i_state_kkr=1,n_state
             do j_state_kkr=1, n_state
                 if (j_state_kkr .ne. i_state_kkr) then
                    energy_gap =abs(pes_all(i_state_kkr)-pes_all(j_state_kkr))*27.2112
                    if(energy_gap .lt. 0.3) then
                       label_kkr = 0
                    endif
                 endif
             enddo
          enddo

          write (file_md_out, *) "Time steps:", it
          write (*, *) "Time steps:", it

          old_2_pes_all = old_pes_all  

          old_2_gra_all_x = old_gra_all_x
          old_2_gra_all_y = old_gra_all_y
          old_2_gra_all_z = old_gra_all_z

          old_2_coor_x = old_coor_x
          old_2_coor_y = old_coor_y
          old_2_coor_z = old_coor_z     

          old_pes_all = pes_all  

          old_gra_all_x = gra_all_x
          old_gra_all_y = gra_all_y
          old_gra_all_z = gra_all_z

          old_nac_x = nac_x
          old_nac_y = nac_y
          old_nac_z = nac_z


          old_vel_x = vel_x
          old_vel_y = vel_y
          old_vel_z = vel_z     

          tmp_vel_x = old_vel_x
          tmp_vel_y = old_vel_y
          tmp_vel_z = old_vel_z

          old_coor_x = coor_x
          old_coor_y = coor_y
          old_coor_z = coor_z     

          gradient_x (:) = gra_all_x (index_state,:)
          gradient_y (:) = gra_all_y (index_state,:)
          gradient_z (:) = gra_all_z (index_state,:)

          call sub_newton_vel (n_atom, &
                      vel_x, vel_y, vel_z, &
                      gradient_x, &
                      gradient_y, &
                      gradient_z, &
                      mass, &
                      dtime )

          call sub_newton_coor (n_atom, &
                      coor_x, coor_y, coor_z, &
                      vel_x, vel_y, vel_z, &
                      dtime )

          call sub_many_ana_pes  (n_atom, &
                               n_state, md_state, &
                               atom_label, &
                               coor_x, coor_y, coor_z, &
                               label_ZN, &
                               label_kkr, &
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

          pes_current =  pes_all (index_state)

          
!         Propagate the velocity half time step dt/2
          gradient_x (:) = gra_all_x (index_state,:)
          gradient_y (:) = gra_all_y (index_state,:)
          gradient_z (:) = gra_all_z (index_state,:)


          call sub_newton_vel (n_atom, &
                      vel_x, vel_y, vel_z, &
                      gradient_x, &
                      gradient_y, &
                      gradient_z, &
                      mass, &
                      dtime )

          old_index_state = index_state

          call     sub_zn_hopping   (n_atom, &
                                      mass, &
                                      atom_label, &
                                      label_ZN, &
                                      label_reject_hops, &
                                      hop_e, &
                                      time, &
                                      it, &
                                      dtime, &
                                      n_state, &
                                      md_state, &
                                      index_state, &
                                      ntime_ele, &
                                      pes_all, &
                                      old_pes_all, &
                                      old_2_Pes_all, &
                                      coor_x, &
                                      coor_y, &
                                      coor_z, &
                                      old_coor_x, &
                                      old_coor_y, &
                                      old_coor_z, &
                                      old_2_coor_x, &
                                      old_2_coor_y, &
                                      old_2_coor_z, &
                                      old_vel_x, &
                                      old_vel_y, &
                                      old_vel_z, &
                                      gra_all_x, &
                                      gra_all_y, &
                                      gra_all_z, &
                                      old_gra_all_x, &
                                      old_gra_all_y, &
                                      old_gra_all_z, &
                                      old_2_gra_all_x, &
                                      old_2_gra_all_y, &
                                      old_2_gra_all_z, &
                                      old_nac_x, &
                                      old_nac_y, &
                                      old_nac_z, &
                                      seed_random, &
                                      file_save_ele,&
                                      file_md_out)
                   

          new_index_state = index_state

          if (old_index_state .ne. new_index_state) then

               index_state = new_index_state

               write (file_md_out, *)  "Real hop happens at Step", &
                                       it
               write (file_md_out, *)  md_state(old_index_state), &
                                       "-->", &
                                       md_state(new_index_state)
               write (file_md_out, *)  "Time(fs), energy gap (au)", &
                      time*TOFS,                                    &
                      old_pes_all(old_index_state)-old_pes_all(new_index_state)


              gra_all_x = old_gra_all_x
              gra_all_y = old_gra_all_y
              gra_all_z = old_gra_all_z

              nac_x = old_nac_x
              nac_y = old_nac_y
              nac_z = old_nac_z

              pes_all = old_pes_all
              
              coor_x = old_coor_x
              coor_y = old_coor_y
              coor_z = old_coor_z

              vel_x = old_vel_x
              vel_y = old_vel_y
              vel_z = old_vel_z

              gradient_x (:) = gra_all_x (index_state,:)
              gradient_y (:) = gra_all_y (index_state,:)
              gradient_z (:) = gra_all_z (index_state,:)

              call sub_newton_vel (n_atom, &
                          vel_x, vel_y, vel_z, &
                          gradient_x, &
                          gradient_y, &
                          gradient_z, &
                          mass, &
                          dtime )


              call sub_newton_coor (n_atom, &
                          coor_x, coor_y, coor_z, &
                          vel_x, vel_y, vel_z, &
                          dtime )



              call    sub_many_ana_pes  (n_atom, &
                                   n_state, md_state, &
                                   atom_label, &
                                   coor_x, coor_y, coor_z, &
                                   label_ZN, &
                                   label_kkr, &
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


              gradient_x (:) = gra_all_x (index_state,:)
              gradient_y (:) = gra_all_y (index_state,:)
              gradient_z (:) = gra_all_z (index_state,:)


              call sub_newton_vel (n_atom, &
                          vel_x, vel_y, vel_z, &
                          gradient_x, &
                          gradient_y, &
                          gradient_z, &
                          mass, &
                          dtime )
        endif


!       save restart file
          call sub_save_restart (n_atom, &
              old_coor_x, old_coor_y, old_coor_z, &
              old_vel_x, old_vel_y, old_vel_z, &
              atom_label, &
              n_state, &
              rho, &
              index_state, &
              it, time)


          call sub_save_hopping_ana_nac (n_atom, n_state, md_state, &
                              it,time, &
                              index_state, &
                              old_pes_all, &
                              old_gra_all_x, &
                              old_gra_all_y, &
                              old_gra_all_z, &
                              old_nac_x, &
                              old_nac_y, &
                              old_nac_z, &
                              old_vel_x, old_vel_y, old_vel_z, &
                              rho, &
                              file_save_state, &
                              file_save_all &
                               )

          call sub_save_pe (  it,time, &
                              n_state, &
                              index_state, &
                              old_pes_all, &
                              file_save_pe )


!!!       Save the current geometry and velocity
          call  sub_write_current_geom (n_atom, &
                                old_coor_x, old_coor_y, old_coor_z, &
                                old_vel_x, old_vel_y, old_vel_z, &
                                atom_label, &
                                n_state, &
                                rho, &
                                index_state, &
                                it, time )


!!!!!!    Save the energy
          if (  mod(it, n_sav_stat) .eq. 0 ) then

             pes_current =  old_pes_all (index_state) 
             call sub_save_energy ( n_atom, &
                               pes_current, &
                               old_vel_x, old_vel_y, old_vel_z, &
                               mass, &
                               it,time, &
                               file_save_energy )

          endif




!!!!!     Save the trajectory
          if ( mod(it, n_sav_traj) .eq. 0 ) then
             call sub_save_traj ( n_atom, &
                               old_coor_x, old_coor_y, old_coor_z, &
                               old_vel_x, old_vel_y, old_vel_z, &
                               atom_label, &
                               it, time, &
                               file_save_traj, file_save_vel )
          endif


!!!!!     Save the gradient
          if ( mod(it, n_sav_traj) .eq. 0 ) then
             call sub_save_grad (n_atom, n_state, index_state, &
                                   old_gra_all_x, &
                                   old_gra_all_y, &
                                   old_gra_all_z, &
                                   atom_label, &
                                   it, time, &
                                   file_save_grad )

          endif
        endif
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

9999  format (i10,10(f24.14,1x) )

      return
 
      end 
