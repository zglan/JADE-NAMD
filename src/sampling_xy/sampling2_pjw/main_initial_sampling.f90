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
           

!!!!!!!!!!!!!!!!!!!!!!! by hudp !!!!!!!!!!!!!!!!!!!!!!
integer :: file_freq_input
!!!!!!!!!!!!!!!!!!!!!!! end !!!!!!!!!!!!!!!!!!!!!!!!!!       


integer :: file_random_gau, file_random_uni                  

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!       
!!!!!!!!-- Define all variables to read the normal modes----
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
      integer :: n_atom, n_mode
      double precision, allocatable, dimension(:) ::  frequency, &
                                               mass_mode
      double precision, allocatable, dimension(:) ::  ex_vib
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
 integer :: number_frozen, number_negative
 integer, allocatable, dimension(:) :: list_frozen
 integer, allocatable, dimension(:) :: frozen_or_not
 integer :: frozen_mode     

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!-------------- T-K temperature
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
 double precision  :: t_k

!       Define the local variables
 integer :: i, i_mode, level, excitation_list


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

 read (*,*)
 read (*,*) n_geom
 read (*,*) label_method

 if ( label_method .eq. 1 ) then
     t_k = 0
 endif
 if ( label_method .eq. 2 &
 .or. &
 label_method .eq. 11 ) then ! yxie. wigner, just generate x and p of each mode with freq input
     read (*,*) t_k            
 endif
  
 allocate(ex_vib(n_mode))
 ex_vib(:) = 0         
 if ( label_method .eq. 3 ) then
     t_k = 0
 endif
 if ( label_method .eq. 4 ) then
     read (*,*) t_k
 endif
 if ( label_method .eq. 5 ) then
     read (*,*) excitation_list
     do i = 1 , excitation_list 
        read (*,*) i_mode, level
        ex_vib (i_mode) = level
     enddo
 endif
 if ( label_method .eq. 6) then
     read (*,*) t_k
 endif


 if ( label_method .eq. 10 ) then
     read (*,*) t_k
     read (*,*) number_negative
 endif
!        if ( label_method .eq. 11 ) then
!            read (*,*) t_k
!        endif

 read (*,*) 
 read (*,*) label_frozen
 if (  label_frozen  .ne. 0 ) then
    read (*,*) number_frozen
    allocate( list_frozen (number_frozen) )
    read (*,*) list_frozen(:)
 endif



allocate ( frequency(n_mode) )
allocate ( mass_mode(n_mode) )
allocate ( coor_x(n_atom)    )
allocate ( coor_y(n_atom)    )
allocate ( coor_z(n_atom)    )
allocate ( coor_vib(n_mode,3*n_atom))
allocate ( atom_label(n_atom))
allocate ( frozen_or_not(n_mode) ) 


write (*,*)  "n_atom =", n_atom             
write (*,*)  "n_mode =", n_mode                
write (*,*)  "label_random=", label_random
write (*,*)  "nr=", nr                  
write (*,*)  "nbin=", nbin
write (*,*)  "label_read_vib=", label_read_vib
write (*,*)  "label_es_output=", label_es_output 
write (*,*)  "filename_es_output=", filename_es_output
write (*,*)  "label_displacement=", label_displacement 
write (*,*)  "label_dis_wigner=",   label_dis_wigner
write (*,*)  "n_geom=", n_geom
write (*,*)  "label_method=", label_method
write (*,*)  "t_k", t_k
write (*,*)  "label_frozen=", label_frozen 
write (*,*)  "number_frozen=", number_frozen 
write (*,*)  "list_frozen=",  list_frozen 



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

!         Reversed the sign of frequency for the mode responsible for the reaction coordinate
!         in the transition state sampling.

   if ( label_method .ge. 10 ) then
       do i=1, number_negative
          frequency(i) = abs(frequency(i))
       enddo
   endif  





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

!!!!!!!!!!!!!!!!!!!    by hudp   !!!!!!!!!!!!!!!!!!!!!!!!
if (label_read_vib .eq. 2) then
   file_freq_input=61
   open(unit=file_freq_input, file="freq_sam.input")
   do i_mode = 1 , n_mode
       read (file_freq_input,*) frequency(i_mode)
       frequency(i_mode)=frequency(i_mode)/TOEV
   enddo
   close(file_freq_input)
endif
!!!!!!!!!!!!!!!!!!    End        !!!!!!!!!!!!!!!!!!!!!!!!







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




