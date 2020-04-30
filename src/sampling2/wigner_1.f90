      subroutine   displacement_wigner_1 (label_method, &
                                          n_geom, &
                                          file_random_gau, &
                                          n_atom, &
                                          atom_label, &
                                          coor_x, coor_y, coor_z, &
                                          n_mode, &
                                          frequency, &
                                          coor_vib, &
                                          freeze_or_not, &
                                          file_x_Q, &
                                          file_v_V_au, &
                                          file_x_Q_au, &
                                          file_p_P_au, &
                                          file_stat_q)


      implicit none
!     include parameters
      include "param.def"     

!     Define the input and output variables
      integer, intent(in) :: label_method, n_geom, &
                             file_random_gau, &
                             n_atom, n_mode, &
                             file_x_Q, file_v_V_au, &
                             file_x_Q_au, file_p_P_au, &
                             file_stat_q

      double precision, intent(in), dimension(n_atom)  :: &
                                                    coor_x, &
                                                    coor_y, &
                                                    coor_z

      double precision, intent(in ), dimension(n_mode,3*n_atom)  :: &
                                                    coor_vib

      character*2, intent(in), dimension(n_atom)   :: & 
                                                    atom_label

      double precision, intent(in), dimension(n_mode) :: &
                                                    frequency
     
      integer, intent (in), dimension(n_mode)  ::  freeze_or_not
 

!     Local variables
      integer :: i, j, k      
      double precision, allocatable, dimension (:,:) :: Q_normal 
      double precision, allocatable, dimension (:,:) :: Q_xyz
      double precision, allocatable, dimension (:)   :: x, &
                                                        y, &
                                                        z
      double precision, allocatable, dimension (:,:) :: P_normal
      double precision, allocatable, dimension (:,:) :: p_xyz
      double precision, allocatable, dimension (:)   :: px, &
                                                        py, &
                                                        pz


      double precision, allocatable, dimension (:,:) :: v_normal
      double precision, allocatable, dimension (:,:) :: v_xyz
      double precision, allocatable, dimension (:)   :: vx, &
                                                        vy, &
                                                        vz


      double precision, allocatable, dimension (:,:) ::  &
                                                potential_energy, &
                                                kinetic_energy

      double precision,  allocatable, dimension (:)   :: average_pe

      double precision  ::  sum_pe, sum_pe_all
   
      double precision, allocatable, dimension (:) :: atom_mass      

      character*2 :: atom_label_tmp
      double precision  :: atom_mass_tmp
       
      
       
      allocate (Q_normal(1,n_mode))
      allocate (Q_xyz(1,3*n_atom))
      allocate (x(n_atom))
      allocate (y(n_atom))
      allocate (z(n_atom))


      allocate (P_normal(1,n_mode))
      allocate (p_xyz(1,3*n_atom))
      allocate (px(n_atom))
      allocate (py(n_atom))
      allocate (pz(n_atom))

      allocate (atom_mass(n_atom))

      allocate (v_normal(1,n_mode))
      allocate (v_xyz(1,3*n_atom))
      allocate (vx(n_atom))
      allocate (vy(n_atom))
      allocate (vz(n_atom))


      allocate (potential_energy(n_geom, n_mode))
      allocate (kinetic_energy(n_geom, n_mode))
      allocate (average_pe(n_mode))
      
 

!    Generate P and Q from wigner distribution funcion.
!    Read all random numbrs


       read (file_random_gau,*)
   
       do i=1, n_geom
         
         Q_normal = 0.0
         P_normal = 0.0

!  ------------ Read the P and Q
         do j=1, n_mode 
         read (file_random_gau,*) Q_normal(1,j), &
                                  P_normal(1,j)
         enddo

!  ----------------------------------------------------------
!  ----------------If some modes j are frozen, ----------------
! ---------------- set Q_normal(1,j) =0 ---------------------- 
! ------------------------------------------------------------- 
                   
         do j=1, n_mode
         if (freeze_or_not(j)  .eq. 1 ) then
         Q_normal(1,j) =0
         endif
         enddo




