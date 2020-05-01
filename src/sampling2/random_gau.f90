        subroutine random_gaussian_2d  (nr, &
                                        file_random_gau, &
                                        file_random_uni )




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
     
       integer, intent (in) :: nr, file_random_gau, file_random_uni      
      

!      ---- local variables ---
       double precision, allocatable, dimension(:) :: random_gau1, &
                                                      random_gau2
       double precision, allocatable, dimension(:) :: random_1, &
                                                      random_2
       integer :: seed, i 



       allocate(random_gau1(nr))
       allocate(random_gau2(nr))
       allocate(random_1(nr))
       allocate(random_2(nr))
       
       
       CALL RANDOM_SEED()
       CALL RANDOM_NUMBER(random_1)
    
       write (*,*) "Generate the first set of random number &
                    from the uniform distribution [0,1) " 
 
       seed=random_1(nr/2)*6965896
     

       CALL RANDOM_SEED(seed)
       CALL RANDOM_NUMBER(random_2)
      
       write (*,*) "Generate the second set of random number &
                    from the uniform distribution [0,1)"


       write (file_random_uni,*)  "# Uniform distribution"
       do i=1, nr
       write (file_random_uni,*) random_1(i), random_2(i)
       enddo



       do i=1,nr
!          write (*,*) 1, random_1(i)
!          write (*,*) PI, random_1(i) * PI
!          write (*,*) log( random_1(i) * PI )
          random_1(i) = (-   log( random_1(i)  )    &
                          / log(2.718281828)    &
                        ) ** 0.5    
!          write (*,*) 2, random_1(i)
       enddo


       do i=1,nr
       random_2(i) = 2* PI * random_2(i)
       enddo


       do i=1, nr
       random_gau1(i) = random_1(i) * cos(random_2(i))
       random_gau2(i) = random_1(i) * sin(random_2(i))
       enddo       

 
       write (file_random_gau,*)  "# Gaussian distribution"
       do i=1, nr
       write (file_random_gau,*) random_gau1(i), random_gau2(i)
       enddo


       deallocate(random_gau1)
       deallocate(random_gau2)

       deallocate(random_1)
       deallocate(random_2)
         
       return


       end subroutine  random_gaussian_2d
