        subroutine   random_mu_st_2         (n_geom, &
                                          n_mode, &
                                          frequency, &
                                          t_k, &
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
      
       double precision, intent(in), dimension(n_mode) :: frequency
       double precision, intent(in) :: t_k


!      ---- local variables ---
       double precision, allocatable, dimension(:) :: random_gau1, &
                                                      random_gau2
       double precision, allocatable, dimension(:) :: random_1, &
                                                      random_2, &
                                                      random_3
       double precision, allocatable, dimension(:,:) ::  ex_vib
       double precision, allocatable, dimension(:,:) :: pro, &
                                                     pro_sum
       integer :: seed, i_geom, j_mode, nr_total, i_total
       integer :: n_level, top_level, i_level, i_random
       double precision :: alpha, temp_sum

       nr_total = n_mode * n_geom


       allocate (ex_vib(n_geom, n_mode))
       allocate (random_gau1(nr_total))
       allocate (random_gau2(nr_total))
       allocate (random_1(nr_total))
       allocate (random_2(nr_total))
       allocate (random_3(nr_total))

       write (*,*)  "Generate the occpuation number &
                     from Bolzmann distribution"

       CALL RANDOM_SEED()
       CALL RANDOM_NUMBER(random_1)

       n_level = 1000 
       allocate (pro(n_mode, n_level))
       allocate (pro_sum(n_mode, n_level))
       pro = 0.d0
       do j_mode = 1, n_mode
          do i_level =1, n_level
             pro(j_mode, i_level)  &
                         =  exp (   ( - (i_level-1) * frequency(j_mode) ) &
                                  / ( KB*t_k*TOCM )  & 
                                )  & 
                          * ( 1- exp (   - frequency(j_mode)    &
                                       / (KB*t_k*TOCM)        & 
                                     )                        &
                            )                                 

            if (pro(j_mode, i_level) .lt. 0.00001) then
                pro(j_mode, i_level) = 0.0 
                goto 990
            endif 

          enddo

990       write (*,*) "for Mode", j_mode
          write (*,*) "Frequency", frequency(j_mode)
          write (*,*) "Energy Level: 0,1,2, ..."
          write (*,*) "Occupation probability:"
!          write (*,*) pro(j_mode, 1), pro(j_mode, 2), pro(j_mode, 3)
          write (*,9999) pro(j_mode, 1:20)
       enddo

9999   format ( 10(f10.5, 1X) )


       write (*,*)  "------------------------------"
       write (*,*)  "Population Probability: SUM (1-->n) "
       write (*,*)  "-----------------------------"

       pro_sum = 0.d0
       do j_mode = 1, n_mode
          temp_sum=0
          do i_level =1, n_level
             temp_sum = temp_sum +  pro(j_mode, i_level)
             pro_sum (j_mode, i_level) =  temp_sum
             if (pro(j_mode, i_level)  .eq. 0) then
                goto 991
             endif
          enddo
991       write (*,*) "for Mode", j_mode
          write (*,*) "Frequency", frequency(j_mode)
          write (*,*) "Probability summation:"
          write (*,9999) pro_sum (j_mode, 1:20)
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


       CALL RANDOM_SEED()
       CALL RANDOM_NUMBER(random_3)
       

       i_random = 1 
       do i_geom = 1, n_geom
          write (*,*)   "Geom", i_geom
          do  j_mode = 1, n_mode
              do i_level = 1, n_level 
                 if (  random_3(i_random)   &
                       .lt.                 &
                       pro_sum (j_mode, i_level) &
                    )  &
                 then
                    ex_vib(i_geom, j_mode) = i_level - 1 
                    goto 992
                 endif
             enddo
992          write (*,*) "Mode and level", &
                         j_mode,  ex_vib(i_geom, j_mode)          
             i_random = i_random + 1    
          enddo 
       enddo   
  
       do i_geom = 1, n_geom 
          do  j_mode = 1, n_mode

              i_total = (i_geom-1) * n_mode + j_mode
              random_gau1(i_total) =  ( (ex_vib(i_geom, j_mode)*2+1)**0.5)     &
                                     * cos(random_2(i_total))
              random_gau2(i_total) =  (( ex_vib(i_geom, j_mode)*2+1)**0.5)     &
                                     * sin(random_2(i_total))
              write (file_random_gau,*) random_gau1(i_total),  &
                                        random_gau2(i_total)
           enddo
       enddo




       deallocate (ex_vib)
       deallocate (random_gau1)
       deallocate (random_gau2)
       deallocate (random_1)
       deallocate (random_2)
       deallocate (random_3)
       deallocate (pro)
       deallocate (pro_sum)


         
       return


       end subroutine  random_mu_st_2