!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111
!     Check whether the random number genaration is needed!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

if ( label_random .eq. 1 ) then
   
   file_random_gau=30
   file_random_uni=31

   file_dis1d_random1=40
   file_dis1d_random2=41
   file_dis2d_random=42
 
endif

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





 write (*,*)
 write (*,*)  
 write (*,*) "----------------------------------------"
 write (*,*) "Make the displacements of Q and P"
 write (*,*) "----------------------------------------"

!   Lable_method = 1 
!   Wigner sampling for T=0, V=0

!   Label_method = 2
!   Wigner sampling for T


 if ( (label_method .eq. 1)  &
      .OR.                       &
      (label_method .eq. 2)  &
      .OR.                       &
      (label_method .eq. 11)  &
    )  then                    

      write (*,*)
      write (*,*)  
      write (*,*) "----------------------------------------"
      write (*,*) "Make the displacements of Q and P from  &
                     Wigner distributions"
      write (*,*) "----------------------------------------"
      write (*,*) "Standard Wigner distribution function"
      write (*,*) "Temperature is", T_k
 endif



!   label_method = 3 
!   Sampling by Mueller and Stock
!   T=0
!   label_method = 4
!   Sampling by Mueller and Stock
!   T_k 
!   < V > =  1/ ( exp ( omega/(KB*t_k*TOCM) ) -1    )
!   label_method =5 
!   Sampling by Mueller and Stock
!   V = input
!   label_method = 6 
!   Sampling by Mueller and Stock
!   P_v <- Bolzmann distribution


 if ( (label_method .eq. 3)  &
      .OR.                       &
      (label_method .eq. 4)  &
    )  then                     

      write (*,*)
      write (*,*)
      write (*,*) "----------------------------------------"
      write (*,*) "Make the displacements of Q and P from  &
                   the method by Mueller and Stock!"

      write (*,*) ""
      write (*,*) "----------------------------------------"
      write (*,*) "Temperature is", T_k
 endif
 
 if (label_method .eq. 5)    then       
      write (*,*)
      write (*,*)
      write (*,*) "----------------------------------------"
      write (*,*) "Make the displacements of Q and P from  &
                   the method by Mueller and Stock!"

      write (*,*) ""
      write (*,*) "----------------------------------------"
      write (*,*) "The list of vibrational excitation"
      write (*,*) "Mode   |  Level "
      do i_mode = 1 , n_mode
         write (*,*) i_mode, ex_vib
      enddo
      write (*,*)  "--------------------------------------"
 endif


 if (label_method .eq. 6)    then
      write (*,*)
      write (*,*)
      write (*,*) "----------------------------------------"
      write (*,*) "Make the displacements of Q and P  &
                   from the method by Mueller and Stock!  "
      write (*,*) "P_v is generated from Bolzmann distribution"
      write (*,*) "----------------------------------------"
      write (*,*) "Temperature is", T_k

 endif


!   label_method = 10 
!   Sampling of transition state
!   T_k

 if (label_method .eq. 10)    then
      write (*,*)
      write (*,*)
      write (*,*) "----------------------------------------"
      write (*,*) "Make the displacements of Q and P  &
                   around TS !  "
      write (*,*) "P_v is generated from Bolzmann distribution"
      write (*,*) "----------------------------------------"
      write (*,*) "Temperature is", T_k

 endif


