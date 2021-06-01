       Program main


!      This program computes the overlap of electronic wavefunctions
!      of two closing molecular geometris. 
!      The method is given by 
!      |Psi_m > = C_mk  |psi_k  >
!               = C_m0 * |psi_0  >  + \sum C_m i^j |psi_i^j  > 
!      |psi_i^j  > is the slater deterimant describing the 
!      single excitations from orbital i to orbital j   
!      Next <Psi_m (R1) | Psi_n (R2) > = C_mk (R1) < psi_k (R1)  | psi_l(R2) > C_ml(R2)
!      The key issue here is to compute the overlap of two 
!      slater deterimants.
!      The element of slater deterimants are spin orbitals 
!      | mo_a > = \sum_b c_ar |ao_b>. 
!      c_ar is the MO coefficient.
!      The overlap of two slater deterimants finally becomes    
!      < psi_k (R1) | psi_l (R2) > =  det (S_ab)
!      where 
!       S_ab = delta [spin(a), spin(b)] *
!            = \sum (r,p) c_ar(R1) < ao_r(R1) | ao_p(R2) > c_bp(R2)            

   
      
       implicit none
!      Include all parameters
       include 'param.def'




!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!! Define all input and output files
!      file_input1: The calculation results at Geom1
!      file_input2: The calculation results at Geom2
!      file_input3: The calculation results at Geom1+Geom2
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
!      Define input files
       integer :: file_input1, file_input2, file_input3, type_input
       character*20 :: filename_input1, filename_input2, filename_input3

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
!         n_ao_alpha      Number of atomic orbitals for alpha electrons
!         n_ao_beta       Number of atomic orbitals for beta electrons
!         n_mo_alpha      Number of molecular orbitals for alpha electrons
!         n_mo_beta       Number of molecular orbitals for beta electrons
!         n_ele_alpha     Number of alpha electrons
!         n_ele_beta      Number of beta electrons

!         In close-shell case, we always have
!         n_ao = n_mo =  n_ao_alpha = n_ao_beta = n_mo_alpha = n_mo_beta 
!         n_ele_alpha =  n_ele_beta = n_ele_half = n_ele / 2 

