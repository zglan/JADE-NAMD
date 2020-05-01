      subroutine  sub_overlap_half_positive(n_basis, &
                               overlap_ao, &
                               overlap_half, &
                               trans_overlap_half )



!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
!      The current subroutine constructs S^1/2 matrix.
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

       integer, intent (in) :: n_basis
       double precision, intent (in), dimension(n_basis,n_basis) :: &
                                                              overlap_ao
       double precision, intent (inout), dimension(n_basis,n_basis) :: &
                                                         overlap_half, &
                                                     trans_overlap_half 


!      ---- local variables ---
       double precision, allocatable, dimension(:,:) :: temp_matrix, &
                                                        trans_matrix, &
                                                        s_eigen_half
                                                         
       double precision, allocatable, dimension(:) :: s_eigen
                                                        
       integer :: i, j
      
!      Variables for LAPACK package 
       integer :: lwork,ifail
       double precision, allocatable, dimension(:) :: work

       lwork=3*n_basis-1





       allocate ( temp_matrix (n_basis, n_basis))
       allocate ( trans_matrix (n_basis, n_basis))
       allocate ( s_eigen (n_basis))
       allocate ( s_eigen_half (n_basis, n_basis))
 


!   Set values for LAPACK package 
       allocate (work(lwork))
       work (:) = 0.0



!   Read overlap matrix

       trans_matrix = overlap_ao 

           
!  Diagonalize overlap matrix

      

      call  DSYEV( 'V', 'U', &
                  n_basis, trans_matrix, &
                  n_basis, s_eigen, &
                  work, lwork, ifail )

      s_eigen_half(:,:) = 0.0
      do i=1, n_basis
         s_eigen_half(i,i) = (s_eigen(i))**(0.5D0)
      enddo 

      temp_matrix  = MATMUL(trans_matrix, s_eigen_half )
      overlap_half = MATMUL(temp_matrix, TRANSPOSE(trans_matrix))

      trans_overlap_half = trans_matrix 

       deallocate ( temp_matrix )
       deallocate ( trans_matrix )
       deallocate ( s_eigen  )
       deallocate ( s_eigen_half )
       deallocate (work)

      return
      end subroutine   sub_overlap_half_positive
     


