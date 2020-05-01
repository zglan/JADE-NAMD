       Program main

   
       implicit none
!      Include all parameters
       include 'param.def'


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        integer :: label_random, label_displacement, &
                   label_dis_wigner, label_read_vib, &
                   label_method, label_frozen, label_es_output

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!! Define all important variables for the generation of the
!!     random numbers from a two-dimensional Gaussian distribution. 
!      Define all input and output file
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
       integer :: nr, nbin, i_col
       integer :: file_dis1d_random1, file_dis1d_random2, &
                  file_dis2d_random
       integer :: file_random_gau, file_random_uni                  

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!       
!!!!!!!!-- Define all variables to read the normal modes----
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
      integer :: n_atom, n_mode
      double precision, allocatable, dimension(:) ::  frequency, &
                                                      mass_mode
      double precision, allocatable, dimension(:) ::  coor_x, &
                                                      coor_y, &
                                                      coor_z
      double precision, allocatable, dimension(:,:) ::  coor_vib
      character*2, allocatable, dimension(:)      ::  atom_label
      integer ::  file_molden, file_q_vib
      character*100 :: filename_es_output
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1a
!      Generate the normal mode from -1 to 1
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

       integer :: file_stru_au, file_stru_ang




!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!-- Define all variables to generate the (X,P) from wigner distribution----
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        integer :: n_geom
        integer :: file_x_Q 
        integer :: file_v_V_au, file_x_Q_au, file_p_P_au
        integer :: file_stat_q





!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!  ---------------- Define the list of frozen normal mode ------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        integer :: number_frozen
        integer, allocatable, dimension(:) :: list_frozen
        integer, allocatable, dimension(:) :: frozen_or_not
        integer :: frozen_mode     

!       Define the local variables
        integer :: i


        read (*,*) n_atom
        read (*,*) n_mode
 
        read (*,*)
        read (*,*) label_random
        read (*,*) nr      
        read (*,*) nbin

        read (*,*)
        read (*,*)  label_read_vib
        read (*,*)  label_es_output
        read (*,*)  filename_es_output


        read (*,*)
        read (*,*) label_displacement

        read (*,*)
        read (*,*) label_dis_wigner
        read (*,*) n_geom
        read (*,*) label_method

        read (*,*) 
        read (*,*) label_frozen
        read (*,*) number_frozen
        allocate( list_frozen (number_frozen) )
        read (*,*) list_frozen(:)


       allocate ( frequency(n_mode) )
       allocate ( mass_mode(n_mode) )
       allocate ( coor_x(n_atom)    )
       allocate ( coor_y(n_atom)    )
       allocate ( coor_z(n_atom)    )
       allocate ( coor_vib(n_mode,3*n_atom))
       allocate ( atom_label(n_atom))
       allocate ( frozen_or_not(n_mode) ) 


       





