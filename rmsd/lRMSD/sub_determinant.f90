      subroutine sub_determinant ( total_matrix, &
                                   n_ele,        &
                                   s_det,        &
                                   output_level  &
                                  )


       implicit none

       integer, intent (in) :: n_ele, output_level
       double precision, intent (in), dimension(n_ele,n_ele) :: &
                                                    total_matrix
       double precision, intent (inout)  :: s_det



!      local variables
!      IPIV:  INTEGER array, dimension (min(M,N))
       integer, allocatable, dimension(:) :: IPIV
!      INFO    (output) INTEGER
!          = 0:  successful exit
!          < 0:  if INFO = -i, the i-th argument had an illegal value
!          > 0:  if INFO = i, U(i,i) is exactly zero. The factorization
!                has been completed, but the factor U is exactly
!                singular, and division by zero will occur if it is used
!                to solve a system of equations.

        integer :: INFO
        integer :: i 
        double precision, allocatable, dimension(:,:) :: input_matrix
     

        allocate (input_matrix(n_ele, n_ele))
        allocate (IPIV(n_ele))
       
        input_matrix = total_matrix 


9999      format (100(1x, f10.5))
 
       if (output_level  .eq. 2) then     
               
          write (*,*) "Input matrix to calculate determinant!"
          do i=1, n_ele
             write (*,*) "Line", i
             write (*,9999) input_matrix(i,:)
          enddo
      
          do i=1, n_ele
             write (*,*) "dia", i, input_matrix(i,i)
          enddo

       endif

       call dgetrf(n_ele,n_ele,input_matrix,n_ele,IPIV,INFO)


       s_det = 0.d0

       if (info .lt. 0) then
          write (*,*) "Wrong matrix determinant!"
          if (output_level  .eq. 2) then
              write (*,*) "info:", INFO
              do i=1, n_ele
                  write (*,9999) input_matrix(i,:)
              enddo
              do i=1, n_ele
                  write (*,*) "ipiv", i, IPIV(i)
              enddo
          endif
          stop
       endif


       if (info .gt. 0) then
          if (output_level  .eq. 2) then
               write (*,*) "U(i,i) is exactly zero!"
          endif
          s_det = 0.d0
       endif

        if (info .eq. 0) then

          s_det = 1d0

          if (output_level  .eq. 2) then
               write (*,*) "info:", INFO
               do i=1, n_ele
                   write (*,9999) input_matrix(i,i)
               enddo
               do i=1, n_ele
                   write (*,*) "ipiv", i, IPIV(i)
               enddo
          endif

          do i=1, n_ele
             if (ipiv(i) .ne. i ) then
                 s_det = - s_det * input_matrix(i,i)
             else
                 s_det = s_det * input_matrix(i,i)
             endif
          enddo

       endif

       if (output_level  .eq. 2) then
          write (*,*) "Determinant is: ", s_det 
       endif



        deallocate (input_matrix)
        deallocate (IPIV)



       return 

       end subroutine sub_determinant
