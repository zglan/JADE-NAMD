       Program main


       implicit none
!      Include all parameters
       include 'param.def'




!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!! Define all input and output files
!      file_input1: The calculation output
!      file_input2: The file to save MOS
!      file_input3: The file to save CI vector (CIS format)
!      file_input4: The file to save overlap matrix in AO basis
!      file input5:
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11

!      Define input files
       integer :: file_input1, file_input2, file_input3, &
                  file_input4, file_input5, type_input
       character*20 :: filename_input1, filename_input2, filename_input3, &
                       filename_input4, filename_input5

!      Define output files
       integer :: file_output, output_level            
       character*20 :: filename_output

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!       
!!!!!!!!-- All variables
!         Please not that the current code only available for RKS ground states.
!           
!--       n_atom:         Number of atoms
!--       n_ao:           Number of atomic spatial orbitals
!--       n_mo:           Number of molecular spatial orbitals

!-------------------------------------------------------------------------------------
! 
!         s_ao_overlap ::     Overlap matrix in AO basis for Geom1 and Geom2
!         s_ao_to_mo : MO coefficient for orbitals with alpha spin for Geom1
!
! ------------------------------------------------------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!         n_state:  The number of electronic states in calculations.
!         n_csf:    The number of configuration state functions. 
!                   The number of Slater deterimants. 
!         ci_1, ci_2 contain the CI vector.
!         The dimension of ci_1 is n_state*n_csf*3
!         For example: ci_1(n_state,n_ao,n_ao): CI coefficient

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
!
!         tra_density :  Transition density (n_occ, n_vir)
!         tra_lis:       transition(n_atom, n_atom)  (Lischka's paper)
!         pop_lis:       pop(n_atom)   (Barbatti's paper)  
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1


      integer :: n_atom, n_ao, n_mo,  &         
                 n_state,n_csf, n_occ, n_vir
    
      integer, allocatable, dimension(:) :: basis 
      double precision, allocatable, dimension(:,:) ::  &
                                                        s_ao_overlap, &
                                                   s_ao_to_mo 
      double precision, allocatable, dimension(:,:,:) ::  ci_1
      double precision, allocatable, dimension(:,:) :: tra_density1, &
                                                       tra_density2, &
                                                       tra_lis, &
                                                       pop_lis

      integer :: i, j, k 
    


        read (*,*) 
        read (*,*) n_atom
        read (*,*) n_ao
        read (*,*) n_occ
        read (*,*) n_vir
        read (*,*) 
        read (*,*) n_state
        read (*,*) 
        read (*,*) type_input
        read (*,*) filename_input1
        read (*,*) filename_input2
        read (*,*) filename_input3
        read (*,*) filename_input4
        read (*,*) filename_input5
        read (*,*) 
        read (*,*) output_level
        read (*,*) filename_output  
 
        file_input1=31
        file_input2=32
        file_input3=33
        file_input4=34
        file_input5=35

        file_output=70


        allocate (s_ao_overlap       (n_ao, n_ao))
        allocate (s_ao_to_mo         (n_ao, n_ao))

        allocate (ci_1 (n_state, n_ao, n_ao))
        allocate (tra_density1 (n_ao, n_ao) )
        allocate (tra_density2 (n_ao, n_ao) )
!        allocate (tra_lis (n_atom, n_atom))
!        allocate (pop_lis (n_atom))
        allocate (basis(n_atom))


        s_ao_overlap(:,:)        = 0.d0
        s_ao_to_mo (:,:)         = 0.d0

        ci_1(:,:,:)              = 0.d0
        tra_density1             = 0.d0
        tra_density1             = 0.d0
   
!        tra_lis                  = 0.d0
!        pop_lis                  = 0.d0
 
        write (*,*) "---------------------------------------"
        write (*,*) "INPUT INFORMATION:" 
        write (*,*) "The number of atoms are:", n_atom
        write (*,*) "The number of atomic orbitals are:", n_ao
        write (*,*) "The number of occupied orbitals are:", n_occ
        write (*,*) "The number of vitural orbitals are:",  n_vir
        write (*,*) "---------------------------------------"
        write (*,*) "Check the input file format: "
        write (*,*) "1: Default"
        write (*,*) "Input format:", type_input
        write (*,*) "Input file are:"
        write (*,*) filename_input1, filename_input2, filename_input3
        write (*,*) filename_input4, filename_input5
        write (*,*) "---------------------------------------"
        write (*,*) "Onput file is:", filename_output
        write (*,*) "Check the The level of screen output: "
        write (*,*) "1: Normal"
        write (*,*) "2: Debug"
        write (*,*)  "The level of screen output is:", output_level
        write (*,*)  "fort.51: Lischka's way; fort.52: Lowdin's way"
  

!!!  Read all matrix       
        write (*,*) "---------------------------------------"
        write (*,*) 
        write (*,*)
        write (*,*) "---------------------------------------"
        write (*,*) "Read CI vectors, MOs and AO overlap matrix!"

 
        call sub_read_all (        n_ao, &
                                   n_atom, &
                                   n_state, &
                                   type_input, &
                                   ci_1, &
                                   basis, &
                                   s_ao_to_mo,  & 
                                   s_ao_overlap )



        write (*,*) "Finish to read CI vectors and MOs!"
        write (*,*) "Finish to read AO overlap matrix!"
        write (*,*) "---------------------------------------"
        write (*,*)
        write (*,*)
  
        if (output_level .ge. 1 )  then
             write (*,*)  "Print CI vectors of Geom 1"
             do i=1, n_state
                write (*,*)  "State, ", i
                do j= 1, n_occ
                   do k =1, n_vir
                      if ( abs(ci_1(i,j,k))**2  .ne. 0.01) then
                          write (*,9999)     i, j, k, ci_1(i,j,k)
                      endif
                   enddo 
                enddo
             enddo
        endif
        
9999    format( "State:", i5, ", Occ:", i5, "--> Vir:", i5, 1x, f8.5)

!  Print the CI vectors and MOs in debug option
        if (output_level .eq. 2 )  then
            write (*,*)  "--------------------"
            write (*,*)  "MOs "
            do i=1, n_ao
               do j=1, n_ao
                  write (*,*) i, j, s_ao_to_mo(i,j)
               enddo
            enddo
        endif



        do i=2, n_state

           write (*,*) "Analyze the transition density !"    
           write (*,*) "---------------------------------------"
           do j=1, n_ao
              do k=1, n_ao
                 tra_density1(j,k) = ci_1 (i,j,k)
              enddo
           enddo 
           call  sub_transition_density ( n_atom, &
                                          n_ao, &
                                          tra_density1,  &
                                          s_ao_to_mo, &
                                          tra_density2, &
                                          s_ao_overlap, &
                                          basis &
                                        )

        enddo



!        do i=2, n_state
!
!           write (*,*) "Analyze the electronic population !"
!           write (*,*) "---------------------------------------"
!           do j=1, n_ao
!              do k=1, n_ao
!                 tra_density1(j,k) = ci_1 (i,j,k)
!            enddo
!          enddo
!           call  sub_pop_density        ( n_atom, &
!                                         n_ao,  &
!                                          tra_density1,  &
!                                          s_ao_to_mo,  &
!                                          tra_density2, &
!                                          s_ao_overlap, &
!                                          basis &
!                                        )
!
!        enddo

  
       end program main