!    Generate the random P and Q
 

 if (label_method .eq. 1)   then
      if ( (n_mode*n_geom) .gt. nr  ) then
         write (*,*) "ERROR MESSAGES"
         write (*,*) "PLEASE GENERATE MORE RANDOM NUMBERS!"
         stop
      endif  
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


 endif 
 
 if (  label_method .eq. 2)  then
  
      nr=n_geom*n_mode 

      write (*,*) "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
      write (*,*) "---------------------------------------"
      write (*,*) "Generate two sets of random &
                   numbers from 2D Gaussian distribution &
                   (certain T_k) "

      open(unit=file_random_gau, file="random_gau.dat")
      open(unit=file_random_uni, file="random_uni.dat")
      !write(*,*) 'frequency test, yxie'
      !write(*,*) frequency(1)
      call random_gaussian_2d_tk  (n_geom, &
                                   t_k, &
                                   n_mode, &
                                   frequency, &
                                   file_random_gau, &
                                   file_random_uni)
      close(file_random_gau)
      close(file_random_uni)


      write (*,*) "---------------------------------------"
      write (*,*) "Wigner sampling at temperature T_k"
 endif
 
 if (  label_method .eq. 11)  then
  
      nr=n_geom*n_mode 

      write (*,*) "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
      write (*,*) "---------------------------------------"
      write (*,*) "Generate two sets of random &
                   numbers from 2D Gaussian distribution &
                   (certain T_k) "

      open(unit=file_random_gau, file="random_gau.dat")
      open(unit=file_random_uni, file="random_uni.dat")
      !write(*,*) 'frequency test, yxie'
      !write(*,*) frequency(1)
      frequency = frequency * TOCM
      call random_gaussian_2d_tk  (n_geom, &
                                   t_k, &
                                   n_mode, &
                                   frequency, &
                                   file_random_gau, &
                                   file_random_uni)
      close(file_random_gau)
      close(file_random_uni)


      write (*,*) "---------------------------------------"
      write (*,*) "Wigner sampling at temperature T_k"
 endif
 

 if ( (  label_method .ge. 3)  &
      .AND.   &
      (  label_method .le. 6)  )  &
 then

      write (*,*) "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
      write (*,*) "---------------------------------------"
      write (*,*) "Generate two sets of random &
                   numbers based on the method  &
                   by Mueller and Stock."
 

      nr=n_geom*n_mode            
      if  (label_method .eq. 3) then
           open(unit=file_random_gau, file="random_gau.dat")
           open(unit=file_random_uni, file="random_uni.dat")
           call random_mu_st_1         (n_geom, &
                                        n_mode, &
                                        frequency, &
                                        ex_vib, &
                                        file_random_gau, &
                                        file_random_uni)
          close(file_random_gau)
          close(file_random_uni)
          write (*,*) "---------------------------------------"
      endif 

      if  (label_method .eq. 4) then
           
!                  write (*,*)   "Frequency:", frequency(:)
!                  write (*,*)   "w/kb*t", frequency(:) &
!                                      / (KB*t_k*TOCM)
!                  write (*,*)  "1/ (e(w/kb*t) -1 )",  1/ ( exp (  frequency(:) &
!                                                  / (KB*t_k*TOCM) &
!                                                ) &
!                                           -1     &
!                                          )

           ex_vib(:) =   1/ ( exp (  frequency(:) &
                               / (KB*t_k*TOCM) &
                                  ) &
                             -1    &
                            ) 
!                  write (*,*) "ex_vib",  ex_vib(:)

           open(unit=file_random_gau, file="random_gau.dat")
           open(unit=file_random_uni, file="random_uni.dat")
           call random_mu_st_1         (n_geom, &
                                        n_mode, &
                                        frequency, &
                                        ex_vib, &
                                        file_random_gau, &
                                        file_random_uni)
           close(file_random_gau)
           close(file_random_uni)
           write (*,*) "---------------------------------------"
      endif

      if  (label_method .eq. 5) then
           open(unit=file_random_gau, file="random_gau.dat")
           open(unit=file_random_uni, file="random_uni.dat")
           call random_mu_st_1         (n_geom, &
                                        n_mode, &
                                        frequency, &
                                        ex_vib, &
                                        file_random_gau, &
                                        file_random_uni)
           close(file_random_gau)
           close(file_random_uni)
           write (*,*) "---------------------------------------"
      endif


    
      if  (label_method .eq. 6) then 
          open(unit=file_random_gau, file="random_gau.dat")
          open(unit=file_random_uni, file="random_uni.dat")
          call random_mu_st_2         (n_geom, &
                                  n_mode, &
                                  frequency, &
                                  t_k, &
                                  file_random_gau, &
                                  file_random_uni)
           close(file_random_gau)
           close(file_random_uni)
           write (*,*) "---------------------------------------"
       endif
  endif



  if  (label_method .eq. 10) then
     nr=n_geom*n_mode
     open(unit=file_random_gau, file="random_gau.dat")
     open(unit=file_random_uni, file="random_uni.dat")
     call random_ts_3         (n_geom, &
                                  n_mode, &
                                  frequency, &
                                  t_k, &
                                  number_negative, &
                                  file_random_gau, &
                                  file_random_uni)
    close(file_random_gau)
    close(file_random_uni)
    write (*,*) "---------------------------------------"
 endif




