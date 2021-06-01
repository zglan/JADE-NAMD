      subroutine sub_orbital_overlap ( n_basis, &
                                       s1_ao_to_mo_alpha, &
                                       s2_ao_to_mo_alpha, &
                                       s1_ao_to_mo_beta, &
                                       s2_ao_to_mo_beta, &
                                       s_double_ao_overlap, &
                                       s_mo_overlap &
                                      )



!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
!      The current subroutine constructs the orbital overlap!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!     Local variables: s_mo_spatial: the overlap of two orbitals with same spin. 
              


       implicit none

!
!     ----- Parameters -----
!
       include 'param.def'
!       include "info_comm.itf"
!      
!     ----- Argument -----
!

       integer, intent (in) :: n_basis
       double precision, intent (in), dimension(n_basis,n_basis) :: &
                                                 s1_ao_to_mo_alpha, &
                                                 s2_ao_to_mo_alpha, &
                                                 s1_ao_to_mo_beta, &
                                                 s2_ao_to_mo_beta, &
                                                 s_double_ao_overlap

       double precision,intent (inout),dimension(2*n_basis,2*n_basis) :: &
                                                         s_mo_overlap


!      ---- local variables ---
       double precision, allocatable, dimension(:,:) :: temp_matrix
       double precision, allocatable, dimension(:,:) :: s_mo_spatial
                                                         
       integer :: i, j
      
       allocate ( temp_matrix (n_basis, n_basis))
       allocate ( s_mo_spatial (n_basis, n_basis))




       s_mo_overlap (:,:) =0.d0
       
!      When two electron have the different spin, we have zero overlap 


!      Construct the MO overlap  for alpha spin electrons
!       temp_matrix  = MATMUL(TRANSPOSE(s1_ao_to_mo_alpha), &
!                                       s_double_ao_overlap )
!       s_mo_spatial = MATMUL(temp_matrix, s2_ao_to_mo_alpha)

       temp_matrix  = MATMUL(s1_ao_to_mo_alpha, &
                                       s_double_ao_overlap )
       s_mo_spatial = MATMUL(temp_matrix, Transpose(s2_ao_to_mo_alpha))
       


       do i= 1, n_basis
          do j=1, n_basis
              s_mo_overlap (i,j) = s_mo_spatial (i,j)
          enddo
       enddo    
  
!      Construct the MO overlap  for beta spin electrons
!       temp_matrix  = MATMUL(TRANSPOSE(s1_ao_to_mo_beta),&
!                                       s_double_ao_overlap )
!       s_mo_spatial = MATMUL(temp_matrix, s2_ao_to_mo_beta)

       temp_matrix  = MATMUL(s1_ao_to_mo_beta, &
                                       s_double_ao_overlap )
       s_mo_spatial = MATMUL(temp_matrix, Transpose(s2_ao_to_mo_beta))

       do i= 1, n_basis
          do j=1, n_basis
              s_mo_overlap (i+n_basis,j+n_basis) = s_mo_spatial (i,j)
          enddo
       enddo
 



       deallocate ( temp_matrix  )
       deallocate ( s_mo_spatial )

      return
      end subroutine  sub_orbital_overlap
     