!-------------------------------------------------------------------------------------
! 
!         s_ao_overlap ::     Overlap matrix in AO basis for Geom1 and Geom2
!         s1_ao_to_mo_alpha : MO coefficient for orbitals with alpha spin for Geom1
!         s1_ao_to_mo_beta  : MO coefficient for orbitals with beta spin for Geom1
!         s1_ao_to_mo_alpha : MO coefficient for orbitals with alpha spin for Geom1
!         s1_ao_to_mo_beta :  MO coefficient for orbitals with beta spin for Geom2
!
!         In close-shell case, we always have
!         s1_ao_to_mo_alpha = s1_ao_to_mo_beta
!         s1_ao_to_mo_alpha = s1_ao_to_mo_beta
! ------------------------------------------------------------------------------------
!         s_mo_overlap : Overlap matrix of MOs at Geom1 and Geom2
!         Please note that this matrix is block diagonalized matrix.
!         | S_mo_overlap_alpha    0                     |
!         | 0                     S_mo_overlap_beta     |
!         The overlap of two MOs with different spins should be zero!
!        
!     
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!         n_state:  The number of electronic states in calculations.
!         n_csf:    The number of configuration state functions. 
!                   The number of Slater deterimants. 
!         ci_1, ci_2 contain the CI vector information for Geom1 and Geom2.
!         The dimension of ci_1 is n_state*n_csf*3
!         For example: ci_1(3,2,1): State 3, CSF 2, CI coefficient
!                                   CSF 2: single excitation from Orbital k to l 
!                      ci_1(3,2,1): State 3, CSF 2, Orbital k
!                      ci_1(3,2,1): State 3, CSF 2, Orbital l               
!         For ground-state configuration (reference configuration)
!                      Let us assume that CSF1 is the ground state configuration
!                      We always set
!                      ci_1(1,1,1): State 1 
!                                   ci_1(1,1,1) = 1.0
!                                   ci_1(1,1,2) = 0
!                                   ci_1(1,1,3) = 0
!                                   ci_1(1,j,m) = 0.0  (j>0)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
!
!         s_wf_overlap :  The overlap of electronic wavefunctions
!                         Dimension (n_state, n_state)
!          s_ci_overlap:  The overlap of CI vectors between  electronic wavefunctions!    
!                          Dimension (n_state, n_state)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1


      integer :: n_atom, n_ao, n_mo,  &         
                 n_ele_alpha, n_ele_beta, n_ele, n_ele_half, &
                 n_state,n_csf
    

      double precision, allocatable, dimension(:,:) ::  &
                                                        s_ao_overlap, &
                                                   s1_ao_to_mo_alpha, &
                                                   s2_ao_to_mo_alpha, &
                                                    s1_ao_to_mo_beta, &
                                                    s2_ao_to_mo_beta  
      double precision, allocatable, dimension(:,:) ::  s_mo_overlap
      double precision, allocatable, dimension(:,:) ::  s_wf_overlap, &
                                                        s_ci_overlap
      double precision, allocatable, dimension(:,:,:) ::  ci_1, ci_2

      integer :: i, j 
    


        read (*,*) 
        read (*,*) n_atom
        read (*,*) n_ao
        read (*,*) n_ele_alpha
        read (*,*) n_ele_beta
        read (*,*) 
        read (*,*) n_state
        read (*,*) 
        read (*,*) type_input
        read (*,*) filename_input1
        read (*,*) filename_input2
        read (*,*) filename_input3
        read (*,*) 
        read (*,*) output_level
        read (*,*) filename_output  
 
        file_input1=31
        file_input2=32
        file_input3=33

        file_output=70

        n_ele=n_ele_alpha + n_ele_beta
        n_ele_half = n_ele/ 2
        n_mo = n_ao
        
        n_csf =20

        allocate (s_ao_overlap       (n_ao, n_ao))
        allocate (s1_ao_to_mo_alpha  (n_ao, n_ao))
        allocate (s1_ao_to_mo_beta  (n_ao, n_ao))
        allocate (s2_ao_to_mo_alpha   (n_ao, n_ao))
        allocate (s2_ao_to_mo_beta   (n_ao, n_ao))

        allocate (s_mo_overlap (2*n_ao, 2*n_ao))
        
        allocate (s_wf_overlap (n_state, n_state))
        allocate (s_ci_overlap (n_state, n_state))
         
        allocate (ci_1 (n_state, n_csf, 3))
        allocate (ci_2 (n_state, n_csf, 3))




        s_ao_overlap(:,:)        = 0.d0
        s1_ao_to_mo_alpha (:,:)  = 0.d0
        s1_ao_to_mo_beta(:,:)    = 0.d0
        s2_ao_to_mo_alpha (:,:)  = 0.d0
        s2_ao_to_mo_beta(:,:)    = 0.d0
    
        s_mo_overlap(:,:)        = 0.d0  
        s_wf_overlap(:,:)        = 0.d0
        ci_1(:,:,:)              = 0.d0
        ci_2(:,:,:)              = 0.d0

        
        write (*,*) "---------------------------------------"
        write (*,*) "INPUT INFORMATION:" 
        write (*,*) "The number of atoms are:", n_atom
        write (*,*) "The number of atomic orbitals are:", n_ao
        write (*,*) "The number of alpha electrons are:", n_ele_alpha
        write (*,*) "The number of beta electrons are:",  n_ele_beta
        write (*,*) "---------------------------------------"
        write (*,*) "Check the input file format: "
        write (*,*) "1: Default"
        write (*,*) "Input format:", type_input
        write (*,*) "Input file are:"
        write (*,*) filename_input1, filename_input2, filename_input3 
        write (*,*) "---------------------------------------"
        write (*,*) "Onput file is:", filename_output
        write (*,*) "Check the The level of screen output: "
        write (*,*) "1: Normal"
        write (*,*) "2: Debug"
        write (*,*)  "The level of screen output is:", output_level
  

!!!  Read all fock matrix and overlap matrix            
        write (*,*) "---------------------------------------"
        write (*,*) 
        write (*,*)
        write (*,*) "---------------------------------------"
        write (*,*) "Read CI vectors and MOs of two geometries!"
        write (*,*) "Read AO overlap between two geometries!"

 
        call sub_read_all (        n_ao, &
                                   n_state, &
                                   n_csf, &
                                   type_input, &
                                   file_input1, &
                                   filename_input1, &
                                   ci_1, &
                                   s1_ao_to_mo_alpha, &
                                   s1_ao_to_mo_beta, &
                                   file_input2, &
                                   filename_input2, &
                                   ci_2, &
                                   s2_ao_to_mo_alpha, &
                                   s2_ao_to_mo_beta, &
                                   file_input3, &
                                   filename_input3, &
                                   s_ao_overlap )



        write (*,*) "Finish to read CI vectors and MOs!"
        write (*,*) "Finish to read AO overlap between two geometries!"
        write (*,*) "---------------------------------------"
        write (*,*)
        write (*,*)
  
        if (output_level .ge. 1 )  then
             write (*,*)  "Print CI vectors of Geom 1"
             do i=1, n_state
                write (*,*)  "State, ", i
                do j= 1, n_csf
                  if (ci_1(i,j,1)  .ne. 0) then
                      write (*,9999)     ci_1(i,j,1), &
                                     int(ci_1(i,j,2)), &
                                     int(ci_1(i,j,3))
                  endif 
                enddo
             enddo
        endif
        
