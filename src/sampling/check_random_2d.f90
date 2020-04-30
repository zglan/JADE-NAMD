       subroutine check_random_2d (file_random_gau, &
                                   nr, & 
                                   nbin, &
                                   file_dis2d )


       implicit none

!
!     ----- Parameters -----
!
       include 'param.def'
!
!     ----- Argument -----
!      
       
       integer, intent (in) :: file_random_gau, nbin, &
                               nr, file_dis2d      


                                                      
!      ---- local variables ---
       integer :: i, j, k, l
     
        double precision, allocatable, dimension (:) ::  random_set_1, &
                                                         random_set_2
       double precision, allocatable, dimension(:,:) :: occupation

        double precision, allocatable, dimension(:)  :: bin_center_1, &
                                                        bin_center_2 
       double precision :: random_max_1, random_min_1, random_dx_1, &
                           bin_upper_1, bin_lower_1
       double precision :: random_max_2, random_min_2, random_dx_2, &
                           bin_upper_2, bin_lower_2

       double precision :: sum_occpation
       

       allocate (random_set_1(nr))
       allocate (random_set_2(nr))

       allocate (occupation(nbin, nbin))
       allocate (bin_center_1(nbin))
       allocate (bin_center_2(nbin))



       read (file_random_gau,*)
       do i=1, nr
       read (file_random_gau,*) random_set_1(i), random_set_2(i)
       enddo





       random_max_1=random_set_1(1)
       random_min_1=random_set_1(1)      


       do i=1, nr
        if ( random_set_1(i) .gt. random_max_1  ) then
         random_max_1 = random_set_1(i)
        endif
        if ( random_min_1 .gt. random_set_1(i)  ) then
         random_min_1 = random_set_1(i)
        endif
       enddo  
       random_dx_1= (random_max_1 -  random_min_1) / nbin 
    


      
        random_max_2=random_set_2(1)
        random_min_2=random_set_2(1)
       
        do j=1, nr
        if ( random_set_2(j) .gt. random_max_2  ) then
         random_max_2 = random_set_2(j)
        endif
        if ( random_min_2 .gt. random_set_2(j)  ) then
         random_min_2 = random_set_2(j)
        endif
       enddo
       random_dx_2= (random_max_2 -  random_min_2) / nbin










       do i=1, nbin
       do j=1, nbin
         
          occupation(i,j)=0

          bin_lower_1 = random_min_1 + (i-1) * random_dx_1
          bin_upper_1 = random_min_1 + (i) * random_dx_1          
          bin_center_1 (i)  =  0.5 * ( bin_lower_1 + bin_upper_1)     
       
          bin_lower_2 = random_min_2 + (j-1) * random_dx_2
          bin_upper_2 = random_min_2 + (j) * random_dx_2
          bin_center_2 (j)  =  0.5 * ( bin_lower_2 + bin_upper_2)

          do k=1, nr
           if (   ( bin_upper_1 .ge. random_set_1(k) ) &
                  .and. &
                  ( random_set_1(k) .ge. bin_lower_1 ) &
                  .and. &
                  ( bin_upper_2 .ge. random_set_2(k) ) &
                  .and. &
                  ( random_set_2(k) .ge. bin_lower_2 ) & 
              ) then
              occupation(i,j) =  occupation(i,j) +1
           endif
          enddo

       enddo
       enddo

       sum_occpation =0.0
       do i=1, nbin
       do j=1, nbin
       sum_occpation = sum_occpation +  occupation(i,j) 
       enddo
       enddo

       do i=1, nbin
       do j=1, nbin
       occupation(i,j) = occupation(i,j) / sum_occpation
       enddo
       enddo

      
       do i=1, nbin
       do j=1, nbin
       write (file_dis2d, *)  bin_center_1(i), bin_center_2(j), &
                              occupation(i,j)/(random_dx_1*random_dx_2)    
       enddo
       enddo

       write (*,*) sum(occupation)


       deallocate (random_set_1)
       deallocate (random_set_2)

       deallocate (occupation) 
       deallocate (bin_center_1)
       deallocate (bin_center_2)

       return


       end subroutine  check_random_2d
