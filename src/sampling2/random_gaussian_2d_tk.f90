        subroutine   random_gaussian_2d_tk  (n_geom, &
                                            t_k, &
                                            n_mode, &
                                            frequency, &
                                            file_random_gau, &
                                            file_random_uni)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!      Generate two set of random number from a 2D Guassian distribution function
!      Reference
!      [1]  Box, G.E.P, M.E. Muller 1958; 
!           A note on the generation of random normal deviates, 
!           Annals Math. Stat, V. 29, pp. 610-611 
!      [2]  Weisstein, Eric W. "Box-Muller Transformation.
!           " From MathWorld--A Wolfram Web Resource. 
!           http://mathworld.wolfram.com/Box-MullerTransformation.html   
!      [3]  http://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform  
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!      R = - 2 * ln (U1)    U1 in [0, 1)
!      theta = 2*pi* U2     U2 in [0, 1)
!      x = R* cos(theta)
!      y = R* sin(theta)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!      random_1:       (1) U1:    [ random numbers from the uniform distribution [0,1]       ]
!!                      (2) R:     [ random_1 =  sqrt ( -2 * log(random_1) )                    ]         
!!      random_2:       (1) U2:    [ random numbers U2 from the uniform distribution [0,1]    ]
!!                      (2) theta: [ random_1 = 2 * pi* random_2                              ]                 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
!!      random_gau1     (1) x: A set of random numbers from the Guassian distribution function
!!      random_gau2     (1) y: A set of random numbers from the Guassian distribution function
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!






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
      
       double precision, intent(in) :: t_k
       double precision, intent(in), dimension(n_mode) :: frequency

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
       
       
       CALL RANDOM_SEED()
       CALL RANDOM_NUMBER(random_1)
    
       write (*,*) "Generate the first set of random number &
                    from the uniform distribution [0,1) " 
 
       seed=random_1(nr_total/2)*6965896
     

       CALL RANDOM_SEED(seed)
       CALL RANDOM_NUMBER(random_2)
      
       write (*,*) "Generate the second set of random number &
                    from the uniform distribution [0,1)"


       write (file_random_uni,*)  "# Uniform distribution"
       do i_total=1, nr_total
       write (file_random_uni,*) random_1(i_total), random_2(i_total)
       enddo

   
       write (file_random_gau,*)  "# Gaussian distribution"

  
       do i_geom = 1, n_geom 
          do  j_mode = 1, n_mode

              i_total = (i_geom-1) * n_mode + j_mode

              alpha = tanh( ( frequency(j_mode)/ TOCM) /   &
                        (2 * KB * t_k )  )          

              random_1(i_total) = ( -  log( random_1(i_total) )    &
                                    /  log(2.718281828)    &
                                  ) ** 0.5    

              random_1(i_total) =  random_1(i_total) / (alpha**0.5)

              random_2(i_total) = 2* PI * random_2(i_total)


              random_gau1(i_total) =   random_1(i_total)  &
                                     * cos(random_2(i_total))
              random_gau2(i_total) =   random_1(i_total)    &
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


       end subroutine  random_gaussian_2d_tk