!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111
!      Generate two sets of ramdom number from Gaussian distribution 
!      W(P,Q) = 1/ Pi (- (X**2+P**2) )
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

       if ( label_random .eq. 1 ) then
          
          file_random_gau=30
          file_random_uni=31

          file_dis1d_random1=40
          file_dis1d_random2=41
          file_dis2d_random=42

          write (*,*) "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
          write (*,*) "---------------------------------------"
          write (*,*) "Generate two sets of random &
                       numbers from 2D Gaussian distribution "
          open(unit=file_random_gau, file="random_gau.dat")
          open(unit=file_random_uni, file="random_uni.dat")
          call random_gaussian_2d  (nr, &
                                    file_random_gau, &
                                    file_random_uni)
          close(file_random_gau)
          close(file_random_uni)

          
          write (*,*) "---------------------------------------"

          write (*,*) "Check two sets of random &
                       numbers"
          open(unit=file_random_gau, file="random_gau.dat")
          open(unit=file_dis1d_random1, file="dis1d_random1.dat")
          i_col=1
          call check_random_1d (file_random_gau, &
                                nr, &
                                nbin, &
                                i_col, &
                                file_dis1d_random1)
          close(file_random_gau)
          close(file_dis1d_random1) 
               


          open(unit=file_random_gau, file="random_gau.dat")
          open(unit=file_dis1d_random2, file="dis1d_random2.dat")
          i_col=2
          call check_random_1d (file_random_gau, &
                                nr, &
                                nbin, &
                                i_col, &
                                file_dis1d_random2)
          close(file_random_gau)
          close(file_dis1d_random2)

        
          open(unit=file_random_gau, file="random_gau.dat")
          open(unit=file_dis2d_random, file="dis2d_random.dat")
          call check_random_2d (file_random_gau, &
                                nr, &
                                nbin, &
                                file_dis2d_random)
          close(file_random_gau)
          close(file_dis2d_random)
          write (*,*) "---------------------------------------"

       endif


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!   --------Read the normal mode
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!      -------Please note that the normal mode has mass for Gaussian output--------
!      -------- For MNDO, this term is not defined, therefore I set to one---
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
      
       if (label_read_vib .eq. 1) then

          write (*,*) ""
          write (*,*) "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
          write (*,*) "----------------------------------------"
          write (*,*) "The number of atoms", n_atom
          write (*,*) "The number of normal modes", n_mode
          write (*,*) "----------------------------------------"
          do i=1, n_mode
             mass_mode(i)=1
          enddo
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!   --------- Read the normal mode ----------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          write (*,*) "Begin to read the normal modes"
          file_molden=50
          call  read_normal_mode2 (n_atom, atom_label, &
                                  coor_x, coor_y, coor_z, &
                                  n_mode, frequency, mass_mode, &
                                  coor_vib, &
                                  label_es_output,  &
                                  filename_es_output,  &
                                  file_molden)
          write (*,*) "End to read the normal modes"


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!  -------- Change to dimensionaless normal coordinates------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          write (*,*) "----------------------------------------"


          write (*,*) "Construct dimensionless normal coordinates"
          file_q_vib=60
          open(unit=file_q_vib, file="Q_v.dat")
          call   dimensionless_mode (n_atom, &
                                     atom_label, &
                                     coor_x, coor_y, coor_z, &
                                     n_mode, &
                                     frequency, &
                                     mass_mode, &
                                     coor_vib, &
                                     file_Q_vib  )
          close(file_q_vib)
       
          write (*,*) "----------------------------------------"

        endif

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!  -------- Make the displacement along the dimensionaless normal coordinates
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!   --------- Make the displacement by hand --------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1


        if (label_displacement .eq. 1) then


          write (*,*) ""
          write (*,*) "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
          write (*,*) "----------------------------------------"


            
            file_stru_au=70
            file_stru_ang=71  
            open(unit=file_stru_au, file="stru_au.dat")
            open(unit=file_stru_ang, file="stru_ang.dat")

            write (*,*) "Make the displacements along all mode -2<Q<2"
            call  displacement_hand (n_atom, &
                                     atom_label, &
                                     coor_x, coor_y, coor_z, &
                                     n_mode, &
                                     frequency, &
                                     coor_vib, &
                                     file_stru_au, &
                                     file_stru_ang )
          close(file_stru_au)
          close(file_stru_ang)

          write (*,*) "----------------------------------------"
        endif

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!   --------- Make the displacement from Winger distribution --------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1







!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!--------------- Check whether we need to freeze some mode ----
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


          frozen_or_not(:)=0

          if (label_frozen .eq. 1 ) then
          do i=1, number_frozen
          frozen_mode=   list_frozen (i)  
          frozen_or_not(frozen_mode)  = 1 
          enddo
          endif