!  ----------  Calculate the potential energy ------------
         do j=1, n_mode 
!         print *, frequency(j), Q_normal(1,j)
         potential_energy(i, j) = 0.5 * &
                                  frequency(j) * &
                                  Q_normal(1,j)**2         
         enddo



! --------    Q -> x
         Q_xyz = MATMUL (Q_normal, coor_vib)
         do k=1, n_atom
               x(k) = coor_x(k) + Q_xyz(1, 3*(k-1)+1)
               y(k) = coor_y(k) + Q_xyz(1, 3*(k-1)+2)
               z(k) = coor_z(k) + Q_xyz(1, 3*(k-1)+3)
         enddo



         write (file_x_Q_au,*) n_atom
         write (file_x_Q_au,*) "Geom", i

          
         write (file_x_Q,*) n_atom
         write (file_x_Q,*) "Geom", i



         do k=1, n_atom
         write (file_x_Q_au,7777) atom_label(k), &
                                  x(k), y(k), z(k)

         write (file_x_Q,7777) atom_label(k), &
                         x(k)*BOHRTOANG, &
                         y(k)*BOHRTOANG, &
                         z(k)*BOHRTOANG

         enddo

! --------    P -> p     



         do k=1, n_atom
         atom_label_tmp = atom_label(k)
         call label_to_mass (atom_label_tmp, atom_mass_tmp)
         atom_mass(k) = atom_mass_tmp 
         enddo


!  ----------------------------------------------------------
!  ----------------If some modes j are frozen, ----------------
! ---------------- set P_normal(1,j) =0 ----------------------
! -------------------------------------------------------------

        

         do j=1, n_mode
         if (freeze_or_not(j)  .eq. 1 ) then
         P_normal(1,j) =0
         endif
         enddo


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!------------------------------------------------------------
!--------  Test purpose --------------------------------

!-------   P_normal(1,:)=-1 ------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



!  ----------  Calculate the kinetic energy ------------
         do j=1, n_mode
!         print *, frequency(j), Q_normal(1,j)
         kinetic_energy(i, j) = 0.5 * &
                                  frequency(j) * &
                                  P_normal(1,j)**2
         enddo




         
         do j=1, n_mode        
         v_normal(1, j) = P_normal (1, j) * &
                          (frequency(j)/TOCM)
         enddo


         
         v_xyz = MATMUL (v_normal, coor_vib)
         do k=1, n_atom
               vx(k) =  v_xyz(1, 3*(k-1)+1)
               vy(k) =  v_xyz(1, 3*(k-1)+2)
               vz(k) =  v_xyz(1, 3*(k-1)+3)
         enddo
       
          do k=1, n_atom
               px(k) = vx(k)*atom_mass(k)*ATOMMASS   
               py(k) = vy(k)*atom_mass(k)*ATOMMASS
               pz(k) = vz(k)*atom_mass(k)*ATOMMASS
         enddo


         write (file_v_V_au,*)  n_atom
         write (file_v_V_au,*) "Momenta", i

         write (file_p_P_au,*)  n_atom
         write (file_p_P_au,*) "Momenta", i
        
         do k=1, n_atom
         write (file_v_V_au,7777) atom_label(k), &
                                  vx(k), vy(k), vz(k)
         write (file_p_P_au,7777) atom_label(k), &
                         px(k), &
                         py(k), &
                         pz(k)
         enddo

       enddo
 

7777  format (a, 1x, 3(f20.10, 2x)  )




