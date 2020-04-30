      subroutine sub_inverse_matrix (matrix,n)

      implicit none
      integer :: n
      double precision, intent(inout), dimension(n,n) :: matrix 
      
  
!     local variables
      double precision, allocatable, dimension (:,:) :: tmp_matrix  

      integer :: LWORK, INFO
      double precision, allocatable, dimension(:) :: WORK
      integer, allocatable, dimension(:) :: IPIV
      integer :: i,j


      LWORK = n*n
      ALLOCATE (tmp_matrix(n,n))
      ALLOCATE (WORK(LWORK))
      ALLOCATE (IPIV(n))



!     DGETRF: LU decomposition


      tmp_matrix = matrix

      call DGETRF( n, n, tmp_matrix, n, IPIV, INFO )

      if ( INFO  .eq.  0) then
         write (*,*) "Successful LU decomposition"
      endif
      if ( INFO  .lt.  0) then
         write (*,*) "Wrong LU decomposition!"
      endif
      if ( INFO  .gt.  0) then
         write (*,*) "U(i,i) is exactly zero!!"
      endif


!  DGETRI computes the inverse of a matrix using the LU factorization
!  computed by DGETRF.

      CALL DGETRI(n, tmp_matrix, n, IPIV, WORK, LWORK, INFO)


      if ( info .ne.  0) then
         write (*,*) 'Matrix inversion failed!'
         stop
      else
         write (*,*) 'Inverse Successful'  
      endif

      matrix = tmp_matrix

      end subroutine 