9999    format( "CSF", f8.5, 1x, i3, "-->", i3)

!  Print the CI vectors and MOs in debug option
        if (output_level .eq. 2 )  then
            write (*,*)  "--------------------"
            write (*,*)  "MOs for Geom 1"
            write (*,*)  "Alpha Spin" 
            do i=1, n_ao
               do j=1, n_ao
                  write (*,*) i, j, s1_ao_to_mo_alpha(i,j)
               enddo
            enddo
            write (*,*)  "Beta Spin"    
            do i=1, n_ao
               do j=1, n_ao
                  write (*,*) i, j, s1_ao_to_mo_beta(i,j)
               enddo
            enddo
        endif


        if (output_level .ge. 1 )  then  
             write (*,*)  "Print CI vectors of Geom 2"
             do i=1, n_state
                write (*,*)  "State, ", i
                do j= 1, n_csf
                   if (ci_2(i,j,1)  .ne. 0) then
                     write (*,9999)      ci_2(i,j,1), &
                                     int(ci_2(i,j,2)), &
                                     int(ci_2(i,j,3))
                   endif
                enddo
             enddo
        endif

 
        if (output_level .eq. 2 )  then    
            write (*,*)  "--------------------"
            write (*,*)  "MO2 for Geom 2" 
            write (*,*)  "Alpha Spin"
            do i=1, n_ao
               do j=1, n_ao
                  write (*,*) i, j, s2_ao_to_mo_alpha(i,j)
               enddo
            enddo
            write (*,*)  "Beta Spin" 
            do i=1, n_ao
               do j=1, n_ao
                  write (*,*) i, j, s1_ao_to_mo_beta(i,j)
               enddo
            enddo
            write (*,*) "-------------------------------"
!       stop
       endif 



        write (*,*) "Begin to construct the overlap of orbitals!"    
        write (*,*) "---------------------------------------"
        call  sub_orbital_overlap ( n_ao, &
                                    s1_ao_to_mo_alpha, &
                                    s2_ao_to_mo_alpha, &
                                    s1_ao_to_mo_beta, &
                                    s2_ao_to_mo_beta, &
                                    s_ao_overlap, &
                                    s_mo_overlap    &          
                                  )




!        if (output_level .eq. 2 )  then
!            write (*,*)  "--------------------"
!            write (*,*)  "AO overlap between Geom1 and Geom 2"
!            write (*,*)  "AO overlap does not count different spins"
!            do i=1, n_ao
!               do j=1, n_ao
!                  write (*,*) i, j, s_ao_overlap(i,j)
!               enddo
!            enddo
!            write (*,*) "-------------------------------"
!       stop
!       endif

       open (unit=60, file="mo_overlap.dat")
!       if (output_level .eq. 2 )  then
            write (60,*)  "--------------------"
            write (60,*)  "MO overlap between Geom1 and Geom 2"
            write (60,*)  "MO overlap count different spins"
            do i=1, n_ao*2
               do j=1, n_ao*2
                  write (60,*) i, j, s_mo_overlap(i,j)
               enddo
            enddo
            write (60,*) "-------------------------------"
!       stop
!       endif

        write (*,*) "Finish to construct the the overlap of orbitals!"  
        write (*,*) "---------------------------------------"


!!     Build the overlap of two electronic wavefunctions

       call sub_wf_overlap ( n_atom,  &
                             n_ao, &
                             n_ele, &
                             n_ele_alpha, &
                             n_ele_beta,  &
                             n_state,  &
                             n_csf, &
                             s_mo_overlap, &
                             ci_1, ci_2, &
                             s_wf_overlap, &
                             s_ci_overlap, &
                             output_level  )           


!!     Write down the overlap of two electronic wavefunctions


        deallocate (s_ao_overlap     )
        deallocate (s1_ao_to_mo_alpha  )
        deallocate (s1_ao_to_mo_beta  )
        deallocate (s2_ao_to_mo_alpha   )
        deallocate (s2_ao_to_mo_beta   )

        deallocate (s_mo_overlap )

        deallocate (s_wf_overlap )

        deallocate (ci_1 )
        deallocate (ci_2 )

              

       write (*,*)  "Finish to compute the overlap between R and R+dR"
  
       end program main