!----------------   The average potential energy  for each mode

       write (*,*) "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
       write (*,*) "The average energy for v=0 "
        write (*,*) "This energy should be half of sum of &
                     all frequencies over all modes!"
       write (*,*)
       write (*,*)  "The eigenenergy of v=0 (cm-1)" , &
                     0.5*sum(frequency)
       write (*,*)  "The kinetic energy of v=0 (cm-1)" , &
                     0.5*sum(frequency)/2
       write (*,*)  "The kinetic energy of v=0 (eV)" , &
                     0.5*sum(frequency)/2 *TOEV/TOCM



       write (*,*)
       write (*,*)  "Warning: please note that the energya &
                     of v=0 here should be DIFFERENT to "
       write (*,*)  "the below average kinetic and potential &
                     energy by counting all &
                     modes  &
                     if some modes are frozen !!!!!!!!!"





      
       write (*,*) "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
       write (*,*) "The average potential energy in &
                     dimensionaless normal coordinates"
       write (*,*) 
       
      do j=1, n_mode

       average_pe(j)=0.0
       sum_pe=0.0      

       do i=1, n_geom
       sum_pe= sum_pe + potential_energy(i, j)
       enddo 

       average_pe(j) = sum_pe / n_geom        
       write (*,*)  "Mode", j 
       write (*,*)  "Frequency", frequency(j)
       write (*,*)  "Average potential energy (cm-1)", average_pe(j)
       write (*,*)  "Average potential energy (eV)", &
                     average_pe(j)/TOCM*TOEV

      enddo  

! ---------- The average potential energy for all modes

       sum_pe_all=0.0  

       do i=1, n_geom
       do j=1, n_mode
       sum_pe_all = sum_pe_all + potential_energy(i, j)
       enddo
       enddo

       write (*,*)  
       write (*,*)  "Average potential energy for all modes (cm-1)", &
                     sum_pe_all / (n_geom)
       write (*,*)  "Average potential energy for all modes (eV)", &
                     sum_pe_all / (n_geom) /TOCM*TOEV
       write (*,*)




       write (*,*) "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
       write (*,*) "The average kinetic energy in &
                     dimensionaless normal coordinates"
       write (*,*) 

      do j=1, n_mode

       average_pe(j)=0.0
       sum_pe=0.0

       do i=1, n_geom
       sum_pe= sum_pe + kinetic_energy(i, j)
       enddo

       average_pe(j) = sum_pe / n_geom
       write (*,*)  "Mode", j
       write (*,*)  "Frequency", frequency(j)
       write (*,*)  "Average kinetic energy (cm-1)", average_pe(j)
       write (*,*)  "Average kinetic energy (eV)", &
                     average_pe(j)/TOCM*TOEV

      enddo

! ---------- The average kinetic energy for all modes

       sum_pe_all=0.0

       do i=1, n_geom
       do j=1, n_mode
       sum_pe_all = sum_pe_all + kinetic_energy(i, j)
       enddo
       enddo

       write (*,*)
       write (*,*)  "Average kinetic energy for all modes (cm-1)", &
                     sum_pe_all / (n_geom)
       write (*,*)  "Average kinetic energy for all modes (eV)", &
                     sum_pe_all / (n_geom) /TOCM*TOEV
       write (*,*)



       write (*,*) "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
       write (*,*) "The average total energy in &
                     dimensionaless normal coordinates"
       write (*,*)

      do j=1, n_mode

       average_pe(j)=0.0
       sum_pe=0.0

       do i=1, n_geom
         sum_pe= sum_pe + kinetic_energy(i, j) +  potential_energy(i, j)
       enddo

       average_pe(j) = sum_pe / n_geom
       write (*,*)  "Mode", j
       write (*,*)  "Frequency", frequency(j)
       write (*,*)  "Average total energy (cm-1)", average_pe(j)
       write (*,*)  "Average total energy (eV)", &
                     average_pe(j)/TOCM*TOEV
       write (*,*)  "Ratio: (Energy_mode / Frequency) ", &
                     average_pe(j) / frequency(j)

      enddo





      deallocate (Q_normal)
      deallocate (Q_xyz)
      deallocate (x)
      deallocate (y)
      deallocate (z)


      deallocate (P_normal)
      deallocate (P_xyz)
      deallocate (px)
      deallocate (py)
      deallocate (pz)

      deallocate (v_normal)
      deallocate (v_xyz)
      deallocate (vx)
      deallocate (vy)
      deallocate (vz)



      deallocate (atom_mass)
      deallocate (potential_energy)
      deallocate (kinetic_energy)
      deallocate (average_pe)
      return 


      

        
       end subroutine displacement_wigner_1
       


