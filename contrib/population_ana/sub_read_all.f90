       subroutine sub_read_all (   n_ao, &
                                   n_atom, &
                                   n_state, &
                                   type_input, &
                                   ci_1, &
                                   basis, &
                                   s_ao_to_mo,  &
                                   s_ao_overlap  )



!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
!      The current subroutine reads CI vectors and MOs (for Geom A and Geom B) 
!      and AO overlap of Geom A and Geom B.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

       implicit none

!
!     ----- Parameters -----
!
       include 'param.def'
!       include "info_comm.itf"
!      
!     ----- Argument -----
!

       integer, intent (in) :: n_ao, n_atom, n_state, type_input

       double precision, intent (inout), dimension(n_ao,n_ao) :: &
                                                 s_ao_to_mo, &
                                                 s_ao_overlap
      double precision, intent (inout), dimension(n_state, n_ao, n_ao) :: &
                                                 ci_1
      integer, intent(inout), dimension (n_atom) :: basis

       !      ---- local variables ---
      integer :: i, j, k, i_status, system, i_atom
      integer :: i_tmp, j_tmp, k_tmp  
      double precision :: ene_tmp, ci_tmp
      character*10 :: char_tmp
      integer :: n_atom_1, n_ao_1, n_state_1

      integer, allocatable, dimension(:) :: IPIV
      double precision, allocatable, dimension(:) :: WORK
      integer :: INFO, LWORK
      LWORK = n_ao
      allocate (IPIV(n_ao))
      allocate (WORK(LWORK))
      LWORK=-1

          ci_1(:,:,:) =0
          s_ao_overlap (:,:) = 0
 

          if (type_input .eq. 0 ) then
            write (*,*) "Read CI vectors and mos from standard files!"    
          endif
 
          if (type_input .eq. 1 ) then
            write (*,*) "Read CI vectors and mos from Turbomole output!"
             i_status = system ("tur_read_tddft.py")
             if (i_status  .ne. 0) then
                write (*,*) "The interface errors!", i_status
                write (*,*) "Check Turbomole calculations!"
                stop
             endif
          endif
  
          if (type_input .eq. 2 ) then
            write (*,*) "Read CI vectors and mos from Turbomole output!"
             i_status = system ("tur_read_ricc.py")
             if (i_status  .ne. 0) then
                write (*,*) "The interface errors!", i_status
                write (*,*) "Check Turbomole calculations!"
                stop
             endif
          endif


          if (type_input .eq. 3 ) then
             write (*,*) "Read CI vectors and mos from ORCA output!"   
             i_status = system ("orca_read.py")
             if (i_status  .ne. 0) then
                write (*,*) "The interface errors!", i_status
                write (*,*) "Check ORCA calculations!"
                stop
             endif
          endif

          if (type_input .eq. 4 ) then
             write (*,*) "Read CI vectors and mos from Gaussian output!" 
             i_status = system ("gaussian_read.py")
             if (i_status  .ne. 0) then
                write (*,*) "The interface errors!", i_status
                write (*,*) "Check Gaussian calculations!"
                stop
             endif
          endif
           
       

!         Read the summary of QM file
     
       
          open (unit=50, file="qm_results.dat")
          do i=1, 3
             read (50,*)
          enddo

          read (50,*) char_tmp, char_tmp, char_tmp, &
                         char_tmp, char_tmp, n_state_1
          if (  n_state_1 .ne. n_state) then
                write (*,*) "Check the number of states in inputs!"
                write (*,*) n_state, n_state_1
                stop
          endif


          do i=1, 5
             read (50,*)
          enddo
    
          read (50, *) char_tmp, char_tmp, n_atom_1
          if (  n_atom_1 .ne. n_atom) then
                write (*,*) "Check atomic number in inputs!"
                stop
          endif

          read (50,*)
          do i_atom= 1, n_atom
              read (50, *) char_tmp, basis(i_atom)
          enddo
          
          read (50,*)
          read (50,*) char_tmp, char_tmp, char_tmp, &
                         char_tmp, char_tmp, n_ao_1
          if (  n_ao_1 .ne. n_ao) then
                write (*,*) "Check the number of aos in inputs!!!"
                write (*,*) n_ao_1, n_ao
                stop
          endif
        


       
!         Read the CI vectors.
    
  
           ci_1 = 0.d0
           open (unit=50, file="ci.dat")
           read (50,*) 
           do i=2, n_state
              do j= 1, 20
                 read (50, *) char_tmp, ci_tmp ,  &
                                        j_tmp, k_tmp
                 ci_1(i,j_tmp,k_tmp) = ci_tmp
              enddo
           enddo
           close(50)


!    Read the MO coefficient!
!    MO at R
!    
     
          open (unit=50, file="mo.dat")
          read (50, *)
          do  i= 1, n_ao
              read (50, *)
              do j= 1, n_ao
                 read (50,*) i_tmp, j_tmp, &
                                      s_ao_to_mo(i,j)
              enddo
          enddo
          close(50)


!    Compute the AO overlap matrix   

      s_ao_overlap = matmul (transpose(s_ao_to_mo),  s_ao_to_mo)

      write (*,*)  "Compute (CC^T)^-1"
      call sub_inverse_matrix (s_ao_overlap, n_ao )
     


      open (unit=50, file="ao_overlap.dat")
      do i = 1, n_ao
         do j = 1, n_ao
            write (50, *)  i, j, s_ao_overlap(i,j)
         enddo
      enddo
      close(50)   
    
!      stop

!    Read the orbital overlap between R and R+dR

!          open (unit=file_input3, file="ao_overlap.dat")
!          read (file_input3, *)
!          do i = 1, n_ao
!             do j = 1, n_ao
!                read (file_input3, *)  i_tmp, j_tmp, s_ao_overlap(i,j)
!             enddo
!          enddo
!          close(file_input3)      
 

     


        return 

        end     subroutine sub_read_all                 
