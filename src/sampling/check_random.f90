       subroutine check_random_1d (file_random_gau, &
                                   nr, &
                                   nbin, &
                                   i_gau_random, & 
                                   file_dis1d)


       implicit none

!
!     ----- Parameters -----
!
       include 'param.def'
!
!     ----- Argument -----
!
             
       integer, intent (in) :: file_random_gau, nr, &
                               nbin, file_dis1d, i_gau_random      


                                                      
!      ---- local variables ---
       integer :: i,j 
     
       double precision, allocatable, dimension(:) :: random_set
       double precision, allocatable, dimension(:) :: occupation, &
                                                      bin_center 
       double precision :: random_max, random_min, random_dx, &
                           bin_upper, bin_lower, &
                           sum_occpation, tmp
       



       allocate (random_set(nr))
       allocate (occupation(nbin))
       allocate (bin_center(nbin))


       
       read (file_random_gau,*)

       if (i_gau_random .eq. 1) then  
       do i=1, nr
       read (file_random_gau,*) random_set(i), tmp
       enddo
       endif

       if (i_gau_random .eq. 2) then
       do i=1, nr
       read (file_random_gau,*) tmp, random_set(i)
       enddo
       endif





       random_max=random_set(1)
       random_min=random_set(1)


       do i=1, nr
        if ( random_set(i) .gt. random_max  ) then
         random_max = random_set(i)
        endif
        if ( random_min .gt. random_set(i)  ) then
         random_min = random_set(i)
        endif
       enddo    

       random_dx= (random_max -  random_min) / nbin 
    
       do i=1, nbin
         
          occupation(i)=0

          bin_lower = random_min + (i-1) * random_dx
          bin_upper = random_min + (i) * random_dx          
          bin_center (i)  =  0.5 * ( bin_lower + bin_upper)  
             
     
          do j=1, nr
           if (  ( bin_upper .ge. random_set(j) ) &
                  .and. &
                  ( random_set(j) .ge. bin_lower ) &
              ) then
            occupation(i) =  occupation(i) +1
           endif
          enddo
       enddo


       sum_occpation =0.0
       do i=1, nbin
       sum_occpation = sum_occpation +  occupation(i) 
       enddo

       do i=1, nbin
       occupation(i) = occupation(i) / sum_occpation
       enddo

      
       do i=1, nbin
       write (file_dis1d, *)  bin_center(i), occupation(i)/random_dx
       enddo
 


!      Check the normalization
        
       write (*,*) "Norm is",  sum(occupation)


 
       deallocate (random_set)
       deallocate (occupation) 
       deallocate (bin_center)

       return


       end subroutine  check_random_1d