!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!   --------- Generate x and p from Method 1--------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1


         write (*,*)
         write (*,*)  
         write (*,*) "----------------------------------------"
         write (*,*) "Make the displacements of Q and P from  &
                       Wigner distributions"
        


        if (   (label_dis_wigner .eq. 1)  &
               .and. &
               (label_method .eq. 1)    &
           ) then


          write (*,*) ""
          write (*,*) "----------------------------------------"
          
          if (label_frozen .eq. 0) then
          write (*,*)  "No mode is frozen"
          endif

          if (label_frozen .eq. 1) then
          write (*,*)  "The following modes are frozen"
          do i=1, number_frozen
          write (*,*)  "Mode, ", list_frozen (i)
          enddo
          endif 

          write (*,*) "----------------------------------------"

          if ( (n_mode*n_geom) .gt. nr  ) then
          write (*,*) "ERROR MESSAGES"
          write (*,*) "PLEASE GENERATE MORE RANDOM NUMBERS !!!!!!!!"
          stop
          endif         
          
          
          
          file_random_gau=30
          file_x_Q=80
          file_v_V_au=81
          file_x_Q_au=82
          file_p_P_au=83
          file_stat_q=84
          open(unit=file_random_gau, file="random_gau.dat")
          open(unit=file_x_Q, file="x_Q_ang.dat")
          open(unit=file_v_V_au, file="v_V_au.dat")
          open(unit=file_x_Q_au, file="x_Q_au.dat")
          open(unit=file_p_P_au, file="p_P_au.dat")
          open(unit=file_stat_q, file="stat_Q.dat")
          call  displacement_wigner_1 (label_method, &
                                       n_geom, &
                                       file_random_gau, &
                                       n_atom, &
                                       atom_label, &
                                       coor_x, coor_y, coor_z, &
                                       n_mode, &
                                       frequency, &
                                       coor_vib, &
                                       frozen_or_not, &
                                       file_x_Q, &
                                       file_v_V_au, &
                                       file_x_Q_au, &
                                       file_p_P_au, &
                                       file_stat_q)
                                       
          close(file_random_gau)
          close(file_x_Q)
          close(file_v_V_au)
          close(file_x_Q_au)
          close(file_p_P_au)
          close(file_stat_q) 


          open(unit=file_v_V_au, file="v_V_au.dat")
          open(unit=file_p_P_au, file="p_P_au.dat")          
          call check_kinetic   (n_geom, &
                                n_atom, &
                                file_v_V_au, &
                                file_p_P_au )
          close(file_v_V_au)
          close(file_p_P_au)

          write (*,*) "----------------------------------------"

       endif




!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!   --------- Generate x and p from Method 2  --------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1


       if (   (label_dis_wigner .eq. 1)  &
               .and. &
               (label_method .eq. 2)   &
           ) then


          if ( (n_mode*n_geom) .gt. nr  ) then
          write (*,*) "Please generate more random numbers"
          stop
          endif


          write (*,*) "Make the displacements of Q &
                       from Wigner functons.       &
                       P is generate from T=E-V."

          file_random_gau=30
          file_x_Q=80
          file_v_V_au=81
          file_x_Q_au=82
          file_p_P_au=83
          file_stat_q=84
          open(unit=file_random_gau, file="random_gau.dat")
          open(unit=file_x_Q, file="x_Q_ang.dat")
          open(unit=file_v_V_au, file="v_V_au.dat")
          open(unit=file_x_Q_au, file="x_Q_au.dat")
          open(unit=file_p_P_au, file="p_P_au.dat")
          open(unit=file_stat_q, file="stat_Q.dat")
!          call  displacement_wigner_2 (label_method, &
!                                       n_geom
!                                       file_random_gau, &
!                                       n_atom, &
!                                       atom_label, &
!                                       coor_x, coor_y, coor_z, &
!                                       n_mode, &
!                                       frequency, &
!                                       coor_vib,
!                                       file_x_Q,
!                                       file_p_P,
!                                       file_x_Q_au,
!                                       file_p_P_au)

          close(file_random_gau)
          close(file_x_Q)
          close(file_v_V_au)
          close(file_x_Q_au)
          close(file_p_P_au)
          close(file_stat_q)
       endif





       
       deallocate ( frequency)
       deallocate ( coor_x   )
       deallocate ( coor_y   )
       deallocate ( coor_z   )
       deallocate ( coor_vib )
       deallocate ( atom_label)

!       return
 
       end 
