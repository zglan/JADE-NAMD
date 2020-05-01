        subroutine   random_mu_st_1         (n_geom, &
                                          n_mode, &
                                          frequency, &
                                          ex_vib, &
                                          file_random_gau, &
                                          file_random_uni)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!      Generate (P,Q) from the method proposed by Mueller and Stock
!      Reference
!      [1]  Mueller, Stock, JCP 107, 6230, (1997).
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!      Q = (2*n +1)**0.5 *  cos(theta)    theta in [0, 2*pi)
!      P = (2*n +1)**0.5 *  sin(theta)    theta in [0, 2*pi)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!






       implicit none

!
!     ----- Parameters -----
!
       include 'param.def'
!       include "info_comm.itf"
!      
!     ----- Argument -----
!a
     
       integer, intent (in) :: n_geom, file_random_gau, file_random_uni, &
                               n_mode      
      
       double precision, intent (in), dimension(n_mode) :: frequency
       double precision, intent (in), dimension(n_mode) ::  ex_vib

!      ---- local variables ---
       double precision, allocatable, dimension(:) :: random_gau1, &
                                                      random_gau2
       double precision, allocatable, dimension(:) :: random_1, &
                                                      random_2
       integer :: seed, i_geom, j_mode, nr_total, i_total
       double precision :: alpha

       nr_total = n_mode * n_geom



       allocate(random_gau1(nr_total))
       allocate(random_gau2(nr_total))
       allocate(random_1(nr_total))
       allocate(random_2(nr_total))
      

       do j_mode = 1, n_mode
          write (*,*) "Mode", j_mode
          write (*,*) "Frequency ", frequency(j_mode)
          write (*,*) "Average <N>: ", ex_vib(j_mode)    
       enddo
      
       write (*,*) "Generate the first set of random number &
                    from the uniform distribution [0,1) " 
 
       CALL RANDOM_SEED()
       CALL RANDOM_NUMBER(random_1)
       random_2 = random_1 * 2* PI
 
       write (file_random_uni,*)  "# Uniform distribution"
       do i_total=1, nr_total
       write (file_random_uni,*) random_1(i_total), random_2(i_total)
       enddo

   
       write (file_random_gau,*)  "# (P,Q)"

  
       do i_geom = 1, n_geom 
          do  j_mode = 1, n_mode

              i_total = (i_geom-1) * n_mode + j_mode
              random_gau1(i_total) =  ((ex_vib(j_mode)*2+1)**0.5)      &
                                     * cos(random_2(i_total))
              random_gau2(i_total) =  (( ex_vib(j_mode)*2+1)**0.5)     &
                                     * sin(random_2(i_total))
              write (file_random_gau,*) random_gau1(i_total),  &
                                        random_gau2(i_total)
           enddo
       enddo


       deallocate(random_gau1)
       deallocate(random_gau2)

       deallocate(random_1)
       deallocate(random_2)
         
       return


       end subroutine  random_mu_st_1