!hudp        if (label_frozen .eq. 0) then
!hudp        write (*,*)  "No mode is frozen"
!hudp        endif
!hudp
!hudp        if (label_frozen .eq. 1) then
!hudp        write (*,*)  "The following modes are frozen"
!hudp        do i=1, number_frozen
!hudp        write (*,*)  "Mode, ", list_frozen (i)
!hudp        enddo
!hudp        endif 
!hudp
!hudp        write (*,*) "----------------------------------------"
!hudp
!hudp        
!hudp        file_random_gau=30
!hudp        file_x_Q=80
!hudp        file_v_V_au=81
!hudp        file_x_Q_au=82
!hudp        file_p_P_au=83
!hudp        file_stat_q=84
!hudp        open(unit=file_random_gau, file="random_gau.dat")
!hudp        open(unit=file_x_Q, file="x_Q_ang.dat")
!hudp        open(unit=file_v_V_au, file="v_V_au.dat")
!hudp        open(unit=file_x_Q_au, file="x_Q_au.dat")
!hudp        open(unit=file_p_P_au, file="p_P_au.dat")
!hudp        open(unit=file_stat_q, file="stat_Q.dat")
!hudp        call  displacement_wigner_1 (label_method, &
!hudp                                     n_geom, &
!hudp                                     file_random_gau, &
!hudp                                     n_atom, &
!hudp                                     atom_label, &
!hudp                                     coor_x, coor_y, coor_z, &
!hudp                                     n_mode, &
!hudp                                     frequency, &
!hudp                                     coor_vib, &
!hudp                                     frozen_or_not, &
!hudp                                     file_x_Q, &
!hudp                                     file_v_V_au, &
!hudp                                     file_x_Q_au, &
!hudp                                     file_p_P_au, &
!hudp                                     file_stat_q)
!hudp                                     
!hudp        close(file_random_gau)
!hudp        close(file_x_Q)
!hudp        close(file_v_V_au)
!hudp        close(file_x_Q_au)
!hudp        close(file_p_P_au)
!hudp        close(file_stat_q) 
!hudp      
      
!hudp        open(unit=file_v_V_au, file="v_V_au.dat")
!hudp        open(unit=file_p_P_au, file="p_P_au.dat")          
!hudp        call check_kinetic   (n_geom, &
!hudp                              n_atom, &
!hudp                              file_v_V_au, &
!hudp                              file_p_P_au )
!hudp        close(file_v_V_au)
!hudp        close(file_p_P_au)
!hudp      
!hudp        write (*,*) "----------------------------------------"
!hudp
!hudp
!hudp
!hudp        write (*,*) "---------------------------------------"
!hudp
!hudp        write (*,*) "Check two sets of random &
!hudp                     numbers"
!hudp        open(unit=file_random_gau, file="random_gau.dat")
!hudp        open(unit=file_dis1d_random1, file="dis1d_random1.dat")
!hudp        i_col=1
!hudp        write (*,*) "First dimension"
!hudp        call check_random_1d (file_random_gau, &
!hudp                              nr, &
!hudp                              nbin, &
!hudp                              i_col, &
!hudp                              file_dis1d_random1)
!hudp        close(file_random_gau)
!hudp        close(file_dis1d_random1) 
!hudp             
!hudp
!hudp
!hudp        open(unit=file_random_gau, file="random_gau.dat")
!hudp        open(unit=file_dis1d_random2, file="dis1d_random2.dat")
!hudp        i_col=2
!hudp        write (*,*) "Second dimension"
!hudp        call check_random_1d (file_random_gau, &
!hudp                              nr, &
!hudp                              nbin, &
!hudp                              i_col, &
!hudp                              file_dis1d_random2)
!hudp        close(file_random_gau)
!hudp        close(file_dis1d_random2)
!hudp
!hudp        
!hudp        open(unit=file_random_gau, file="random_gau.dat")
!hudp        open(unit=file_dis2d_random, file="dis2d_random.dat")
!hudp        write (*,*) "Two dimension"
!hudp        call check_random_2d (file_random_gau, &
!hudp                              nr, &
!hudp                              nbin, &
!hudp                              file_dis2d_random)
!hudp        close(file_random_gau)
!hudp        close(file_dis2d_random)
!hudp        write (*,*) "---------------------------------------"
!hudp





deallocate ( frequency)
deallocate ( coor_x   )
deallocate ( coor_y   )
deallocate ( coor_z   )
deallocate ( coor_vib )
deallocate ( atom_label)

!       return
 
end 
